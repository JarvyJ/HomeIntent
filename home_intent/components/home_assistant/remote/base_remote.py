from home_intent import Intents

intents = Intents(__name__)


class BaseRemote:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("remote.")]

    @intents.dictionary_slots
    def remote(self):
        slots = {f"{x['attributes'].get('friendly_name')}": x["entity_id"] for x in self.entities}
        return slots

    def _toggle_remote(self, remote):
        response = self.ha.api.call_service("remote", "toggle", {"entity_id": remote})
        response = self.ha.api.get_entity(remote, response)
        return response

    def _turn_off(self, remote):
        response = self.ha.api.call_service("remote", "turn_off", {"entity_id": remote})
        response = self.ha.api.get_entity(remote, response)
        return response

    def _turn_on(self, remote):
        response = self.ha.api.call_service("remote", "turn_on", {"entity_id": remote})
        response = self.ha.api.get_entity(remote, response)
        return response
