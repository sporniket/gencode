# 'gencpp' CLI

Generator of C++ code.

**Content**

1. User manual
2. Common sets of arguments
3. Configuration file specification

## User Manual

### Synopsys

`gencpp [--help] <generator> <arguments>...`

#### Positional arguments

* `<generator>` : the name of the generator to use.
* `<arguments>...` : the arguments of the generator, see the specific user manual for further details.

#### Options

*  `-h`, `--help`: shows an help message and exits.

### Description

Invoke the specified generator.

### Typical invocation

```
gencpp blank foo bar
```

Invoke the generator `blank` with arguments `foo` and `bar`.

## Common sets of arguments

Generators will share some groups of arguments that are described here : 

* the root path set
* the configuration file set
* the metadata set

## The root path set

* `--root <path>` : path to the root of the project where the files will be generated. When not specified, it will work in the current directory.

## The configuration file set

* `--config <configuration>` : a configuration file from which can be extracted some of the options common to files from the same project ; the configuration file specification follows the scheme `<format>:<path/to/file>`, with `<format>` being `gencode` ; e.g. `--config gencode:./gencpp_project.json`. Any settings contained by the configuration file override any corresponding option from the command line.

## The metadata set

* `--copyright_years <years>` : specifies the years of the copyright, either simple like '2023' or complex like '2019,2020,2021'.
* `--copyright_authors <authors>` : specifies one (e.g. 'John Doe') or more (e.g. 'John Doe, Jane Dee') authors for copyright attribution.
* `--project_name <name>` : specifies the project name.
* `--project_description <description>` : specifies a short, one line description of the project.
* `--project_licence <licence>` : A SPDX licence identifier or expression.

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