import os

import fixtup

from alfred import ctx


def test_env_pythonpath_should_build_pythonpath_with_project_root():
    # Arrange
    with fixtup.up("project"):
        root_dir = os.getcwd()

        # Acts
        pythonpath = ctx.env_pythonpath(root_dir)

        # Asserts
        pythonpath_parts = pythonpath.split(os.pathsep)
        assert pythonpath_parts[0] == root_dir


def test_env_pythonpath_should_use_the_pythonpath_extension_of_manifest():
    # Arrange
    with fixtup.up("pythonpath_extends"):
        root_dir = os.getcwd()

        # Acts
        pythonpath = ctx.env_pythonpath(root_dir)

        # Asserts
        pythonpath_parts = pythonpath.split(os.pathsep)
        assert pythonpath_parts[0] == os.path.join(root_dir, "tests")


def test_env_path_should_use_the_path_extension_of_manifest():
    # Arrange
    with fixtup.up("path_extends"):
        root_dir = os.getcwd()

        # Acts
        pythonpath = ctx.env_path(root_dir)

        # Asserts
        pythonpath_parts = pythonpath.split(os.pathsep)
        assert pythonpath_parts[0] == os.path.join(root_dir, "bin")
