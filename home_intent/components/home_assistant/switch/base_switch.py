from home_intent import Intents

intents = Intents(__name__)


class BaseSwitch:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("switch.")]

    @intents.dictionary_slots
    def switch(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if x["state"] in ("on", "off")
        }
        return slots

    def _toggle_switch(self, switch):
        response = self.ha.api.call_service("switch", "toggle", {"entity_id": switch})
        response = self.ha.api.get_entity(switch, response)
        return response

    def _turn_off(self, switch):
        response = self.ha.api.call_service("switch", "turn_off", {"entity_id": switch})
        response = self.ha.api.get_entity(switch, response)
        return response

    def _turn_on(self, switch):
        response = self.ha.api.call_service("switch", "turn_on", {"entity_id": switch})
        response = self.ha.api.get_entity(switch, response)
        return response
