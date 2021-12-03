from .base_lock import BaseLock, intents


class Lock(BaseLock):
    @intents.sentences(["lock [the] ($lock) [lock]"])
    def lock_the_lock(self, lock):
        response = self._lock_the_lock(lock)
        return f"Locking the {response['attributes']['friendly_name']}"

    @intents.sentences(["unlock [the] ($lock) [lock]"])
    def unlock_the_lock(self, lock):
        response = self._unlock_the_lock(lock)
        return f"Unlocking the {response['attributes']['friendly_name']}"

    @intents.sentences(["open [the] ($lock_open_entity) [lock]"])
    def open_the_lock(self, lock_open_entity):
        response = self._open_the_lock(lock_open_entity)
        return f"Turning off the {response['attributes']['friendly_name']}"
