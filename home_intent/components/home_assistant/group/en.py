from .base_group import intents, BaseGroup


class Group(BaseGroup):
    @intents.sentences(["toggle [the] ($group)"])
    def toggle_group(self, group):
        response = self._toggle_group(group)
        return f"Toggling the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn on [the] ($group)"])
    def turn_on_group(self, group):
        response = self._turn_on_group(group)
        return f"Turning on the {response['attributes']['friendly_name']}"

    @intents.sentences(["turn off [the] ($group)"])
    def turn_off_group(self, group):
        response = self._turn_off_group(group)
        return f"Turning off the {response['attributes']['friendly_name']}"
