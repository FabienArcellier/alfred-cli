Getting started
###############

To configure a python project to use alfred, here is the procedure:

.. code-block:: bash
    pip install alfred-cli
    alfred init


You can run alfred to see the available commands.

.. code-block::bash

    alfred

.. code-block:: text

    Usage: alfred [OPTIONS] COMMAND [ARGS]...

    ...

    Commands:
      hello_world  let alfred introduce it self


The "hello_world" command is created automatically during initialization. It serves as an introduction to Alfred.

.. code-block:: bash

    alfred hello_world

.. code-block:: text

    Hello world, I am alfred, an extensible automation tool.

    I am here to assist you and your team in your daily tasks.
    You can ask me to run simple tasks as just run automatic tests.
    You can also ask me to run complex workflow as continuous integration & application deployment.

    You will write your commands in python, and I will run them for you


    Would you want to start ? (y, n) [n]
