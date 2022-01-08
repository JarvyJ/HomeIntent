from typing import Dict

from pydantic import BaseModel, conint
from pydantic.color import Color
import yaml

from home_intent import Intents

intents = Intents(__name__)


class ColorTemperatures(BaseModel):
    color_temperature: Dict[str, conint(multiple_of=100, ge=2000, le=6500)]


class ColorNames(BaseModel):
    color_names: Dict[str, Color]


class BaseLight:
    def __init__(self, home_assistant, home_intent):
        self.ha = home_assistant
        self.home_intent = home_intent
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("light.")]
        self.color_value_to_name = {}
        self.color_temp_to_name = {}

    @intents.dictionary_slots
    def light(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if x["state"] in ("on", "off")
        }
        return slots

    @intents.dictionary_slots
    def light_color(self):
        color_file = self.home_intent.get_file("home_assistant/color_names.yaml")
        raw_colors = yaml.load(color_file.read_text(), Loader=yaml.SafeLoader)
        color_names = ColorNames(**raw_colors).color_names
        self.color_value_to_name = {str(v): k for k, v in color_names.items()}
        return color_names

    @intents.dictionary_slots
    def light_color_temperature(self):
        color_temperature_file = self.home_intent.get_file("home_assistant/color_temperature.yaml")
        color_temperature_dict = yaml.load(
            color_temperature_file.read_text(), Loader=yaml.SafeLoader
        )
        color_temperatures = ColorTemperatures(**color_temperature_dict).color_temperature
        self.color_temp_to_name = {v: k for k, v in color_temperatures.items()}
        return color_temperatures

    def _toggle_light(self, light):
        response = self.ha.api.call_service("light", "toggle", {"entity_id": light})
        response = self.ha.api.get_entity(light, response)
        return response

    def _turn_on(self, light):
        response = self.ha.api.call_service("light", "turn_on", {"entity_id": light})
        response = self.ha.api.get_entity(light, response)
        return response

    def _turn_off(self, light):
        response = self.ha.api.call_service("light", "turn_off", {"entity_id": light})
        response = self.ha.api.get_entity(light, response)
        return response

    def _change_color(self, light, color):
        response = self.ha.api.call_service(
            "light", "turn_on", {"entity_id": light, "rgb_color": color_to_hex(color)}
        )
        response = self.ha.api.get_entity(light, response)
        color_name = self.color_value_to_name[color]
        return response, color_name

    def _change_color_brightness(self, light, color, brightness):
        response = self.ha.api.call_service(
            "light",
            "turn_on",
            {"entity_id": light, "rgb_color": color_to_hex(color), "brightness_pct": brightness},
        )
        response = self.ha.api.get_entity(light, response)
        color_name = self.color_value_to_name[color]
        return response, color_name

    def _change_brightness(self, light, brightness):
        response = self.ha.api.call_service(
            "light", "turn_on", {"entity_id": light, "brightness_pct": brightness}
        )
        response = self.ha.api.get_entity(light, response)
        return response

    def _change_color_temperature(self, light, color_temperature):
        response = self.ha.api.call_service(
            "light", "turn_on", {"entity_id": light, "kelvin": color_temperature}
        )
        response = self.ha.api.get_entity(light, response)
        color_name = self.color_temp_to_name[int(color_temperature)]
        return response, color_name

    def _change_color_temperature_brightness(self, light, color_temperature, brightness):
        response = self.ha.api.call_service(
            "light",
            "turn_on",
            {"entity_id": light, "kelvin": color_temperature, "brightness_pct": brightness},
        )
        response = self.ha.api.get_entity(light, response)
        color_name = self.color_temp_to_name[int(color_temperature)]
        return response, color_name


def color_to_hex(color: str):
    return Color(color).as_rgb_tuple()
