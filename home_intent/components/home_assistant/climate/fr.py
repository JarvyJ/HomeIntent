from .base_climate import BaseClimate, intents


class Climate(BaseClimate):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_fan)

    @intents.sentences(["Basculer l'état de ($climate)", "(allumer | éteindre) [le] ($climate)"])
    def toggle_climate(self, climate):
        response = self._toggle_climate(climate)
        return f"Bascule de l'état de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["éteindre [le] ($climate)"])
    def turn_off(self, climate):
        response = self._turn_off(climate)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["Allumer [le] ($climate)"])
    def turn_on(self, climate):
        response = self._turn_on(climate)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"
    
    @intents.repeatable_dictionary_slots
    def climate_hvac_mode_french(self):
        # this is used to overwrite (or add) some climate_havc_mode attributes provided by homeassistant
        return {
            "ventilation": "cool",
            "chauffage": "heat",
            "éteint": "off",
        }

    @intents.sentences(["(régler | changer | ajuster) le ($climate) à ($climate_hvac_mode | $climate_hvac_mode_french)"])
    def set_hvac_mode(self, climate, climate_hvac_mode):
        response = self._set_hvac_mode(climate, climate_hvac_mode)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(
        [
            "(régler | changer | ajuster) la température de ($climate_target_temperature_entity) à (0..250){temperature} [degrés] [(fahrenheit|celsius)]"
        ]
    )
    def set_target_temperature(self, climate_target_temperature_entity, temperature):
        response = self._set_target_temperature(climate_target_temperature_entity, temperature)
        return f"Régalge de {response['attributes']['friendly_name']} à {temperature}"

    @intents.sentences(
        [
            "(régler | changer | ajuster) la température minimum de ($climate_target_temperature_range_entity) à (0..250){temperature} [degrés] [(fahrenheit|celsius)]"
        ]
    )
    def set_target_temperature_low(self, climate_target_temperature_range_entity, temperature):
        response = self._set_target_temperature_low(
            climate_target_temperature_range_entity, temperature
        )
        return f"Réglage de {response['attributes']['friendly_name']} à la température minimmum de {temperature}"

    @intents.sentences(
        [
            "(régler | changer | ajuster) la température maximum de ($climate_target_temperature_range_entity) à (0..250){temperature} [degrés] [(fahrenheit|celsius)]"
        ]
    )
    def set_target_temperature_high(self, climate_target_temperature_range_entity, temperature):
        response = self._set_target_temperature_high(
            climate_target_temperature_range_entity, temperature
        )
        return f"Réglage de {response['attributes']['friendly_name']} à la température maximum de {temperature}"

    @intents.sentences(
        [
            "(régler | changer | ajuster) la ($climate_target_humidity_entity) à (30..99){humidity} [pour] [cent] d'humidité"
        ]
    )
    def set_humidity(self, climate_target_humidity_entity, humidity):
        response = self._set_humidity(climate_target_humidity_entity, humidity)
        return f"Régalge de {response['attributes']['friendly_name']} à {humidity}% d'humidité"

    @intents.sentences(
        ["(régler | changer | ajuster) la ($climate_preset_mode_entity) à ($climate_preset_mode)"]
    )
    def set_preset_mode(self, climate_preset_mode_entity, climate_preset_mode):
        response = self._set_preset_mode(climate_preset_mode_entity, climate_preset_mode)
        return f"Régalge de {response['attributes']['friendly_name']} à {response['attributes']['preset_mode']}"

    @intents.sentences(
        [
            "Basculer l'état de la chaleur auxiliaire de ($climate_aux_heat_entity)",
            "(allumer | éteindre) la chaleur auxiliaire de ($climate_aux_heat_entity)",
        ]
    )
    def toggle_aux_heat(self, climate_aux_heat_entity):
        response = self._toggle_aux_heat(climate_aux_heat_entity)
        return f"Bascule de l'état de la chaleur auxiliaire de {response['attributes']['friendly_name']}"

    @intents.sentences(["éteindre la chaleur auxiliaire de ($climate_aux_heat_entity)"])
    def turn_aux_off(self, climate_aux_heat_entity):
        response = self._turn_aux_off(climate_aux_heat_entity)
        return f"Extinction de la chaleur auxiliaire de {response['attributes']['friendly_name']}"

    @intents.sentences(["allumer la chaleur auxiliaire de  ($climate_aux_heat_entity)"])
    def turn_aux_on(self, climate_aux_heat_entity):
        response = self._turn_aux_on(climate_aux_heat_entity)
        return f"Allumage de la chaleur auxiliaire de {response['attributes']['friendly_name']}"
