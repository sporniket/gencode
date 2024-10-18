# 'gencpp blank' CLI

Generate a blank program file and its blank header file.

**Content**

1. User manual
2. $$$Other things noteworthy...

## User Manual

### Synopsys

`gencpp blank [--help] [--root <path>] <names>...`

#### Positional arguments

* `<names>...` : a list of blank filesets to generate (e.g. for the name `foo` : `foo.hpp` and `foo.cpp`).

#### Options

*  `-h`, `--help`: shows an help message and exits.
*  `--root <path>` : path to the root of the project where the files will be generated. When not specified, it will work in the current directory.

### Description

For each specified name, it generates the following files : 

* A header file, in a `include` directory.
* A program file, in a `src` directory.

### Typical invocation

```
gencpp blank foo bar
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

