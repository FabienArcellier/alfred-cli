import unittest

from alfred.lib import list_hierarchy_directory
from alfred.os import is_posix, is_windows


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


if __name__ == '__main__':
    unittest.main()
