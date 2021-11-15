from enum import IntFlag, auto

from home_intent import Intents

intents = Intents(__name__)


class SupportedFeatures(IntFlag):
    SUPPORT_DIRECTION = auto()
    SUPPORT_SET_SPEED = auto()
    SUPPORT_OSCILLATE = auto()
    SUPPORT_PRESET_MODE = auto()


class BaseFan:
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

    def _toggle_fan(self, fan):
        self.ha.api.call_service("fan", "toggle", {"entity_id": fan})
        response = self.ha.api.get_entity(fan)
        return response

    def _turn_off(self, fan):
        self.ha.api.call_service("fan", "turn_off", {"entity_id": fan})
        response = self.ha.api.get_entity(fan)
        return response

    def _turn_on(self, fan):
        self.ha.api.call_service("fan", "turn_on", {"entity_id": fan})
        response = self.ha.api.get_entity(fan)
        return response

    def _oscillate_fan(self, oscillating_fan):
        response = self.ha.api.get_entity(oscillating_fan)
        oscillation_change = not response["attributes"]["oscillating"]
        self.ha.api.call_service(
            "fan", "oscillate", {"entity_id": oscillating_fan, "oscillating": oscillation_change,},
        )
        response = self.ha.api.get_entity(oscillating_fan)
        return response

    def _set_preset(self, preset_fan, preset_mode):
        self.ha.api.call_service(
            "fan", "set_preset_mode", {"entity_id": preset_fan, "preset_mode": preset_mode}
        )
        response = self.ha.api.get_entity(preset_fan)
        return f"Setting the {response['attributes']['friendly_name']} to {preset_mode}"

    def _reverse_airflow(self, directional_fan):
        response = self.ha.api.get_entity(directional_fan)
        forward_or_reverse = (
            "reverse" if response["attributes"]["direction"] == "reverse" else "forward"
        )
        self.ha.api.call_service(
            "fan",
            "set_direction",
            {"entity_id": directional_fan, "direction": forward_or_reverse,},
        )
        response = self.ha.api.get_entity(directional_fan)
        return response

    def _set_fan_speed(self, speed_fan, fan_speed):
        self.ha.api.call_service(
            "fan", "set_speed", {"entity_id": speed_fan, "speed": fan_speed},
        )
        response = self.ha.api.get_entity(speed_fan)
        return f"Setting the {response['attributes']['friendly_name']} to {fan_speed}"

    def _increase_fan_speed(self, speed_fan, fan_speed_list):
        response = self.ha.api.get_entity(speed_fan)
        current_fan_speed = response["attributes"]["speed"]
        # if it's in one of the presets like "auto", this step will fail.
        # we could just increase it to high, but that would be wild if it was in "sleep"
        # maybe these two are default disabled and the user can enable them if wanted?
        current_fan_speed_index = fan_speed_list.index(current_fan_speed)

        if current_fan_speed == len(fan_speed_list):
            new_fan_speed = fan_speed_list[len(fan_speed_list) - 1]
        else:
            new_fan_speed = fan_speed_list[current_fan_speed_index + 1]

        self.ha.api.call_service(
            "fan", "set_speed", {"entity_id": speed_fan, "speed": new_fan_speed},
        )
        response = self.ha.api.get_entity(speed_fan)
        return response, new_fan_speed

    def _decrease_fan_speed(self, speed_fan, fan_speed_list):
        response = self.ha.api.get_entity(speed_fan)
        current_fan_speed = response["attributes"]["speed"]
        current_fan_speed_index = fan_speed_list.index(current_fan_speed)

        if current_fan_speed == 0:
            new_fan_speed = fan_speed_list[0]
        else:
            new_fan_speed = fan_speed_list[current_fan_speed_index - 1]

        self.ha.api.call_service(
            "fan", "set_speed", {"entity_id": speed_fan, "speed": new_fan_speed},
        )
        response = self.ha.api.get_entity(speed_fan)
        return response, new_fan_speed
