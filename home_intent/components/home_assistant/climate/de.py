from .base_climate import BaseClimate, intents


class Climate(BaseClimate):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_fan)

    @intents.sentences(["Schalte die ($climate)", "Schalte  [die] ($climate) (an | aus)"])
    def toggle_climate(self, climate):
        response = self._toggle_climate(climate)
        return f"Schalte die {response['attributes']['friendly_name']} {response['state']}"

    @intents.sentences(["Schalte [die] ($climate) aus"])
    def turn_off(self, climate):
        response = self._turn_off(climate)
        return f"Schalte die {response['attributes']['friendly_name']} {response['state']}"

    @intents.sentences(["Schalte [die] ($climate) an"])
    def turn_on(self, climate):
        response = self._turn_on(climate)
        return f"Schalte die {response['attributes']['friendly_name']} {response['state']}"

    @intents.sentences(["(Stelle | ändere) die ($climate) auf ($climate_hvac_mode)"])
    def set_hvac_mode(self, climate, climate_hvac_mode):
        response = self._set_hvac_mode(climate, climate_hvac_mode)
        return f"Stelle die {response['attributes']['friendly_name']} auf {response['state']}"

    @intents.sentences(
        [
            "(Stelle | ändere) die ($climate_target_temperature_entity) [Temperatur] auf (0..30){temperature} grad [celsius]"
        ]
    )
    def set_target_temperature(self, climate_target_temperature_entity, temperature):
        response = self._set_target_temperature(climate_target_temperature_entity, temperature)
        return f"Stelle {response['attributes']['friendly_name']} auf {temperature} grad"

    @intents.sentences(
        [
            "(Stelle | ändere) die (untere | niedrige) Temperatur der ($climate_target_temperature_range_entity) auf (0..30){temperature} grad [celsius]"
        ]
    )
    def set_target_temperature_low(self, climate_target_temperature_range_entity, temperature):
        response = self._set_target_temperature_low(
            climate_target_temperature_range_entity, temperature
        )
        return f"Unterer Wert für {response['attributes']['friendly_name']} beträgt jetzt {temperature} grad"

    @intents.sentences(
        [
            "(Stelle | ändere) die (obere | hohe) Temperatur der ($climate_target_temperature_range_entity) auf (0..30){temperature} grad [celsius]"
        ]
    )
    def set_target_temperature_high(self, climate_target_temperature_range_entity, temperature):
        response = self._set_target_temperature_high(
            climate_target_temperature_range_entity, temperature
        )
        return f"Oberer Wert für {response['attributes']['friendly_name']} beträgt jetzt {temperature} grad"

    @intents.sentences(
        [
            "(Stelle | ändere) die ($climate_target_humidity_entity) auf (30..99){humidity} Prozent (Luftfeuchte | Luftfeuchtigkeit)"
        ]
    )
    def set_humidity(self, climate_target_humidity_entity, humidity):
        response = self._set_humidity(climate_target_humidity_entity, humidity)
        return f"Stelle {response['attributes']['friendly_name']} auf {humidity}% Luftfeuchte"

    @intents.sentences(
        ["(Stelle | ändere) die ($climate_preset_mode_entity) auf ($climate_preset_mode)"]
    )
    def set_preset_mode(self, climate_preset_mode_entity, climate_preset_mode):
        response = self._set_preset_mode(climate_preset_mode_entity, climate_preset_mode)
        return f"Stelle {response['attributes']['friendly_name']} auf {response['attributes']['preset_mode']}"

    @intents.sentences(
        [
            "(Stelle | ändere) die ($climate_aux_heat_entity) auf Heizen",
            "Mach die die ($climate_aux_heat_entity) Heizung (an | aus)",
        ]
    )
    def toggle_aux_heat(self, climate_aux_heat_entity):
        response = self._toggle_aux_heat(climate_aux_heat_entity)
        return f"Stelle {response['attributes']['friendly_name']} Heizung {response['state']}"

    @intents.sentences(["(Schalte | Mache) die ($climate_aux_heat_entity) heizung aus"])
    def turn_aux_off(self, climate_aux_heat_entity):
        response = self._turn_aux_off(climate_aux_heat_entity)
        return f"Stelle {response['attributes']['friendly_name']} Heizung {response['state']}"

    @intents.sentences(["(Schalte | Mache) die ($climate_aux_heat_entity) Heizung an"])
    def turn_aux_on(self, climate_aux_heat_entity):
        response = self._turn_aux_on(climate_aux_heat_entity)
        return f"Stelle {response['attributes']['friendly_name']} Heizung {response['state']}"
