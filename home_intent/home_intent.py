from functools import partial
import json
import logging
import os
from pathlib import PosixPath
from typing import NamedTuple

import paho.mqtt.client as mqtt
import requests

from home_intent.audio_config import AudioConfig
from home_intent.intent_handler import IntentHandler
from home_intent.intents import Intents, Sentence
from home_intent.path_finder import get_file
from home_intent.rhasspy_api import RhasspyAPI, RhasspyError

LOGGER = logging.getLogger(__name__)


class HomeIntentException(Exception):
    pass


class RegisteredIntent(NamedTuple):
    class_instance: object
    intent: Intents


class StartupMessenger:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "accept": "application/json"}
        )

    def update(self, message):
        try:
            self.session.post(self.url, json={"data": message}, timeout=1)

        # just ignore any errors, if it doesnt post, that's okay. It's just missing a log in the frontend.
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ConnectionError:
            pass


class HomeIntent:
    def __init__(self, settings):
        self.registered_intents = []
        self.intent_function = {}
        self.settings = settings
        self.rhasspy_api = RhasspyAPI(settings.rhasspy.url)
        self.mqtt_client = mqtt.Client()
        self.arch = None
        self.startup_messenger = StartupMessenger("http://localhost:11102/api/v1/jobs/restart")
        self.intent_handler = IntentHandler(
            self.mqtt_client, self.settings, self.intent_function, self.startup_messenger
        )
        self.audio_config = AudioConfig(self.rhasspy_api, self.settings)
        self.all_slots = {}

        uname = os.uname()
        if uname.machine == "x86_64":
            self.arch = "x86_64"
        elif uname.machine.startswith("arm"):
            self.arch = "arm"
        elif uname.machine == "aarch64":
            self.arch = "arm"
        else:
            raise ValueError("HomeIntent only runs on x86_64 and armv7/aarch64 architectures")

        self.startup_messenger.update("Loading Components...")

    def get_config(self, settings_object):
        component_name = settings_object.__module__.split(".")[-1]
        raw_config = getattr(self.settings, component_name)

        # this will do the parsing/basic validation
        parsed_config = settings_object(**raw_config) if raw_config else settings_object()

        return parsed_config

    def register(self, class_instance, intents: Intents):
        LOGGER.info(f"Verifying sentences' slots for {intents.name}...")

        if intents.name.startswith("home_intent.components"):
            customization_filestem = "/".join(intents.name.split(".")[2:])
        else:
            customization_filestem = intents.name

        customization_file = PosixPath(f"/config/customizations/{customization_filestem}.yaml")
        if customization_file.is_file():
            intents.handle_customization(customization_file, class_instance)

        for sentence_name, sentence in intents.all_sentences.items():
            for slot in sentence.slots:
                if slot not in intents.all_slots:
                    raise HomeIntentException(
                        f"The method '{sentence.func}' has a slot ({slot}) that is not defined. "
                        f"Ensure there is a slot method with the name '{slot}' "
                        f"in the class {intents.name}"
                    )

            LOGGER.debug(sentence_name)
            LOGGER.debug(sentence)
            if self._enable_sentence(sentence):
                self.intent_function[f"{intents.name}.{sentence_name}"] = partial(
                    sentence.func, class_instance
                )

        LOGGER.info("Sentences look good!")
        # while I am using a partial here, I keep track of the instantiated class instance for the
        # register_sentences callback
        self.registered_intents.append(RegisteredIntent(class_instance, intents))

    def initialize(self):
        self._initialize_rhasspy()
        self._write_slots_to_rhasspy()
        self._write_sentences_to_rhasspy()
        self._train()
        self.intent_handler.setup_mqtt_and_loop()

    def _initialize_rhasspy(self):
        self.startup_messenger.update("Setting up Rhasspy...")
        if self.settings.rhasspy.externally_managed:
            LOGGER.info("Externally Managed Setting enabled - skipping rhasspy profile processing")
            return
        LOGGER.info("Checking profile")
        rhasspy_profile = self._load_rhasspy_profile_file()
        installed_profile = self.rhasspy_api.get("/api/profile?layers=profile")
        if rhasspy_profile != installed_profile:
            LOGGER.info("Installing profile")
            self.rhasspy_api.post("/api/profile", rhasspy_profile)

            LOGGER.info("Restarting Rhasspy...")
            self.rhasspy_api.post("/api/restart")
        else:
            LOGGER.info("Rhasspy profile matches Home Intent profile, moving on!")

        profile_meta = self.rhasspy_api.get("/api/profiles")
        if not profile_meta["downloaded"]:
            LOGGER.info("Downloading profile (can take 30s+ first time)...")
            self.rhasspy_api.post("/api/download-profile")
        else:
            LOGGER.info("Profile is up to date, nothing to download")

    def _load_rhasspy_profile_file(self):
        config_file_path = get_file("rhasspy_profile.json", arch_dependentant=True)
        rhasspy_config = json.loads(config_file_path.read_text())
        try:
            self.audio_config.add_sounds_microphone_device(rhasspy_config)
        except RhasspyError:
            LOGGER.info("Installing profile for first boot")
            self.rhasspy_api.post("/api/profile", rhasspy_config)

            LOGGER.info("Restarting Rhasspy...")
            self.rhasspy_api.post("/api/restart")
            self.audio_config.add_sounds_microphone_device(rhasspy_config)

        LOGGER.debug(json.dumps(rhasspy_config, indent=True))

        return rhasspy_config

    def _write_slots_to_rhasspy(self):
        self.startup_messenger.update("Updating slots in Rhasspy...")
        for registered_intent in self.registered_intents:
            LOGGER.info(f"Getting slots for {registered_intent.intent.name}")
            for slot in registered_intent.intent.all_slots:

                LOGGER.info(f"Getting slot values for {slot}")

                if slot in self.all_slots:
                    raise HomeIntentException(
                        f"The slot {slot} in {registered_intent.intent.name} is already"
                        "in Home Intent. Please rename the slot to avoid conflict."
                    )

                slot_values = registered_intent.intent.all_slots[slot](
                    registered_intent.class_instance
                )

                self.all_slots[slot] = slot_values

        LOGGER.info("Updating all slots in Rhasspy")
        self.rhasspy_api.post("/api/slots?overwriteAll=true", self.all_slots)

    def _write_sentences_to_rhasspy(self):
        self.startup_messenger.update("Updating sentences in Rhasspy...")
        # this will force clear out the defaults in sentences.ini
        sentences = []
        for registered_intent in self.registered_intents:
            LOGGER.info(f"Getting sentences for {registered_intent.intent.name}")

            # HACK: the slot values still get registered but Rhasspy wont try to learn them
            # if they aren't used in any sentences. I should have a more advanced state system,
            # but this should do for now.
            for register_func in registered_intent.intent.events["register_sentences"]:
                LOGGER.info(f"Running register func: {register_func}")
                register_func(registered_intent.class_instance)

            for (sentence_name, sentence,) in registered_intent.intent.all_sentences.items():
                if self._enable_sentence(sentence) and self._sentence_slots_have_value(sentence):
                    # the rhasspy API does '\n' for newlines
                    sentences_string = "\n".join(sentence.sentences)
                    sentences.append(
                        f"[{registered_intent.intent.name}.{sentence_name}]\n{sentences_string}"
                    )

        LOGGER.info("Updating all sentences in Rhasspy...")
        self.rhasspy_api.post("/api/sentences", {"intents/home_intent.ini": "\n".join(sentences)})

    def _sentence_slots_have_value(self, sentence: Sentence) -> bool:
        # NOTE: all([]) will also return True, so intents without slots will not break
        return all(len(self.all_slots[slot]) > 0 for slot in sentence.slots)

    def _train(self):
        self.startup_messenger.update("Training Rhasspy (can take some time)...")
        LOGGER.info("Training Rhasspy... (can take up to 1m if many devices)")
        try:
            self.rhasspy_api.post("/api/train", timeout=60)
        except requests.exceptions.Timeout:
            LOGGER.warning(
                "Timed out waiting for Rhasspy to train. Moving on, we will likely be okay."
            )

    def say(self, text):
        notification = {"text": text, "siteId": "default"}
        self.mqtt_client.publish("hermes/tts/say", json.dumps(notification))

    def play_audio_file(self, filename: str, site_id="default"):
        audio_file = get_file(filename)
        if audio_file.suffix != ".wav":
            raise HomeIntentException("play_audio_file currently only supports playing .wav files!")
        self.mqtt_client.publish(
            f"hermes/audioServer/{site_id}/playBytes/homeintent_audio",
            payload=audio_file.read_bytes(),
        )

    def _enable_sentence(self, sentence: Sentence):
        if self.settings.home_intent.enable_all:
            return True

        if self.settings.home_intent.enable_beta and sentence.beta:
            return True

        if sentence.disabled is False:
            return True

        return False
