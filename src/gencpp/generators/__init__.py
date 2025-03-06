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

from .generators import _GeneratorOf


def generatorOfHppFiles(rootPath: str, templates) -> _GeneratorOf:
    return _GeneratorOf(rootPath, templates, "hpp", "HPP_", "spdx_line__slash_star")


def generatorOfCppFiles(rootPath: str, templates) -> _GeneratorOf:
    return _GeneratorOf(rootPath, templates, "cpp", "CPP_", "spdx_line__slash_star")


def generatorOfCMakeListsTxtFiles(rootPath: str, templates) -> _GeneratorOf:
    return _GeneratorOf(rootPath, templates, "txt", "CMAKE_", "spdx_line__hash")


__all__ = [
    "generatorOfCMakeListsTxtFiles",
    "generatorOfCppFiles",
    "generatorOfHppFiles",
]
