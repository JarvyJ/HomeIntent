from .base_remote import BaseRemote, intents


class Remote(BaseRemote):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_remote)

    @intents.sentences(["Basculer [le | la] ($remote)", "(activer | désactiver) [le | la] ($remote)"])
    def toggle_remote(self, remote):
        response = self._toggle_remote(remote)
        return f"Bascule de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["Désactiver [le | la] ($remote)"])
    def turn_off(self, remote):
        response = self._turn_off(remote)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["Activer [le | la] ($remote)"])
    def turn_on(self, remote):
        response = self._turn_on(remote)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"
