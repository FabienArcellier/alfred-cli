## Alfred

Alfred is an extensible automation tool. It allows you to build your **continuous integration scripts** in python, and much more. You can replace any scripts using **the best of both worlds, shell and python**.

[![asciicast](https://asciinema.org/a/i7YVDmQBRYVKAq1k74n9oYp0x.svg)](https://asciinema.org/a/i7YVDmQBRYVKAq1k74n9oYp0x)
**introductory video on using alfred**

Want to try and look for inspiration, here are examples of commands that I implement in my projects :

```bash
alfred ci # run your own continuous integration process
alfred publish # publish a package on pypi
alfred run # run your app
alfred db:init # initialize a database
alfred db:migrate # plays your migrations on your database
...
```

[![version](https://img.shields.io/pypi/v/alfred-cli.svg?label=version)](https://pypi.org/project/alfred-cli/) [![MIT](https://img.shields.io/badge/license-MIT-007EC7.svg)](LICENSE.md)

[![ci](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci.yml) [![ci-windows](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci-windows.yml/badge.svg)](https://github.com/FabienArcellier/pyalfred/actions/workflows/ci-windows.yml)

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Getting started](#getting-started)
- [Links](#links)
- [Cookbook](#cookbook)
  * [Write your first command](#write-your-first-command)
  * [Write your first workflow](#write-your-first-workflow)
- [Benefits](#benefits)
  * [Alfred scales with your team](#alfred-scales-with-your-team)
  * [Alfred likes mono-repository](#alfred-likes-mono-repository)
- [Behind the scene](#behind-the-scene)
  * [Why using alfred instead of Makefile or Bash scripts](#why-using-alfred-instead-of-makefile-or-bash-scripts)
- [Why not using alfred](#why-not-using-alfred)
- [The latest version](#the-latest-version)
- [Cookbook](#cookbook-1)
  * [Display the commands really executed](#display-the-commands-really-executed)
  * [Customize a command for a specific OS](#customize-a-command-for-a-specific-os)
  * [Override environment variables](#override-environment-variables)
    + [Add directories into pythonpath](#add-directories-into-pythonpath)
- [Developper guideline](#developper-guideline)
  * [Run the linter and the unit tests](#run-the-linter-and-the-unit-tests)
- [Contributors](#contributors)
- [License](#license)

<!-- TOC end -->

## Getting started

To configure a python project to use alfred, here is the procedure:

```bash
pip install alfred-cli
alfred init
```

You can run alfred to see the available commands.

```bash
alfred
```

The "hello_world" command is created automatically during initialization. It serves as an introduction to Alfred.


```bash
alfred hello_world
```

## Links

* Documentation : https://alfred-cli.readthedocs.io/en/latest
* PyPI Release : https://pypi.org/project/alfred-cli
* Source code: https://github.com/FabienArcellier/alfred-cli
* Chat: https://discord.gg/nMn9YPRGSY

## Cookbook

### Write your first command

You can add your command in a new module in `./alfred`.
In this example we will add the command `alfred lint` :

*alfred/lint.py*
```python
import alfred

@alfred.command('lint', help="validate your product using mypy")
def lint():
    mypy = alfred.sh('mypy', "mypy is not installed")
    alfred.run(mypy, ["src/alfred"])
```

### Write your first workflow

*alfred/ci.py*
```python
import alfred

@alfred.command('ci', help="execute continuous integration process")
def ci(verbose: bool):
    alfred.invoke_command('lint')
    alfred.invoke_command('tests')
```

## Benefits

### Alfred scales with your team

Alfred grows with your team. You can start with one command and then add more. When you feel that your command file is too crowded, you can restructure it into several files, or even separate it into several subfolders. Alfred is able to search all your orders by scanning a folder and its subfolders. It's all configurable.

### Alfred loves mono-repository

Alfred is built with the idea of being usable in a mono-repository which brings together several python, react, node projects in the same code repository. You can create several alfred sub-projects. At the root of the project, you will have access to all the commands of all the subprojects using the subproject name ``alfred project1 ci``.

## Behind the scene

Alfred rely heavily on click and plumblum :

* [click](https://click.palletsprojects.com/en/8.0.x/)
* [plumblum](https://plumbum.readthedocs.io/en/latest/)

### Why using alfred instead of Makefile or Bash scripts

One of the advantages of `bash` and `Makefile` is their native presence in many environments. By default, a `Makefile` allows you to segment these commands efficiently. Autocompletion is first-citizen  feature. Alfred doesn't have it yet.

Alfred allows you to create more complex commands than with Make. From the start, you benefit from a formatted documentation for each of your orders. It is easy to create one command per file  thanks to auto discovery. You can see an implementation in this repository in [`alfred_cmd/`](alfred/).

Alfred allows you to mix shell code with python instructions. In some cases, it allows you to perform efficient processing on API calls. You can use either the cli (for git, ...) or pythons libraries depending on the nature of the treatment you want to perform.

In our development process, we frequently need to operate on application with several process (frontend in react, server in flask, two external service in flask). To mount those process, we use `honcho` with alfred to load `Procfile` that will manage those process.

## Why not using alfred

Alfred is not designed to build a cli you will distribute on pypi. You should use [click](https://click.palletsprojects.com/en/8.0.x/) for that.

Alfred command can import only installed library. You can't use relative import in command module. You have to extend python path to share function between commands.

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/alfred-cli.git
```

## Cookbook

### Use debug mode

You can display the shell commands really executed, either to debug the arguments,
either to run in your terminal again with other attributes.

The option `d` / `--debug` display all the shell commands that are executed by
`alfred.run()` in your alfred command.

```bash
$ alfred -d ci

2022-02-07 19:38:31,834 DEBUG - /home/far/.local/share/virtualenvs/20210821_1530__alfred-cli-a8dwJte3/bin/python -m unittest discover units - wd: /home/far/documents/projects/20210821_1530__alfred-cli/tests
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

### Customize a command for a specific OS

Alfred can run a specific part of the build for an OS,
for example to only run the linter on a linux machine.

```python
@alfred.command('ci', help="execute continuous integration process of alfred")
@alfred.option('-v', '--verbose', is_flag=True)
def ci(verbose: bool):
    if alfred.is_posix():
        alfred.invoke_command('lint', verbose=verbose)
    else:
        print("linter is not supported on non posix platform as windows")

    alfred.invoke_command('tests', verbose=verbose)
```

the ``alfred.is_posix``, ``alfred.is_linux``, ``alfred.is_macos``, ``alfred.is_windows`` functions allow you to quickly
target the environment on which specific processing must be performed.

### Override environment variables

```python
@alfred.command('ci', help="execute continuous integration process of alfred")
def ci():
    with alfred.env(SCREEN="display"):
        bash = alfred.sh("bash")
        bash.run("-c" "echo $SCREEN")
```

#### Add directories into pythonpath

Adding a folder in the pythonpath variable allows you to expose packages without declaring them in ``pyproject.toml``.

```python
@alfred.command('ci', help="execute continuous integration process of alfred")
@alfred.pythonpath(['tests'], append_project=False)
def ci():
    bash = alfred.sh("bash")
    alfred.run(bash, ["-c", "echo $SCREEN"])
```

```python
@alfred.command('ci', help="execute continuous integration process of alfred")
def ci():
    with alfred.pythonpath():
        bash = alfred.sh("bash")
        alfred.run(bash, ["-c", "echo $SCREEN"])
```

The ``alfred.pythonpath`` decorator adds the project root. You can save specific folders here. It's useful if you have deactivate ``python_path_project_root`` in ``.alfred.toml``, otherwise, it's already imported.

```python
@alfred.command('ci', help="execute continuous integration process of alfred")
@alfred.pythonpath()
def ci():
    bash = alfred.sh("bash")
    alfred.run(bash, ["-c" "echo $SCREEN"])
```

## Developper guideline

```bash
poetry install
poetry shell
```

```
$ alfred
Usage: alfred [OPTIONS] COMMAND [ARGS]...

  alfred is a building tool to make engineering tasks easier to develop and to
  maintain

Options:
  -d, --debug  display debug information like command runned and working
               directory
  --help       Show this message and exit.

Commands:
  ci                 execute continuous integration process of alfred
  dist               build distribution packages
  lint               validate alfred using pylint on the package alfred
  publish            tag a new release and trigger pypi publication
  tests              validate alfred with all the automatic testing
  tests:acceptances  validate alfred with acceptances testing
  tests:units        validate alfred with unit testing
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

Copyright (c) 2021-2023 Fabien Arcellier

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
