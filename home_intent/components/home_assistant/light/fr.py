from .base_light import BaseLight, intents


class Light(BaseLight):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_light)

    @intents.sentences(
        [
            "Basculer [la | le] [lumière] [de | du] ($light)",
            "(allumer | éteindre) [la | le] [lumière] [de | du] ($light)",
        ]
    )
    def toggle_light(self, light):
        response = self._toggle_light(light)
        return (
            f"Bascule de la lumière {response['attributes']['friendly_name']} à {response['state']}"
        )

    @intents.sentences(["Allumer [la | le] lumière ($light)"])
    def turn_on(self, light):
        response = self._turn_on(light)
        return (
            f"Réglage de la lumière {response['attributes']['friendly_name']} à {response['state']}"
        )

    @intents.sentences(["éteindre [la | le] lumière ($light)"])
    def turn_off(self, light):
        response = self._turn_off(light)
        return f"Réglage de la lumière {response['attributes']['friendly_name']} à  {response['state']}"

    @intents.sentences(
        ["(régler | changer | mettre) [la | le] [lumière] ($light) [à] ($light_color)"]
    )
    def change_color(self, light, light_color):
        response, color_name = self._change_color(light, light_color)
        return f"Réglage de la lumière {response['attributes']['friendly_name']} à {color_name}"

    @intents.sentences(
        [
            "(régler | changer | mettre) [la | le] [lumière] ($light) [à] ($light_color) [à] (0..100){brightness} pour cent [de] [luminosité]"
        ]
    )
    def change_color_brightness(self, light, light_color, brightness):
        response, color_name = self._change_color_brightness(light, light_color, brightness)
        return f"Réglage de {response['attributes']['friendly_name']} à {color_name} à {brightness}% de luminosité"

    @intents.sentences(
        [
            "(régler | changer | mettre) [la | le] [lumière] ($light) à (0..100){brightness} pour cent [de] [luminosité]"
        ]
    )
    def change_brightness(self, light, brightness):
        response = self._change_brightness(light, brightness)
        return f"Réglage de {response['attributes']['friendly_name']} à {brightness}% de luminosité"

    @intents.sentences(
        ["(régler | changer | mettre)  [la | le] [lumière] ($light) [à] ($light_color_temperature)"]
    )
    def change_color_temperature(self, light, light_color_temperature):
        response, color_temp_name = self._change_color_temperature(light, light_color_temperature)
        return f"Réglage de {response['attributes']['friendly_name']} à {color_temp_name}"

    @intents.sentences(
        [
            "(régler | changer | mettre)  [la | le] [lumière] ($light) [à] ($light_color_temperature) [à] (0..100){brightness} pour cent [de] [luminosité]"
        ]
    )
    def change_color_temperature_brightness(self, light, light_color_temperature, brightness):
        response, color_temp_name = self._change_color_temperature_brightness(
            light, light_color_temperature, brightness
        )
        return f"Réglage de {response['attributes']['friendly_name']} à {color_temp_name} à {brightness}% de luminosité"
