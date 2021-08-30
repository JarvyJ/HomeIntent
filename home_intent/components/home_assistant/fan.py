from enum import IntFlag, auto
from home_intent import Intents

intents = Intents(__name__)


class SupportedFeatures(IntFlag):
    SUPPORT_DIRECTION = auto()
    SUPPORT_SET_SPEED = auto()
    SUPPORT_OSCILLATE = auto()
    SUPPORT_PRESET_MODE = auto()


FAN_SPEED_LIST = ["off", "low", "medium", "high"]


class Fan:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("fan.")]

    @intents.dictionary_slots
    def fan(self):
        slots = {f"{x['attributes'].get('friendly_name')}": x["entity_id"] for x in self.entities}
        return slots

    @intents.dictionary_slots
    def oscillating_fan(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_OSCILLATE
            in SupportedFeatures(x["attributes"].get("supported_features", 0))
        }
        return slots

    @intents.dictionary_slots
    def preset_fan(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_PRESET_MODE
            in SupportedFeatures(x["attributes"].get("supported_features", 0))
        }
        return slots

    @intents.slots
    def preset_mode(self):
        preset_modes = []

        for entity in self.entities:
            if SupportedFeatures.SUPPORT_PRESET_MODE in SupportedFeatures(
                entity["attributes"].get("supported_features", 0)
            ):
                preset_modes.extend(entity["attributes"]["preset_modes"])

        return preset_modes

    @intents.dictionary_slots
    def directional_fan(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_DIRECTION
            in SupportedFeatures(x["attributes"].get("supported_features", 0))
        }
        return slots

    @intents.dictionary_slots
    def speed_fan(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_SET_SPEED
            in SupportedFeatures(x["attributes"].get("supported_features", 0))
        }
        return slots

    @intents.slots
    def fan_speed(self):
        return FAN_SPEED_LIST

    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_fan)

    @intents.sentences(["toggle the ($fan)", "turn (on | off) [the] ($fan)"])
    def toggle_fan(self, fan):
        self.ha.api.call_service("fan", "toggle", {"entity_id": fan})
        response = self.ha.api.get_entity(fan)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($fan)"])
    def turn_off(self, fan):
        self.ha.api.call_service("fan", "turn_off", {"entity_id": fan})
        response = self.ha.api.get_entity(fan)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($fan)"])
    def turn_on(self, fan):
        self.ha.api.call_service("fan", "turn_on", {"entity_id": fan})
        response = self.ha.api.get_entity(fan)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(
        [
            "(start|stop) oscillating the ($oscillating_fan)",
            "oscillate the ($oscillating_fan)",
            "(set|change|make) the ($oscillating_fan) [to] [not] oscillate",
            "turn (on|off) the ($oscillating_fan) oscillation",
        ]
    )
    def oscillate_fan(self, oscillating_fan):
        response = self.ha.api.get_entity(oscillating_fan)
        oscillation_change = not response["attributes"]["oscillating"]
        start_or_stop = "Starting" if oscillation_change else "Stopping"
        self.ha.api.call_service(
            "fan", "oscillate", {"entity_id": oscillating_fan, "oscillating": oscillation_change,},
        )
        return f"{start_or_stop} the oscillation for the {response['attributes']['friendly_name']}"

    @intents.sentences(["(set | change | make) the ($preset_fan) to ($preset_mode)"])
    def set_preset(self, preset_fan, preset_mode):
        self.ha.api.call_service(
            "fan", "set_preset_mode", {"entity_id": preset_fan, "preset_mode": preset_mode}
        )
        response = self.ha.api.get_entity(preset_fan)
        return f"Setting the {response['attributes']['friendly_name']} to {preset_mode}"

    @intents.sentences(["reverse the ($directional_fan) [flow|airflow]"])
    def reverse_airflow(self, directional_fan):
        response = self.ha.api.get_entity(directional_fan)
        forward_or_reverse = (
            "reverse" if response["attributes"]["direction"] == "reverse" else "forward"
        )
        self.ha.api.call_service(
            "fan",
            "set_direction",
            {"entity_id": directional_fan, "direction": forward_or_reverse,},
        )
        return f"Reversing the {response['attributes']['friendly_name']} flow"

    @intents.sentences(["(set|change|make) the ($speed_fan) [to] ($fan_speed)"])
    def set_fan_speed(self, speed_fan, fan_speed):
        self.ha.api.call_service(
            "fan", "set_speed", {"entity_id": speed_fan, "speed": fan_speed},
        )
        response = self.ha.api.get_entity(speed_fan)
        return f"Setting the {response['attributes']['friendly_name']} to {fan_speed}"

    @intents.sentences(
        ["increase the ($speed_fan) [fan] speed", "increase the fan speed for ($speed_fan)"]
    )
    def increase_fan_speed(self, speed_fan):
        response = self.ha.api.get_entity(speed_fan)
        current_fan_speed = response["attributes"]["speed"]
        # if it's in one of the presets like "auto", this step will fail.
        # we could just increase it to high, but that would be wild if it was in "sleep"
        # maybe these two are default disabled and the user can enable them if wanted?
        current_fan_speed_index = FAN_SPEED_LIST.index(current_fan_speed)

        if current_fan_speed == len(FAN_SPEED_LIST):
            new_fan_speed = FAN_SPEED_LIST[len(FAN_SPEED_LIST) - 1]
        else:
            new_fan_speed = FAN_SPEED_LIST[current_fan_speed_index + 1]

        self.ha.api.call_service(
            "fan", "set_speed", {"entity_id": speed_fan, "speed": new_fan_speed},
        )
        return f"Setting the {response['attributes']['friendly_name']} to {new_fan_speed}"

    @intents.sentences(
        ["decrease the ($speed_fan) [fan] speed", "decrease the fan speed for ($speed_fan)"]
    )
    def decrease_fan_speed(self, speed_fan):
        response = self.ha.api.get_entity(speed_fan)
        current_fan_speed = response["attributes"]["speed"]
        current_fan_speed_index = FAN_SPEED_LIST.index(current_fan_speed)

        if current_fan_speed == 0:
            new_fan_speed = FAN_SPEED_LIST[0]
        else:
            new_fan_speed = FAN_SPEED_LIST[current_fan_speed_index - 1]

        self.ha.api.call_service(
            "fan", "set_speed", {"entity_id": speed_fan, "speed": new_fan_speed},
        )
        return f"Setting the {response['attributes']['friendly_name']} to {new_fan_speed}"
