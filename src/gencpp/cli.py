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
import re
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .producers import ProducerOfBlank, ProducerOfSourcelibTesting

producers = {
    "blank": ProducerOfBlank(),
    "sourcelib-testing": ProducerOfSourcelibTesting(),
}


class GenCppCli:
    @staticmethod
    def createArgParser() -> ArgumentParser:
        # TODO Rewrite parser as needed
        parser = ArgumentParser(
            prog="python3 -m gencode.gencpp",
            description="Generate CPP code files tree or snippet.",
            epilog="""---
(c) 2024 David SPORN
---
This is part of Gencode -- Sporniket's generator of code.

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
""",
            formatter_class=RawDescriptionHelpFormatter,
            allow_abbrev=False,
        )

        # Add the subparsers
        subparsers = parser.add_subparsers(help="The generator to use", required=True)
        for key in producers:
            producers[key].appendSubParser(key, subparsers)

        return parser

    def __init__(self):
        pass

    def checkFolderOrMake(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise ValueError(f"not.directory:{path}")

    def run(self):
        try:
            args = GenCppCli.createArgParser().parse_args()
            return args.func(args)
            # TODO other things that may throw a value error
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        else:
            return 2
