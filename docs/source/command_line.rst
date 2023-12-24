Alfred cli
##########

The use of alfred is done from the command line. To launch alfred, just run ``alfred`` in a terminal

.. raw:: html

    <img src="https://media.githubusercontent.com/media/FabienArcellier/alfred-cli/master/docs/demo-4.gif" alt="alfred command lines" width="100%">

.. contents::
  :backlinks: top

Start an alfred project
=======================

``alfred init`` will create a ``./.alfred.toml``, the manifest about the project, and a ``./alfred`` folder which
contains a first command you should tune.

Discovers commands
==================

If you type ``alfred`` in a project from a terminal, the list of available commands will be displayed in the terminal.

.. code-block::

    Usage: alfred [OPTIONS] COMMAND [ARGS]...

    alfred is a building tool to make engineering tasks easier to develop and to
    maintain

    ...

    Commands:
      ci                  execute continuous integration process of alfred
      dist                build distribution packages
      ...

Execute a command
=================

``alfred {command}`` executes a command. For example, ``alfred lint`` will execute the command ``lint``.

Display inline documentation
============================

``alfred {command} --help`` displays the help of the command. For example, ``alfred lint --help`` will display the
arguments of the command ``lint``.

.. code-block::

    alfred lint --help
    Usage: alfred lint [OPTIONS]

      validate alfred using pylint on the package alfred

    Options:
      -v, --verbose
      --help         Show this message and exit.

Advanced usage
==============

.. contents::
  :local:

Show the version
----------------

.. code-block:: bash

    alfred --version

Configure autocompletion
------------------------

The ``alfred --completion`` command details the configuration to put in place to activate autocompletion in your shell.

.. code-block:: bash

    alfred --completion

.. warning:: ``alfred --completion`` is available for bash, zsh and fish.

    Configuring autocomplete relies on `click <https://click.palletsprojects.com/en/8.1.x/shell-completion/>`__. If you are using another shell and click supports it, open an issue with details for us to add support.

Execute in debug mode
---------------------

.. code-block:: bash

    alfred --debug {command}

    alfred --debug {subproject} {command}

If you run ``alfred`` with the ``--debug`` option, the detail of the execution will be displayed with each shell instruction executed
with the command that is launched, the arguments that are passed to it and the execution folder .

.. code-block::

    2023-05-02 06:44:12,314 DEBUG - /home/user/projects/alfred-cli/.venv/bin/pylint /home/user/projects/alfred-cli/src/alfred - wd: /home/user/projects/alfred-cli [main.py:239]

.. note::

    For debug information to display, an alfred command must implement the following pattern to execute a shell statement.

    .. code-block:: python

        echo = alfred.sh("echo")
        alfred.run(echo, ["hello", "world"])

Check the alfred commands
-------------------------

``alfred --check`` checks the integrity of the commands. It verifies that the command files are interpretable in the main project and in all subprojects.

.. code-block:: bash

    alfred --check

.. note:: it's recommanded to run ``alfred --check`` in your continuous integration process.

.. warning:: ``alfred --check`` don't check the parameters of the command and the code inside commands.


Click **Next** when you are ready to discover how to tune alfred settings !
