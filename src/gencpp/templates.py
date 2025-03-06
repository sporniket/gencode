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

TEMPLATE_SOURCES__META_STRINGS = {
    "copyright": "Copyright (C) {{YEARS_COPYRIGHT}} {{NAMES_COPYRIGHT}}",
    # ---
    "project_label__no_licence": "ALL RIGHT RESERVED -- project **{{LABEL_PROJECT}}**.",
    "project_label__with_licence": "This is part of **{{LABEL_PROJECT}}**.",
    # ---
    "licence_spdx_id": "SPDX-License-Identifier: {{SPDX_CLAUSE}}",
}

TEMPLATE_SOURCE__SPDX = {
    "spdx_wrap": """{{SPDX_LINE}}
{{BODY}}""",
    "spdx_line__slash_star": "/* {{LICENCE_SPDX}} */",
    "spdx_line__hash": "# {{LICENCE_SPDX}}",
}

TEMPLATE_SOURCES__HPP_FILES = {
    "HPP_SOURCE": """/****************************************

---
{{COPYRIGHT}}
---
{{PROJECT_LABEL_CLAUSE}}
{{PROJECT_DESCRIPTION_CLAUSE}}
****************************************/
#ifndef {{CODE_GUARD}}
#define {{CODE_GUARD}}
// ================[ CODE BEGINS ]================

{{HPP_INCLUDES}}

{{HPP_BODY}}

// ================[ END OF CODE ]================
#endif""",
    # ---
    # Source file includes
    # ---
    "header_includes__blank": """// ...your includes... """,
    # ---
    # Header file bodies
    # ---
    "header_body__blank": """// ...your code...""",
}

TEMPLATE_SOURCE__CPP_FILES = {
    "CPP_SOURCE": """/****************************************

---
{{COPYRIGHT}}
---
{{PROJECT_LABEL_CLAUSE}}
{{PROJECT_DESCRIPTION_CLAUSE}}
****************************************/
{{CPP_INCLUDES}}

{{CPP_BODY}}

""",
    # ---
    # Source file includes
    # ---
    "source_includes__blank": """#include "{{NAME_HEADER}}.hpp\"""",
    "source_includes__source_lib_testing": """#include <criterion/criterion.h>
// FIXME includes your hpp files from ../include
// e.g. #include "whatever.hpp\"""",
    # ---
    # Source file bodies
    # ---
    "source_body__blank": """// ...your code...""",
    "source_body__source_lib_testing": """Test (groupName, doThis_should_return_zero) {
    cr_assert_eq(doThis(), 0);
}""",
}

TEMPLATE_SOURCE__CMAKE_FILES = {
    "CMAKE_SOURCE": """# {{COPYRIGHT}}
# ---
# {{PROJECT_LABEL_CLAUSE}}
# {{PROJECT_DESCRIPTION_CLAUSE}}
# ---
{{CMAKE_BODY}}
""",
    ########
    # Cmake bodies
    ########
    "cmake_body__source_lib_testing__main": """# This is a source library project. As such, no deliverable binary is generated.
#
# HOWEVER there is a test suite that can be compiled and invoked
# ---
# How to build and verify
# 
# 1. Create a build directory : `mkdir built-tests`
# 2. Change to this build directory : `cd build-tests`
# 3. Initialize the build system : `cmake ..`
# 4. Invoke the build system to perform the test suite :
#    * either `cmake --build . -- verify` to build incrementally.
#    * or `cmake --build . --clean-first -- verify` to trigger a full rebuild.
# ---
cmake_minimum_required(VERSION 3.28)
project({{NAME_SLUG}})
set(CMAKE_CXX_STANDARD 11)

# The test suite is implemented in a dedicated source folder.
add_subdirectory(src-tests)""",
    # ---
    "cmake_body__source_lib_testing__test_runner": """
# Define how to build the test suite 
set(BINARY ${CMAKE_PROJECT_NAME}--test)

# FIXME registers your cpp files from ../src
# e.g. : set(SOURCES TestRunner.cpp ../src/whatever.cpp)

add_executable(${BINARY} ${SOURCES})
target_include_directories(${BINARY} PUBLIC ../include)

# Uses criterion, see https://github.com/Snaipe/Criterion
find_library(LIBCRITERION criterion REQUIRED)
target_link_libraries(${BINARY} PRIVATE criterion)

# ---
# Create the custom task `verify` that MUST be invoked to run the test suite. 
# i.e. `cmake --build . -- verify`
add_custom_target(
    verify COMMAND env CLICOLOR_FORCE=1 ${CMAKE_CTEST_COMMAND} --verbose
    DEPENDS ${BINARY}
)

# ---
# Specify how to launch the test suite, and how to check that it pass
enable_testing()
add_test(NAME DoTest COMMAND ${CMAKE_CURRENT_BINARY_DIR}/${BINARY} --color=always)""",
}
