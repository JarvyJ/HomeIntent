from typing import Set

from pydantic import AnyHttpUrl, BaseModel, Field

from . import cover, fan, group, light, lock, remote, shopping_list, switch, weather
from .api import HomeAssistantAPI


class HomeAssistantSettings(BaseModel):
    url: AnyHttpUrl = Field(..., description="The URL for your Home Assistant instance")
    bearer_token: str = Field(
        ...,
        description="The long-lived access token that Home Intent uses to interact with Home Assistant"
        "<br /> <br />"
        "Instructions on getting a "
        '<a href="/docs/integrations/home-assistant/#getting-a-bearer-token" target="_blank">bearer token</a>',
        example="It should start with 'ey' and be ~180 characters",
    )
    prefer_toggle: bool = Field(
        True,
        description="Prefer to toggle instead using on or off when handling intents"
        "<br /><br />"
        'Reason to use <a href="/docs/integrations/home-assistant/#on-prefer_toggle" target="_blank">prefer toggle</a>',
    )
    ignore_domains: Set[str] = Field(
        set(),
        description="A list of domains that shouldn't be controlled via Home Intent",
        example=["light.kitchen", "fan.attic", "switch.tv"],
    )
    ignore_entities: Set[str] = Field(
        set(),
        description="A list of entities that shouldn't be controlled via Home Intent.",
        example=["shopping_list", "light", "remote"],
    )


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
