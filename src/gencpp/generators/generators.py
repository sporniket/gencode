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


class _GeneratorOf:
    def __init__(
        self,
        rootPath: str,
        templates,
        extension: str,
        template_prefix: str,
        template_spdx: str,
    ):
        self._rootPath = rootPath
        self._templates = templates
        self._extension = extension
        self._template_prefix = template_prefix
        self._template_spdx = template_spdx

    def computeFileName(self, localPath: str, baseName: str, extension: str) -> str:
        return (
            os.path.join(self._rootPath, localPath, f"{baseName}.{extension}")
            if len(extension) > 0
            else os.path.join(self._rootPath, localPath, baseName)
        )

    def write(self, fileName, fileContent):
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

    def _computeConfig(
        self, config: dict[str, str], index: int, **kwargs
    ) -> dict[str, str]:
        configWithIndex = {"__index": index}
        configWithIndex.update(config)
        result = {
            f"{self._template_prefix}{k}": self._templates[v].render(configWithIndex)
            for k, v in kwargs.items()
        }
        result.update(configWithIndex)
        return result

    def generate(
        self,
        localPath: str,
        baseNameWithoutExtension,
        index: int,
        config: dict[str, str],
        **kwargs,
    ):
        configOfGenerator = self._computeConfig(config, index, **kwargs)
        source = self.applyTemplates(
            configOfGenerator, f"{self._template_prefix}SOURCE"
        )
        target = self.computeFileName(
            localPath, baseNameWithoutExtension, self._extension
        )
        self.write(target, source)
