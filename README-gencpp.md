# 'gencpp' CLI

Generator of C++ code.

**Content**

1. User manual
2. $$$Other things noteworthy...

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