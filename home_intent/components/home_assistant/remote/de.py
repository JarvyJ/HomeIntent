from .base_remote import BaseRemote, intents


class Remote(BaseRemote):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_remote)

    @intents.sentences(["Schalte ($remote)", "Schalte ($remote) (an | aus)"])
    def toggle_remote(self, remote):
        response = self._toggle_remote(remote)
        return f"Schalte {response['attributes']['friendly_name']} {response['state']}"

    @intents.sentences(["Schalte ($remote) aus"])
    def turn_off(self, remote):
        response = self._turn_off(remote)
        return f"Schalte {response['attributes']['friendly_name']} {response['state']}"

    @intents.sentences(["Schalte ($remote) an"])
    def turn_on(self, remote):
        response = self._turn_on(remote)
        return f"Schalte {response['attributes']['friendly_name']} {response['state']}"