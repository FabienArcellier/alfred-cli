Alfred
======

.. image:: https://img.shields.io/pypi/v/alfred-cli.svg?label=Version
    :target: https://pypi.org/project/alfred-cli/

.. image:: https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci.yml

.. image:: https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci-windows.yml/badge.svg
    :target: https://github.com/FabienArcellier/alfred-cli/actions/workflows/ci-windows.yml

.. image:: https://readthedocs.org/projects/alfred-cli/badge/?version=latest
    :target: https://alfred-cli.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/discord-alfred-5865F2?logo=discord&logoColor=white
    :target: https://discord.gg/nMn9YPRGSY

.. image:: https://img.shields.io/badge/license-MIT-007EC7.svg
    :target: https://github.com/FabienArcellier/alfred-cli/blob/master/LICENSE

Alfred is an extensible automation tool designed to **streamline repository operations**. It allows you various commands as continuous integration, runner, build commands ...

You'll craft advanced commands harnessing **the strengths of both worlds: shell and Python**.

Demo
----

.. raw:: html

    <img src="https://media.githubusercontent.com/media/FabienArcellier/alfred-cli/master/docs/demo-1.gif" alt="introductory video of alfred" width="100%">

Quick start
-----------

You will generate commands to launch of the linter and unit tests process.

.. code-block:: bash
    :caption: generate the command to lint the code base

    $ alfred --new pylint src/myapp

.. code-block:: text

    Name of the command ?: lint
    Description of `lint` command ?: run linter on codebase
    Module of `lint` command ? [alfred/commands.py]:
    >>> @alfred.command('lint', help="run linter on codebase")
    >>> def pylint():
    >>>   alfred.run('pylint src/myapp')

    Do you want to create the following `lint` command in `alfred/commands.py` ?  (y, n) [y]: y

.. code-block:: bash
    :caption: generate the command to run test on the code base

    $ alfred --new pytest tests/unit

.. code-block:: text

    Name of the command ?: tests
    Description of `tests` command ?: run unit tests on codebase
    Module of `tests` command ? [alfred/commands.py]:
    >>> @alfred.command('tests', help="run unit tests on codebase")
    >>> def tests():
    >>>   alfred.run('pytest tests/unit')

    Do you want to create the following `tests` command in `alfred/commands.py` ?  (y, n) [y]: y


.. code-block:: bash
    :caption: show alfred commands

    $ alfred

.. code-block:: text

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


Documentation
-------------

.. toctree::
   :maxdepth: 1

   installation
   getting_started
   command
   pipelines
   command_line
   project
   api_reference
   features
   benefits
   advanced

Links
-----

* Documentation : https://alfred-cli.readthedocs.io/en/latest
* PyPI Release : https://pypi.org/project/alfred-cli
* Source code: https://github.com/FabienArcellier/alfred-cli
* Chat: https://discord.gg/nMn9YPRGSY

Related
-------

Alfred-cli exists thanks to this 2 open source projects.

* `click <https://github.com/pallets/click/>`__
* `plumbum <https://github.com/tomerfiliba/plumbum>`__

Click **Next** when you are ready to install alfred !
