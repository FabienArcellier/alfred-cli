## Motivation

Alfred is an extensible building tool that can replace a Makefile or Fabric.
Writing commands in python is done in a few minutes, even in the case of a mono-repository
which contains several products.

In this dev, we are eating our own dog food. We are using `alfred` for the continuous integration process
of itself instead of `Makefile` as I usually do.

```bash
# run the continuous integration process
alfred ci

# publish the package on pypi
alfred twine
```

[![ci](https://github.com/FabienArcellier/pyalfred/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/pyalfred/actions/workflows/ci.yml)

## Getting started

To configure a python project to use alfred, here is the procedure:

```bash
pip3 install alfred-cli
alfred init
```

A hello_world command was created for the example:

```bash
alfred hello_world --name "Fabien"
```

A file `.alfred.yml` will be initialized at the root of the repository.

## Behind the scene

Alfred rely heavily on click and plumblum :

* [click](https://click.palletsprojects.com/en/8.0.x/)
* [plumblum](https://plumbum.readthedocs.io/en/latest/)

## Why using alfred instead of Makefile or Bash scripts

One of the advantages of `bash` and `Makefile` is their native presence in many environments.
By default, a `Makefile` allows you to segment these commands efficiently. Autocompletion is first-citizen
feature. Alfred doesn't have it yet.

Alfred allows you to create more complex commands than with Make. From the start, you benefit from a
formatted documentation for each of your orders. It is easy to create one command per file  thanks
to auto discovery. You can see an implementation in this repository in [`alfred_cmd/`](alfred_cmd/).

Thanks to the power of Click, it's easy to add options to your commands.
They allow for example to implement flags for your CI process which
offer you an execution for the frontend.

Alfred allows you to mix shell code with python instructions. In some cases, it allows you
to perform efficient processing on API calls. You can use either the cli (for git, ...) or
pythons libraries depending on the nature of the treatment you want to perform.

In our development process, we frequently need to operate on application with several process (frontend in react,
server in flask, two external service in flask). To mount those process, we use `honcho` with alfred
to load `Procfile` that will manage those process.

## Why not using alfred

If you want to create a cli you will distribute, alfred is not designed for that. I won't recommand
as well to use it to build a data application even if you can use python and many library.

Alfred command can import only installed library. You can't use relative import. That makes difficult to
share code between your commands.

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
  dist               build distributions for alfred in dist/
  lint               validate alfred using pylint on the package alfred
  tests              validate alfred with all the automatic testing
  tests:acceptances  validate alfred with acceptances testing
  tests:units        validate alfred with unit testing
  twine              push the package to pypi
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
