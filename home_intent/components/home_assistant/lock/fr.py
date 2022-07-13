from .base_lock import BaseLock, intents


class Lock(BaseLock):
    @intents.sentences(["Vérouiller [le | la] [serrure | vérrou | porte] ($lock)"])
    def lock_the_lock(self, lock):
        response = self._lock_the_lock(lock)
        return f"Vérouillage de {response['attributes']['friendly_name']}"

    @intents.sentences(["Dévérouiller [le | la] [serrure | vérrou | porte] ($lock)"])
    def unlock_the_lock(self, lock):
        response = self._unlock_the_lock(lock)
        return f"Dévérouillage de {response['attributes']['friendly_name']}"

    @intents.sentences(["Ouvrir [la | la] [serrure | vérrou | porte] ($lock_open_entity)"])
    def open_the_lock(self, lock_open_entity):
        response = self._open_the_lock(lock_open_entity)
        return f"Ouverture de {response['attributes']['friendly_name']}"
