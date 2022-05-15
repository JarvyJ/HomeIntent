from functools import partial
import json
import logging
import os
from pathlib import PosixPath
from typing import NamedTuple, Dict
from importlib import import_module

import paho.mqtt.client as mqtt
import requests

from home_intent.audio_config import AudioConfig
from home_intent.intent_handler import IntentHandler
from home_intent.intents import Intents, Sentence
from home_intent.rhasspy_api import RhasspyAPI, RhasspyError
from home_intent.updater import update_homeintent

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
        self.intent_function: Dict[str, Sentence] = {}
        self.settings = settings
        self.language = settings.home_intent.language
        self.rhasspy_api = RhasspyAPI(settings.rhasspy.url)
        self.mqtt_client = mqtt.Client()
        self.arch = None
        self.startup_messenger = StartupMessenger("http://localhost:11102/api/v1/jobs/restart")
        self.intent_handler = IntentHandler(
            self.mqtt_client, self.settings, self.intent_function, self.startup_messenger
        )
        self.audio_config = AudioConfig(self.rhasspy_api, self.settings, self.get_file)
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
            # remove the home_intent.components from the beginning
            customization_filestem = "/".join(class_instance.__module__.split(".")[2:])
        else:
            customization_filestem = intents.name

        # Minor hack to support English fallback
        if customization_filestem.endswith((f"/{self.settings.home_intent.language}", "/en")):
            # we need to remove the base_{component}.{language} from the end
            customization_filestem = "/".join(customization_filestem.split("/")[:-1])

        module_name = customization_filestem.split("/")[-1]

        customization_file = PosixPath(f"/config/customizations/{customization_filestem}.yaml")
        if customization_file.is_file():
            intents.handle_customization(customization_file, class_instance)

        for slot in intents.all_slots:
            if not (slot == module_name or slot.startswith(f"{module_name}_")):
                raise HomeIntentException(
                    f"The slot '{slot}' should start with the module name ({module_name}) "
                    f"in the class {class_instance.__module__}"
                )

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
                # I may regret just updating func later...we shall see.
                sentence.func = partial(sentence.func, class_instance)
                self.intent_function[f"{intents.name}.{sentence_name}"] = sentence

        LOGGER.info("Sentences look good!")
        # while I am using a partial here, I keep track of the instantiated class instance for the
        # register_sentences callback
        self.registered_intents.append(RegisteredIntent(class_instance, intents))

    def import_module(self, module_name):
        try:
            module = import_module(f"{module_name}.{self.settings.home_intent.language}")
        except ModuleNotFoundError:
            module = import_module(f"{module_name}.en")
        return module

    def say(self, text: str, satellite_id: str):
        notification = {"text": text, "siteId": satellite_id}
        self.mqtt_client.publish("hermes/tts/say", json.dumps(notification))

    def play_audio_file(self, filename: str, satellite_id: str, language_dependent: bool = False):
        audio_file = self.get_file(filename, language_dependent=language_dependent)
        if audio_file.suffix != ".wav":
            raise HomeIntentException("play_audio_file currently only supports playing .wav files!")
        self.mqtt_client.publish(
            f"hermes/audioServer/{satellite_id}/playBytes/homeintent_audio",
            payload=audio_file.read_bytes(),
        )

    def get_file(self, filename: str, arch_dependent=False, language_dependent=True) -> PosixPath:
        config_file_path = PosixPath(f"/config/{filename}")
        if config_file_path.is_file():
            LOGGER.info(f"Found file overrided in config: {config_file_path}")
            return config_file_path

        if language_dependent:
            composed_filename = f"{self.language}/{filename}"
        else:
            composed_filename = filename

        # relative from where this file is located. Man, paths are weird, but pathlib is great!
        relative_from = __file__

        if arch_dependent:
            source_file_path = (
                PosixPath(relative_from).parent / f"default_configs/{self.arch}/{composed_filename}"
            )
        else:
            source_file_path = (
                PosixPath(relative_from).parent / f"default_configs/{composed_filename}"
            )

        if source_file_path.is_file():
            return source_file_path
        else:
            if language_dependent:
                return self.get_file(
                    f"en/{filename}", arch_dependent=arch_dependent, language_dependent=False
                )

        raise HomeIntentException(f"Can't find path to file {filename}")

    def initialize(self):
        update_homeintent(self)
        self._initialize_rhasspy()
        self._setup_satellites()
        self._write_slots_to_rhasspy()
        self._write_sentences_to_rhasspy()
        self._train()
        self.intent_handler.setup_mqtt_and_loop()

    def _initialize_rhasspy(self):
        self.startup_messenger.update("Setting up Rhasspy...")
        if self.settings.rhasspy.externally_managed:
            LOGGER.info("Externally Managed Setting enabled - skipping Rhasspy profile processing")
            return
        log_section("Setting up the base Rhasspy instance")
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

    def _setup_satellites(self):
        if not self.settings.rhasspy.managed_satellites:
            return

        LOGGER.info("Setting up managed satellites")

        # TODO: this may need to be executed via the API, so we'll see how that influences things
        for satellite_id, satellite_info in self.settings.rhasspy.managed_satellites.items():
            log_section(f"Setting up satellite config for {satellite_id}")
            try:
                satellite_api = RhasspyAPI(satellite_info.url, retry=False)
            except RhasspyError:
                LOGGER.warning(f"Couldn't connect to Rhasspy Satellite at {satellite_info.url}")
                continue

            config_file_path = self.get_file("satellite_profile.json", language_dependent=False)
            satellite_config = json.loads(config_file_path.read_text(encoding="utf-8"))

            self.audio_config.add_audio_settings_to_satellite(
                satellite_api, satellite_config, satellite_id, satellite_info
            )

            installed_profile = satellite_api.get("/api/profile?layers=profile")
            if satellite_config != installed_profile:
                LOGGER.info("Installing profile")
                satellite_api.post("/api/profile", satellite_config)

                LOGGER.info("Restarting Satellite...")
                satellite_api.post("/api/restart")
            else:
                LOGGER.info("Satellite profile matches Home Intent profile, moving on!")

            profile_meta = satellite_api.get("/api/profiles")
            if not profile_meta["downloaded"]:
                LOGGER.info("Downloading profile (can take 30s+ first time)...")
                satellite_api.post("/api/download-profile")
            else:
                LOGGER.info("Profile is up to date, nothing to download")

            LOGGER.info(f"Satellite config complete for {satellite_id}\n\n\n")

    def _load_rhasspy_profile_file(self):
        config_file_path = self.get_file(
            "rhasspy_profile.json", arch_dependent=True, language_dependent=False
        )
        rhasspy_config = json.loads(config_file_path.read_text(encoding="utf-8"))
        try:
            self.audio_config.add_audio_settings_to_config(rhasspy_config)
        except RhasspyError:
            LOGGER.info("Installing profile for first boot")
            self.rhasspy_api.post("/api/profile", rhasspy_config)

            LOGGER.info("Restarting Rhasspy...")
            self.rhasspy_api.post("/api/restart")
            self.audio_config.add_audio_settings_to_config(rhasspy_config)

        LOGGER.debug(json.dumps(rhasspy_config, indent=True))

        return rhasspy_config

    def _write_slots_to_rhasspy(self):
        self.startup_messenger.update("Updating slots in Rhasspy...")
        log_section("Updating slots in Rhasspy")
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
        log_section("Updating sentences to Rhasspy")
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

            for (
                sentence_name,
                sentence,
            ) in registered_intent.intent.all_sentences.items():
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
        except RhasspyError as rhasspy_error:
            if "TrainingFailedException" in str(rhasspy_error):
                # TODO: properly identify if this is the first boot.
                LOGGER.warning(
                    "Rhasspy training failed. This can happen on first boot due to no sentences being registered."
                )
            else:
                raise

    def _enable_sentence(self, sentence: Sentence):
        if self.settings.home_intent.enable_all:
            return True

        if self.settings.home_intent.enable_beta and sentence.beta:
            return True

        if sentence.disabled is False:
            return True

        return False


def log_section(title):
    LOGGER.info(f"\n\n\n{'='*100}\n{title}\n{'='*100}\n\n")
