from home_intent import Intents, get_file

intents = Intents(__name__)


class Light:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("light.")]
        self.light_service = next(x for x in self.ha.services if x["domain"] == "light")

    @intents.dictionary_slots
    def light(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if x["state"] in ("on", "off")
        }
        return slots

    @intents.dictionary_slots
    def color(self):
        color_file = get_file("home_assistant/colors.txt")
        colors = color_file.read_text().strip().split("\n")
        return {color: color.replace(" ", "") for color in colors}

        # The original colors came from here:
        # self.light_service["services"]["turn_on"]["fields"]["color_name"]["selector"]["select"]["options"]

    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_light)

    @intents.sentences(["toggle the ($light) [light]", "turn (on|off) the ($light) [light]"])
    def toggle_light(self, light):
        self.ha.api.call_service("light", "toggle", {"entity_id": light})
        response = self.ha.api.get_entity(light)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} light"

    @intents.sentences(["turn on the ($light) [light]"])
    def turn_on(self, light):
        self.ha.api.call_service("light", "turn_on", {"entity_id": light})
        response = self.ha.api.get_entity(light)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} light"

    @intents.sentences(["turn off the ($light) [light]"])
    def turn_off(self, light):
        self.ha.api.call_service("light", "turn_off", {"entity_id": light})
        response = self.ha.api.get_entity(light)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} light"

    @intents.sentences(["(set | change | make) the ($light) [light] [to] ($color)"])
    def change_color(self, light, color):
        self.ha.api.call_service("light", "turn_on", {"entity_id": light, "color_name": color})
        response = self.ha.api.get_entity(light)
        return f"Setting the {response['attributes']['friendly_name']} to {color}"

    @intents.sentences(
        [
            "(set | change | make) the ($light) [light] [to] ($color) [at] (0..100){brightness} [percent] [brightness]"
        ]
    )
    def change_color_brightness(self, light, color, brightness):
        self.ha.api.call_service(
            "light",
            "turn_on",
            {"entity_id": light, "color_name": color, "brightness_pct": brightness},
        )
        response = self.ha.api.get_entity(light)
        return f"Setting the {response['attributes']['friendly_name']} to {color} at {brightness}% brightness"

    @intents.sentences(
        [
            "(set | change | make) the ($light) [light] to (0..100){brightness} [percent] [brightness]"
        ]
    )
    def change_brightness(self, light, brightness):
        self.ha.api.call_service(
            "light", "turn_on", {"entity_id": light, "brightness_pct": brightness}
        )
        response = self.ha.api.get_entity(light)
        return f"Setting the {response['attributes']['friendly_name']} to {brightness}% brightness"
