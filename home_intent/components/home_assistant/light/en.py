from .base_light import BaseLight, intents


class Light(BaseLight):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_light)

    @intents.sentences(["toggle the ($light) [light]", "turn (on|off) the ($light) [light]"])
    def toggle_light(self, light):
        response = self._toggle_light(light)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} light"

    @intents.sentences(["turn on the ($light) [light]"])
    def turn_on(self, light):
        response = self._turn_on(light)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} light"

    @intents.sentences(["turn off the ($light) [light]"])
    def turn_off(self, light):
        response = self._turn_off(light)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} light"

    @intents.sentences(["(set | change | make) the ($light) [light] [to] ($light_color)"])
    def change_color(self, light, light_color):
        response, color_name = self._change_color(light, light_color)
        return f"Setting the {response['attributes']['friendly_name']} to {color_name}"

    @intents.sentences(
        [
            "(set | change | make) the ($light) [light] [to] ($light_color) [at] (0..100){brightness} [percent] [brightness]"
        ]
    )
    def change_color_brightness(self, light, light_color, brightness):
        response, color_name = self._change_color_brightness(light, light_color, brightness)
        return f"Setting the {response['attributes']['friendly_name']} to {color_name} at {brightness}% brightness"

    @intents.sentences(
        [
            "(set | change | make) the ($light) [light] to (0..100){brightness} [percent] [brightness]"
        ]
    )
    def change_brightness(self, light, brightness):
        response = self._change_brightness(light, brightness)
        return f"Setting the {response['attributes']['friendly_name']} to {brightness}% brightness"

    @intents.sentences(
        ["(set | change | make) the ($light) [light] [to] ($light_color_temperature)"]
    )
    def change_color_temperature(self, light, light_color_temperature):
        response, color_temp_name = self._change_color_temperature(light, light_color_temperature)
        return f"Setting the {response['attributes']['friendly_name']} to {color_temp_name}"

    @intents.sentences(
        [
            "(set | change | make) the ($light) [light] [to] ($light_color_temperature) [at] (0..100){brightness} [percent] [brightness]"
        ]
    )
    def change_color_temperature_brightness(self, light, light_color_temperature, brightness):
        response, color_temp_name = self._change_color_temperature_brightness(
            light, light_color_temperature, brightness
        )
        return f"Setting the {response['attributes']['friendly_name']} to {color_temp_name} at {brightness}% brightness"
