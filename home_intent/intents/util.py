from dataclasses import dataclass
import re
import inspect
from typing import List, Callable

# we'll likely have to get more sophisticated than regexes eventually
SLOT_REGEX = re.compile(r"\(\$([a-z_]*)")
TAG_REGEX = re.compile(r"""{([a-z_]*)}""")


class IntentException(Exception):
    pass


@dataclass
class Sentence:
    sentences: List[str]
    func: Callable
    slots: List[str]
    disabled: bool = False
    disabled_reason: str = ""
    beta: bool = False


def _sanitize_slot(slot_name: str):
    # okay, maybe a regex would be better at this point...
    return "".join(
        x if x.isalnum() or x in ("(", ")", "|", "[", "]", ".", ":") else " " for x in slot_name
    )


def _get_slots_from_sentences(sentences: List[str]):
    sentence_slots = set()
    for sentence in sentences:
        sentence_slots.update((SLOT_REGEX.findall(sentence)))

    return sentence_slots


def _get_tags_from_sentences(sentences: List[str]):
    sentence_tags = set()
    for sentence in sentences:
        sentence_tags.update(TAG_REGEX.findall(sentence))

    return sentence_tags


def _check_if_args_in_sentence_slots(sentences, func):
    sentence_slots = _get_slots_from_sentences(sentences)
    sentence_tags = _get_tags_from_sentences(sentences)

    argument_spec = inspect.getfullargspec(func)

    # first arg is 'self', the last args are optionals with defaults set
    required_args = (
        argument_spec.args[1 : -len(argument_spec.defaults)]
        if argument_spec.defaults
        else argument_spec.args[1:]
    )

    # check if arg in sentence slot
    for arg in required_args:
        valid_argument = arg in sentence_slots or arg in sentence_tags
        if not valid_argument:
            if arg not in sentence_slots:
                raise IntentException(
                    f"The argument '{arg}' is not associated in the sentence for {func}. "
                    f"Make sure the sentence decorator includes a (${arg}) or "
                    "remove it as an argument."
                )

            if arg not in sentence_tags:
                raise IntentException(
                    f"The argument '{arg}' is not associated in the sentence for {func}. "
                    f"Make sure the sentence decorator includes a {{{arg}}} or "
                    "remove it as an argument."
                )

    return sentence_slots
