"""
---
(c) 2024 David SPORN
---
This is part of $$$

$$$ is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

$$$ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with $$$.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

import json
import os

from abc import ABC

import jinja2

GENCODE = "gencode"
SUPPORTED_FORMATS = [GENCODE]


class _Producer(ABC):
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

    #########################
    ### general utilities ###
    #########################

    def checkFolderOrMake(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise ValueError(f"not.directory:{path}")

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
