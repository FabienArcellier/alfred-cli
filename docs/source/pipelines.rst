Write pipeline
###############

A pipeline in alfred is a command that invokes other commands. No fuss ...
The declaration remains identical to a command.

Write a command chain
*********************

.. code-block:: python
    :caption: alfred/ci.py

    import alfred

    @alfred.command('ci', help="execute continuous integration process")
    def ci():
        alfred.invoke_command('lint')
        alfred.invoke_command('tests')


.. warning::

    You can't a subcommand directly using ``lint()``. Currently the pattern is not supported and even if it may work in the future, it will broke as soon as you move the command ``lint`` into another module.

Use optional parameter in command chain
***************************************

A pipeline can pass an optional parameter to the commands it invokes.

.. code-block:: python
    :caption: alfred/ci.py

    import alfred

    @alfred.command('ci', help="execute continuous integration process")
    @alfred.option('verbose', help="run continuous integration in verbose mode", is_flag=True, default=False)
    def ci(verbose):
        alfred.invoke_command('lint')
        alfred.invoke_command('test', verbose=verbose)

Click **Next** when you are ready to discover the command line of alfred !
