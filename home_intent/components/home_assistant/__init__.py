from typing import Set

from pydantic import AnyHttpUrl, BaseModel

from . import cover, fan, group, light, lock, remote, shopping_list, switch, weather
from .api import HomeAssistantAPI


class HomeAssistantSettings(BaseModel):
    url: AnyHttpUrl
    bearer_token: str
    prefer_toggle: bool = True
    ignore_domains: Set[str] = set()
    ignore_entities: Set[str] = set()


class HomeAssistantComponent:
    def __init__(self, config: HomeAssistantSettings):
        self.api = HomeAssistantAPI(config.url, config.bearer_token)
        self.services = self.api.get("/api/services")
        all_entities = self.api.get("/api/states")
        self.entities = [x for x in all_entities if x["entity_id"] not in config.ignore_entities]
        self.domains = {x["entity_id"].split(".")[0] for x in self.entities}
        self.domains.update(x["domain"] for x in self.services)
        print(self.domains)
        self.prefer_toggle = config.prefer_toggle


def setup(home_intent):
    # only needed if there are additional settings!
    config = home_intent.get_config(HomeAssistantSettings)
    home_assistant_component = HomeAssistantComponent(config)

    if "cover" in home_assistant_component.domains and "cover" not in config.ignore_domains:
        home_intent.register(cover.Cover(home_assistant_component), cover.intents)

    if "fan" in home_assistant_component.domains and "fan" not in config.ignore_domains:
        home_intent.register(fan.Fan(home_assistant_component), fan.intents)

    if "group" not in config.ignore_domains:
        home_intent.register(group.Group(home_assistant_component), group.intents)

    if "light" in home_assistant_component.domains and "light" not in config.ignore_domains:
        home_intent.register(light.Light(home_assistant_component), light.intents)

    if "lock" in home_assistant_component.domains and "lock" not in config.ignore_domains:
        home_intent.register(lock.Lock(home_assistant_component), lock.intents)

    if "remote" in home_assistant_component.domains and "remote" not in config.ignore_domains:
        home_intent.register(remote.Remote(home_assistant_component), remote.intents)

    if (
        "shopping_list" in home_assistant_component.domains
        and "shopping_list" not in config.ignore_domains
    ):
        home_intent.register(
            shopping_list.ShoppingList(home_assistant_component), shopping_list.intents
        )

    if "switch" in home_assistant_component.domains and "switch" not in config.ignore_domains:
        home_intent.register(switch.Switch(home_assistant_component), switch.intents)

    if "weather" in home_assistant_component.domains and "weather" not in config.ignore_domains:
        home_intent.register(weather.Weather(home_assistant_component), weather.intents)
