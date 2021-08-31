from home_intent import Intents, get_file
from typing import Dict

intents = Intents(__name__)


class SampleLight:
    def __init__(self):
        self.ha = {}
        self.color_temp_to_name = {}

    @intents.dictionary_slots
    def color(self):
        colors = ["red", "yellow", "blue", "light goldenrod", "light blue"]
        return {color: color.replace(" ", "") for color in colors}

    @intents.slots
    def light(self):
        return ["bedroom", "kitchen", "attic"]

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
