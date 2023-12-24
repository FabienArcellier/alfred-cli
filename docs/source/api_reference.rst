API Reference
#############

Alfred offers APIs to write commands, reuse existing commands, ...
It aim to make your commands easy to read, write and maintain.

.. contents:: Table of Contents
  :local:
  :backlinks: top

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

API to ask information to the user
**********************************

.. autofunction:: prompt

.. autofunction:: confirm

API to check environment
************************

.. autofunction:: is_posix

.. autofunction:: is_windows

.. autofunction:: is_linux

.. autofunction:: is_macos

.. autofunction:: project_directory

.. autofunction:: execution_directory
