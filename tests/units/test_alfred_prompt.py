import pytest

import alfred.alfred_prompt as prompt


def test_prompt_should_support_test_mode_to_validate_in_automatic_test():
    # Arrange
    with prompt.use_test_prompt():
        prompt.send_test_response('y')

        # Act
        result = prompt.confirm('Are you sure ?', default='n')

        # Assert
        assert result is True


def test_prompt_should_validate_input_on_test_mode_using_validation_func():
    # Arrange
    with prompt.use_test_prompt():
        prompt.send_test_response('no')

        # Act
        try:
            result = prompt.confirm('Are you sure ?', default='no')
            pytest.fail('should have raised a ValueError')
        except ValueError as e:
            assert str(e) == "Please enter 'y' or 'n'"


