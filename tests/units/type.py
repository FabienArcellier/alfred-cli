import unittest

from alfred.type import AlfredConfiguration


class TestType(unittest.TestCase):

    def setUp(self):
        pass

    def test_AlfredConfiguration_manage_environment_variables(self):
        # Assign
        configuration = AlfredConfiguration({
            'environment': [
                "PIP_VALUE=1",
                "PIP",
            ]
        })
        # Acts
        result = configuration.environments()

        # Assert
        self.assertEqual("PIP_VALUE", result[0].key)
        self.assertEqual("1", result[0].value)
        self.assertEqual("PIP", result[1].key)
        self.assertEqual("", result[1].value)


if __name__ == '__main__':
    unittest.main()
