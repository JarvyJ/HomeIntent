# HomeIntent object
An instantiated `HomeIntent` object gets passed in to the `setup` function when setting up components.

Example:
```python hl_lines="4"
class TimerSettings(BaseModel):
    max_time_days: int = 1

def setup(home_intent: HomeIntent):
    config = home_intent.get_config(TimerSettings)
    home_intent.register(Timer(config), intents)
```

## `home_intent.get_config(pydantic.BaseModel)`
Home Intent uses [pydantic](https://pydantic-docs.helpmanual.io/) models for handling configuration. The `get_config` method will parse the config from `config.yaml` given the pydantic BaseModel object and return it for use.

## `home_intent.register(Class(), Intents)`
The `register` method expects an instantiated intent class object and an `Intents` object. This method registers the class and verifies all the slots and sentences are setup correctly. Later in the Home Intent initialization process, the registered intents are used to configure Rhasspy and setup the Intent Handler.

## `home_intent.say(str)`
Have Home Intent say something to the user. This method will likely be modified a bit when satellite support is enabled so a sentence is said at the right location.

## `home_intent.play_audio_file(filename)`
This will load a `.wav` file from the filename using the [`get_file`](/developer-reference/api-reference/get-file/) and play it back using Home Intent. It will also need to be modified once satellite support is in.