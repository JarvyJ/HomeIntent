from home_intent import Intents, get_file
from typing import Dict

intents = Intents(__name__)


class Light:
    def __init__(self):
        self.ha = {}
        self.color_temp_to_name = {}

    @intents.dictionary_slots
    def color(self):
        colors = ["red", "yellow", "blue", "light goldenrod"]
        return {color: color.replace(" ", "") for color in colors}

    @intents.sentences(["toggle the ($light) [light]", "turn (on|off) the ($light) [light]"])
    def toggle_light(self, light):
        return "Turning light"

    @intents.sentences(["turn on the ($light) [light]"])
    def turn_on(self, light):
        return "Turning light"

    @intents.sentences(["turn off the ($light) [light]"])
    def turn_off(self, light):
        return "Turning light"

    @intents.beta
    @intents.sentences(["(set | change | make) the ($light) [light] [to] ($color_temperature)"])
    def change_color_temperature(self, light, color_temperature):
        return "Setting to "

    @intents.default_disable("uhhh, no good for some reason!")
    @intents.sentences(["(set | change | make) the ($light) [light] [to] ($color_temperature)"])
    def change_color_temperature2(self, light, color_temperature):
        return "Setting to "


def test_registered_slots():
    assert len(intents.all_slots) == 1


def test_registered_sentences():
    assert len(intents.all_sentences) == 5


def test_disabled_sentences():
    assert len({k: v for (k, v) in intents.all_sentences.items() if v.disabled is True}) == 2
