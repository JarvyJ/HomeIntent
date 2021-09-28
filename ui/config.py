from functools import lru_cache
import os
from ruamel.yaml import YAML

import aiofiles

from extract_settings import ExtractSettings

CONFIG_FILE = "/config/config.yaml"
FullSettings = ExtractSettings.get()


@lru_cache
def get_settings() -> FullSettings:
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            contents = file.read()
            return FullSettings(**YAML().load(contents))
    else:
        return FullSettings()


async def get_settings_async() -> FullSettings:
    # TODO: switch this to aiofiles.os.path when 0.8.0 is released
    if os.path.isfile(CONFIG_FILE):
        async with aiofiles.open(CONFIG_FILE, "r") as file:
            contents = await file.read()
            return FullSettings(**YAML().load(contents))
    else:
        return FullSettings()
