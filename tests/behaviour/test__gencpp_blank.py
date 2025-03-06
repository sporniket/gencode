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
EXPECTED_DATA_FILES = os.path.join(".", "tests", "data.expected", "blank")


def thenItHasExpectedFolders(folders: list[str]):
    for f in folders:
        assert os.path.exists(f)
        assert os.path.isdir(f)


def test_that_it_generate_a_blank_cpp_file_and_its_header():
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
            os.path.join(EXPECTED_DATA_FILES, "with-params", "root_whatever.hpp"),
        ],
        [
            os.path.join(tmp_dir, "src", "whatEver.cpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-params", "root_whatever.cpp"),
        ],
        [
            os.path.join(tmp_dir, "include", "foo.hpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-params", "root_foo.hpp"),
        ],
        [
            os.path.join(tmp_dir, "src", "foo.cpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-params", "root_foo.cpp"),
        ],
    ]:
        thenActualFileIsSameAsExpected(fileset[0], fileset[1])


def test_that_it_generate_a_valid_copyright_notice():
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
            "--copyright_years",
            "2021~2024",
            "--copyright_authors",
            "John Doe, John Dee",
            "foo",
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
            os.path.join(tmp_dir, "include", "foo.hpp"),
            os.path.join(
                EXPECTED_DATA_FILES, "with-copyright", "root_foo_copyright.hpp"
            ),
        ],
        [
            os.path.join(tmp_dir, "src", "foo.cpp"),
            os.path.join(
                EXPECTED_DATA_FILES, "with-copyright", "root_foo_copyright.cpp"
            ),
        ],
    ]:
        thenActualFileIsSameAsExpected(fileset[0], fileset[1])


def test_that_it_generate_a_valid_licence_notice():
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
            "--project_name",
            "Super project",
            "--project_description",
            "A project you did not know that you needed it",
            "--project_licence",
            "GPL-3.0-or-later WITH this OR that",
            "foo",
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
            os.path.join(tmp_dir, "include", "foo.hpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-licence", "root_foo_licence.hpp"),
        ],
        [
            os.path.join(tmp_dir, "src", "foo.cpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-licence", "root_foo_licence.cpp"),
        ],
    ]:
        thenActualFileIsSameAsExpected(fileset[0], fileset[1])


def test_that_it_generate_a_header_guard_using_a_library_name():
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
            "--library",
            "superUtils",
            "foo",
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
            os.path.join(tmp_dir, "lib", "superUtils", "include", "foo.hpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-library", "lib_foo.hpp"),
        ],
        [
            os.path.join(tmp_dir, "lib", "superUtils", "src", "foo.cpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-library", "lib_foo.cpp"),
        ],
    ]:
        thenActualFileIsSameAsExpected(fileset[0], fileset[1])


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
            "foo",
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
            os.path.join(tmp_dir, "include", "foo.hpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-option", "root_foo_config.hpp"),
        ],
        [
            os.path.join(tmp_dir, "src", "foo.cpp"),
            os.path.join(EXPECTED_DATA_FILES, "with-option", "root_foo_config.cpp"),
        ],
    ]:
        thenActualFileIsSameAsExpected(fileset[0], fileset[1])
