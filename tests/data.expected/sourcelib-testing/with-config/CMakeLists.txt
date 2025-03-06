# SPDX-License-Identifier: GPL-3.0-or-later WITH this OR that
# Copyright (C) 2021~2024 John Doe, John Dee
# ---
# This is part of **Super project**.
# A project you did not know that you needed it
# ---
# This is a source library project. As such, no deliverable binary is generated.
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
project(super_project)
set(CMAKE_CXX_STANDARD 11)

# The test suite is implemented in a dedicated source folder.
add_subdirectory(src-tests)