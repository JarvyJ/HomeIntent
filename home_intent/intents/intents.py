from functools import wraps
import logging
from typing import Callable, Dict, List

from .customization_mixin import IntentCustomizationMixin, SlotCustomization
from .util import _sanitize_slot, _check_if_args_in_sentence_slots, Sentence, IntentException

LOGGER = logging.getLogger(__name__)


class Intents(IntentCustomizationMixin):
    def __init__(self, name):
        self.name = name
        self.all_slots: Dict[str, Callable] = {}
        self.all_sentences: Dict[str, Sentence] = {}
        self.slot_modifications: Dict[str, SlotCustomization] = {}
        self.events = {"register_sentences": []}

    def dictionary_slots(self, func):
        LOGGER.debug(f"Registering {func.__name__}")

        @wraps(func)
        def wrapper(*arg, **kwargs):
            slot_dictionary = func(*arg, **kwargs)
            non_dictionary_additions = []
            if func.__name__ in self.slot_modifications:
                non_dictionary_additions = self._handle_dictionary_slot_modification(
                    func.__name__, slot_dictionary
                )

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
            synonym_values = []
            if func.__name__ in self.slot_modifications:
                synonym_values = self._handle_slot_modification(func.__name__, slot_values)

            slot_list = [f"{_sanitize_slot(x)}{{{func.__name__}}}" for x in slot_values]
            slot_list.extend(synonym_values)

            return slot_list

        self.all_slots[func.__name__] = wrapper
        return wrapper

    def sentences(self, sentences: List[str]):
        def inner(func):
            if not isinstance(sentences, list):
                raise IntentException(f"The sentences decorator expects a list for {func}")
            sentence_slots = _check_if_args_in_sentence_slots(sentences, func)
            self.all_sentences[func.__name__] = Sentence(sentences, func, sentence_slots)

            @wraps(func)
            def wrapper(*arg, **kwargs):
                LOGGER.info(f"Running function {func.__name__}")
                func(*arg, **kwargs)

            return wrapper

        return inner

    def beta(self, func):
        if func.__name__ not in self.all_sentences:
            raise IntentException("Put the beta decorator above the sentences decorator")
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

            if func.__name__ not in self.all_sentences:
                raise IntentException(
                    "Put the default_disable decorator above the sentences decorator"
                )

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

    def _handle_dictionary_slot_modification(self, func_name, slot_dictionary) -> List[str]:
        non_dictionary_additions = []
        reverse_slot_dictionary = {v: k for (k, v) in slot_dictionary.items()}

        if self.slot_modifications[func_name].remove:
            for slots_to_remove in self.slot_modifications[func_name].remove:
                if slots_to_remove in slot_dictionary:
                    del slot_dictionary[slots_to_remove]
                elif slots_to_remove in reverse_slot_dictionary:
                    del slot_dictionary[reverse_slot_dictionary[slots_to_remove]]
                else:
                    LOGGER.warning(f"'{slots_to_remove}' not in slot list for {func_name}")

        if self.slot_modifications[func_name].add:
            for slot_addition in self.slot_modifications[func_name].add:

                if isinstance(slot_addition, str):
                    if slot_addition in slot_dictionary:
                        del slot_dictionary[slot_addition]
                    non_dictionary_additions.append(
                        f"{_sanitize_slot(slot_addition)}{{{func_name}}}"
                    )

                elif isinstance(slot_addition, dict):
                    synonyms, value = next(iter(slot_addition.items()))
                    if synonyms in slot_dictionary:
                        del slot_dictionary[synonyms]
                    elif value in reverse_slot_dictionary:
                        del slot_dictionary[reverse_slot_dictionary[value]]
                    slot_dictionary[synonyms] = value

        return non_dictionary_additions

    def _handle_slot_modification(self, func_name, slot_values):
        synonmy_values = []

        if self.slot_modifications[func_name].remove:
            for slots_to_remove in self.slot_modifications[func_name].remove:
                if slots_to_remove in slot_values:
                    slot_values.remove(slots_to_remove)
                else:
                    LOGGER.warning(f"'{slots_to_remove}' not in slot list for {func_name}")

        if self.slot_modifications[func_name].add:
            for slot_addition in self.slot_modifications[func_name].add:

                if isinstance(slot_addition, str):
                    if slot_addition in slot_values:
                        slot_values.remove(slot_addition)
                    slot_values.add(slot_addition)

                elif isinstance(slot_addition, dict):
                    synonyms, value = next(iter(slot_addition.items()))
                    if synonyms in slot_values:
                        slot_values.remove(synonyms)
                    synonmy_values.append(f"{_sanitize_slot(synonyms)}{{{func_name}:{value}}}")

        return synonmy_values
