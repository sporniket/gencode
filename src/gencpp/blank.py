"""
---
(c) 2024 David SPORN
---
This is part of Gencode -- whatever.

Gencode is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Gencode is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Gencode.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

import json
import os
import re
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from enum import Enum

from gencode_lib import Identifier

import jinja2

from .templates import (
    TEMPLATE_SOURCES__META_STRINGS,
    TEMPLATE_SOURCE__SPDX,
    TEMPLATE_SOURCES__HPP_FILES,
    TEMPLATE_SOURCE__CPP_FILES,
)
from .generators import GeneratorOfHppFiles, GeneratorOfCppFiles
from .argparsers import (
    addConfigurationFileOptions,
    addProjectMetadataOptions,
    addRootPathOptions,
)

ONLY_DOTS = re.compile(r"[.]{3,}")  # accept '.' and '..' as path fragment


def splitAndFilterPath(path: str) -> list[str]:
    return [f for f in path.split("/") if f and not ONLY_DOTS.match(f)]


GENCODE = "gencode"
SUPPORTED_FORMATS = [GENCODE]


# TODO : make it abc
class Producer:
    def __init__(self):
        self._env = jinja2.Environment()
        self.populateTemplates()
        self._argParserArgumentHelpers = []

    def applyArgumentHelpers(self, parser):
        for h in self._argParserArgumentHelpers:
            h(parser)

    def appendSubParser(self, codename: str, subparser):
        # TODO Rewrite parser as needed
        parser = subparser.add_parser(
            codename,
            help=self.helpMessage,
        )

        # Add the arguments
        self.applyArgumentHelpers(parser)
        self.addCustomArguments(parser)

        parser.set_defaults(func=self.run)

    def populateTemplates(self):
        templates = {}
        dictionnary = self.dictionnaryOfTemplates
        for key in dictionnary:
            templates[key] = self._env.from_string(dictionnary[key])
        self._templates = templates

    @property
    def dictionnaryOfTemplates(self):
        return {}

    def addCustomArguments(self, parser):
        pass

    #####################################
    ### Configuration of meta strings ###
    #####################################
    def configureMetaStrings(self, args) -> dict[str, str]:
        config = self.getMetaStringsFromArgs(args)

        if args.config:
            format, pathToFile = args.config.split(":", 1)
            if format not in SUPPORTED_FORMATS:
                raise ValueError(f"unsupported.config.format:{format}")
            if not os.path.isfile(pathToFile):
                raise ValueError(f"file.not.found.or.not.regular.file:{pathToFile}")
            if format == GENCODE:
                with open(pathToFile) as sourceJson:
                    source = json.load(sourceJson)
                self.applyMetaStringsFrom_GENCODE(config, source)

        self.finalizeMetaStrings(config)
        return config

    def getMetaStringsFromArgs(self, args):
        return {
            "YEARS_COPYRIGHT": args.copyright_years,
            "NAMES_COPYRIGHT": args.copyright_authors,
            "LABEL_PROJECT": args.project_name,
            "DESCRIPTION_PROJECT": args.project_description,
            "SPDX_CLAUSE": args.project_licence,
        }

    def applyMetaStringsFrom_GENCODE(self, configOrigin, configJson):
        if configJson["copyright"]:
            if configJson["copyright"]["years"]:
                configOrigin["YEARS_COPYRIGHT"] = configJson["copyright"]["years"]
            if configJson["copyright"]["authors"]:
                configOrigin["NAMES_COPYRIGHT"] = configJson["copyright"]["authors"]
        if configJson["project"]:
            if configJson["project"]["name"]:
                configOrigin["LABEL_PROJECT"] = configJson["project"]["name"]
            if configJson["project"]["description"]:
                configOrigin["DESCRIPTION_PROJECT"] = configJson["project"][
                    "description"
                ]
            if configJson["project"]["licence"]:
                configOrigin["SPDX_CLAUSE"] = configJson["project"]["licence"]

    def finalizeMetaStrings(self, config):
        config["COPYRIGHT"] = self._templates["copyright"].render(config)
        config["PROJECT_DESCRIPTION_CLAUSE"] = (
            config["DESCRIPTION_PROJECT"] if config["DESCRIPTION_PROJECT"] else ""
        )
        if config["SPDX_CLAUSE"]:
            config["LICENCE_SPDX"] = self._templates["licence_spdx_id"].render(config)
            config["PROJECT_LABEL_CLAUSE"] = self._templates[
                "project_label__with_licence"
            ].render(config)
        else:
            config["LICENCE_SPDX"] = ""
            config["PROJECT_LABEL_CLAUSE"] = self._templates[
                "project_label__no_licence"
            ].render(config)


class MainGeneratorForBlank(Producer):
    def __init__(self):
        super().__init__()
        self._argParserArgumentHelpers = [
            addConfigurationFileOptions,
            addRootPathOptions,
            addProjectMetadataOptions,
        ]

    def addCustomArguments(self, parser):
        parser.add_argument(
            "--library",
            metavar="<library>",
            type=str,
            default="",
            help="The library label, e.g. 'superUtils', into which directory the files will be generated",
        )

        parser.add_argument(
            "params",
            metavar="<parameter...>",
            type=str,
            nargs="+",
            help="a non-empty list of specific parameters required by the template",
        )

    @property
    def helpMessage(self):
        return "Generate empty CPP file and its empty header file."

    @property
    def dictionnaryOfTemplates(self):
        result = {}
        for template in [
            TEMPLATE_SOURCES__META_STRINGS,
            TEMPLATE_SOURCE__SPDX,
            TEMPLATE_SOURCES__HPP_FILES,
            TEMPLATE_SOURCE__CPP_FILES,
        ]:
            result.update(template)

        return result

    def checkFolderOrMake(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise ValueError(f"not.directory:{path}")

    def run(self, args):
        config = self.configureMetaStrings(args)

        rootPath = "."
        if args.root:
            parts = splitAndFilterPath(args.root)
            rootPath = os.path.join(rootPath, *parts)

        if args.library:
            rootPath = os.path.join(
                rootPath, "lib", splitAndFilterPath(args.library)[0]
            )

        self.checkFolderOrMake(os.path.join(rootPath, "include"))
        self.checkFolderOrMake(os.path.join(rootPath, "src"))

        header = GeneratorOfHppFiles(rootPath, self._templates)
        program = GeneratorOfCppFiles(rootPath, self._templates)
        for i, n in enumerate(args.params):
            guardName = (
                f"_lib_{args.library}_{args.params[i]}.hpp"
                if args.library
                else f"{args.params[i]}.hpp"
            )
            config["CODE_GUARD"] = Identifier(guardName).allcaps
            config["NAME_HEADER"] = args.params[i]
            header.generate(
                n,
                i,
                config,
                includesTemplates="header_includes__blank",
                bodyTemplate="header_body__blank",
                localPath="include",
            )
            program.generate(
                n,
                i,
                config,
                includesTemplates="source_includes__blank",
                bodyTemplate="source_body__blank",
                localPath="src",
            )

        return 0
