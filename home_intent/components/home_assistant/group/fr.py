from .base_group import BaseGroup, intents


class Group(BaseGroup):
    @intents.sentences(["Basculer l'état de ($group)"])
    def toggle_group(self, group):
        response = self._toggle_group(group)
        return f"Basculer l'état de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["Activer [le | la] ($group)"])
    def turn_on_group(self, group):
        response = self._turn_on_group(group)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"

    @intents.sentences(["Désactiver [le | la] ($group)"])
    def turn_off_group(self, group):
        response = self._turn_off_group(group)
        return f"Réglage de {response['attributes']['friendly_name']} à {response['state']}"
