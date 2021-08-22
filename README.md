## Motivation

Alfred is an extensible building tool that can replace a Makefile or Fabric.
Writing commands in python is done in a few minutes, even in the case of a mono-repository
which contains several products.

```bash
# run the continuous integration process
alfred ci

alfred product1:migrate:database
```

[![ci](https://github.com/FabienArcellier/blueprint-library-pip/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/blueprint-library-pip/actions/workflows/ci.yml)

## Behind the scene

Alfred is magic thanks to click and plumblum :

* click
* plumblum

Those libraries are hidden but they are the core of execution of alfred.

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/blueprint-library-pip.git
```

## Developper guideline

```
$ make
activate                       activate the virtualenv associate with this project
coverage                       output the code coverage in htmlcov/index.html
help                           provides cli help for this makefile (default)
install_requirements_dev       install pip requirements for development
install_requirements           install pip requirements based on requirements.txt
lint                           run pylint
tests                          run automatic tests
tests_units                    run only unit tests
tox                            run existing test suite on python 2.7, python 3.6 and python 3.7
update_requirements            update the project dependencies based on setup.py declaration
```

### Install development environment

Use make to instanciate a python virtual environment in ./venv and install the
python dependencies.

```bash
make install_requirements_dev
```

### Install production environment

```bash
make install_requirements
```

### Initiate or update the library requirements

If you want to initiate or update all the requirements `install_requires` declared in `setup.py`
and freeze a new `Pipfile.lock`, use this command

```bash
make update_requirements
```

### Activate the python environment

When you setup the requirements, a `venv` directory on python 3 is created.
To activate the venv, you have to execute :

```bash
make venv
source venv/bin/activate
```

### Run the linter and the unit tests

Before commit or send a pull request, you have to execute `pylint` to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
make lint
make tests
```

## Contributors

* Fabien Arcellier

## License

MIT License

Copyright (c) 2021 Fabien Arcellier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
