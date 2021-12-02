from .base_fan import BaseFan, intents

# TODO: figure out if these change with HA language
FAN_SPEED_LIST = ["off", "low", "medium", "high"]


class Fan(BaseFan):
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
        response = self._toggle_fan(fan)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($fan)"])
    def turn_off(self, fan):
        response = self._turn_off(fan)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($fan)"])
    def turn_on(self, fan):
        response = self._turn_on(fan)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(
        [
            "(start|stop) oscillating the ($fan_oscillate_entity)",
            "oscillate the ($fan_oscillate_entity)",
            "(set|change|make) the ($fan_oscillate_entity) [to] [not] oscillate",
            "turn (on|off) the ($fan_oscillate_entity) oscillation",
        ]
    )
    def oscillate_fan(self, fan_oscillate_entity):
        response = self._oscillate_fan(fan_oscillate_entity)
        oscillation_change = response["attributes"]["oscillating"]
        start_or_stop = "Starting" if oscillation_change else "Stopping"
        return f"{start_or_stop} the oscillation for the {response['attributes']['friendly_name']}"

    @intents.sentences(
        ["(set | change | make) the ($fan_preset_mode_entity) to ($fan_preset_mode)"]
    )
    def set_preset(self, fan_preset_mode_entity, fan_preset_mode):
        response = self._set_preset(fan_preset_mode_entity, fan_preset_mode)
        return f"Setting the {response['attributes']['friendly_name']} to {fan_preset_mode}"

    @intents.sentences(["reverse the ($fan_direction_entity) [flow|airflow]"])
    def reverse_airflow(self, fan_direction_entity):
        response = self._reverse_airflow(fan_direction_entity)
        return f"Reversing the {response['attributes']['friendly_name']} airflow"

    @intents.sentences(["(set|change|make) the ($fan_set_speed_entity) [to] ($fan_speed)"])
    def set_fan_speed(self, fan_set_speed_entity, fan_speed):
        response = self._set_fan_speed(fan_set_speed_entity, fan_speed)
        return f"Setting the {response['attributes']['friendly_name']} to {fan_speed}"

    @intents.sentences(
        [
            "increase the ($fan_set_speed_entity) [fan] speed",
            "increase the fan speed for ($fan_set_speed_entity)",
        ]
    )
    def increase_fan_speed(self, fan_set_speed_entity):
        response, new_fan_speed = self._increase_fan_speed(fan_set_speed_entity, FAN_SPEED_LIST)
        return f"Setting the {response['attributes']['friendly_name']} to {new_fan_speed}"

    @intents.sentences(
        [
            "decrease the ($fan_set_speed_entity) [fan] speed",
            "decrease the fan speed for ($fan_set_speed_entity)",
        ]
    )
    def decrease_fan_speed(self, fan_set_speed_entity):
        response, new_fan_speed = self._decrease_fan_speed(fan_set_speed_entity, FAN_SPEED_LIST)
        return f"Setting the {response['attributes']['friendly_name']} to {new_fan_speed}"
