import unittest

from alfred.lib import list_hierarchy_directory
from alfred.type import path


class TestLib(unittest.TestCase):

    def test_list_hierarchy_directory_should_return_a_list_of_all_parents(self):
        # Assign
        mypath = path("/root/path/os/file")
        # Acts
        parents_directory = list_hierarchy_directory(mypath)

        # Assert
        self.assertEqual(5, len(parents_directory))
        self.assertEqual("/root/path/os/file", parents_directory[0])
        self.assertEqual("/root/path/os", parents_directory[1])
        self.assertEqual("/", parents_directory[4])


if __name__ == '__main__':
    unittest.main()
