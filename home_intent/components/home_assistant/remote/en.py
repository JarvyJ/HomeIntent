from .base_remote import BaseRemote, intents


class Remote(BaseRemote):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_remote)

    @intents.sentences(["toggle the ($remote)", "turn (on | off) [the] ($remote)"])
    def toggle_remote(self, remote):
        response = self._toggle_remote(remote)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($remote)"])
    def turn_off(self, remote):
        response = self._turn_off(remote)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($remote)"])
    def turn_on(self, remote):
        response = self._turn_on(remote)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"
