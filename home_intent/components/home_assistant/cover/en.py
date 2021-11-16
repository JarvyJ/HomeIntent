from .base_cover import BaseCover, intents


class Cover(BaseCover):
    @intents.dictionary_slots
    def cover_positions(self):
        slots = {"half way": 50}
        return slots

    @intents.sentences(["open [the] ($cover_open)"])
    def open_cover(self, cover_open):
        response = self._open_cover(cover_open)
        return f"Opening the {response['attributes']['friendly_name']}"

    @intents.sentences(["close [the] ($cover_close)"])
    def close_cover(self, cover_close):
        response = self._close_cover(cover_close)
        return f"Closing the {response['attributes']['friendly_name']}"

    @intents.sentences(["stop [the] ($cover_stop)"])
    def stop_cover(self, cover_stop):
        response = self._stop_cover(cover_stop)
        return f"Stopping the {response['attributes']['friendly_name']}"

    @intents.sentences(["tilt open [the] ($cover_open_tilt)"])
    def open_cover_tilt(self, cover_open_tilt):
        response = self._open_cover_tilt(cover_open_tilt)
        return f"Opening the {response['attributes']['friendly_name']}"

    @intents.sentences(["tilt close [the] ($cover_close_tilt)"])
    def close_cover_tilt(self, cover_close_tilt):
        response = self._close_cover_tilt(cover_close_tilt)
        return f"Closing the {response['attributes']['friendly_name']}"

    @intents.sentences(
        [
            "(set|change|make) [the] ($cover_set_position) [position] [to] ($cover_positions:!int) [percent]",
            "(open|close) [the] ($cover_set_position) [to] ($cover_positions:!int) [percent]",
        ]
    )
    def set_cover_position(self, cover_set_position, cover_positions):
        response = self._set_cover_position(cover_set_position, cover_positions)
        return f"Setting the {response['attributes']['friendly_name']} to {cover_positions}%"

    @intents.sentences(
        [
            "(set|change|make) [the] ($cover_set_tilt_position) tilt [position] [to] ($cover_positions:!int) [percent]",
            "tilt (open|close) [the] ($cover_set_tilt_position) [to] ($cover_positions:!int) [percent]",
        ]
    )
    def set_cover_tilt_position(self, cover_set_tilt_position, cover_positions):
        response = self._set_cover_tilt_position(cover_set_tilt_position, cover_positions)
        return f"Setting the {response['attributes']['friendly_name']} to {cover_positions}%"
