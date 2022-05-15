import json
import logging
from typing import Dict
from home_intent.intents import Sentence

import paho.mqtt.client as mqtt

LOGGER = logging.getLogger(__name__)

# since this has to integrate with paho, there are just extra args everywhere.
# pylint: disable=unused-argument


class IntentHandler:
    def __init__(self, mqtt_client, settings, intent_function, startup_messenger):
        self.mqtt_client = mqtt_client
        self.settings = settings
        self.intent_function: Dict[str, Sentence] = intent_function
        self.startup_messenger = startup_messenger

    def setup_mqtt_and_loop(self):
        self.startup_messenger.update("Connecting to MQTT")
        self.mqtt_client.message_callback_add("hermes/intent/#", self._handle_intent)
        if self.settings.rhasspy.mqtt_username and self.settings.rhasspy.mqtt_password:
            self.mqtt_client.username_pw_set(
                username=self.settings.rhasspy.mqtt_username,
                password=self.settings.rhasspy.mqtt_password,
            )
        self.mqtt_client.on_connect = _on_connect
        self.mqtt_client.connect(
            self.settings.rhasspy.mqtt_host, self.settings.rhasspy.mqtt_port, 60
        )
        LOGGER.info("Waiting to handle intents!")
        self.startup_messenger.update("Ready to handle intents!")
        self.mqtt_client.loop_forever()

    def _handle_intent(self, client, userdata, message: mqtt.MQTTMessage):
        payload = json.loads(message.payload)
        intent_name = payload["intent"]["intentName"]

        if intent_name not in self.intent_function:
            LOGGER.info(f"Not a Home Intent intent to handle: {intent_name}")
            return

        slots = {}
        for slot in payload["slots"]:
            slots[slot["slotName"]] = slot["value"]["value"]
        LOGGER.info(f"Handling intent: {intent_name}")
        LOGGER.debug(slots)
        try:
            if self.intent_function[intent_name].needs_satellite_id:
                slots["satellite_id"] = payload["siteId"]

            response = self.intent_function[intent_name].func(**slots)

        except Exception as exception:  # pylint: disable=broad-except
            LOGGER.exception(exception)
            _error(client, payload["siteId"], payload["sessionId"], exception, payload["input"])
        else:
            if response:
                _say(client, response, payload["siteId"], payload["sessionId"])


def _on_connect(client, userdata, flags, return_code):
    LOGGER.info("Connected to MQTT. This happens when the Rhasspy MQTT starts (or restarts)")
    if return_code == 0:
        LOGGER.info("Subscribed to intent messages: hermes/intent/#")
        client.subscribe("hermes/intent/#")
    else:
        LOGGER.error(f"Failed to connect to MQTT. Return Code: {return_code}")


def _error(client, site_id, session_id, custom_data, input_str):
    notification = {
        "siteId": site_id,
        "sessionId": session_id,
        "customData": f"{custom_data}",
        "input": input_str,
    }
    client.publish("hermes/nlu/intentNotRecognized", json.dumps(notification))


def _say(client, text, site_id, session_id):
    text = _remove_duplicate_word_at_end(text)
    notification = {"text": text, "siteId": site_id, "sessionId": session_id}
    LOGGER.info(text)
    client.publish("hermes/dialogueManager/endSession", json.dumps(notification))


def _remove_duplicate_word_at_end(text):
    split = text.rsplit(maxsplit=2)
    if len(split) == 3 and split[-1] == split[-2]:
        return f"{split[0]} {split[1]}"
    else:
        return text
