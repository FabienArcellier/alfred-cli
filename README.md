## Alfred

[![PyPi](https://img.shields.io/pypi/v/alfred-cli.svg?label=Version)](https://pypi.org/project/alfred-cli/)
[![Python](https://img.shields.io/pypi/pyversions/alfred-cli.svg)](https://pypi.org/project/alfred-cli/)
[![CI](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci.yml) [![CI-Windows](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci-windows.yml/badge.svg)](https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci-windows.yml)
[![Documentation Status](https://readthedocs.org/projects/alfred-cli/badge/?version=latest)](https://alfred-cli.readthedocs.io/en/latest/?badge=latest)
[![Discord](https://img.shields.io/badge/discord-alfred-5865F2?logo=discord&logoColor=white)](https://discord.gg/nMn9YPRGSY)
[![License](https://img.shields.io/badge/license-MIT-007EC7.svg)](LICENSE)

Alfred is an extensible automation tool designed to **streamline repository operations**. It allows you various commands as continuous integration, runner, build commands ...

You'll craft advanced commands harnessing **the strengths of both worlds: shell and Python**.


### Demo

![introductory video of alfred](https://media.githubusercontent.com/media/FabienArcellier/alfred-cli/master/docs/demo-1.gif)
**introductory video**

### Quick-start

You will generate commands to launch of the linter and unit tests process.

```bash
$ alfred --new pylint src/myapp
```

```bash
$ alfred --new pytest tests/unit
```

```bash
alfred
```

```text
Usage: alfred [OPTIONS] COMMAND [ARGS]...

  alfred is an extensible automation tool designed to streamline repository
  operations.

Options:
  -d, --debug    display debug information like command runned and working
                 directory
  -v, --version  display the version of alfred
  --new          open a wizard to generate a new command
  -c, --check    check the command integrity
  --completion   display instructions to enable completion for your shell
  --help         Show this message and exit.

Commands:
  lint                run linter on codebase
  tests               run unit tests on codebase
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
