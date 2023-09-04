Features
########

Welcome to the documentation page dedicated to the features implemented on Alfred.

Alfred offers a full range of features to simplify creating deployment scripts and writing maintenance scripts
for a project. Here is an exhaustive list of all implemented features.

Command line & Shell
********************

* create a new alfred project with ``alfred init``
* execute a command ``alfred {my command}``
* document existing command ``alfred --help``
* debug a command ``alfred --debug {my command}``

Commands
********

* create a new command in existing project with ``@alfred.command``
* invoke a sub-command with argument in alfred command with ``alfred.shell`` and ``alfred.run``
* ensure command invokation from alfred project root
* use the output of sub-command in python in alfred command

Projects
********

* discovers commands in multiple locations
* discover commands in subprojects as multi command ``alfred {project} {command}``
* execute a command from a virtual environment associated with the project
* detect automatically virtual environment in ``.venv`` directory

Utilities
*********

* configure the shell completion with ``alfred --completion``
* check the alfred commands for continuous integration with ``alfred --check``
* show the installed alfred version with ``alfred --version``
