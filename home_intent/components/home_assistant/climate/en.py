from .base_climate import BaseClimate, intents


class Climate(BaseClimate):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_fan)

    @intents.sentences(["toggle the ($climate)", "turn (on | off) [the] ($climate)"])
    def toggle_climate(self, climate):
        response = self._toggle_climate(climate)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($climate)"])
    def turn_off(self, climate):
        response = self._turn_off(climate)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($climate)"])
    def turn_on(self, climate):
        response = self._turn_on(climate)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"

    @intents.sentences(["(set | change | make) the ($climate) to ($climate_hvac_mode)"])
    def set_hvac_mode(self, climate, climate_hvac_mode):
        response = self._set_hvac_mode(climate, climate_hvac_mode)
        return f"Settings the {response['attributes']['friendly_name']} to {response['state']}"

    @intents.sentences(
        [
            "(set | change | make) the ($climate_target_temperature_entity) [(temperature|temp)] to (0..250){temperature} [degrees] [(farenheit|celsius)]"
        ]
    )
    def set_target_temperature(self, climate_target_temperature_entity, temperature):
        response = self._set_target_temperature(climate_target_temperature_entity, temperature)
        return f"Setting the {response['attributes']['friendly_name']} to {temperature}%"

    @intents.sentences(
        [
            "(set | change | make) the ($climate_target_temperature_range_entity) low [(temperature|temp)] to (0..250){temperature} [degrees] [(farenheit|celsius)]"
        ]
    )
    def set_target_temperature_low(self, climate_target_temperature_range_entity, temperature):
        response = self._set_target_temperature_low(
            climate_target_temperature_range_entity, temperature
        )
        return f"Setting the {response['attributes']['friendly_name']} to {temperature}%"

    @intents.sentences(
        [
            "(set | change | make) the ($climate_target_temperature_range_entity) high [(temperature|temp)] to (0..250){temperature} [degrees] [(farenheit|celsius)]"
        ]
    )
    def _set_target_temperature_high(self, climate_target_temperature_range_entity, temperature):
        response = self._set_target_temperature_high(
            climate_target_temperature_range_entity, temperature
        )
        return f"Setting the {response['attributes']['friendly_name']} to {temperature}%"

    @intents.sentences(
        [
            "(set | change | make) the ($climate_target_humidity_entity) to (30..99){humidity} [percent] humidity"
        ]
    )
    def set_humidity(self, climate_target_humidity_entity, humidity):
        response = self._set_humidity(climate_target_humidity_entity, humidity)
        return f"Setting the {response['attributes']['friendly_name']} to {humidity}% humidity"

    @intents.sentences(
        ["(set | change | make) the ($climate_preset_mode_entity) to ($climate_preset_mode)"]
    )
    def set_preset_mode(self, climate_preset_mode_entity, climate_preset_mode):
        response = self._set_preset_mode(climate_preset_mode_entity, climate_preset_mode)
        return f"Settings the {response['attributes']['friendly_name']} to {response['attributes']['preset_mode']}"

    @intents.sentences(
        [
            "toggle the ($climate_aux_heat_entity) (aux|auxiliary) heat",
            "turn (on | off) [the] ($climate_aux_heat_entity) (aux|auxiliary) heat",
        ]
    )
    def toggle_aux_heat(self, climate_aux_heat_entity):
        response = self._toggle_aux_heat(climate_aux_heat_entity)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} auxiliary heat"

    @intents.sentences(["turn off [the] ($climate_aux_heat_entity) (aux|auxiliary) heat"])
    def turn_aux_off(self, climate_aux_heat_entity):
        response = self._turn_aux_off(climate_aux_heat_entity)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} auxiliary heat"

    @intents.sentences(["turn on [the] ($climate_aux_heat_entity) (aux|auxiliary) heat"])
    def turn_aux_on(self, climate_aux_heat_entity):
        response = self._turn_aux_on(climate_aux_heat_entity)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} auxiliary heat"
