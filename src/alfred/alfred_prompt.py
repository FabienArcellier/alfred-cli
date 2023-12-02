import contextlib
import dataclasses
import threading
from sys import stdin
from typing import Optional, List, Callable

import click
import prompt_toolkit
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
from prompt_toolkit.validation import Document, Validator, ValidationError

class Driver:
    prompt_toolkit='prompt_toolkit'
    pytest= 'pytest'

@dataclasses.dataclass
class Context:
    driver: str = Driver.prompt_toolkit
    input: List[str] = dataclasses.field(default_factory=list)

module_var = threading.local()
module_var.ctx = Context()
module_context = module_var.ctx

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

    if default is not None:
        label = label + f"[{default}] "

    if module_context.driver == Driver.pytest:
        _input = _emulate_prompt_on_test(default, validation_func)
    elif stdin.isatty():
        _input = prompt_toolkit.prompt(label, completer=AlfredFuzzyCompleter(proposals), validator=FuncValidator(default, validation_func))
    else:
        _input = _emulate_prompt_on_non_tty(label, default, validation_func)

    if _input.strip() == "":
        return default

    return _input.strip()


def AlfredFuzzyCompleter(proposals):  # pylint: disable=invalid-name
    """
    Create a fuzzy completer with proposals and support for special characters as / and : and \

    >>> completer = AlfredFuzzyCompleter(proposals=["/home/user", "/home/user/alfred"])

    :param proposals:
    :return:
    """
    return FuzzyCompleter(WordCompleter(words=proposals), pattern=r"^[a-zA-Z0-9_/]+")


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

        if self.default is not None and (document.text in ["", self.default]):
            error = self.validation_func(self.default)
            if error is not None:
                raise ValidationError(message=error, cursor_position=len(document.text))
        else:
            error = self.validation_func(document.text)
            if error is not None:
                raise ValidationError(message=error, cursor_position=len(document.text))


def _check_confirm(proposition: str) -> Optional[str]:
    if proposition not in ["y", "n"]:
        return "Please enter 'y' or 'n'"

    return None


def _emulate_prompt_on_test(default, validation_func):
    _input = module_context.input.pop(0)
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
        else:
            is_valid = True

    return _input

### The following method are dedicated to testing ###

@contextlib.contextmanager
def use_test_prompt():
    previous_driver = module_context.driver
    module_context.driver = Driver.pytest
    module_context.input = []
    yield
    module_context.driver = previous_driver


def reset_test_prompt():
    module_context.input = []

def send_test_response(response: str):
    module_context.input.append(response)
