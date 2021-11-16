from importlib import import_module
from home_intent import HomeIntent, Intents


def setup(home_intent: HomeIntent, language: str):
    timer = import_module(f"{__name__}.{language}")
    home_intent.register(timer.Timer(home_intent, language), timer.intents)
