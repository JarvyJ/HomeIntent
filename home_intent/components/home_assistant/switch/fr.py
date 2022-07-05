from .base_switch import BaseSwitch, intents


class Switch(BaseSwitch):
    @intents.sentences(["Basculer [le] ($switch)", "(activerr | désactiver) [le] ($switch)"])
    def toggle_switch(self, switch):
        response = self._toggle_switch(switch)
        return f"Bascule de {response['attributes']['friendly_name']} sur {response['state']}"

    @intents.sentences(["Désactiver [le] ($switch)"])
    def turn_off(self, switch):
        response = self._turn_off(switch)
        return f"Désactivation de {response['attributes']['friendly_name']} sur {response['state']}"

    @intents.sentences(["Activer [le] ($switch)"])
    def turn_on(self, switch):
        response = self._turn_on(switch)
        return f"Activation de {response['attributes']['friendly_name']} sur {response['state']}"
