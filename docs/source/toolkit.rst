Command toolkit
###############

Alfred offers APIs to write commands, reuse existing commands, specify behavior depending on the bone, ...
They aim to make your commands easy to read, write and maintain.

.. module:: alfred

API to write command
********************

The following methods are used to set up a command that you can use through alfred.

.. autofunction:: command

.. autofunction:: option

.. autofunction:: sh

.. autofunction:: run

.. autofunction:: invoke_command

.. autofunction:: CMD_RUNNING

.. autofunction:: pythonpath

.. autofunction:: env

API to check environment
************************

.. autofunction:: is_posix

.. autofunction:: is_windows

.. autofunction:: is_linux

.. autofunction:: is_macos

.. autofunction:: project_directory

.. autofunction:: execution_directory
