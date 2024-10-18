# ${PROJECT_LABEL}

![PyPI - Version](https://img.shields.io/pypi/v/${PROJECT_PYPI})
![PyPI - License](https://img.shields.io/pypi/l/${PROJECT_PYPI})


> [WARNING] Please read carefully this note before using this project. It contains important facts.

Content

1. What is **${PROJECT_LABEL}**, and when to use it ?
2. What should you know before using **${PROJECT_LABEL}** ?
3. How to use **${PROJECT_LABEL}** ?
4. Known issues
5. Miscellanous

## 1. What is **${PROJECT_LABEL}**, and when to use it ?

**${PROJECT_LABEL}** is ....

### What's new in ...

* Initial release 

### Licence
 **${PROJECT_LABEL}** is free software: you can redistribute it and/or modify it under the terms of the
 GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
 option) any later version.

 **${PROJECT_LABEL}** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
 even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 more details.

 You should have received a copy of the GNU General Public License along with **${PROJECT_LABEL}**.
 If not, see http://www.gnu.org/licenses/ .


## 2. What should you know before using **${PROJECT_LABEL}** ?

> **SECURITY WARNING** : **${PROJECT_LABEL}** is not meant to be installed on a public server.

**${PROJECT_LABEL}** is written in [Python](http://python.org) language, version 3.9 or above, and consists of :

* [${PROJECT_CLI}](./${README_CLI}.md) : the Pretty Printer.

> Do not use **${PROJECT_LABEL}** if this project is not suitable for your project

## 3. How to use **${PROJECT_LABEL}** ?

### Requirements

Python 3.9 or later versions, `pip3` and `pdm` are required.

### From source

To get the latest available code, one must clone the git repository, build and install to the maven local repository.

	git clone https://github.com/${PROJECT_GITHUB_REPO}.git
	cd spasm
	pdm build
    sudo pip3 install dist/${PROJECT_PYPI}-<version>-py3-none-any.whl

### From Pypi
Add any of the following dependencies that are appropriate to your project.

```
sudo pip3 install ${PROJECT_PYPI}
```

### Documentation

* [User manual of `${PROJECT_CLI}`](./${README_CLI}.md) ; [Specifications of whatever](./${README_CLI}--whatever.md)

## 4. Known issues
See the [project issues](https://github.com/${PROJECT_GITHUB_REPO}/issues) page.

## 5. Miscellanous

### Report issues
Use the [project issues](https://github.com/${PROJECT_GITHUB_REPO}/issues) page.
