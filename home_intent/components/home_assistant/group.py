from home_intent import Intents

intents = Intents(__name__)


class Group:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("group.")]

    @intents.dictionary_slots
    def group(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if x["state"] in ("on", "off")
        }
        return slots

    @intents.sentences(["toggle [the] ($group)"])
    def toggle_group(self, group):
        self.ha.api.call_service("homeassistant", "toggle", {"entity_id": group})
        response = self.ha.api.get_entity(group)
        return f"Toggling the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($group)"])
    def turn_on_group(self, group):
        self.ha.api.call_service("homeassistant", "turn_on", {"entity_id": group})
        response = self.ha.api.get_entity(group)
        return f"Turning on the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($group)"])
    def turn_off_group(self, group):
        self.ha.api.call_service("homeassistant", "turn_off", {"entity_id": group})
        response = self.ha.api.get_entity(group)
        return f"Turning off the {response['attributes']['friendly_name']}"
