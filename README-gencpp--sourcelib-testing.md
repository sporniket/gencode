# 'gencpp sourcelib-testing' CLI

Generate a blank program file and its blank header file.

**Content**

1. User manual
  * Synopsys
  * Positional arguments
  * Options
  * Description
  * Typical invocations

## User Manual

### Synopsys

`gencpp sourcelib-testing [--help] [--root <path>] [--copyright_years <years>] [--copyright_authors <authors>] [--project_name <name>] [--project_description <description>] [--project_licence <licence>] [--config <configuration>]`

### Positional arguments

_None_

### Options

_In addition to the **root path**, **configuration file** and **metada** sets of options._

* `-h`, `--help`: shows an help message and exits.

### Description

Generates a test runner using the [Criterion unit testing framework](https://github.com/Snaipe/Criterion), and specification files for `cmake`.

The project is supposed to be **a source library project**. The test runner is generated into a `src-tests` folder.

You need to edit the files generated in `src-tests` to implements the test suite. The main `CMakeLists.txt` explains how to build and run the test suite.

### Typical invocations

> It is better to prepare a configuration file to configure things like the project name and description, copyright notices and licence notices.

```
gencpp sourcelib-testing [options...]
```

Working in the current directory as root, the following hierarchy of files are created : 

```
<root>
    src-tests
    |   CMakeLists.txt
    |   TestRunner.cpp
    CMakeLists.txt
```
