Write commands
##############

Command generation with ``alfred --new`` is limited to simple cases. It is possible to create more complex commands using the library functions.

You can write a command in any python module inside the ``alfred`` folder. Just decorate a function with ``alfred.command``.

Write a simple command
**********************

The command is the basic element to create a task to be executed.

.. code-block:: python

    @alfred.command('lint', help="validate your product using mypy")
    def lint():
        alfred.run("mypy src/alfred")

.. warning::

    It's not run in a shell. Operations like ">" or ">>" are not supported

.. warning::

    On windows, commands like ``Echo`` or ``Copy`` on Windows are internal commands to the Cmd.exe shell, not executable. They cannot be used from Alfred.

    I recommand using ``print`` and ``shutil.copy`` instead.

Compose a command
*****************

Retrieving the executable and using an argument array makes command composition easier. It is possible to add or remove arguments depending on the platform or environment.

.. code-block:: python
    :caption: alfred/lint.py

    import alfred

    @alfred.command('lint', help="validate your product using mypy")
    def lint():
        mypy = alfred.sh('mypy', "mypy is not installed")
        alfred.run(mypy, ["src/alfred"])

Use optional parameters
***********************

It would be great to be able to investigate a failing job and run it in verbose mode without writing a new command.

For example, we want to run the unit tests in verbose mode to get more information about the tests.

.. code-block:: python
    :caption: alfred/tests.py

    import alfred

    @alfred.command('test', help="execute unit tests with pytest")
    @alfred.option('--verbose', help="run pytest in verbose mode", is_flag=True, default=False)
    def test(verbose):
        pytest = alfred.sh('pytest', "pytest is not installed")
        args = [] if not verbose else ['-v']
        args += ['tests']

        alfred.run(pytest, args)

Click **Next** when you are ready to write your first pipeline !
