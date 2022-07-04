from .base_media_player import BaseMediaPlayer, intents
class MediaPlayer(BaseMediaPlayer):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_media_player)
    @intents.sentences(["toggle the ($media_player)", "turn (on | off) [the] ($media_player)"])
    def toggle_media_player(self, media_player):
        response = self._toggle_media_player(media_player)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"
    @intents.sentences(["turn off [the] ($media_player)"])
    def turn_off(self, media_player):
        response = self._turn_off(media_player)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"
    @intents.sentences(["turn on [the] ($media_player)"])
    def turn_on(self, media_player):
        response = self._turn_on(media_player)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']}"
    @intents.sentences(["turn down the volume of ($media_player)"])
    def volume_down(self, media_player):
        response = self._volume_down(media_player)
        return f"Turning down the volume of {response['attributes']['friendly_name']}"
    @intents.sentences(["turn up the volume of ($media_player)"])
    def volume_up(self, media_player):
        response = self._volume_up(media_player)
#        return f"Turning up the volume of {response['attributes']['friendly_name']}"
        return f"Yes master nicolas"
    @intents.sentences(["mute the volume of ($media_player)"])
    def volume_mute(self, media_player):
        response = self._volume_mute(media_player)
        return f"Muting the volume of {response['attributes']['friendly_name']}"
#    @intents.sentences(["set the volume of ($media_player) to ($volume_level)"])
#    def volume_set(self, media_player):
#        response = self._volume_set(media_player)
#        return f"Setting the volume of {response['attributes']['friendly_name']} xto {response['attributes']['volu>
    @intents.sentences(["Play on ($media_player)"])
    def media_play(self, media_player):
        response = self._media_play(media_player)
        return f"Playback paused on {response['attributes']['friendly_name']}"
    @intents.sentences(["Pause on ($media_player)"])
    def media_pause(self, media_player):
        response = self._media_pause(media_player)
        return f"Playback resumed on {response['attributes']['friendly_name']}"
    @intents.sentences(["Play next track on ($media_player)"])
    def media_next_track(self, media_player):
        response = self._media_next_track(media_player)
        return f"Playing next track on {response['attributes']['friendly_name']}"
    @intents.sentences(["Play previous track on ($media_player)"])
    def media_previous_track(self, media_player):
        response = self._media_previous_track(media_player)
        return f"Playing previous track on {response['attributes']['friendly_name']}"
