## Motivation

Alfred is an extensible building tool that can replace a Makefile or Fabric.
Writing commands in python is done in a few minutes, even in the case of a mono-repository
which contains several products.

```bash
# run the continuous integration process
alfred ci

alfred product1:migrate:database
```

[![ci](https://github.com/FabienArcellier/pyalfred/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/pyalfred/actions/workflows/ci.yml)

## Behind the scene

Alfred rely heavily on click and plumblum :

* [click]()
* [plumblum]()

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/pyalfred.git
```

## Developper guideline

```bash
pipenv install
pipenv shell
```

```
$ alfred

Usage: alfred [OPTIONS] COMMAND [ARGS]...

  alfred is a building tool to make engineering tasks easier to develop and to
  maintain

Options:
  --help  Show this message and exit.

Commands:
  ci                 execute continuous integration process of alfred
  lint               validate alfred using pylint on the package alfred
  tests              validate alfred with all the automatic testing
  tests:acceptances  validate alfred with acceptances testing
  tests:units        validate alfred with unit testing
```

### Install development environment

Use make to instanciate a python virtual environment in ./venv and install the
python dependencies.

```bash
pipenv install --dev
```

### Install production environment

```bash
pipenv install
```

### Initiate or update the library requirements

If you want to initiate or update all the requirements `install_requires` declared in `setup.py`
and freeze a new `Pipfile.lock`, use this command

```bash
pipenv update
```

### Activate the python environment

When you setup the requirements, a `venv` directory on python 3 is created.
To activate the venv, you have to execute :

```bash
pipenv shell
```

### Run the linter and the unit tests

Before commit or send a pull request, you have to execute `pylint` to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
alfred ci
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
