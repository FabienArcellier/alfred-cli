Getting started
###############

To configure a python project to use alfred, here is the procedure:

.. code-block:: bash

    alfred init

Write a first command to run the linter
***************************************

.. raw:: html

    <img src="https://media.githubusercontent.com/media/FabienArcellier/alfred-cli/master/docs/demo-2.gif" alt="demo of alfred lint" width="100%">

.. code-block:: bash
    :caption: generate the command to lint the code base

    $ alfred --new pylint src/myapp

.. code-block:: python
    :caption: alfred/commands.py

    import alfred

    @alfred.command('lint', help="run linter on codebase")
    def pylint():
        alfred.run('pylint src/myapp')

Write a second command to run the tests
***************************************

.. raw:: html

    <img src="https://media.githubusercontent.com/media/FabienArcellier/alfred-cli/master/docs/demo-3.gif" alt="demo of alfred tests" width="100%">

.. code-block:: bash
    :caption: generate the command to run test on the code base

    $ alfred --new pytest tests/unit


.. code-block:: python
    :caption: alfred/commands.py

    import alfred

    @alfred.command('lint', help="run linter on codebase")
    def pylint():
        alfred.run('pylint src/myapp')

    @alfred.command('tests', help="run unit tests on codebase")
    def tests():
        alfred.run('pytest tests/unit')


View documentation of commands
******************************

.. raw:: html

    <img src="https://media.githubusercontent.com/media/FabienArcellier/alfred-cli/master/docs/demo-4.gif" alt="self documenting alfred commands" width="100%">

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


Click **Next** when you are ready to customize command !
