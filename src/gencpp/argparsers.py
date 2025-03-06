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


def addConfigurationFileOptions(parser):
    parser.add_argument(
        "--config",
        metavar="<format>:<path/to/config file>",
        type=str,
        help="the project wide configuration file",
    )


def addRootPathOptions(parser):
    parser.add_argument(
        "--root",
        metavar="<rootdir>",
        type=str,
        default=".",
        help="the relative path of the project, defaults to the current path",
    )


def addProjectMetadataOptions(parser):
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
