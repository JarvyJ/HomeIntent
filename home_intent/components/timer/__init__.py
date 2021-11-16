from home_intent import HomeIntent, Intents


def setup(home_intent: HomeIntent):
    timer = home_intent.import_module(__name__)
    home_intent.register(timer.Timer(home_intent), timer.intents)
