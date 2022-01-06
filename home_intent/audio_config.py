import json
import logging
from typing import Set

LOGGER = logging.getLogger(__name__)

ISO639_1_TO_IETF_BCP_47 = {
    "en": "en-GB",
    "de": "de-DE",
    "es": "es-ES",
    "fr": "fr-FR",
    "it": "it-IT",
}


class AudioConfigException(Exception):
    pass


class AudioConfig:
    def __init__(self, rhasspy_api, settings, get_file):
        self.rhasspy_api = rhasspy_api
        self.settings = settings
        self.get_file = get_file

    def add_audio_settings_to_config(self, rhasspy_config):
        microphone_devices = self.rhasspy_api.get("/api/microphones")
        sounds_devices = self.rhasspy_api.get("/api/speakers")

        config_microphone_device = self.settings.rhasspy.microphone_device
        config_sounds_device = self.settings.rhasspy.sounds_device

        _log_out_audio_config(microphone_devices, sounds_devices)
        _setup_microphone_device(config_microphone_device, microphone_devices, rhasspy_config)
        _setup_sounds_device(config_sounds_device, sounds_devices, rhasspy_config)
        if self.settings.home_intent.language in ISO639_1_TO_IETF_BCP_47:
            _setup_nanotts_language(self.settings.home_intent.language, rhasspy_config)
        else:
            _setup_espeak_language(self.settings.home_intent.language, rhasspy_config)

        if self.settings.home_intent.beeps:
            self.setup_beeps(rhasspy_config)

        if self.settings.rhasspy.satellite_ids:
            _setup_satellite_ids(self.settings.rhasspy.satellite_ids, rhasspy_config)

    def setup_beeps(self, rhasspy_config):
        beep_high = self.get_file("beep-high.wav", language_dependent=False)
        beep_low = self.get_file("beep-low.wav", language_dependent=False)
        error = self.get_file("error.wav", language_dependent=False)
        if "sounds" in rhasspy_config:
            beep_config = {
                "error": str(error.resolve()),
                "recorded": str(beep_low.resolve()),
                "wake": str(beep_high.resolve()),
            }
            rhasspy_config["sounds"].update(beep_config)


def _log_out_audio_config(microphone_devices, sounds_devices):
    # Figure we should always show this so people can switch without unsetting first.
    LOGGER.info(
        "\nThese are the attached microphones (The default has an asterisk):\n"
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


def _setup_microphone_device(config_microphone_device, microphone_devices, rhasspy_config):
    if not config_microphone_device:
        LOGGER.info("Microphone not set, using default microphone\n")
    else:
        LOGGER.info(f"Using {config_microphone_device} for pyaudio device")
        if config_microphone_device not in microphone_devices:
            raise AudioConfigException(
                f"Microphone device {config_microphone_device} not found in "
                "microphone devices list above."
            )
        if "microphone" in rhasspy_config:
            if "pyaudio" in rhasspy_config["microphone"]:
                rhasspy_config["microphone"]["pyaudio"]["device"] = config_microphone_device
            else:
                rhasspy_config["microphone"].update(
                    {"pyaudio": {"device": config_microphone_device}}
                )
        else:
            LOGGER.warning("No microphone section in rhasspy_profile.json to add microphone device")


def _setup_sounds_device(config_sounds_device, sounds_devices, rhasspy_config):
    if not config_sounds_device:
        LOGGER.warning("Sounds device not set, using sysdefault sound device\n")
    else:
        LOGGER.info(f"Using {config_sounds_device} for aplay device")
        if config_sounds_device not in sounds_devices:
            raise AudioConfigException(
                f"Sounds device {config_sounds_device} not found in sounds devices list above."
            )
        if "sounds" in rhasspy_config:
            if "aplay" in rhasspy_config["sounds"]:
                rhasspy_config["sounds"]["aplay"]["device"] = config_sounds_device
            else:
                rhasspy_config["sounds"].update({"aplay": {"device": config_sounds_device}})
        else:
            LOGGER.warning("No sounds section in rhasspy_profile.json to add sounds device")


def _setup_nanotts_language(language, rhasspy_config):
    if "text_to_speech" in rhasspy_config:
        rhasspy_config["text_to_speech"]["system"] = "nanotts"
        if "nanotts" in rhasspy_config["text_to_speech"]:
            rhasspy_config["text_to_speech"]["nanotts"]["language"] = ISO639_1_TO_IETF_BCP_47[
                language
            ]

        else:
            rhasspy_config["text_to_speech"].update(
                {"nanotts": {"language": ISO639_1_TO_IETF_BCP_47[language]}}
            )
    else:
        LOGGER.warning("Can only auto-setup language if 'text_to_speech' is set in profile.json")


def _setup_espeak_language(language, rhasspy_config):
    if "text_to_speech" in rhasspy_config:
        rhasspy_config["text_to_speech"]["system"] = "espeak"
        if "espeak" in rhasspy_config["text_to_speech"]:
            rhasspy_config["text_to_speech"]["espeak"]["voice"] = language

        else:
            rhasspy_config["text_to_speech"].update({"espeak": {"voice": language}})
    else:
        LOGGER.warning("Can only auto-setup language if 'text_to_speech' is set in profile.json")


def _setup_satellite_ids(satellite_ids: Set[str], rhasspy_config):
    satellite_ids_string = ",".join(satellite_ids)
    if "dialogue" in rhasspy_config:
        rhasspy_config["dialogue"]["satellite_site_ids"] = satellite_ids_string
    if "intent" in rhasspy_config:
        rhasspy_config["intent"]["satellite_site_ids"] = satellite_ids_string
    if "speech_to_text" in rhasspy_config:
        rhasspy_config["speech_to_text"]["satellite_site_ids"] = satellite_ids_string
    if "text_to_speech" in rhasspy_config:
        rhasspy_config["text_to_speech"]["satellite_site_ids"] = satellite_ids_string
