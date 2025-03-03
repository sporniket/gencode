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

import os
from .templates import TEMPLATE_SOURCES__BLANK


class _GeneratorOf:
    def __init__(self, rootPath: str, templates):
        self._rootPath = rootPath
        self._templates = templates
        self._template_spdx = "DEFINE IT IN SUBCLASS"

    def _computeFileName(self, localPath: str, baseName: str, extension: str) -> str:
        return (
            os.path.join(self._rootPath, localPath, f"{baseName}.{extension}")
            if len(extension) > 0
            else os.path.join(self._rootPath, localPath, baseName)
        )

    def _write(self, fileName, fileContent):
        try:
            with open(fileName, "x") as out:
                out.write(fileContent)
        except FileExistsError:
            print(f"error.file.exists:{fileName}")

    def _prependSpdxLineIfAppliable(self, config: dict[str, str], source: str) -> str:
        if len(config["LICENCE_SPDX"]) == 0:
            return source

        config.update(
            {
                "BODY": source,
                "SPDX_LINE": self._templates[self._template_spdx].render(config),
            }
        )
        return self._templates["spdx_wrap"].render(config)

    def applyTemplates(self, config: dict[str, str], templateKey: str) -> str:
        source = self._templates[templateKey].render(config)
        return self._prependSpdxLineIfAppliable(config, source)

    def generate(
        self,
        name,
        index: int,
        config: dict[str, str],
        *,
        bodyTemplate: str = "header_body_blank",
        localPath: str = "include",
    ):
        pass


class _GeneratorOfC(_GeneratorOf):
    def __init__(self, rootPath: str, templates):
        super().__init__(rootPath, templates)
        self._extension = "nope"
        self._template_prefix = "NOPE_"
        self._template_spdx = "spdx_line__slash_star"

    def _computeConfig(
        self, config: dict[str, str], includesTemplateKey: str, bodyTemplateKey: str
    ) -> dict[str, str]:
        result = {
            f"{self._template_prefix}INCLUDES": self._templates[
                includesTemplateKey
            ].render(config),
            f"{self._template_prefix}BODY": self._templates[bodyTemplateKey].render(
                config
            ),
        }
        result.update(config)
        return result

    def generate(
        self,
        name,
        index: int,
        config: dict[str, str],
        *,
        includesTemplates: str = "header_includes__blank",
        bodyTemplate: str = "header_body__blank",
        localPath: str = "include",
    ):
        configOfGenerator = self._computeConfig(config, includesTemplates, bodyTemplate)
        source = self.applyTemplates(
            configOfGenerator, f"{self._template_prefix}SOURCE"
        )
        target = self._computeFileName(localPath, name, self._extension)
        self._write(target, source)


class GeneratorOfHppFiles(_GeneratorOfC):
    def __init__(self, rootPath: str, templates):
        super().__init__(rootPath, templates)
        self._extension = "hpp"
        self._template_prefix = "HPP_"


class GeneratorOfCppFiles(_GeneratorOfC):
    def __init__(self, rootPath: str, templates):
        super().__init__(rootPath, templates)
        self._extension = "cpp"
        self._template_prefix = "CPP_"
