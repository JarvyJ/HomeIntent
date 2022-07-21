from .base_cover import BaseCover, intents


class Cover(BaseCover):
    @intents.dictionary_slots
    def cover_positions(self):
        slots = {"moitié": 50}
        return slots

    @intents.sentences(["ouvrir [le | la] ($cover_open_entity)"])
    def open_cover(self, cover_open_entity):
        response = self._open_cover(cover_open_entity)
        return f"Ouverture de {response['attributes']['friendly_name']}"

    @intents.sentences(["fermer [le | la] ($cover_close_entity)"])
    def close_cover(self, cover_close_entity):
        response = self._close_cover(cover_close_entity)
        return f"Fermeture de {response['attributes']['friendly_name']}"

    @intents.sentences(["arrêter [le | la] ($cover_stop_entity)"])
    def stop_cover(self, cover_stop_entity):
        response = self._stop_cover(cover_stop_entity)
        return f"Arrêt de {response['attributes']['friendly_name']}"

    @intents.sentences(["ouvrir [le | la] ($cover_open_tilt_entity)"])
    def open_cover_tilt(self, cover_open_tilt_entity):
        response = self._open_cover_tilt(cover_open_tilt_entity)
        return f"Ouverture de {response['attributes']['friendly_name']}"

    @intents.sentences(["fermer [le | la] ($cover_close_tilt_entity)"])
    def close_cover_tilt(self, cover_close_tilt_entity):
        response = self._close_cover_tilt(cover_close_tilt_entity)
        return f"fermeture de {response['attributes']['friendly_name']}"

    @intents.sentences(
        [
            "(régler|changer|ajuster) [la] [position] [du|de] ($cover_set_position_entity) [à] ($cover_positions:!int) [pour] [cent]",
            "(ouvrir|fermer) [le|la] ($cover_set_position_entity) [à] ($cover_positions:!int) [percent]",
        ]
    )
    def set_cover_position(self, cover_set_position_entity, cover_positions):
        response = self._set_cover_position(cover_set_position_entity, cover_positions)
        return f"Réglage de {response['attributes']['friendly_name']} à {cover_positions}%"

    @intents.sentences(
        [
            "(régler|changer|ajuster) [la] [position] [du|de] ($cover_set_tilt_position_entity) [à] ($cover_positions:!int) [pour] [cent]",
            "(ouvrir|fermer) [le] ($cover_set_tilt_position_entity) [à] ($cover_positions:!int)  [pour] [cent]",
        ]
    )
    def set_cover_tilt_position(self, cover_set_tilt_position_entity, cover_positions):
        response = self._set_cover_tilt_position(cover_set_tilt_position_entity, cover_positions)
        return f"Réglage de {response['attributes']['friendly_name']} à {cover_positions}%"
