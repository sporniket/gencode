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

import os
import re

from gencode_lib import Identifier

from .producer import _Producer


from gencpp.templates import (
    TEMPLATE_SOURCES__META_STRINGS,
    TEMPLATE_SOURCE__SPDX,
    TEMPLATE_SOURCES__HPP_FILES,
    TEMPLATE_SOURCE__CPP_FILES,
)
from gencpp.generators import generatorOfHppFiles, generatorOfCppFiles
from gencpp.argparsers import (
    addConfigurationFileOptions,
    addProjectMetadataOptions,
    addRootPathOptions,
)

ONLY_DOTS = re.compile(r"[.]{3,}")  # accept '.' and '..' as path fragment


def splitAndFilterPath(path: str) -> list[str]:
    return [f for f in path.split("/") if f and not ONLY_DOTS.match(f)]


class ProducerOfBlank(_Producer):
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

        hpp = generatorOfHppFiles(rootPath, self._templates)
        cpp = generatorOfCppFiles(rootPath, self._templates)
        for i, n in enumerate(args.params):
            guardName = (
                f"_lib_{args.library}_{args.params[i]}.hpp"
                if args.library
                else f"{args.params[i]}.hpp"
            )
            config["CODE_GUARD"] = Identifier(guardName).allcaps
            config["NAME_HEADER"] = args.params[i]
            hpp.generate(
                "include",
                n,
                i,
                config,
                INCLUDES="header_includes__blank",
                BODY="header_body__blank",
            )
            cpp.generate(
                "src",
                n,
                i,
                config,
                INCLUDES="source_includes__blank",
                BODY="source_body__blank",
            )

        return 0
