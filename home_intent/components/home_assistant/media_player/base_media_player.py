from home_intent import Intents
intents = Intents(__name__)
class BaseMediaPlayer:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("media_player.")]
    @intents.dictionary_slots
    def media_player(self):
        slots = {f"{x['attributes'].get('friendly_name')}": x["entity_id"] for x in self.entities}
        return slots
    def _toggle_media_player(self, media_player):
        response = self.ha.api.call_service("media_player", "toggle", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _turn_off(self, media_player):
        response = self.ha.api.call_service("media_player", "turn_off", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _turn_on(self, media_player):
        response = self.ha.api.call_service("media_player", "turn_on", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _volume_up(self, media_player):
        response = self.ha.api.call_service("media_player", "volume_up", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _volume_down(self, media_player):
        response = self.ha.api.call_service("media_player", "volume_down", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _volume_mute(self, media_player):
        response = self.ha.api.call_service("media_player", "volume_mute", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _volume_set(self, media_player, volume_level):
        response = self.ha.api.call_service("media_player", "volume_set", {"entity_id": media_player}, {"volume_level": volume_level})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _media_play(self, media_player):
        response = self.ha.api.call_service("media_player", "media_play", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _media_pause(self, media_player):
        response = self.ha.api.call_service("media_player", "media_pause", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _media_next_track(self, media_player):
        response = self.ha.api.call_service("media_player", "media_next_track", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
    def _media_previous_track(self, media_player):
        response = self.ha.api.call_service("media_player", "media_previous_track", {"entity_id": media_player})
        response = self.ha.api.get_entity(media_player, response)
        return response
