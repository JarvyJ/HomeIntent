from .base_media_player import BaseMediaPlayer, intents


class MediaPlayer(BaseMediaPlayer):
    @intents.dictionary_slots
    def media_player_volume_level(self):
        slots = {
            "100": "1.00",
            "95": "0.95",
            "90": "0.90",
            "85": "0.85",
            "80": "0.80",
            "75": "0.75",
            "70": "0.70",
            "65": "0.65",
            "60": "0.60",
            "55": "0.55",
            "50": "0.50",
            "45": "0.45",
            "40": "0.40",
            "35": "0.35",
            "30": "0.30",
            "25": "0.25",
            "20": "0.20",
            "15": "0.15",
            "10": "0.10",
            "05": "0.05",
            "00": "0.00",
        }
        return slots

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

    @intents.sentences(["turn down the volume of [the] ($media_player)"])
    def volume_down(self, media_player):
        response = self._volume_down(media_player)
        return f"Turning down the volume of {response['attributes']['friendly_name']}"

    @intents.sentences(["turn up the volume of [the] ($media_player)"])
    def volume_up(self, media_player):
        response = self._volume_up(media_player)
        return f"Turning up the volume of {response['attributes']['friendly_name']}"

    @intents.sentences(["mute the volume of [the] ($media_player)"])
    def volume_mute(self, media_player):
        response = self._volume_mute(media_player)
        return f"Muting the volume of {response['attributes']['friendly_name']}"

    @intents.sentences(["set the volume of [the] ($media_player) to ($media_player_volume_level)"])
    def volume_set(self, media_player, media_player_volume_level):
        response = self._volume_set(media_player, media_player_volume_level)
        return f"Setting the volume level of {response['attributes']['friendly_name']} to {media_player_volume_level}"

    @intents.sentences(["Play on [the] ($media_player)"])
    def media_play(self, media_player):
        response = self._media_play(media_player)
        return f"Playback paused on {response['attributes']['friendly_name']}"

    @intents.sentences(["Pause on [the] ($media_player)"])
    def media_pause(self, media_player):
        response = self._media_pause(media_player)
        return f"Playback resumed on {response['attributes']['friendly_name']}"

    @intents.sentences(["Play next track on [the] ($media_player)"])
    def media_next_track(self, media_player):
        response = self._media_next_track(media_player)
        return f"Playing next track on {response['attributes']['friendly_name']}"

    @intents.sentences(["Play previous track on [the] ($media_player)"])
    def media_previous_track(self, media_player):
        response = self._media_previous_track(media_player)
        return f"Playing previous track on {response['attributes']['friendly_name']}"
