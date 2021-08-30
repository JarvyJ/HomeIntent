from home_intent import Intents, get_file
from typing import Dict

intents = Intents(__name__)


class SampleLight:
    def __init__(self):
        self.ha = {}
        self.color_temp_to_name = {}

    @intents.dictionary_slots
    def color(self):
        colors = ["red", "yellow", "blue", "light goldenrod"]
        return {color: color.replace(" ", "") for color in colors}

    @intents.sentences(["toggle the ($lights) [light]", "turn (on|off) the ($lights) [light]"])
    def toggle_light(self, light):
        return "Turning light"
