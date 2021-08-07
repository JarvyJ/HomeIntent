"""Start up HomeIntent"""
import importlib
import logging

from home_intent import HomeIntent
from settings import Settings


def main():
    _setup_logging()
    settings = Settings()
    home_intent = HomeIntent(settings)
    _load_integrations(settings, home_intent)
    home_intent.initialize()


def _setup_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s", level=logging.INFO,
    )


def _load_integrations(settings: Settings, home_intent: HomeIntent):
    for component in settings.dict():
        component_settings = getattr(settings, component)
        if isinstance(component_settings, dict) or component_settings is None:
            integration = importlib.import_module(f"components.{component}")
            integration.setup(home_intent)


if __name__ == "__main__":
    main()
