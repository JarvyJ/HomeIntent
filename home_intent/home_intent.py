from functools import partial
import json
import logging
import os
from typing import NamedTuple

import paho.mqtt.client as mqtt

from intents import Intents, get_slots_from_sentences
from rhasspy_api import RhasspyAPI, RhasspyError
from requests.exceptions import Timeout

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
        self.mqtt_client = mqtt.Client()
        self.arch = None
        uname = os.uname()
        if uname.machine == "x86_64":
            self.arch = "x86_64"
        elif uname.machine.startswith("arm"):
            self.arch = "arm"
        elif uname.machine == "aarch64":
            self.arch = "arm"
        else:
            raise ValueError("HomeIntent only runs on x86_64 and armv7/aarch64 architectures")

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
            self.intent_function[f"{intents.name}.{sentence}"] = partial(
                intents.all_sentences[sentence].func, class_instance
            )

        LOGGER.info("Sentences look good!")
        self.registered_intents.append(RegisteredIntent(class_instance, intents))

    def initialize(self):
        self._initialize_rhasspy()
        self._write_slots_to_rhasspy()
        self._write_sentences_to_rhasspy()
        self._train()
        self._setup_mqtt_and_loop()

    def _initialize_rhasspy(self):
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
        config_file_path = f"home_intent/default_configs/{self.arch}/rhasspy_profile.json"
        LOGGER.info(config_file_path)
        print(os.path.isfile(config_file_path))
        if os.path.isfile("/config/rhasspy_profile.json"):
            LOGGER.info("Loading custom rhasspy profile!")
            config_file_path = "/config/rhasspy_profile.json"
        else:
            LOGGER.info(f"Loading default {self.arch} rhasspy profile")
        rhasspy_config = json.load(open(config_file_path, "r"))
        try:
            microphone_sounds_config = self._add_sounds_microphone_device()
        except RhasspyError:
            LOGGER.info("Installing profile for first boot")
            self.rhasspy_api.post("/api/profile", rhasspy_config)

            LOGGER.info("Restarting Rhasspy...")
            self.rhasspy_api.post("/api/restart")
            microphone_sounds_config = self._add_sounds_microphone_device()

        rhasspy_config.update(microphone_sounds_config)
        return rhasspy_config

    def _add_sounds_microphone_device(self):
        microphone_devices = self.rhasspy_api.get("/api/microphones")
        sounds_devices = self.rhasspy_api.get("/api/speakers")

        microphone_sounds_config = {}
        config_microphone_device = self.settings.rhasspy.microphone_device
        config_sounds_device = self.settings.rhasspy.sounds_device

        # Figure we should always show this so people can switch without unsetting first.
        LOGGER.info(
            "\nThese are the attached microphones (I think the default has an asterisk):\n"
            f"{json.dumps(microphone_devices, indent=True)}\n"
            "\nTo configure a microphone, set 'microphone_device' to the corresponding number "
            "above in the 'rhasspy' section in '/config/config.yaml'\n"
        )

        # Same reason for displaying as above.
        LOGGER.info(
            "These are the attached sounds devices:\n"
            f"{json.dumps(sounds_devices, indent=True)}\n"
            "\nTo configure a sounds device, set 'sounds_device' to the corresponding "
            "key (ex: default:CARD=Headphones) above in the 'rhasspy' section "
            "in '/config/config.yaml'. You probably want one of the 'default' devices. "
            "The plughw ones can have a fun chipmunk effect!\n"
        )

        if not config_microphone_device:
            LOGGER.info("Microphone not set, using default microphone\n")
        else:
            LOGGER.info(f"Using {config_microphone_device} for pyaudio device")
            if config_microphone_device not in microphone_devices:
                raise HomeIntentException(
                    f"Microphone device {config_microphone_device} not found in microphone devices list above."
                )
            microphone_sounds_config["microphone"] = {
                "pyaudio": {"device": config_microphone_device}
            }

        if not config_sounds_device:
            LOGGER.warning("Sounds device not set, using sysdefault sound device\n")
        else:
            LOGGER.info(f"Using {config_sounds_device} for aplay device")
            if config_sounds_device not in sounds_devices:
                raise HomeIntentException(
                    f"Sounds device {config_sounds_device} not found in sounds devices list above."
                )
            microphone_sounds_config["sounds"] = {"aplay": {"device": config_sounds_device}}

        return microphone_sounds_config

    def _write_slots_to_rhasspy(self):
        all_slots = {}
        for registered_intent in self.registered_intents:
            LOGGER.info(f"Getting slots for {registered_intent.intent.name}")
            for slot in registered_intent.intent.all_slots:

                LOGGER.info(f"Getting slot values for {slot}")

                if slot in all_slots:
                    raise HomeIntentException(
                        f"The slot {slot} in {registered_intent.intent.name} is already"
                        "in Home Intent. Please rename the slot to avoid conflict."
                    )

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
                sentences.append(
                    f"[{registered_intent.intent.name}.{sentence_name}]\n{sentences_string}"
                )

        LOGGER.info("Updating all sentences in Rhasspy...")
        self.rhasspy_api.post("/api/sentences", {"sentences.ini": "\n".join(sentences)})

    def _train(self):
        LOGGER.info("Training Rhasspy... (can take up to 1m if many devices)")
        try:
            self.rhasspy_api.post("/api/train", timeout=60)
        except Timeout as timeout_exception:
            LOGGER.warning(
                "Timed out waiting for Rhasspy to train. Moving on, we will likely be okay."
            )

    def _setup_mqtt_and_loop(self):
        self.mqtt_client.message_callback_add("hermes/intent/#", self._handle_intent)
        if self.settings.rhasspy.mqtt_username and self.settings.rhasspy.mqtt_password:
            self.mqtt_client.username_pw_set(
                username=self.settings.rhasspy.mqtt_username,
                password=self.settings.rhasspy.mqtt_password,
            )
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.connect(
            self.settings.rhasspy.mqtt_host, self.settings.rhasspy.mqtt_port, 60
        )
        LOGGER.info("Waiting to handle intents!")
        self.mqtt_client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        LOGGER.info("Connected to MQTT. This happens when the Rhasspy MQTT starts (or restarts)")
        if rc == 0:
            LOGGER.info("Subscribed to intent messages: hermes/intent/#")
            client.subscribe("hermes/intent/#")
        else:
            LOGGER.error(f"Failed to connect to MQTT. Return Code: {rc}")

    def _handle_intent(self, client, userdata, message):
        payload = json.loads(message.payload)
        intent_name = payload["intent"]["intentName"]
        slots = {}
        for slot in payload["slots"]:
            slots[slot["slotName"]] = slot["value"]["value"]
        LOGGER.info(f"Handling intent: {intent_name}")
        LOGGER.debug(slots)
        try:
            response = self.intent_function[intent_name](**slots)
        except Exception as exception:
            LOGGER.exception(exception)
        else:
            if response:
                self._say(client, response, session_id=payload["sessionId"])

    def _say(self, client, text, session_id):
        notification = {"text": text, "siteId": "default"}
        if session_id:
            print("Using the session manager to close the session")
            notification["sessionId"] = session_id
            client.publish("hermes/dialogueManager/endSession", json.dumps(notification))

    def say(self, text):
        notification = {"text": text, "siteId": "default"}
        self.mqtt_client.publish("hermes/tts/say", json.dumps(notification))
