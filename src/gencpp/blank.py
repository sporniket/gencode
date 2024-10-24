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

TEMPLATE_SOURCES = {
    "copyright": """Copyright (C) {{YEARS_COPYRIGHT}} {{NAMES_COPYRIGHT}}""",
    # ---
    "no_licence_no_description": """ALL RIGHT RESERVED -- project '{{LABEL_PROJECT}}'""",
    "no_licence_with_description": """ALL RIGHT RESERVED -- project '{{LABEL_PROJECT}}' -- {{DESCRIPTION_PROJECT}}.""",
    "with_licence_no_description": """This is part of {{LABEL_PROJECT}}.""",
    "with_licence_with_description": """This is part of {{LABEL_PROJECT}} -- {{DESCRIPTION_PROJECT}}.""",
    # ---
    "licence_spdx_id": """/* SPDX-License-Identifier: {{SPDX_CLAUSE}} */

""",
    # ---
    "source_header": """{{LICENCE_SPDX}}/****************************************

---
{{COPYRIGHT}}
---
{{LICENCE}}
****************************************/
#ifndef {{CODE_GUARD}}
#define {{CODE_GUARD}}
// ================[ CODE BEGINS ]================

// ...your code...

// ================[ END OF CODE ]================
#endif""",
    # ---
    "source_main": """{{LICENCE_SPDX}}/****************************************

---
{{COPYRIGHT}}
---
{{LICENCE}}
****************************************/
#include "{{NAME_HEADER}}.hpp"

// ...your code...

""",
}


ONLY_DOTS = re.compile(r"[.]{3,}")  # accept '.' and '..' as path fragment


def splitAndFilterPath(path: str) -> list[str]:
    return [f for f in path.split("/") if f and not ONLY_DOTS.match(f)]


GENCODE = "gencode"
SUPPORTED_FORMATS = [GENCODE]

class GeneratorOfBlankFiles:
    def __init__(self):
        env = jinja2.Environment()
        templates = {}
        for key in TEMPLATE_SOURCES:
            templates[key] = env.from_string(TEMPLATE_SOURCES[key])
        self._templates = templates

    def appendSubParser(self, codename: str, subparser):
        # TODO Rewrite parser as needed
        parser = subparser.add_parser(
            codename,
            help="Generate empty CPP file and its empty header file.",
        )

        # Add the arguments
        parser.add_argument(
            "--config",
            metavar="<format>:<path/to/config file>",
            type=str,
            help="the project wide configuration file",
        )

        parser.add_argument(
            "--root",
            metavar="<rootdir>",
            type=str,
            default=".",
            help="the relative path of the project, defaults to the current path",
        )

        parser.add_argument(
            "--copyright_years",
            metavar="<years>",
            type=str,
            default="20xx",
            help="A string listing all the years to report in the copyright notice",
        )

        parser.add_argument(
            "--copyright_authors",
            metavar="<authors>",
            type=str,
            default="Unknown author",
            help="A string listing all the authors to report in the copyright notice",
        )

        parser.add_argument(
            "--project_name",
            metavar="<project name>",
            type=str,
            default="Unknown project",
            help="The project name or title",
        )

        parser.add_argument(
            "--project_description",
            metavar="<project description>",
            type=str,
            default="",
            help="An hopefully short, one-line phrase that describe what this project is all about",
        )

        parser.add_argument(
            "--project_licence",
            metavar="<project licence>",
            type=str,
            default="",
            help="A SPDX identifier or a SPDX license expressions",
        )

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

        parser.set_defaults(func=self.run)

    def checkFolderOrMake(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise ValueError(f"not.directory:{path}")

    def computeHeaderFileBody(self, args, config, index: int = 0):
        return self._templates["source_header"].render(config)

    def computeProgramFileBody(self, args, config, index: int = 0):
        return self._templates["source_main"].render(config)

    def generateHeaderFile(self, rootPath, args, config, index: int = 0):
        target = os.path.join(rootPath, "include", args.params[index] + ".hpp")
        try:
            with open(target, "x") as out:
                source = self.computeHeaderFileBody(args, config, index)
                out.write(source)
        except FileExistsError:
            print(f"error.file.exists:{target}")

    def generateProgramFile(self, rootPath, args, config, index: int = 0):
        target = os.path.join(rootPath, "src", args.params[index] + ".cpp")
        try:
            with open(target, "x") as out:
                source = self.computeProgramFileBody(args, config, index)
                out.write(source)
        except FileExistsError:
            print(f"error.file.exists:{target}")

    def prepareConfig(self, args):
        return {
            "YEARS_COPYRIGHT": args.copyright_years,
            "NAMES_COPYRIGHT": args.copyright_authors,
            "LABEL_PROJECT": args.project_name,
            "DESCRIPTION_PROJECT": args.project_description,
            "SPDX_CLAUSE": args.project_licence,
        }

    def applyConfigFile_GENCODE(self, configOrigin, configJson):
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

    def finalizeConfig(self, config):
        config["COPYRIGHT"] = self._templates["copyright"].render(config)
        if config["SPDX_CLAUSE"]:
            config["LICENCE_SPDX"] = self._templates["licence_spdx_id"].render(config)
            if config["DESCRIPTION_PROJECT"]:
                config["LICENCE"] = self._templates[
                    "with_licence_with_description"
                ].render(config)
            else:
                config["LICENCE"] = self._templates[
                    "with_licence_no_description"
                ].render(config)
        else:
            config["LICENCE_SPDX"] = ""
            if config["DESCRIPTION_PROJECT"]:
                config["LICENCE"] = self._templates[
                    "no_licence_with_description"
                ].render(config)
            else:
                config["LICENCE"] = self._templates["no_licence_no_description"].render(
                    config
                )

    def run(self, args):
        config = self.prepareConfig(args)

        if args.config:
            format, pathToFile = args.config.split(":", 1)
            if format not in SUPPORTED_FORMATS:
                raise ValueError(f"unsupported.config.format:{format}")
            if not os.path.isfile(pathToFile):
                raise ValueError(f"file.not.found.or.not.regular.file:{pathToFile}")
            if format == GENCODE:
                with open(pathToFile) as sourceJson:
                    source = json.load(sourceJson)
                self.applyConfigFile_GENCODE(config, source)

        self.finalizeConfig(config)

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

        for i, n in enumerate(args.params):
            guardName = (
                f"_lib_{args.library}_{args.params[i]}.hpp"
                if args.library
                else f"{args.params[i]}.hpp"
            )
            config["CODE_GUARD"] = Identifier(guardName).allcaps
            config["NAME_HEADER"] = args.params[i]
            self.generateHeaderFile(rootPath, args, config, i)
            self.generateProgramFile(rootPath, args, config, i)

        return 0
