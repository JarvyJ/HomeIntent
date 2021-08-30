from home_intent import Intents

intents = Intents(__name__)


class Remote:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("remote.")]

    @intents.dictionary_slots
    def remote(self):
        slots = {f"{x['attributes'].get('friendly_name')}": x["entity_id"] for x in self.entities}
        return slots

    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_remote)

    @intents.sentences(["toggle the ($remote)", "turn (on | off) [the] ($remote)"])
    def toggle_remote(self, remote):
        self.ha.api.call_service("remote", "toggle", {"entity_id": remote})
        response = self.ha.api.get_entity(remote)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($remote)"])
    def turn_off(self, remote):
        self.ha.api.call_service("remote", "turn_off", {"entity_id": remote})
        response = self.ha.api.get_entity(remote)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($remote)"])
    def turn_on(self, remote):
        self.ha.api.call_service("remote", "turn_on", {"entity_id": remote})
        response = self.ha.api.get_entity(remote)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"
