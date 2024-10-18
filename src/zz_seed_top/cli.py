"""
---
(c) 2024 David SPORN
---
This is part of $$$ -- whatever.

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
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter


class PrettyPrinterCli:
    @staticmethod
    def createArgParser() -> ArgumentParser:
        # TODO Rewrite parser as needed
        parser = ArgumentParser(
            prog="python3 -m $$$.pp",
            description="Whatever.",
            epilog="""---
(c) 2024 David SPORN
---
This is part of $$$ -- Sporniket's toolbox for assembly language.

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
""",
            formatter_class=RawDescriptionHelpFormatter,
            allow_abbrev=False,
        )

        # Add the arguments
        parser.add_argument(
            "--stylesheet",
            metavar="<stylesheet>",
            type=str,
            help="the formatting rules to follow, either 'builtin:heritage' (the default) or 'builtin:sporniket'",
        )

        parser.add_argument(
            "sources",
            metavar="<source files...>",
            type=str,
            nargs="*",
            help="a list of source files",
        )

        commandGroup = parser.add_mutually_exclusive_group(required=False)
        commandGroup.add_argument(
            "-r",
            "--rewrite",
            action="store_true",
            help=f"Replace the source files by their pretty-printed version WHEN THERE IS A DIFFERENCE.",
        )

        return parser

    def __init__(self):
        pass

    def run(self):
        try:
            args = PrettyPrinterCli.createArgParser().parse_args()
            # TODO other things that may throw a value error
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        else:
            if len(args.sources) > 0:
                # EITHER process given list of files...
                sourcesErrors = []

                # -- Check the list of files
                for source in args.sources:
                    if os.path.exists(source):
                        if os.path.isfile(source):
                            # NO PROBLEM
                            continue
                        else:
                            sourcesErrors += [
                                {"errorType": "NOT_A_FILE", "path": source}
                            ]
                    else:
                        sourcesErrors += [{"errorType": "MISSING_FILE", "path": source}]
                if len(sourcesErrors) > 0:
                    report = []
                    for e in sourcesErrors:
                        message = (
                            f"* MISSING : {e['path']}"
                            if e["errorType"] == "MISSING_FILE"
                            else f"* NOT A FILE : {e['path']}"
                        )
                        report += [message]
                    report = "\n".join(report)
                    print(
                        f"ERROR -- in given list of files :\n{report}", file=sys.stderr
                    )
                    return 1

                # -- Proceed
                for source in args.sources:
                    # This is a bootstrap with just reading the lines without further thinking
                    # If the input file is to be loaded in a whole string or as a binary file,
                    # write another loading code
                    with open(source, "rt") as f:
                        lines = f.readlines()
                    if args.whatever:
                        # WHATEVER PROCESSING MODE
                        for line in lines:
                            # TODO process lines accordingly
                            pass
                    else:
                        # Normal mode
                        for line in lines:
                            # TODO process lines accordingly
                            pass
            else:
                # ...OR process standard input

                # -- unless SOMETHING IS WRONG
                if args.rewrite:
                    print(
                        "ERROR -- rewrite mode requires a list of files",
                        file=sys.stderr,
                    )
                    return 1

                # -- Proceed
                for line in sys.stdin:
                    pass

            return 0
