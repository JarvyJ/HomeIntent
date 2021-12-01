from .base_humidifier import BaseHumidifier, intents


class Humidifier(BaseHumidifier):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_humidifier)

    @intents.sentences(["toggle the ($humidifier)", "turn (on | off) [the] ($humidifier)"])
    def toggle_humidifier(self, humidifier):
        response = self._toggle_humidifier(humidifier)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($humidifier)"])
    def turn_off(self, humidifier):
        response = self._turn_off(humidifier)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($humidifier)"])
    def turn_on(self, humidifier):
        response = self._turn_on(humidifier)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(
        ["(set | change | make) the ($humidifier) to (0..100){humidity} [percent] [humidity]"]
    )
    def change_humidity(self, humidifier, humidity):
        response = self._change_humidity(humidifier, humidity)
        return f"Setting the {response['attributes']['friendly_name']} to {humidity}% humidity"

    @intents.sentences(["(set | change | make) the ($humidifier) to ($humidifier_mode)"])
    def set_mode(self, humidifier, humidifier_mode):
        response = self._set_mode(humidifier, humidifier_mode)
        return f"Setting the {response['attributes']['friendly_name']} to {humidifier_mode}"
