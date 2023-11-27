import contextlib
import threading
from sys import stdin
from typing import Optional, List, Callable

import click
import prompt_toolkit
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.validation import Document, Validator, ValidationError

class Driver:
    prompt_toolkit='prompt_toolkit'
    pytest= 'pytest'

prompt_context = threading.local()
prompt_context.input = [] # use only with fake driver
prompt_context.driver = Driver.prompt_toolkit

def prompt(label: str, proposals: Optional[List[str]] = None, default: Optional[str] = None, validation_func: Optional[Callable[[str], Optional[str]]] = None) -> str:
    """
    Prompt the user for an input

    >>> alfred.prompt("What is your name ?")

    >>> alfred.prompt("Where were you born ?", proposals=["France", "Other"], default="France")

    >>> alfred.prompt("What is your name ?", validation_func=lambda name: "Name is required" if name == "" else None)

    :param label: the question asked to the user
    :param proposals: the proposals displayed to the user in auto-completion
    :param default: the default value if the user leaves the field empty
    :param validation_func: a function that validates the user input
    :return: the user input
    """
    if proposals is None:
        proposals = []

    if prompt_context.driver == Driver.pytest:
        _input = _emulate_prompt_on_test(default, validation_func)
    elif stdin.isatty():
        _input = prompt_toolkit.prompt(label, completer=FuzzyWordCompleter(proposals), validator=FuncValidator(default, validation_func))
    else:
        _input = _emulate_prompt_on_non_tty(label, default, validation_func)

    if _input == "":
        return default

    return _input


def confirm(question: str, default: str = "n") -> bool:
    """
    Ask the user for a confirmation

    >>> alfred.confirm("Are you sure ?")

    >>> alfred.confirm("Are you sure ?", default="y")

    :param question: the question asked to the user
    :param default: the default value if the user leaves the field empty
    :return: True if the user confirmed, False otherwise
    """
    return prompt(question + f" (y, n) [{default}]: ", proposals=["y", "n"], default=default, validation_func=_check_confirm) == "y"


class FuncValidator(Validator):
    def __init__(self, default: str, validation_func: Callable[[str], Optional[str]]):
        self.validation_func = validation_func
        self.default = default

    def validate(self, document: Document) -> None:
        if self.validation_func is None:
            return

        if document.text == self.default:
            return

        error = self.validation_func(document.text)
        if error is not None:
            raise ValidationError(message=error, cursor_position=len(document.text))


def _check_confirm(proposition: str) -> Optional[str]:
    if proposition not in ["y", "n"]:
        return "Please enter 'y' or 'n'"

    return None


def _emulate_prompt_on_test(default, validation_func):
    _input = prompt_context.input.pop(0)
    if _input == "" and default is not None:
        _input = default

    if validation_func is not None:
        validation = validation_func(_input)
        if validation is not None:
            raise ValueError(validation)

    return _input


def _emulate_prompt_on_non_tty(label: str, default: Optional[str], validation_func: Optional[Callable[[str], Optional[str]]] = None):
    is_valid = False
    _input = ''
    while not is_valid:
        _input = input(label)
        if _input == "" and default is not None:
            _input = default

        if validation_func is not None:
            validation = validation_func(_input)
            if validation is not None:
                click.echo(f"Not valid: {validation}")
                is_valid = False
            else:
                is_valid = True

    return _input

### The following method are dedicated to testing ###

@contextlib.contextmanager
def use_test_prompt():
    previous_driver = prompt_context.driver
    prompt_context.driver = Driver.pytest
    prompt_context.input = []
    yield
    prompt_context.driver = previous_driver


def reset_test_prompt():
    prompt_context.input = []

def send_test_response(response: str):
    prompt_context.input.append(response)
