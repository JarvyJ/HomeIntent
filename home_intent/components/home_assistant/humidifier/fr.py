from .base_humidifier import BaseHumidifier, intents


class Humidifier(BaseHumidifier):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_humidifier)

    @intents.sentences(["Basculer l'état de ($humidifier)", "(allumer | éteindre) [le] ($humidifier)"])
    def toggle_humidifier(self, humidifier):
        response = self._toggle_humidifier(humidifier)
        return f"Bascule de l'état de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["éteindre [le] ($humidifier)"])
    def turn_off(self, humidifier):
        response = self._turn_off(humidifier)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["allumer [le] ($humidifier)"])
    def turn_on(self, humidifier):
        response = self._turn_on(humidifier)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(
        ["(régler | changer | ajuster) [le] ($humidifier) à (0..100){humidity} [pourcent] [d'humidité]]"]
    )
    def change_humidity(self, humidifier, humidity):
        response = self._change_humidity(humidifier, humidity)
        return f"Réglage de {response['attributes']['friendly_name']} à {humidity}% d'humidité"

    @intents.sentences(["(régler | changer | ajuster) [le] [mode] [de] ($humidifier) à ($humidifier_mode)"])
    def set_mode(self, humidifier, humidifier_mode):
        response = self._set_mode(humidifier, humidifier_mode)
        return f"Réglage du mode de {response['attributes']['friendly_name']} à {humidifier_mode}"
