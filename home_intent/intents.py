from dataclasses import dataclass
from functools import wraps, partial, partialmethod
import inspect
import logging
from pathlib import PosixPath
import re
from typing import Callable, Dict, List, Optional, Union

from pydantic import BaseModel, Extra
import yaml

LOGGER = logging.getLogger(__name__)
# we'll likely have to get more sophisticated than regexes eventually
SLOT_REGEX = re.compile(r"\(\$([a-z_]*)\)")
TAG_REGEX = re.compile(r"""{([a-z_]*)}""")


class IntentException(Exception):
    pass


class SlotCustomization(BaseModel, extra=Extra.forbid):
    add: Optional[List[Union[str, Dict[str, str]]]]
    remove: Optional[List[str]]


class SentenceModification(BaseModel, extra=Extra.forbid):
    add: Optional[List[str]]
    remove: Optional[List[str]]


class SentenceAlias(BaseModel, extra=Extra.forbid):
    sentences: List[str]
    slots: Optional[Dict[str, str]]


class SentenceCustomization(BaseModel, extra=Extra.forbid):
    sentences: Optional[SentenceModification]
    alias: Optional[List[SentenceAlias]]
    enable: Optional[bool] = None


class Customization(BaseModel, extra=Extra.forbid):
    slots: Optional[Dict[str, SlotCustomization]]
    intents: Optional[Dict[str, SentenceCustomization]]
    enable_all: Optional[bool] = None


@dataclass
class Sentence:
    sentences: List[str]
    func: Callable
    disabled: bool = False
    disabled_reason: str = None
    beta: bool = False


class Intents:
    def __init__(self, name):
        self.name = name
        self.all_slots = {}
        self.all_sentences = {}
        self.slot_modifications = {}
        self.events = {"register_sentences": []}

    def dictionary_slots(self, func):
        LOGGER.debug(f"Registering {func.__name__}")

        @wraps(func)
        def wrapper(*arg, **kwargs):
            slot_dictionary = func(*arg, **kwargs)
            non_dictionary_additions = []
            if func.__name__ in self.slot_modifications:
                if self.slot_modifications[func.__name__].remove:
                    for slots_to_remove in self.slot_modifications[func.__name__].remove:
                        if slots_to_remove in slot_dictionary:
                            del slot_dictionary[slots_to_remove]
                        else:
                            LOGGER.warning(
                                f"'{slots_to_remove}' not in slot list for {func.__name__}"
                            )

                if self.slot_modifications[func.__name__].add:
                    for slot_addition in self.slot_modifications[func.__name__].add:

                        if isinstance(slot_addition, str):
                            if slot_addition in slot_dictionary:
                                del slot_dictionary[slot_addition]
                            non_dictionary_additions.append(
                                f"{_sanitize_slot(slot_addition)}{{{func.__name__}}}"
                            )

                        elif isinstance(slot_addition, dict):
                            synonyms, value = next(iter(slot_addition.items()))
                            if synonyms in slot_dictionary:
                                del slot_dictionary[synonyms]
                            slot_dictionary[synonyms] = value

            slot_list = [
                f"{_sanitize_slot(x)}{{{func.__name__}:{slot_dictionary[x]}}}"
                for x in slot_dictionary
            ]
            slot_list.extend(non_dictionary_additions)
            return slot_list

        self.all_slots[func.__name__] = wrapper
        return wrapper

    def slots(self, func):
        LOGGER.debug(f"Registering {func.__name__}")

        @wraps(func)
        def wrapper(*arg, **kwargs):
            slot_values = set(func(*arg, **kwargs))
            synonmym_values = []
            if func.__name__ in self.slot_modifications:
                if self.slot_modifications[func.__name__].remove:
                    for slots_to_remove in self.slot_modifications[func.__name__].remove:
                        if slots_to_remove in slot_values:
                            slot_values.remove(slots_to_remove)
                        else:
                            LOGGER.warning(
                                f"'{slots_to_remove}' not in slot list for {func.__name__}"
                            )

                if self.slot_modifications[func.__name__].add:
                    for slot_addition in self.slot_modifications[func.__name__].add:

                        if isinstance(slot_addition, str):
                            if slot_addition in slot_values:
                                slot_values.remove(slot_addition)
                            slot_values.add(slot_addition)

                        elif isinstance(slot_addition, dict):
                            synonyms, value = next(iter(slot_addition.items()))
                            if synonyms in slot_values:
                                slot_values.remove(synonyms)
                            synonmym_values.append(
                                f"{_sanitize_slot(synonyms)}{{{func.__name__}:{value}}}"
                            )

            slot_list = [f"{_sanitize_slot(x)}{{{func.__name__}}}" for x in slot_values]
            slot_list.extend(synonmym_values)

            return slot_list

        self.all_slots[func.__name__] = wrapper
        return wrapper

    def sentences(self, sentences):
        def inner(func):
            _check_if_args_in_sentence_slots(sentences, func)
            self.all_sentences[func.__name__] = Sentence(sentences, func)

            @wraps(func)
            def wrapper(*arg, **kwargs):
                LOGGER.info(f"Running function {func.__name__}")
                func(*arg, **kwargs)

            return wrapper

        return inner

    def beta(self, func):
        self.all_sentences[func.__name__].disabled = True
        self.all_sentences[func.__name__].beta = True
        self.all_sentences[func.__name__].disabled_reason = "BETA"

        def inner(func):
            @wraps(func)
            def wrapper(*arg, **kwargs):
                return func(*arg, **kwargs)

            return wrapper

        return inner

    def default_disable(self, reason: str):
        def inner(func):
            @wraps(func)
            def wrapper(*arg, **kwargs):
                return func(*arg, **kwargs)

            self.all_sentences[func.__name__].disabled_reason = reason
            self.all_sentences[func.__name__].disabled = True
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
            self.all_sentences[sentence_func].disabled = True
        else:
            self.all_sentences[sentence_func.__name__].disabled = True

    def enable_intent(self, sentence_func: Union[Callable, str]):
        if isinstance(sentence_func, str):
            self.all_sentences[sentence_func].disabled = False
        else:
            self.all_sentences[sentence_func.__name__].disabled = False

    def disable_all(self):
        self.all_sentences = {}

    def enable_all(self):
        for _, sentence in self.all_sentences:
            sentence.disabled = False

    def handle_customization(self, customization_file: PosixPath, class_instance):
        LOGGER.info(f"Loading customization file {customization_file}")
        customization_yaml = yaml.load(
            customization_file.read_text("utf-8"), Loader=yaml.SafeLoader
        )
        component_customization = Customization(**customization_yaml)
        if component_customization.enable_all is not None:
            if component_customization.enable_all is True:
                self.enable_all()
            elif component_customization.enable_all is False:
                self.disable_all()

        if component_customization.intents:
            for intent, customization in component_customization.intents.items():
                if intent in self.all_sentences:
                    self._customize_intents(intent, customization, class_instance)
                else:
                    raise IntentException(
                        f"'{intent}'' not in intent sentences: {self.all_sentences.keys()}"
                    )

        if component_customization.slots:
            for slot, customization in component_customization.slots.items():
                if slot in self.all_slots:
                    self.slot_modifications[slot] = customization
                else:
                    raise IntentException(f"'{slot}' not associated with {self.name}")

    def _customize_intents(self, intent: str, customization: SentenceCustomization, class_instance):
        if customization.enable is not None:
            if customization.enable is True:
                self.enable_intent(intent)
            elif customization.enable is False:
                self.disable_intent(intent)

        if customization.sentences:
            if customization.sentences.add:
                self.all_sentences[intent].sentences.extend(customization.sentences.add)

            if customization.sentences.remove:
                for sentence_to_remove in customization.sentences.remove:
                    if sentence_to_remove in self.all_sentences[intent].sentences:
                        self.all_sentences[intent].sentences.remove(sentence_to_remove)
                    else:
                        LOGGER.warning(f"'{sentence_to_remove}' not in {intent} ")

        if customization.alias:
            for count, alias in enumerate(customization.alias):
                sentences = alias.sentences
                funcname = f"{intent}.alias_function.{count}"

                # alright, this is some insanity. We get the alias' intent func dynamically
                # and then populate its arguments, then re-inject it into the class with a new name
                if alias.slots:
                    alias_function = partial(
                        getattr(class_instance, intent).__func__, **alias.slots
                    )
                else:
                    alias_function = getattr(class_instance, intent).__func__
                setattr(class_instance, funcname, alias_function)
                self.all_sentences[funcname] = Sentence(sentences, alias_function)


def _sanitize_slot(slot_name: str):
    return "".join(x if x.isalnum() else " " for x in slot_name)


def get_slots_from_sentences(sentences: List[str]):
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
    sentence_slots = get_slots_from_sentences(sentences)
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
