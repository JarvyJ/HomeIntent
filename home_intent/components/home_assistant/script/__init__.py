from typing import List

from pydantic import BaseModel

from home_intent import Intents

intents = Intents(__name__)


class HomeAssistantScriptException(Exception):
    pass


class ScriptActions(BaseModel):
    sentences: List[str]
    response: str


class Script:
    def __init__(self, home_assistant, scripts):
        self.ha = home_assistant
        self.scripts = scripts
        ha_scripts = {
            x["entity_id"] for x in self.ha.entities if x["entity_id"].startswith("script.")
        }
        for script in scripts:
            if not script.startswith("script."):
                raise HomeAssistantScriptException(
                    f"Your script ({script}) should start with 'script.'"
                )
            if script not in ha_scripts:
                raise HomeAssistantScriptException(
                    f"Couldn't find your script ({script}) in Home Assistant. "
                    "Make sure the script exists and the name matches what's in Home Assistant"
                )

    @intents.dictionary_slots
    def script(self):
        scripts = {}
        for script_entity_id, script_actions in self.scripts.items():
            for sentence in script_actions.sentences:
                scripts[sentence] = script_entity_id

        return scripts

    @intents.sentences(["($script)"])
    def execute_script(self, script):
        script_entity_without_prefix = script.split(".")[1]
        self.ha.api.call_service("script", script_entity_without_prefix, {})
        return self.scripts[script].response
