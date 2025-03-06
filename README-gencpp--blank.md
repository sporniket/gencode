# 'gencpp blank' CLI

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

`gencpp blank [--help] [--library <library>] [--root <path>] [--copyright_years <years>] [--copyright_authors <authors>] [--project_name <name>] [--project_description <description>] [--project_licence <licence>] [--config <configuration>] <names>...`

### Positional arguments

* `<names>...` : a list of blank filesets to generate (e.g. for the name `foo` : `foo.hpp` and `foo.cpp`).

### Options

_In addition to the **root path**, **configuration file** and **metada** sets of options._

* `-h`, `--help`: shows an help message and exits.
* `--library <library>` : files will be generated as part of the named library, in a subfolder of the project.

### Description

For each specified name, it generates the following files : 

* A header file, in a `include` directory.
* A program file, in a `src` directory.

### Typical invocations

> It is better to prepare a configuration file to configure things like the project name and description, copyright notices and licence notices.

#### Generate files for the main program

Use any options except `--library`

```
gencpp blank [options...] foo bar
```

Working in the current directory as root, the following hierarchy of files are created : 

```
<root>
    include
    |   bar.hpp
    |   foo.hpp
    src
        bar.cpp
        foo.cpp
```


#### Generate files for a library

Use option `--library` and any other options

```
gencpp blank --library FooLibrary [options...] foo bar
```

Working in the current directory as root, the following hierarchy of files are created : 

```
<root>
    lib
        FooLibrary
            include
            bar.hpp
            |   foo.hpp
            src
                bar.cpp
                foo.cpp
```
