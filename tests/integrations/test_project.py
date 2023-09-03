import os

from fixtup import fixtup

from alfred import project


def test_list_all_should_get_current_project_first():
    # Arrange
    with fixtup.up('project_with_name'):

        # Acts
        all_projects = project.list_all()

        # Asserts
        assert all_projects[0].name == 'project'
        assert all_projects[0].directory == os.path.realpath(os.getcwd())

def test_list_all_should_get_current_project_and_all_subproject():
    # Arrange
    # This test is slow because loading the multiproject fixture loads the virtualenv of the 2 subprojects.
    with fixtup.up('multiproject'):

        # Acts
        all_projects = project.list_all()

        # Asserts
        assert all_projects[0].directory == os.path.realpath(os.getcwd())
        project_names = [project.name for project in all_projects]
        assert "product1" in project_names
        assert "product2" in project_names
