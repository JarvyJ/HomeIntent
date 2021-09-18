from pathlib import Path

from ruamel.yaml import YAML

from extract_settings import ExtractSettings

CONFIG_FILE = Path("/config/config.yaml")
FullSettings = ExtractSettings.get()
SETTINGS = FullSettings(**YAML().load(CONFIG_FILE.read_text()))
