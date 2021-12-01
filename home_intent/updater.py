from pathlib import Path
from importlib import import_module
import json
from meta import HomeIntentMeta
from constants import VERSION


class SemanticVersion:
    def __init__(self, version: str):
        self.version = version
        self.version_int = self.generate_int(version)

    def __lt__(self, other):
        return self.version_int < other.version_int

    def __repr__(self):
        return self.version

    def generate_int(self, version: str):
        split_version = version.split(".")
        version_str = f"{split_version[0]}{split_version[1].zfill(2)}{split_version[2].zfill(2)}"
        return int(version_str)


class FileVersion:
    def __init__(self, filename: Path):
        self.filename = filename
        self.version_number = SemanticVersion(filename.stem.replace("-", "."))

    def __lt__(self, other):
        return self.version_number < other.version_number

    def __str__(self):
        return str(self.filename)

    def __repr__(self):
        return str(self.filename)

    def run(self, home_intent):
        print(f"Running update script for version: {self.version_number}")
        update_import_path = f'{".".join(self.filename.parts[-3:-1])}.{self.filename.stem}'
        script = import_module(update_import_path)
        script.run(home_intent)


def update_homeintent(home_intent):
    home_intent_meta = HomeIntentMeta()

    # a little bit of bootstrapping...
    # TODO: remove this for the 2022.01.0 release
    last_run_version = SemanticVersion(home_intent_meta.last_run_version)
    if last_run_version.version == "2021.12.0":
        last_run_version = SemanticVersion("2021.11.0")

    update_scripts = _get_update_script(home_intent_meta, last_run_version)
    _perform_updates(update_scripts, home_intent)
    _update_last_run_version(home_intent_meta)


def _get_update_script(home_intent_meta, last_run_version):
    scripts = Path(__file__).parent / "update_scripts"

    upgrade_scripts = []
    for versioned_filed in scripts.glob("**/*.py"):
        upgrade_file = FileVersion(versioned_filed)
        if upgrade_file.version_number > last_run_version:
            upgrade_scripts.append(upgrade_file)

        if upgrade_file.version_number > SemanticVersion(VERSION):
            raise ValueError(
                "There shouldn't be an upgrade script at a higher version that what is being upgrading to."
                f"\n Current Program Version: {VERSION}\tScript: {upgrade_file.filename}"
            )

    upgrade_scripts.sort()
    return upgrade_scripts


def _perform_updates(update_scripts, home_intent):
    for script in update_scripts:
        script.run(home_intent)


def _update_last_run_version(home_intent_meta):
    home_intent_meta.last_run_version = VERSION
    home_intent_meta.save()


if __name__ == "__main__":
    update_homeintent(None)
