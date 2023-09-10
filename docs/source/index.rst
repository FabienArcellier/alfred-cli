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


Alfred is an extensible automation tool. It allows you to build your **continuous integration scripts** in python, and much more. You can replace any scripts using **the best of both worlds, shell and python**.

Demo
----

.. raw:: html

    <script async id="asciicast-i7YVDmQBRYVKAq1k74n9oYp0x" src="https://asciinema.org/a/i7YVDmQBRYVKAq1k74n9oYp0x.js"></script>

Quick start
-----------

Commands of the code base are documented when you run ``alfred`` in a terminal.

.. code-block:: bash
    :caption: alfred

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

.. code-block:: python
    :caption: ./alfred/ci.py

    @alfred.command('ci', help="execute continuous integration process of alfred")
    @alfred.option('-v', '--verbose', is_flag=True)
    def ci(verbose: bool):
        alfred.invoke_command('lint', verbose=verbose)
        alfred.invoke_command('tests', verbose=verbose)

Documentation
-------------

.. toctree::
   :maxdepth: 1

   installation
   getting_started
   command
   features
   command_line
   project
   toolkit
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
