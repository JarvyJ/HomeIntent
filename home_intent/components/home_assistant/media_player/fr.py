from .base_media_player import BaseMediaPlayer, intents
class MediaPlayer(BaseMediaPlayer):
    @intents.dictionary_slots
    def volume_level(self):
        slots = {"100": 1,00}, {"95": 0,95},  {"90": 0,90}, {"85": 0,85}, {"80": 0,80}, {"75": 0,75}, {"70": 0,70}, {"65": 0,65}, {"60": 0,60}, {"55": 0,55}, {"50": 0,50}, {"45": 0,45},  {"40": 0,40}, {"35": 0,35}, {"30": 0,30}, {"25": 0,25}, {"20": 0,20}, {"15": 0,15}, {"10": 0,10}, {"5": 0,05}, {"0": 0,00}
        return slots
    @intents.sentences(["basculer l'alimentation [de] ($media_player)", "turn (on | off) [the] ($media_player)"])
    def toggle_media_player(self, media_player):
        response = self._toggle_media_player(media_player)
        return f"Bascule de {response['attributes']['friendly_name']} à {response['state']}"
    @intents.sentences(["éteindre [le] [la] ($media_player)"])
    def turn_off(self, media_player):
        response = self._turn_off(media_player)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"
    @intents.sentences(["allumer [le] [la]($media_player)"])
    def turn_on(self, media_player):
        response = self._turn_on(media_player)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"
    @intents.sentences(["baisser le volume [de] ($media_player)"])
    def volume_down(self, media_player):
        response = self._volume_down(media_player)
        return f"Baisser le volume de {response['attributes']['friendly_name']}"
    @intents.sentences(["monter le volume [de] ($media_player)"])
    def volume_up(self, media_player):
        response = self._volume_up(media_player)
        return f"Monter le volume de {response['attributes']['friendly_name']}"
    @intents.sentences(["muter le volume [de] ($media_player)"])
    def volume_mute(self, media_player):
        response = self._volume_mute(media_player)
        return f"Muter le volume de {response['attributes']['friendly_name']}"
    @intents.sentences(["régler le volume de ($media_player) à ($volume_level)"])
    def volume_set(self, media_player, volume_level):
        response = self._volume_set(media_player, volume_level)
        return f"Régler le volume de {response['attributes']['friendly_name']} à  {volume_level}"
    @intents.sentences(["Lire [sur] ($media_player)"])
    def media_play(self, media_player):
        response = self._media_play(media_player)
        return f"Lire sur {response['attributes']['friendly_name']}"
    @intents.sentences(["Mettre en pause ($media_player)"])
    def media_pause(self, media_player):
        response = self._media_pause(media_player)
        return f"Mettre en pause {response['attributes']['friendly_name']}"
    @intents.sentences(["Mettre la piste suivante sur ($media_player)"])
    def media_next_track(self, media_player):
        response = self._media_next_track(media_player)
        return f"Mettre la piste suivante sur {response['attributes']['friendly_name']}"
    @intents.sentences(["Mettre la piste précédente sur ($media_player)"])
    def media_previous_track(self, media_player):
        response = self._media_previous_track(media_player)
        return f"Mettre la piste précédente sur {response['attributes']['friendly_name']}"
