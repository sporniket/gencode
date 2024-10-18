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

import io
import os
import sys


from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from .utils import initializeTmpWorkspace, thenActualFileIsSameAsExpected

from gencpp import GenCppCli

ARGS = ["prog", "blank"]
SOURCE_DATA_FILES = os.path.join(".", "tests", "data")
EXPECTED_DATA_FILES = os.path.join(".", "tests", "data.expected")


def thenItHasExpectedFolders(folders: list[str]):
    for f in folders:
        assert os.path.exists(f)
        assert os.path.isdir(f)


def test_that_it_create_files_in_main_directory():
    # Prepare files
    setupFileNames = []
    tmp_dir = initializeTmpWorkspace(
        [os.path.join(SOURCE_DATA_FILES, f) for f in setupFileNames]
    )

    # execute
    with patch.object(sys, "argv", ARGS + ["--root", tmp_dir, "whatEver", "foo"]):
        with redirect_stdout(io.StringIO()) as out:
            with redirect_stderr(io.StringIO()) as err:
                returnCode = GenCppCli().run()

    # verify
    assert out.getvalue() == ""
    assert err.getvalue() == ""
    assert returnCode == 0
    thenItHasExpectedFolders(
        [
            os.path.join(tmp_dir, "include"),
            os.path.join(tmp_dir, "src"),
        ]
    )
    for fileset in [
        [
            os.path.join(tmp_dir, "include", "whatEver.hpp"),
            os.path.join(EXPECTED_DATA_FILES, "root_whatever.hpp"),
        ],
        [
            os.path.join(tmp_dir, "src", "whatEver.cpp"),
            os.path.join(EXPECTED_DATA_FILES, "root_whatever.cpp"),
        ],
        [
            os.path.join(tmp_dir, "include", "foo.hpp"),
            os.path.join(EXPECTED_DATA_FILES, "root_foo.hpp"),
        ],
        [
            os.path.join(tmp_dir, "src", "foo.cpp"),
            os.path.join(EXPECTED_DATA_FILES, "root_foo.cpp"),
        ],
    ]:
        thenActualFileIsSameAsExpected(fileset[0], fileset[1])
