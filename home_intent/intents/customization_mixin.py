from functools import partial
import logging
from pathlib import PosixPath
from typing import Callable, Dict, List, Optional, Union

from pydantic import BaseModel, Extra
import yaml

from .util import IntentException, Sentence, _get_slots_from_sentences

LOGGER = logging.getLogger(__name__)


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


class IntentCustomizationMixin:
    def handle_customization(self, customization_file: PosixPath, class_instance):
        LOGGER.info(f"Loading customization file {customization_file}")
        customization_yaml = yaml.load(
            customization_file.read_text("utf-8"), Loader=yaml.SafeLoader
        )
        component_customization = Customization(**customization_yaml)
        if component_customization.enable_all is not None:
            if component_customization.enable_all is True:
                self._enable_all()
            elif component_customization.enable_all is False:
                self._disable_all()

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

    def _enable_all(self):
        for _, sentence in self.all_sentences.items():
            sentence.disabled = False

    def _disable_all(self):
        for _, sentence in self.all_sentences.items():
            sentence.disabled = True

    def _customize_intents(self, intent: str, customization: SentenceCustomization, class_instance):
        if customization.enable is not None:
            if customization.enable is True:
                self._enable_intent(intent)
            elif customization.enable is False:
                self._disable_intent(intent)

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
                sentence_slots = _get_slots_from_sentences(sentences)
                self.all_sentences[funcname] = Sentence(sentences, alias_function, sentence_slots)

    def _enable_intent(self, sentence_func: Union[Callable, str]):
        if isinstance(sentence_func, str):
            self.all_sentences[sentence_func].disabled = False
        else:
            self.all_sentences[sentence_func.__name__].disabled = False

    def _disable_intent(self, sentence_func: Union[Callable, str]):
        if isinstance(sentence_func, str):
            self.all_sentences[sentence_func].disabled = True
        else:
            self.all_sentences[sentence_func.__name__].disabled = True
