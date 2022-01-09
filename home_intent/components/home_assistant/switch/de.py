from .base_switch import BaseSwitch, intents


class Switch(BaseSwitch):
    @intents.on_event("register_sentences")
    def handle_prefer_toggle(self):
        if self.ha.prefer_toggle:
            intents.disable_intent(self.turn_on)
            intents.disable_intent(self.turn_off)
        else:
            intents.disable_intent(self.toggle_switch)

    @intents.sentences(["Schalte [(den | die | das)] ($switch) [an | aus]"])
    def toggle_switch(self, switch):
        response = self._toggle_switch(switch)
        return f"{response['attributes']['friendly_name']} wird {response['state']} geschaltet"

    @intents.sentences(["Schalte [(den | die | das)] ($switch) aus"])
    def turn_off(self, switch):
        response = self._turn_off(switch)
        return f"{response['attributes']['friendly_name']} wird {response['state']} geschaltet"

    @intents.sentences(["Schalte [(den | die | das)] ($switch) an"])
    def turn_on(self, switch):
        response = self._turn_on(switch)
        return f"{response['attributes']['friendly_name']} wird {response['state']} geschaltet"