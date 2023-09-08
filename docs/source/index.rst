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

Want to try and look for inspiration, here are examples of commands that I implement in my projects :

.. raw:: html

    <script async id="asciicast-i7YVDmQBRYVKAq1k74n9oYp0x" src="https://asciinema.org/a/i7YVDmQBRYVKAq1k74n9oYp0x.js"></script>

.. code-block:: bash

    alfred ci # run your own continuous integration process
    alfred publish # publish a package on pypi
    alfred run # run your app
    alfred db:init # initialize a database
    alfred db:migrate # plays your migrations on your database
    ...

.. toctree::
   :maxdepth: 1

   installation
   getting_started
   command
   features
   command_line
   project
   toolkit
   advanced


Alfred scales with your team
----------------------------

Alfred grows with your team. You can start with one command and then add more. When you feel that your command file is too crowded, you can restructure it into several files, or even separate it into several subfolders. Alfred is able to search all your orders by scanning a folder and its subfolders. It's all configurable.

Alfred loves mono-repository
----------------------------

Alfred is built with the idea of being usable in a mono-repository which brings together several python, react, node projects in the same code repository. You can create several alfred sub-projects. At the root of the project, you will have access to all the commands of all the subprojects using the subproject name ``alfred project1 ci``.

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
