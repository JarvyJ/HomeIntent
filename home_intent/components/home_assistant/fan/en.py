from .base_fan import intents, BaseFan

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
            "(start|stop) oscillating the ($oscillating_fan)",
            "oscillate the ($oscillating_fan)",
            "(set|change|make) the ($oscillating_fan) [to] [not] oscillate",
            "turn (on|off) the ($oscillating_fan) oscillation",
        ]
    )
    def oscillate_fan(self, oscillating_fan):
        response = self._oscillate_fan(oscillating_fan)
        oscillation_change = response["attributes"]["oscillating"]
        start_or_stop = "Starting" if oscillation_change else "Stopping"
        return f"{start_or_stop} the oscillation for the {response['attributes']['friendly_name']}"

    @intents.sentences(["(set | change | make) the ($preset_fan) to ($preset_mode)"])
    def set_preset(self, preset_fan, preset_mode):
        response = self._set_preset(preset_fan, preset_mode)
        return f"Setting the {response['attributes']['friendly_name']} to {preset_mode}"

    @intents.sentences(["reverse the ($directional_fan) [flow|airflow]"])
    def reverse_airflow(self, directional_fan):
        response = self._reverse_airflow(directional_fan)
        return f"Reversing the {response['attributes']['friendly_name']} airflow"

    @intents.sentences(["(set|change|make) the ($speed_fan) [to] ($fan_speed)"])
    def set_fan_speed(self, speed_fan, fan_speed):
        response = self._set_fan_speed(speed_fan, fan_speed)
        return f"Setting the {response['attributes']['friendly_name']} to {fan_speed}"

    @intents.sentences(
        ["increase the ($speed_fan) [fan] speed", "increase the fan speed for ($speed_fan)"]
    )
    def increase_fan_speed(self, speed_fan):
        response, new_fan_speed = self._increase_fan_speed(speed_fan, FAN_SPEED_LIST)
        return f"Setting the {response['attributes']['friendly_name']} to {new_fan_speed}"

    @intents.sentences(
        ["decrease the ($speed_fan) [fan] speed", "decrease the fan speed for ($speed_fan)"]
    )
    def decrease_fan_speed(self, speed_fan):
        response, new_fan_speed = self._decrease_fan_speed(speed_fan, FAN_SPEED_LIST)
        return f"Setting the {response['attributes']['friendly_name']} to {new_fan_speed}"
