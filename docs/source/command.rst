Command
#######

Write a command
***************

The command is the basic element to create a task to be executed.

.. code-block:: python
    :caption: alfred/lint.py

    import alfred

    @alfred.command('lint', help="validate your product using mypy")
    def lint():
        mypy = alfred.sh('mypy', "mypy is not installed")
        alfred.run(mypy, ["src/alfred"])

.. note::

    You can use write a command in full text. This pattern is a shortcut to avoid instantiating the utility.
    The code runs the same way as above.

    It's not run in a shell. Operations like ">" or ">>" are not supported

    .. code-block:: python

        @alfred.command('lint', help="validate your product using mypy")
        def lint():
            alfred.run("mypy src/alfred")

.. warning::

    On windows, commands like ``Echo`` or ``Copy`` on Windows are internal commands to the Cmd.exe shell, not executable.
    They cannot be used from Alfred.

Write your first workflow
*************************

A workflow in alfred is a command that invokes other commands. No fuss ...
The syntax remains identical to that of a command.

.. code-block:: python
    :caption: alfred/ci.py

    import alfred

    @alfred.command('ci', help="execute continuous integration process")
    def ci():
        alfred.invoke_command('lint')
        alfred.invoke_command('tests')


.. warning::

    You can't a subcommand directly using ``lint()``. Currently the pattern is not supported and even if it may work in the future, it will broke as soon as you move the command ``lint`` into another module.

Use optional parameter
**********************

It would be great to be able to investigate a failing job and run it in verbose mode without writing a new command. It is possible, alfred offers the possibility to define optional parameters for a command to customize the execution.

For example, we want to run the unit tests in verbose mode to get more information about the tests.

We also want to be able to do it from the command ``ci`` that call it.

.. code-block:: python
    :caption: alfred/ci.py

    import alfred

    @alfred.command('ci', help="execute continuous integration process")
    @alfred.option('verbose', help="run continuous integration in verbose mode", is_flag=True, default=False)
    def ci(verbose):
        alfred.invoke_command('lint')
        alfred.invoke_command('test', verbose=verbose)


.. code-block:: python
    :caption: alfred/tests.py

    import alfred

    @alfred.command('test', help="execute unit tests with pytest")
    @alfred.option('--verbose', help="run pytest in verbose mode", is_flag=True, default=False)
    def test(verbose):
        pytest = alfred.sh('pytest', "pytest is not installed")
        args = [] if not verbose else ['-v']
        args.append('-v')

        args += ['tests']

        alfred.run(pytest, args)
