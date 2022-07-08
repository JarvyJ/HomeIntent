from .base_switch import BaseSwitch, intents


class Switch(BaseSwitch):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_switch)
            
    @intents.sentences(["Basculer [le] ($switch)", "(activerr | désactiver) [le] ($switch)"])
    def toggle_switch(self, switch):
        response = self._toggle_switch(switch)
        return f"Bascule (de | du) {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["Désactiver [le] ($switch)"])
    def turn_off(self, switch):
        response = self._turn_off(switch)
        return f"Réglage (de | du)  {response['attributes']['friendly_name']} sur {response['state']}"

    @intents.sentences(["Activer [le] ($switch)"])
    def turn_on(self, switch):
        response = self._turn_on(switch)
        return f"Réglage (de | du) {response['attributes']['friendly_name']} sur {response['state']}"
