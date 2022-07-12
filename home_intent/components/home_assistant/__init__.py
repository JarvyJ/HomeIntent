from typing import Dict, List, Optional, Set

from pydantic import AnyHttpUrl, BaseModel, Field

from . import script
from .api import HomeAssistantAPI


class HomeAssistantSettings(BaseModel):
    url: AnyHttpUrl = Field(
        ...,
        description="The URL for your Home Assistant instance",
        example="ex: http://192.168.1.165:8123",
    )
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
        {"climate", "lock", "humidifier"},
        description="A list of domains that shouldn't be controlled via Home Intent. "
        "<br /> <br />"
        "Climate, Lock, and Humidifier are "
        '<a href="/docs/integrations/home-assistant/#on-ignore_domains-defaults" target="_blank">ignored by default</a> '
        "so you can consider the "
        "overall risk if an entity is accidentally triggered in your household.",
        example=["shopping_list", "light", "remote"],
    )
    ignore_entities: Set[str] = Field(
        set(),
        description="A list of entities that shouldn't be controlled via Home Intent.",
        example=["light.kitchen", "fan.attic", "switch.tv"],
    )
    scripts: Optional[Dict[str, script.ScriptActions]] = Field(
        description="An association of scripts in Home Assistant, sentences to trigger them, and the associated response",
        example={
            "script.test_script": {
                "sentences": ["It's movie time", "I want to watch a movie"],
                "response": "You can now watch your movie.",
            }
        },
    )


class HomeAssistantComponent:
    def __init__(self, config: HomeAssistantSettings, language: str):
        self.api = HomeAssistantAPI(config.url, config.bearer_token, language)
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
    home_assistant_component = HomeAssistantComponent(
        config, home_intent.settings.home_intent.language
    )

    if "climate" in home_assistant_component.domains and "climate" not in config.ignore_domains:
        climate = home_intent.import_module(f"{__name__}.climate")
        home_intent.register(climate.Climate(home_assistant_component), climate.intents)

    if "cover" in home_assistant_component.domains and "cover" not in config.ignore_domains:
        cover = home_intent.import_module(f"{__name__}.cover")
        home_intent.register(cover.Cover(home_assistant_component), cover.intents)

    if "fan" in home_assistant_component.domains and "fan" not in config.ignore_domains:
        fan = home_intent.import_module(f"{__name__}.fan")
        home_intent.register(fan.Fan(home_assistant_component), fan.intents)

    if "group" not in config.ignore_domains:
        group = home_intent.import_module(f"{__name__}.group")
        home_intent.register(group.Group(home_assistant_component), group.intents)

    if (
        "humidifier" in home_assistant_component.domains
        and "humidifier" not in config.ignore_domains
    ):
        humidifier = home_intent.import_module(f"{__name__}.humidifier")
        home_intent.register(humidifier.Humidifier(home_assistant_component), humidifier.intents)

    if "light" in home_assistant_component.domains and "light" not in config.ignore_domains:
        light = home_intent.import_module(f"{__name__}.light")
        home_intent.register(light.Light(home_assistant_component, home_intent), light.intents)

    if "lock" in home_assistant_component.domains and "lock" not in config.ignore_domains:
        lock = home_intent.import_module(f"{__name__}.lock")
        home_intent.register(lock.Lock(home_assistant_component), lock.intents)

    if "remote" in home_assistant_component.domains and "remote" not in config.ignore_domains:
        remote = home_intent.import_module(f"{__name__}.remote")
        home_intent.register(remote.Remote(home_assistant_component), remote.intents)

    if (
        "shopping_list" in home_assistant_component.domains
        and "shopping_list" not in config.ignore_domains
    ):
        shopping_list = home_intent.import_module(f"{__name__}.shopping_list")
        home_intent.register(
            shopping_list.ShoppingList(home_assistant_component, home_intent), shopping_list.intents
        )

    if hasattr(config, "scripts") and config.scripts and "script" not in config.ignore_domains:
        home_intent.register(
            script.Script(home_assistant_component, config.scripts), script.intents
        )

    if "switch" in home_assistant_component.domains and "switch" not in config.ignore_domains:
        switch = home_intent.import_module(f"{__name__}.switch")
        home_intent.register(switch.Switch(home_assistant_component), switch.intents)

    if "weather" in home_assistant_component.domains and "weather" not in config.ignore_domains:
        weather = home_intent.import_module(f"{__name__}.weather")
        home_intent.register(weather.Weather(home_assistant_component), weather.intents)

    if "media_player" in home_assistant_component.domains and "media_player" not in config.ignore_domains:
        media_player = home_intent.import_module(f"{__name__}.media_player")
        home_intent.register(media_player.MediaPlayer(home_assistant_component), media_player.intents)
