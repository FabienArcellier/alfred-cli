import unittest

from alfred.lib import list_hierarchy_directory, override_envs, slugify
from alfred.os import is_posix, is_windows

import os


class TestLib(unittest.TestCase):

    def test_list_hierarchy_directory_should_return_a_list_of_all_parents_for_linux(self):
        if not is_posix():
            self.skipTest("this test run only on linux or macos environment")

        # Assign
        mypath = "/root/path/os/file"
        # Acts
        parents_directory = list_hierarchy_directory(mypath)

        # Assert
        self.assertEqual(5, len(parents_directory))
        self.assertEqual("/root/path/os/file", parents_directory[0])
        self.assertEqual("/root/path/os", parents_directory[1])
        self.assertEqual("/", parents_directory[4])

    def test_list_hierarchy_directory_should_return_a_list_of_all_parents_for_windows(self):
        if not is_windows():
            self.skipTest("this test run only on windows environment")

        # Assign
        mypath = "C:\\root\\path\\os\\file"
        # Acts
        parents_directory = list_hierarchy_directory(mypath)

        # Assert
        self.assertEqual(5, len(parents_directory))
        self.assertEqual("C:\\root\\path\\os\\file", parents_directory[0])
        self.assertEqual("C:\\root\\path\\os", parents_directory[1])
        self.assertEqual("\\", parents_directory[4])


    def test_override_envs_should_override_environment_variables_in_with_block(self):
        # Arrange
        os.environ['TEST'] = '1'

        with override_envs(TEST='2'):
            assert os.getenv('TEST') == '2'

        assert os.getenv('TEST') == '1'


    def test_override_envs_should_create_environment_variables_in_with_block_then_remove_it(self):
        # Arrange
        assert os.getenv('TESTANYYOLO') is None, f"TESTANYYOLO is already defined with value { os.getenv('TESTANYYOLO') }"

        with override_envs(TESTANYYOLO='2'):
            assert os.getenv('TESTANYYOLO') == '2'

        assert os.getenv('TESTANYYOLO') is None

    def test_slugify_should_return_a_slug_of_text(self):
        # Arrange
        text = "This is a test ---"
        # Acts
        result = slugify(text)
        # Assert
        assert result == "this_is_a_test"



if __name__ == '__main__':
    unittest.main()
