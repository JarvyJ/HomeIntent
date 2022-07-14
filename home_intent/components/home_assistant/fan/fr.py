from .base_fan import BaseFan, intents

# TODO: figure out if these change with HA language
FAN_SPEED_LIST = ["éteint", "faible", "moyen", "fort"]


class Fan(BaseFan):
    @intents.slots
    def fan_speed(self):
        return FAN_SPEED_LIST

    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_fan)

    @intents.sentences(["Basculer l'état de ($fan)", "(Allumer | éteindre) [le] ($fan)"])
    def toggle_fan(self, fan):
        response = self._toggle_fan(fan)
        return f"Bascule de l'état de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["éteindre [le|la] ($fan)"])
    def turn_off(self, fan):
        response = self._turn_off(fan)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["Allumer [le] ($fan)"])
    def turn_on(self, fan):
        response = self._turn_on(fan)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(
        [
            "(démarrer|arrêter) l'oscillation de ($fan_oscillate_entity)",
            "Osciller [le] ($fan_oscillate_entity)",
            "(régler|changer|faire) [le] ($fan_oscillate_entity) [à] [ne] [pas] osciller",
            "(activer|désactiver) l'oscillation de ($fan_oscillate_entity)",
        ]
    )
    def oscillate_fan(self, fan_oscillate_entity):
        response = self._oscillate_fan(fan_oscillate_entity)
        oscillation_change = response["attributes"]["oscillating"]
        start_or_stop = "Marche" if oscillation_change else "Arrêt"
        return f"{start_or_stop} de l'oscillation de {response['attributes']['friendly_name']}"

    @intents.sentences(
        ["(régler|changer|ajuster) [le] ($fan_preset_mode_entity) [sur] [à] ($fan_preset_mode)"]
    )
    def set_preset(self, fan_preset_mode_entity, fan_preset_mode):
        response = self._set_preset(fan_preset_mode_entity, fan_preset_mode)
        return f"réglage de {response['attributes']['friendly_name']} à {fan_preset_mode}"

    @intents.sentences(["inverser le flux d'aire de ($fan_direction_entity)"])
    def reverse_airflow(self, fan_direction_entity):
        response = self._reverse_airflow(fan_direction_entity)
        return f"Inversion du dlux d'air de {response['attributes']['friendly_name']}"

    @intents.sentences(["(régler|changer|ajuster) le ($fan_set_speed_entity) [à] ($fan_speed)"])
    def set_fan_speed(self, fan_set_speed_entity, fan_speed):
        response = self._set_fan_speed(fan_set_speed_entity, fan_speed)
        return f"réglage de {response['attributes']['friendly_name']} à {fan_speed}"

    @intents.sentences(
        [
            "augmenter la vitesse [du] [ventilateur] de ($fan_set_speed_entity)",
            "augmenter la ventilation de ($fan_set_speed_entity)",
        ]
    )
    def increase_fan_speed(self, fan_set_speed_entity):
        response, new_fan_speed = self._increase_fan_speed(fan_set_speed_entity, FAN_SPEED_LIST)
        return f"réglage de {response['attributes']['friendly_name']} à {new_fan_speed}"

    @intents.sentences(
        [
            "diminuer la vitesse [du] [ventilateur] de ($fan_set_speed_entity)",
            "diminuer la ventilation de ($fan_set_speed_entity)",
        ]
    )
    def decrease_fan_speed(self, fan_set_speed_entity):
        response, new_fan_speed = self._decrease_fan_speed(fan_set_speed_entity, FAN_SPEED_LIST)
        return f"réglage de {response['attributes']['friendly_name']} à {new_fan_speed}"
