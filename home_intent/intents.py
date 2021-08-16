from functools import wraps
import inspect
import logging
import re
from typing import Callable, List, NamedTuple, Union

LOGGER = logging.getLogger(__name__)
# we'll likely have to get more sophisticated than regexes eventually
SLOT_REGEX = re.compile(r"\(\$([a-z_]*)\)")
TAG_REGEX = re.compile(r"""{([a-z_]*)}""")


class IntentException(Exception):
    pass


class Sentence(NamedTuple):
    sentences: List[str]
    func: Callable


class Intents:
    def __init__(self, name):
        self.name = name
        self.all_slots = {}
        self.all_sentences = {}
        self.events = {"register_sentences": []}

    def dictionary_slots(self, func):
        LOGGER.debug(f"Registering {func.__name__}")

        @wraps(func)
        def wrapper(*arg, **kwargs):
            slot_dictionary = func(*arg, **kwargs)
            return [f"{x}{{{func.__name__}:{slot_dictionary[x]}}}" for x in slot_dictionary]

        self.all_slots[func.__name__] = wrapper
        return wrapper

    def slots(self, func):
        LOGGER.debug(f"Registering {func.__name__}")

        @wraps(func)
        def wrapper(*arg, **kwargs):
            return [f"{x}{{{func.__name__}}}" for x in func(*arg, **kwargs)]

        self.all_slots[func.__name__] = wrapper
        return wrapper

    def sentences(self, sentences):
        def inner(func):
            check_if_args_in_sentence_slots(sentences, func)
            self.all_sentences[func.__name__] = Sentence(sentences, func)

            @wraps(func)
            def wrapper(*arg, **kwargs):
                LOGGER.info(f"Running function {func.__name__}")
                func(*arg, **kwargs)

            return wrapper

        return inner

    def on_event(self, event):
        if event != "register_sentences":
            raise IntentException(
                "Currently you can only register events during 'register_sentences'"
            )

        def inner(func):
            @wraps(func)
            def wrapper(*arg, **kwargs):
                return func(*arg, **kwargs)

            self.events[event].append(func)
            return wrapper

        return inner

    def disable_intent(self, sentence_func: Union[Callable, str]):
        if isinstance(sentence_func, str):
            del self.all_sentences[sentence_func]
        else:
            del self.all_sentences[sentence_func.__name__]

    def disable_all(self):
        self.all_sentences = {}


def get_slots_from_sentences(sentences: List[str]):
    sentence_slots = set()
    for sentence in sentences:
        sentence_slots.update((SLOT_REGEX.findall(sentence)))

    return sentence_slots


def get_tags_from_sentences(sentences: List[str]):
    sentence_tags = set()
    for sentence in sentences:
        sentence_tags.update(TAG_REGEX.findall(sentence))

    return sentence_tags


def check_if_args_in_sentence_slots(sentences, func):
    sentence_slots = get_slots_from_sentences(sentences)
    sentence_tags = get_tags_from_sentences(sentences)

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
