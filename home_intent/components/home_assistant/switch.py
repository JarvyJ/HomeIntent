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

    @intents.sentences(["toggle the ($switch)", "turn (on | off) [the] ($switch)"])
    def toggle_switch(self, switch):
        self.ha.api.call_service("switch", "toggle", {"entity_id": switch})
        response = self.ha.api.get_entity(switch)
        return f"The {response['attributes']['friendly_name']} switch has been turned {response['state']}"
