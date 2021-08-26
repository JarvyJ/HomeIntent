from home_intent import Intents
from enum import IntFlag, auto

intents = Intents(__name__)


class SupportedFeatures(IntFlag):
    SUPPORT_OPEN = auto()
    SUPPORT_CLOSE = auto()
    SUPPORT_SET_POSITION = auto()
    SUPPORT_STOP = auto()
    SUPPORT_OPEN_TILT = auto()
    SUPPORT_CLOSE_TILT = auto()
    SUPPORT_SET_TILT_POSITION = auto()
    SUPPORT_STOP_TILT = auto()


class Cover:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("cover.")]
        self.cover_feautres = {
            x: SupportedFeatures(x["attributes"].get("supported_features", 0))
            for x in self.entities
        }

    @intents.dictionary_slots
    def cover_open(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_OPEN in self.cover_feautres[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_close(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_CLOSE in self.cover_feautres[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_set_position(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_SET_POSITION in self.cover_feautres[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_stop(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_STOP in self.cover_feautres[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_open_tilt(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_OPEN_TILT in self.cover_feautres[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_close_tilt(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_CLOSE_TILT in self.cover_feautres[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_set_tilt_position(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_SET_TILT_POSITION in self.cover_feautres[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_stop_tilt(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_STOP_TILT in self.cover_feautres[x["entity_id"]]
        }
        return slots

    @intents.sentences(["lock [the] ($lock) [lock]"])
    def lock_the_lock(self, lock):
        self.ha.api.call_service("homeassistant", "lock", {"entity_id": lock})
        response = self.ha.api.get_entity(lock)
        return f"Locking the {response['attributes']['friendly_name']} lock"

    @intents.sentences(["unlock [the] ($lock) [lock]"])
    def unlock_the_lock(self, lock):
        self.ha.api.call_service("homeassistant", "unlock", {"entity_id": lock})
        response = self.ha.api.get_entity(lock)
        return f"Unlocking on the {response['attributes']['friendly_name']} lock"

    @intents.sentences(["open [the] ($openable_lock) [lock]"])
    def open_the_lock(self, openable_lock):
        self.ha.api.call_service("homeassistant", "open", {"entity_id": openable_lock})
        response = self.ha.api.get_entity(openable_lock)
        return f"Turning off the {response['attributes']['friendly_name']} lock"
