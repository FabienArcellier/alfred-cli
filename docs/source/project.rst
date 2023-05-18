Project
#######

An alfred project is a set of commands and sub-projects linked by a `.alfred.toml` configuration file.

.. contents::
  :backlinks: top

Starting a project
******************

An alfred project can be initialized in any directory using ``alfred init`` command.

This command creates a ``.alfred.toml`` configuration file and creates a ``alfred`` directory which contains the commands.

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

    .. note::

        For expressions that are relative paths, they are resolved from the folder that contains
        the corresponding .alfred.toml manifest.

Section [alfred.project]
========================

.. glossary::

    command (optional)

        Default value: ``commands = [ "alfred/*.py" ]``

        A list of expressions to search for commands in a project. Commands can be declared in multiple locations.

        .. note::

            The `glob <https:docs.python.org3libraryglob.html>`_ module is used as an expression interpreter.
            The wildcards ``*`` et ``**`` are allowed to search subfolders recursively.

        .. note::

            For expressions that are relative paths, they are resolved from the folder that contains
            the corresponding .alfred.toml manifest.

    python_path_project_root (optional)

        Default value: ``python_path_project_root = true``

        Adds the project directory to the python path to be able to use python packages and modules from the project root without installing them in a virtual environment.

        This parameter corresponds to the option **Add content root to PYTHONPATH** in PyCharm.

    python_path_extends (optional)

        Default value: ``python_path_extends = []``

        Une liste de dossier à ajouter au path python. Ce paramètre permet d'enregistrer votre dossier de tests comme
        racine pour résoudre des imports sans l'installer au dans un environnement virtuel.

        .. code-block::

            [alfred.project]
            python_path_extends = [ "tests" ]

        .. note::

            For expressions that are relative paths, they are resolved from the folder that contains
            the corresponding .alfred.toml manifest.

    venv (optional)

        The virtual environment that is used to run the commands for this project. If this parameter is absent, the interpreter used to invoke the parent is used.

        .. code-block::

            [alfred.project]
            venv = ".venv"

        .. note::

            For expressions that are relative paths, they are resolved from the folder that contains
            the corresponding .alfred.toml manifest.

Organization of a mono-repository with sub-projects
***************************************************

In version-control systems, a monorepo ("mono" meaning 'single' and "repo" being short for 'repository') is a software-development strategy in which the code for a number of projects is stored in the same repository

In the case where these are different applications, they can have their own manifest, therefore their own venv.
Alfred allows them to be managed in a unified way thanks to the concept of sub-projects.

Organization by product
========================

Each application is declared in the ``products`` folder of the mono-repository.

.. code-block:: text

    .
    ├── alfred
    │   ├── ci.py
    │   └── deploy.py
    ├── __init__.py
    ├── products
    │   ├── product_1
    │   │   ├── .venv
    │   │   └── alfred
    │   │       ├── deploy.py
    │   │       └── ci.py
    │   │   └── .alfred.toml
    │   ├── product_2
    │   │   ├── .venv
    │   │   └── alfred
    │   │       ├── deploy.py
    │   │       └── ci.py
    │   │   └── .alfred.toml
    └── .alfred.toml

.. code-block:: toml
    :caption: ./.alfred.toml

    [alfred]
    subprojects = [ "product/*"]

.. code-block:: toml
    :caption: ./product_1/.alfred.toml

    [alfred]
    name = "product1"

    [alfred.project]
    venv = [ ".venv"]

.. code-block:: toml
    :caption: ./product_2/.alfred.toml

    [alfred]
    name = "product2"

    [alfred.project]
    venv = [ ".venv"]



