from .base_light import BaseLight, intents


class Light(BaseLight):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_light)    

    @intents.repeatable_dictionary_slots
    def light_number(self):
        # this is used to overwrite (or add) some numbers provided by Rhasspy's num2words package
        return {            
            "hundert": "100",            
        }
    

    @intents.sentences(["Schalte [(das | die)] ($light)", "(Schalte | Mache) ($light) (an | aus)"])
    def toggle_light(self, light):        
        response = self._toggle_light(light)        
        return f"Schalte {response['attributes']['friendly_name']} {response['state']}"

    @intents.sentences(["(Schalte | Mache) [(das | die)] ($light) (an | ein)"])
    def turn_on(self, light):
        response = self._turn_on(light)
        return f"Schalte {response['attributes']['friendly_name']} {response['state']}"

    @intents.sentences(["(Schalte | Mache) [(das | die)] ($light) aus"])
    def turn_off(self, light):
        response = self._turn_off(light)        
        return f"Schalte {response['attributes']['friendly_name']} {response['state']}"
    
    @intents.sentences(["(Stelle | Ändere) [(das | die)] ($light) [auf] ($light_color)"])
    def change_color(self, light, light_color):
        response, color_name = self._change_color(light, light_color)        
        return f"Stelle {response['attributes']['friendly_name']} auf {color_name}"

    @intents.sentences(["(Stelle | Ändere) [(das | die)] ($light) auf ($light_number | 0..100){brightness} Prozent ($light_color)",
     "(Stelle | Ändere) [(das | die)] ($light) auf ($light_color) (mit | und) ($light_number | 0..100){brightness} Prozent Helligkeit"])
    def change_color_brightness(self, light, light_color, brightness):
        response, color_name = self._change_color_brightness(light, light_color, brightness)        
        return f"Stelle {response['attributes']['friendly_name']} auf {brightness}% {color_name}"

    @intents.sentences(["(Stelle | Ändere) [(das | die)] ($light) auf ($light_number | 0..100){brightness} Prozent [Helligkeit]"])
    def change_brightness(self, light, brightness):
        response = self._change_brightness(light, brightness)        
        return f"Stelle {response['attributes']['friendly_name']} auf {brightness}% Helligkeit"

    @intents.sentences(["(Stelle | Ändere) [(das | die)] ($light) auf ($light_color_temperature)"])
    def change_color_temperature(self, light, light_color_temperature):
        response, color_temp_name = self._change_color_temperature(light, light_color_temperature)
        return f"Stelle {response['attributes']['friendly_name']} auf {color_temp_name}"

    @intents.sentences(["(Stelle | Ändere) [(das | die)] ($light) [auf] ($light_color_temperature) (und | mit) ($light_number | 0..100){brightness} Prozent [Helligkeit]"])
    def change_color_temperature_brightness(self, light, light_color_temperature, brightness):
        response, color_temp_name = self._change_color_temperature_brightness(light, light_color_temperature, brightness)
        return f"Stelle {response['attributes']['friendly_name']} auf {color_temp_name} mit {brightness}% Helligkeit"