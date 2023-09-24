## Alfred

[![PyPi](https://img.shields.io/pypi/v/alfred-cli.svg?label=Version)](https://pypi.org/project/alfred-cli/)
[![Python](https://img.shields.io/pypi/pyversions/alfred-cli.svg)](https://pypi.org/project/alfred-cli/)
[![CI](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci.yml) [![CI-Windows](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci-windows.yml/badge.svg)](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci-windows.yml)
[![Documentation Status](https://readthedocs.org/projects/alfred-cli/badge/?version=latest)](https://alfred-cli.readthedocs.io/en/latest/?badge=latest)
[![Discord](https://img.shields.io/badge/discord-alfred-5865F2?logo=discord&logoColor=white)](https://discord.gg/nMn9YPRGSY)
[![License](https://img.shields.io/badge/license-MIT-007EC7.svg)](LICENSE)

Alfred is an extensible automation tool. It allows you to build your **continuous integration scripts** in python, and much more. You can replace any scripts using **the best of both worlds, shell and python**.

### Demo

[![asciicast](https://asciinema.org/a/i7YVDmQBRYVKAq1k74n9oYp0x.svg)](https://asciinema.org/a/i7YVDmQBRYVKAq1k74n9oYp0x)
**introductory video on using alfred**

### Quick-start

Commands of the code base are documented when you run ``alfred`` in a terminal.

```bash
Usage: alfred [OPTIONS] COMMAND [ARGS]...

  alfred is a building tool to make engineering tasks easier to develop and to
  maintain

Commands:
  ci                  execute continuous integration process of alfred
  docs:html           build documentation in html format
  lint                validate the source code using pylint
  publish             tag a new release and trigger pypi publication
  tests               validate alfred with all the automatic testing
```

the commands are implemented in python in modules in the subdirectory ``./alfred``.

*./alfred/lint.py*
```python
@alfred.command('lint', help="validate the source code using pylint")
@alfred.option('-v', '--verbose', is_flag=True, default=False)
def lint(verbose: bool):
    if verbose is False:
        alfred.run('pylint src/alfred')
    else:
        alfred.run('pylint --verbose --reports y src/alfred')
```

*./alfred/ci.py*
```python
@alfred.command('ci', help="execute continuous integration process of alfred")
@alfred.option('-v', '--verbose', is_flag=True)
def ci(verbose: bool):
    alfred.invoke_command('lint', verbose=verbose)
    alfred.invoke_command('tests', verbose=verbose)
```

## Links

* Documentation : https://alfred-cli.readthedocs.io/en/latest
* PyPI Release : https://pypi.org/project/alfred-cli
* Source code: https://github.com/FabienArcellier/alfred-cli
* Chat: https://discord.gg/nMn9YPRGSY

## Related

``alfred`` exists thanks to this 2 amazing open source projects.

* [click](https://github.com/pallets/click/)
* [plumbum](https://github.com/tomerfiliba/plumbum>)


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
