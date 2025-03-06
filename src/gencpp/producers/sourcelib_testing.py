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
    TEMPLATE_SOURCE__CMAKE_FILES,
    TEMPLATE_SOURCE__CPP_FILES,
)
from gencpp.generators import generatorOfCMakeListsTxtFiles, generatorOfCppFiles
from gencpp.argparsers import (
    addConfigurationFileOptions,
    addProjectMetadataOptions,
    addRootPathOptions,
)

ONLY_DOTS = re.compile(r"[.]{3,}")  # accept '.' and '..' as path fragment


def splitAndFilterPath(path: str) -> list[str]:
    return [f for f in path.split("/") if f and not ONLY_DOTS.match(f)]


class ProducerOfSourcelibTesting(_Producer):
    def __init__(self):
        super().__init__()
        self._argParserArgumentHelpers = [
            addConfigurationFileOptions,
            addRootPathOptions,
            addProjectMetadataOptions,
        ]

    @property
    def helpMessage(self):
        return "Generate Cmake files and test runner for a source library project ; requires the criterion test library."

    @property
    def dictionnaryOfTemplates(self):
        result = {}
        for template in [
            TEMPLATE_SOURCES__META_STRINGS,
            TEMPLATE_SOURCE__SPDX,
            TEMPLATE_SOURCE__CMAKE_FILES,
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

        self.checkFolderOrMake(os.path.join(rootPath, "src-tests"))

        config.update({"NAME_SLUG": Identifier(config["LABEL_PROJECT"]).sluggified})

        cmake = generatorOfCMakeListsTxtFiles(rootPath, self._templates)
        cpp = generatorOfCppFiles(rootPath, self._templates)
        cmake.generate(
            "",
            "CMakeLists",
            0,
            config,
            BODY="cmake_body__source_lib_testing__main",
        )
        cmake.generate(
            "src-tests",
            "CMakeLists",
            0,
            config,
            BODY="cmake_body__source_lib_testing__test_runner",
        )
        cpp.generate(
            "src-tests",
            "TestRunner",
            0,
            config,
            INCLUDES="source_includes__source_lib_testing",
            BODY="source_body__source_lib_testing",
        )

        return 0
