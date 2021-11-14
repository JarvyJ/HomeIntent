from enum import IntFlag, auto

from home_intent import Intents

intents = Intents(__name__)


class SupportedFeatures(IntFlag):
    SUPPORT_OPEN = auto()


class BaseLock:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("lock.")]

    @intents.dictionary_slots
    def lock(self):
        slots = {f"{x['attributes'].get('friendly_name')}": x["entity_id"] for x in self.entities}
        return slots

    @intents.dictionary_slots
    def openable_lock(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_OPEN
            in SupportedFeatures(x["attributes"].get("supported_features", 0))
        }
        return slots

    def _lock_the_lock(self, lock):
        self.ha.api.call_service("lock", "lock", {"entity_id": lock})
        response = self.ha.api.get_entity(lock)
        return response

    def _unlock_the_lock(self, lock):
        self.ha.api.call_service("lock", "unlock", {"entity_id": lock})
        response = self.ha.api.get_entity(lock)
        return response

    def _open_the_lock(self, openable_lock):
        self.ha.api.call_service("lock", "open", {"entity_id": openable_lock})
        response = self.ha.api.get_entity(openable_lock)
        return response
