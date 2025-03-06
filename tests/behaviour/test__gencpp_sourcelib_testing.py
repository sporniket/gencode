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

ARGS = ["prog", "sourcelib-testing"]
SOURCE_DATA_FILES = os.path.join(".", "tests", "data")
EXPECTED_DATA_FILES = os.path.join(".", "tests", "data.expected", "sourcelib-testing")


def test_that_it_uses_a_config_file_to_factor_common_parameters():
    # Prepare files
    setupFileNames = []
    tmp_dir = initializeTmpWorkspace(
        [os.path.join(SOURCE_DATA_FILES, f) for f in setupFileNames]
    )

    # execute
    with patch.object(
        sys,
        "argv",
        ARGS
        + [
            "--root",
            tmp_dir,
            "--config",
            "gencode:tests/data/config.json",
        ],
    ):
        with redirect_stdout(io.StringIO()) as out:
            with redirect_stderr(io.StringIO()) as err:
                returnCode = GenCppCli().run()

    # verify
    assert out.getvalue() == ""
    assert err.getvalue() == ""
    assert returnCode == 0
    for fileset in [
        [
            os.path.join(tmp_dir, "CMakeLists.txt"),
            os.path.join(EXPECTED_DATA_FILES, "with-config", "CMakeLists.txt"),
        ],
        [
            os.path.join(tmp_dir, "src-tests", "CMakeLists.txt"),
            os.path.join(
                EXPECTED_DATA_FILES, "with-config", "src-tests", "CMakeLists.txt"
            ),
        ],
        [
            os.path.join(tmp_dir, "src-tests", "TestRunner.cpp"),
            os.path.join(
                EXPECTED_DATA_FILES, "with-config", "src-tests", "TestRunner.cpp"
            ),
        ],
    ]:
        thenActualFileIsSameAsExpected(fileset[0], fileset[1])
