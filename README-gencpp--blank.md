# 'gencpp blank' CLI

Generate a blank program file and its blank header file.

**Content**

1. User manual
  * Synopsys
  * Positional arguments
  * Options
  * Description
  * Typical invocations
2. Configuration file specification

## User Manual

### Synopsys

`gencpp blank [--help] [--root <path>] [--copyright_years <years>] [--copyright_authors <authors>] [--project_name <name>] [--project_description <description>] [--project_licence <licence>] [--library <library>] [--config <configuration>] <names>...`

### Positional arguments

* `<names>...` : a list of blank filesets to generate (e.g. for the name `foo` : `foo.hpp` and `foo.cpp`).

### Options

* `-h`, `--help`: shows an help message and exits.
* `--root <path>` : path to the root of the project where the files will be generated. When not specified, it will work in the current directory.
* `--copyright_years <years>` : specifies the years of the copyright, either simple like '2023' or complex like '2019,2020,2021'.
* `--copyright_authors <authors>` : specifies one (e.g. 'John Doe') or more (e.g. 'John Doe, Jane Dee') authors for copyright attribution.
* `--project_name <name>` : specifies the project name.
* `--project_description <description>` : specifies a short, one line description of the project.
* `--project_licence <licence>` : A SPDX licence identifier or expression.
* `--library <library>` : files will be generated as part of the named library, in a subfolder of the project.
* `--config <configuration>` : a configuration file from which can be extracted some of the options common to files from the same project ; the configuration file specification follows the scheme `<format>:<path/to/file>`, with `<format>` being `gencode` ; e.g. `--config gencode:./gencpp_project.json`. Any settings contained by the configuration file override any corresponding option from the command line.

### Description

For each specified name, it generates the following files : 

* A header file, in a `include` directory.
* A program file, in a `src` directory.

### Typical invocations

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


#### Generate files for the main program

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

## Configuration file specification

When the `--config <configuration>` option is used, and specify the format `gencode` (e.g. `--config gencode:myconfig.whatever`), **then** the designated file MUST be a JSON representation that must follows the following structure : 

* `copyright`
  * `years` : string, when present, has the same effect as `--copyright_years`
  * `authors` : string, when present, has the same effect as `--copyright_authors`
* `project`
  * `name` : string, when present, has the same effect as `--project_name`
  * `description` : string, when present, has the same effect as `--project_description`
  * `licence` : string, when present, has the same effect as `--project_licence`

All the fields are optionnal.

An exemple of a complete configuration files.

```json
{
    "copyright":{
       "years":"2021~2024",
       "authors":"John Doe, John Dee"
    },
    "project":{
       "name":"Super project",
       "description":"A project you did not know that you needed it",
       "licence":"GPL-3.0-or-later WITH this OR that"
    }
}
```