import json
import logging

LOGGER = logging.getLogger(__name__)


class IntentHandler:
    def __init__(self, mqtt_client, settings, intent_function):
        self.mqtt_client = mqtt_client
        self.settings = settings
        self.intent_function = intent_function

    def setup_mqtt_and_loop(self):
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
            self._error(client, payload["siteId"], payload["sessionId"], exception)
        else:
            if response:
                self._say(client, response, payload["siteId"], payload["sessionId"])

    def _say(self, client, text, site_id, session_id):
        notification = {"text": text, "siteId": site_id, "sessionId": session_id}
        LOGGER.info("Using the session manager to close the session")
        client.publish("hermes/dialogueManager/endSession", json.dumps(notification))

    def _error(self, client, site_id, session_id, custom_data):
        notification = {
            "siteId": site_id,
            "sessionId": session_id,
            "error": f"{custom_data}",
        }
        print(notification)
        # client.publish("hermes/dialogueManager/intentNotRecognized", json.dumps(notification))
        client.publish("hermes/error/dialogueManager", json.dumps(notification))
