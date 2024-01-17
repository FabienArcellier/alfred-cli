"""
The default click autocompletion ignores the character `:`
This module overrides it to offer autocompletion after this character.
"""
import os
import typing as t

from click.parser import split_arg_string
from click.shell_completion import CompletionItem, add_completion_class, BashComplete


class BashCompleteAlfred(BashComplete):
    """Alfred Shell completion for Bash."""
    exclude_separators = [":"]

    def complete(self) -> str:
        args, incomplete = _get_completion_args(self.exclude_separators)
        completions = self.get_completions(args, incomplete)

        out = [_format_bash_completion(self.exclude_separators, item, incomplete) for item in completions]
        return "\n".join(out)


add_completion_class(BashCompleteAlfred)


def _get_completion_args(exclude_separators: t.List[str]) -> t.Tuple[t.List[str], str]:
    comp_words = _comp_words(os.environ["COMP_WORDS"], exclude_separators)
    cwords = split_arg_string(comp_words)

    try:
        incomplete = cwords[-1]
    except IndexError:
        incomplete = ""

    return cwords, incomplete


def _comp_words(param: str, exclude_separators: t.List[str]):
    words = param.split('\n')
    result = []
    previous_word = None
    for word in words:
        current_word = word
        if current_word in exclude_separators:
            result[-1] += word
        elif previous_word in exclude_separators:
            result[-1] += word
        else:
            result.append(word)

        previous_word = word

    return "\n".join(result)


def _format_bash_completion(exclude_separators: t.List[str], item: CompletionItem, incomplete: str) -> str:
    complete = item.value
    for separator in exclude_separators:
        filled_separator = incomplete.count(separator)
        if separator in incomplete:
            complete = separator.join(complete.split(separator)[filled_separator:])
            break

    return f"{item.type},{complete}"
