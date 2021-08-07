from functools import partial
import json
import logging
from typing import NamedTuple

import paho.mqtt.client as mqtt

from intents import Intents, get_slots_from_sentences
from rhasspy_api import RhasspyAPI

LOGGER = logging.getLogger(__name__)


class HomeIntentException(Exception):
    pass


class RegisteredIntent(NamedTuple):
    class_instance: object
    intent: Intents


class HomeIntent:
    def __init__(self, settings):
        self.registered_intents = []
        self.intent_function = {}
        self.settings = settings
        self.rhasspy_api = RhasspyAPI(settings.rhasspy.url)

    def get_config(self, settings_object):
        component_name = settings_object.__module__.split(".")[-1]
        raw_config = getattr(self.settings, component_name)

        # this will do the parsing/basic validation
        parsed_config = settings_object(**raw_config) if raw_config else settings_object()

        return parsed_config

    def register(self, class_instance, intents: Intents):
        LOGGER.info(f"Verifying sentences' slots for {intents.name}...")
        for sentence in intents.all_sentences:
            sentence_slots = get_slots_from_sentences(intents.all_sentences[sentence].sentences)
            for slot in sentence_slots:
                if slot not in intents.all_slots:
                    raise HomeIntentException(
                        f"The sentence '{sentence}' has a slot ({slot}) that is not defined. "
                        f"Ensure there is a slot method with the name '{slot}' in the class {intents.name}"
                    )

            # TODO: this lambda setup no longer really requires keeping the class instance in RegisteredIntent.
            # I may get rid of it in the future.
            LOGGER.debug(sentence)
            LOGGER.debug(intents.all_sentences[sentence])
            self.intent_function[sentence] = partial(
                intents.all_sentences[sentence].func, class_instance
            )

        LOGGER.info("Sentences look good!")
        self.registered_intents.append(RegisteredIntent(class_instance, intents))

    def initialize(self):
        # self._initialize_rhasspy()
        self._write_slots_to_rhasspy()
        self._write_sentences_to_rhasspy()
        self._train()
        self._setup_mqtt_and_loop()

    def _initialize_rhasspy(self):
        LOGGER.info("Setting up profile")
        rhasspy_profile = json.load(open("rhasspy_profile.json", "r"))
        self.rhasspy_api.post("/api/profile", rhasspy_profile)

        LOGGER.info("Restarting Rhasspy...")
        self.rhasspy_api.post("/api/restart")

        LOGGER.info("Downloading profile (can take 30s+ first time)...")
        self.rhasspy_api.post("/api/download-profile")

    def _write_slots_to_rhasspy(self):
        all_slots = {}
        for registered_intent in self.registered_intents:
            LOGGER.info(f"Getting slots for {registered_intent.intent.name}")
            for slot in registered_intent.intent.all_slots:
                LOGGER.info(f"Getting slots for {slot}")
                slot_values = registered_intent.intent.all_slots[slot](
                    registered_intent.class_instance
                )
                all_slots[slot] = slot_values

        LOGGER.info("Updating all slots in Rhasspy")
        self.rhasspy_api.post("/api/slots?overwriteAll=true", all_slots)

    def _write_sentences_to_rhasspy(self):
        # this will force clear out the defaults in sentences.ini
        sentences = []
        for registered_intent in self.registered_intents:
            LOGGER.info(f"Getting sentences for {registered_intent.intent.name}")
            for (sentence_name, sentence,) in registered_intent.intent.all_sentences.items():
                # the rhasspy API does '\n' for newlines
                sentences_string = "\n".join(sentence.sentences)
                sentences.append(f"[{sentence_name}]\n{sentences_string}")

        LOGGER.info("Updating all sentences in Rhasspy...")
        self.rhasspy_api.post("/api/sentences", {"sentences.ini": "\n".join(sentences)})

    def _train(self):
        LOGGER.info("Training Rhasspy... (can take up to 1m if many devices)")
        self.rhasspy_api.post("/api/train")

    def _setup_mqtt_and_loop(self):
        # I had some old notes about how the mqtt_client can't be in a class.
        # It might've been a python 2.7 problem however.
        # Maybe I'll go back and play with it, but it's working for now
        mqtt_client = mqtt.Client()
        mqtt_client.message_callback_add("hermes/intent/#", self._handle_intent)
        mqtt_client.connect(self.settings.rhasspy.mqtt_host, 12183, 60)
        mqtt_client.subscribe("hermes/intent/#")
        LOGGER.info("Waiting to handle intents!")
        mqtt_client.loop_forever()

    def _handle_intent(self, client, userdata, message):
        payload = json.loads(message.payload)
        intent_name = payload["intent"]["intentName"]
        slots = {}
        for slot in payload["slots"]:
            slots[slot["slotName"]] = slot["value"]["value"]
        LOGGER.debug(intent_name)
        LOGGER.debug(slots)
        response = self.intent_function[intent_name](**slots)
        if response:
            self.say(client, response, session_id=payload["sessionId"])

    def say(self, client, text, session_id=None, custom_id="self", site_id=None):
        notification = {"text": text}
        if session_id:
            print("Using the session manager to close the session")
            notification["sessionId"] = session_id
            client.publish("hermes/dialogueManager/endSession", json.dumps(notification))
        else:
            notification["id"] = custom_id
            notification["siteId"] = site_id
            client.publish("hermes/tts/say", json.dumps(notification))
