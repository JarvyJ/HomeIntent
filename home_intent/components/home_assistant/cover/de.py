from .base_cover import BaseCover, intents


class Cover(BaseCover):
    @intents.dictionary_slots
    def cover_positions(self):
        slots = {"half way": 50}
        return slots

    @intents.sentences(["Öffne (das | den | die) ($cover_open_entity)",
                        "Mache (das | den | die) ($cover_open_entity) auf"])
    def open_cover(self, cover_open_entity):
        response = self._open_cover(cover_open_entity)
        return f"Öffne {response['attributes']['friendly_name']}"

    @intents.sentences(["Schließe (das | den | die) ($cover_close_entity)",
                        "Mache (das | den | die) ($cover_close_entity) zu"])
    def close_cover(self, cover_close_entity):
        response = self._close_cover(cover_close_entity)
        return f"Schließe {response['attributes']['friendly_name']}"

    @intents.sentences(["Stoppe [(das | den | die)] ($cover_stop_entity)"])
    def stop_cover(self, cover_stop_entity):
        response = self._stop_cover(cover_stop_entity)
        return f"Stoppe {response['attributes']['friendly_name']}"

    @intents.sentences(["(Drehe | Kippe) (das | den | die) ($cover_open_tilt_entity) zu",
                        "(Mache | Stelle) das ($cover_open_tilt_entity) auf Kipp"])
    def open_cover_tilt(self, cover_open_tilt_entity):
        response = self._open_cover_tilt(cover_open_tilt_entity)
        return f"Drehe {response['attributes']['friendly_name']} auf"

    @intents.sentences(["(Drehe | Kippe) (das | den | die) ($cover_close_tilt_entity) zu",
                        "(Mache | Stelle) das ($cover_open_tilt_entity) zu"])
    def close_cover_tilt(self, cover_close_tilt_entity):
        response = self._close_cover_tilt(cover_close_tilt_entity)
        return f"Drehe {response['attributes']['friendly_name']} zu"

    @intents.sentences(
        [
            "(Öffne | Schließe) (das | den | die) ($cover_set_position_entity) zu ($cover_positions:!int) Prozent",
        ]
    )
    def set_cover_position(self, cover_set_position_entity, cover_positions):
        response = self._set_cover_position(cover_set_position_entity, cover_positions)
        return f"Stelle {response['attributes']['friendly_name']} auf {cover_positions}%"

    @intents.sentences(
        [           
            "(Drehe | Kippe) (das | den | die) ($cover_set_tilt_position_entity) auf ($cover_positions:!int) Prozent"
        ]
    )
    def set_cover_tilt_position(self, cover_set_tilt_position_entity, cover_positions):
        response = self._set_cover_tilt_position(cover_set_tilt_position_entity, cover_positions)
        return f"Drehe {response['attributes']['friendly_name']} auf {cover_positions}%"
