from enum import IntFlag, auto

from home_intent import Intents

intents = Intents(__name__)


class SupportedFeatures(IntFlag):
    SUPPORT_MODE = auto()


class Humidifier:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("humidifier.")]

    @intents.dictionary_slots
    def humidifier(self):
        slots = {f"{x['attributes'].get('friendly_name')}": x["entity_id"] for x in self.entities}
        return slots

    @intents.slots
    def humidifier_mode(self):
        humidifier_modes = []

        for entity in self.entities:
            if SupportedFeatures.SUPPORT_MODE in SupportedFeatures(
                entity["attributes"].get("supported_features", 0)
            ):
                humidifier_modes.extend(entity["attributes"]["available_modes"])

        return humidifier_modes

    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_humidifier)

    @intents.sentences(["toggle the ($humidifier)", "turn (on | off) [the] ($humidifier)"])
    def toggle_humidifier(self, humidifier):
        self.ha.api.call_service("humidifier", "toggle", {"entity_id": humidifier})
        response = self.ha.api.get_entity(humidifier)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($humidifier)"])
    def turn_off(self, humidifier):
        self.ha.api.call_service("humidifier", "turn_off", {"entity_id": humidifier})
        response = self.ha.api.get_entity(humidifier)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($humidifier)"])
    def turn_on(self, humidifier):
        self.ha.api.call_service("humidifier", "turn_on", {"entity_id": humidifier})
        response = self.ha.api.get_entity(humidifier)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(
        ["(set | change | make) the ($humidifier) to (0..100){humidity} [percent] [humidity]"]
    )
    def change_humidity(self, humidifier, humidity):
        self.ha.api.call_service(
            "humidifier", "set_humidity", {"entity_id": humidifier, "humidity": humidity},
        )
        response = self.ha.api.get_entity(humidifier)
        return f"Setting the {response['attributes']['friendly_name']} to {humidity}% humidity"

    @intents.sentences(["(set | change | make) the ($humidifier) to ($humidifier_mode)"])
    def set_mode(self, humidifier, humidifier_mode):
        self.ha.api.call_service(
            "humidifier", "set_mode", {"entity_id": humidifier, "mode": humidifier_mode},
        )
        response = self.ha.api.get_entity(humidifier)
        return f"Setting the {response['attributes']['friendly_name']} to {humidifier_mode}"
