from .base_lock import BaseLock, intents


class Lock(BaseLock):
    @intents.sentences(["Verriegel [der|die|das] ($lock)", "Schließe [der|die|das] ($lock) ab"])
    def lock_the_lock(self, lock):
        response = self._lock_the_lock(lock)
        return f"Verriegele {response['attributes']['friendly_name']}"

    @intents.sentences(["Entriegel [der|die|das] ($lock)", "Schließe [der|die|das] ($lock) auf"])
    def unlock_the_lock(self, lock):
        response = self._unlock_the_lock(lock)
        return f"Entriegele {response['attributes']['friendly_name']}"

    @intents.sentences(["Öffne [der|die|das] ($lock_open_entity)"])
    def open_the_lock(self, lock_open_entity):
        response = self._open_the_lock(lock_open_entity)
        return f"Schließe {response['attributes']['friendly_name']} ab"
