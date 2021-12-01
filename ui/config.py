import os
from ruamel.yaml import YAML

import aiofiles
import aiofiles.os

from extract_settings import ExtractSettings

CONFIG_FILE = "/config/config.yaml"
FullSettings = ExtractSettings.get()


def get_settings() -> FullSettings:
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            contents = file.read()
            return FullSettings(**YAML().load(contents))
    else:
        return FullSettings()


async def get_settings_async() -> FullSettings:
    if await aiofiles.os.path.isfile(CONFIG_FILE):
        async with aiofiles.open(CONFIG_FILE, "r") as file:
            contents = await file.read()
            return FullSettings(**YAML().load(contents))
    else:
        return FullSettings()
