from enum import IntFlag, auto

from home_intent import Intents

intents = Intents(__name__)


class SupportedFeatures(IntFlag):
    SUPPORT_TARGET_TEMPERATURE = auto()
    SUPPORT_TARGET_TEMPERATURE_RANGE = auto()
    SUPPORT_TARGET_HUMIDITY = auto()
    SUPPORT_FAN_MODE = auto()
    SUPPORT_PRESET_MODE = auto()
    SUPPORT_SWING_MODE = auto()
    SUPPORT_AUX_HEAT = auto()


class BaseClimate:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("climate.")]
        self.climate_device_features = {
            x["entity_id"]: SupportedFeatures(x["attributes"].get("supported_features", 0))
            for x in self.entities
        }

    @intents.dictionary_slots
    def climate_target_temperature_entity(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_TARGET_TEMPERATURE
            in self.climate_device_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def climate_target_temperature_range_entity(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_TARGET_TEMPERATURE_RANGE
            in self.climate_device_features[x["entity_id"]]
        }
        return slots

    @intents.slots
    def climate_hvac_mode(self):
        hvac_modes = []

        for entity in self.entities:
            hvac_modes.extend(entity["attributes"]["hvac_modes"])

        return hvac_modes

    @intents.dictionary_slots
    def climate_target_humidity_entity(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_TARGET_HUMIDITY
            in self.climate_device_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def climate_preset_mode_entity(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_PRESET_MODE in self.climate_device_features[x["entity_id"]]
        }
        return slots

    @intents.slots
    def climate_preset_mode(self):
        preset_modes = []

        for entity in self.entities:
            if SupportedFeatures.SUPPORT_PRESET_MODE in SupportedFeatures(
                entity["attributes"].get("supported_features", 0)
            ):
                preset_modes.extend(entity["attributes"]["preset_modes"])

        return preset_modes

    @intents.dictionary_slots
    def climate_aux_heat_entity(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_AUX_HEAT in self.climate_device_features[x["entity_id"]]
        }
        return slots

    def _toggle(self, climate):
        response = self.ha.api.get_entity(climate)
        if response["state"] == "off":
            return self._turn_on(climate)
        else:
            return self._turn_off(climate)

    def _turn_off(self, climate):
        self.ha.api.call_service("climate", "turn_off", {"entity_id": climate})
        response = self.ha.api.get_entity(climate)
        return response

    def _turn_on(self, climate):
        self.ha.api.call_service("climate", "turn_on", {"entity_id": climate})
        response = self.ha.api.get_entity(climate)
        return response

    def _set_target_temperature(self, climate_target_temperature_entity, temperature: float):
        if (
            SupportedFeatures.SUPPORT_TARGET_TEMPERATURE
            in self.climate_device_features[climate_target_temperature_entity]
        ):
            self.ha.api.call_service(
                "climate",
                "set_temperature",
                {"entity_id": climate_target_temperature_entity, "temperature": temperature},
            )
        response = self.ha.api.get_entity(climate_target_temperature_entity)
        return response

    def _set_target_temperature_high(
        self, climate_target_temperature_range_entity, temperature: float
    ):
        if (
            SupportedFeatures.SUPPORT_TARGET_TEMPERATURE_RANGE
            in self.climate_device_features[climate_target_temperature_range_entity]
        ):
            self.ha.api.call_service(
                "climate",
                "set_temperature",
                {
                    "entity_id": climate_target_temperature_range_entity,
                    "target_temp_high": temperature,
                },
            )
        response = self.ha.api.get_entity(climate_target_temperature_range_entity)
        return response

    def _set_target_temperature_low(
        self, climate_target_temperature_range_entity, temperature: float
    ):
        if (
            SupportedFeatures.SUPPORT_TARGET_TEMPERATURE_RANGE
            in self.climate_device_features[climate_target_temperature_range_entity]
        ):
            self.ha.api.call_service(
                "climate",
                "set_temperature",
                {
                    "entity_id": climate_target_temperature_range_entity,
                    "target_temp_low": temperature,
                },
            )
        response = self.ha.api.get_entity(climate_target_temperature_range_entity)
        return response

    def _set_hvac_mode(self, climate, hvac_modes):
        self.ha.api.call_service(
            "climate", "set_temperature", {"entity_id": climate, "hvac_mode": hvac_modes}
        )
        response = self.ha.api.get_entity(climate)
        return response

    def _set_humidity(self, climate_target_humidity_entity, humidity: int):
        if (
            SupportedFeatures.SUPPORT_TARGET_HUMIDITY
            in self.climate_device_features[climate_target_humidity_entity]
        ):
            self.ha.api.call_service(
                "climate",
                "set_humidity",
                {"entity_id": climate_target_humidity_entity, "humidity": humidity},
            )
        response = self.ha.api.get_entity(climate_target_humidity_entity)
        return response

    def _set_preset_mode(self, climate_preset_mode_entity, climate_preset_mode):
        if (
            SupportedFeatures.SUPPORT_PRESET_MODE
            in self.climate_device_features[climate_preset_mode_entity]
        ):
            self.ha.api.call_service(
                "climate",
                "set_preset_mode",
                {"entity_id": climate_preset_mode_entity, "preset_mode": climate_preset_mode},
            )
        response = self.ha.api.get_entity(climate_preset_mode_entity)
        return response

    def _toggle_aux_heat(self, climate_aux_heat_entity):
        response = self.ha.api.get_entity(climate_aux_heat_entity)
        if response["attributes"]["aux_heat"] == "off":
            return self._turn_aux_on(climate_aux_heat_entity)
        else:
            return self._turn_off(climate_aux_heat_entity)

    def _turn_aux_off(self, climate_aux_heat_entity):
        self.ha.api.call_service(
            "climate", "set_aux_heat", {"entity_id": climate_aux_heat_entity, "aux_heat": False}
        )
        response = self.ha.api.get_entity(climate_aux_heat_entity)
        return response

    def _turn_aux_on(self, climate_aux_heat_entity):
        self.ha.api.call_service(
            "climate", "set_aux_heat", {"entity_id": climate_aux_heat_entity, "aux_heat": True}
        )
        response = self.ha.api.get_entity(climate_aux_heat_entity)
        return response
