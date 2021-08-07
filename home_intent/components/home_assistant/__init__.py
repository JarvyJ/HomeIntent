from pydantic import AnyHttpUrl, BaseModel

from . import group, light, shopping_list, switch
from .api import HomeAssistantAPI


class HomeAssistantSettings(BaseModel):
    url: AnyHttpUrl
    bearer_token: str
    prefer_toggle: bool = True


class HomeAssistantComponent:
    def __init__(self, config: HomeAssistantSettings):
        self.api = HomeAssistantAPI(config.url, config.bearer_token)
        self.services = self.api.get("/api/services")
        self.domains = {x["domain"] for x in self.services}
        print(self.domains)
        self.entities = self.api.get("/api/states")
        self.prefer_toggle = config.prefer_toggle


def setup(home_intent):
    # only needed if there are additional settings!
    config = home_intent.get_config(HomeAssistantSettings)
    home_assistant_component = HomeAssistantComponent(config)

    home_intent.register(group.Group(home_assistant_component), group.intents)

    if "shopping_list" in home_assistant_component.domains:
        home_intent.register(
            shopping_list.ShoppingList(home_assistant_component), shopping_list.intents
        )

    if "switch" in home_assistant_component.domains:
        home_intent.register(switch.Switch(home_assistant_component), switch.intents)

    if "light" in home_assistant_component.domains:
        home_intent.register(light.Light(home_assistant_component), light.intents)
