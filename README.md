# gencode – Sporniket's toolbox for generating code

![PyPI - Version](https://img.shields.io/pypi/v/gencode-by-sporniket)
![PyPI - License](https://img.shields.io/pypi/l/gencode-by-sporniket)


> [WARNING] Please read carefully this note before using this project. It contains important facts.

Content

1. What is **gencode – Sporniket's toolbox for generating code**, and when to use it ?
2. What should you know before using **gencode – Sporniket's toolbox for generating code** ?
3. How to use **gencode – Sporniket's toolbox for generating code** ?
4. Known issues
5. Miscellanous

## 1. What is **gencode – Sporniket's toolbox for generating code**, and when to use it ?

**gencode – Sporniket's toolbox for generating code** is a code generator. For now it can generate a set of blanks cpp files and their header files, with parameters to have proper licence notice, copyright notices and taylored header guards.

### What's new in version 1.1.0

A new generator is available to create a test runner for a source library project.

* Resolves #6 : [gencpp] 'gencpp sourcelib-testing'

### What's new in version 1.0.1

Change entry point from `gncpp` to `gencpp`, as expected by the READMEs. 

### What's new in version 1.0.0

Initial release, that can generate blank cpp files and their header files.

* Resolves #1 : [gencpp] generate a blank cpp file and its header
* Resolves #2 : [gencpp] generate a valid copyright notice
* Resolves #3 : [gencpp] generate a valid licence notice
* Resolves #4 : [gencpp] generate a header guard using a library name
* Resolves #5 : [gencpp] use a config file to factor common parameters


### Licence
 **gencode – Sporniket's toolbox for generating code** is free software: you can redistribute it and/or modify it under the terms of the
 GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
 option) any later version.

 **gencode – Sporniket's toolbox for generating code** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
 even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 more details.

 You should have received a copy of the GNU General Public License along with **gencode – Sporniket's toolbox for generating code**.
 If not, see http://www.gnu.org/licenses/ .


## 2. What should you know before using **gencode – Sporniket's toolbox for generating code** ?

> **SECURITY WARNING** : **gencode – Sporniket's toolbox for generating code** is not meant to be installed on a public server.

**gencode – Sporniket's toolbox for generating code** is written in [Python](http://python.org) language, version 3.9 or above, and consists of :

* [gencpp](./README-gencpp.md) : the generator of CPP code.

> Do not use **gencode – Sporniket's toolbox for generating code** if this project is not suitable for your project

## 3. How to use **gencode – Sporniket's toolbox for generating code** ?

### Requirements

Python 3.9 or later versions, `pip3` and `pdm` are required.

### From source

To get the latest available code, one must clone the git repository, build and install to the maven local repository.

	git clone https://github.com/gencode.git
	cd gencode
	pdm sync
	pdm build
    sudo pip3 install dist/gencode-by-sporniket-<version>-py3-none-any.whl

### From Pypi
Add any of the following dependencies that are appropriate to your project.

```
sudo pip3 install gencode-by-sporniket
```

### Documentation

* [User manual of `gencpp`](./README-gencpp.md) 
  * [User manual of `gencpp blank`](./README-gencpp--blank.md)

## 4. Known issues
See the [project issues](https://github.com/gencode/issues) page.

## 5. Miscellanous

### Report issues
Use the [project issues](https://github.com/gencode/issues) page.
