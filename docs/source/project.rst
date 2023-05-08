Project
#######

An alfred project is a set of commands and sub-projects linked by a `.alfred.toml` configuration file.

.. contents::
  :backlinks: top

Starting a project
******************

An alfred project can be initialized in any directory using ``alfred init`` command.

This command creates a ``.alfred.toml`` configuration file and creates a ``alfred`` directory
which contains the commands.

.. code-block:: bash
    :caption: console

    alfred init

.. code-block:: text
    :caption: example of an alfred project structure

    $ tree

    .
    ├── alfred
    │   ├── ci.py
    │   ├── dist.py
    │   ├── docs.py
    │   ├── lint.py
    │   ├── publish.py
    │   └── tests.py
    └── .alfred.toml


Setting up a project with .alfred.toml
**************************************

.. code-block:: toml
    :caption: .alfred.toml

    [alfred]
    name = "fixtup" # optional
    description = "str" # optional
    subprojects = [ "product/*", "lib/*" ] # optional

    [alfred.project]
    command = [ "alfred/*.py" ] # optional
    env = { } # optional
    python_path_project_root = true # optional
    python_path_extends = [] # optional
    venv = "src/.." # optional

Section [alfred]
================

.. glossary::

  name (optional)
    name of the project or sub-project. This parameter defines the name of the group which gives access to the commands
    of a sub-project.

    .. note::

        If this parameter is absent, the name of the project is deduced from the name of the folder which contains the configuration file
        ``.alfred.toml``.

    .. warning::

        The name of a project must not contain spaces. If the name of a subproject contains a space, the commands will
        not be accessible.

  description (optional)
    description of the project or subproject displayed when the user uses ``alfred`` or ``alfred --help``.

  subprojects (optional)

    Default value: ``subprojects = []``

    a list of expressions to search for sub-projects in a mono-repository.

    .. note::

        The `glob <https:docs.python.org3libraryglob.html>`_ module is used as an expression interpreter.
        The wildcards ``*`` et ``**`` are allowed to search subfolders recursively.

    .. warning::

        a sub-project is an alfred project declared in a sub-folder. Currently, alfred only manages one level of subproject.

        Even if a subproject contains a ``subprojects`` declaration, alfred ignores this declaration when crawling
        the contents of the subproject.

Section [alfred.project]
========================

.. glossary::

    command (optional)

        Default value: ``commands = [ "alfred/*.py" ]``

        A list of expressions to search for commands in a project. Commands can be declared in multiple locations.

        .. note::

            The `glob <https:docs.python.org3libraryglob.html>`_ module is used as an expression interpreter.
            The wildcards ``*`` et ``**`` are allowed to search subfolders recursively.

Organisation d'un mono-repository avec des sous projets
*******************************************************

Dans le cas d'un mono-repository qui héberge plusieurs applications, les sous projets peuvent être déclarés au
même niveau des autres manifests (``pyrpoject.toml``, ``package.json``, ...).




