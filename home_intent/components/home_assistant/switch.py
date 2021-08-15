from home_intent import Intents

intents = Intents(__name__)


class Switch:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("switch.")]

    @intents.dictionary_slots
    def switch(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if x["state"] in ("on", "off")
        }
        return slots

    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_switch)

    @intents.sentences(["toggle the ($switch)", "turn (on | off) [the] ($switch)"])
    def toggle_switch(self, switch):
        self.ha.api.call_service("switch", "toggle", {"entity_id": switch})
        response = self.ha.api.get_entity(switch)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($switch)"])
    def turn_off(self, switch):
        self.ha.api.call_service("switch", "turn_off", {"entity_id": switch})
        response = self.ha.api.get_entity(switch)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($switch)"])
    def turn_on(self, switch):
        self.ha.api.call_service("switch", "turn_on", {"entity_id": switch})
        response = self.ha.api.get_entity(switch)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"
