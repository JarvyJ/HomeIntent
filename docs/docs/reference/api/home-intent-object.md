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

## `home_intent.get_file(filename, language_dependent=True)`
Home Intent uses a custom file loading function that will first check if a file exists in `/config` otherwise it'll load the file from the [`default_configs/{lang}`](https://github.com/JarvyJ/HomeIntent/tree/main/home_intent/default_configs) folder in the source code.

By default it will load a file from the corresponding language folder, but you can set `language_dependent` to `False`, and it will instead just load from `default_configs`. NOTE: currently overrides in `/config` are not language dependent. 

This method allows users to easily replace parts of components like lists of colors or sounds. This can also be useful when creating custom components, as users can add component code to `/config/custom_components` and any associated files to `/config`.

```python hl_lines="7"
from home_intent import get_file

#### OTHER COMPONENT CODE #####

@intents.dictionary_slots
def color(self):
    color_file = self.home_intent.get_file("home_assistant/colors.txt")
    colors = color_file.read_text().strip().split("\n")
    return {color: color.replace(" ", "") for color in colors}

```

In the example above, Home Intent will check for the file in `/config/home_assistant/colors.txt`, then load from the default config location in the source code: `default_configs/{lang}/home_assistant/colors.txt`.

### Conventions
When loading a file related to a component, it's best to put it in a folder that references the component's name. In the example above, files will be loaded from the `home_assistant` folder in `/config` or Home Intent's `default_configs` folder.

## `home_intent.say(str)`
Have Home Intent say something to the user. This method will likely be modified a bit when satellite support is enabled so a sentence is said at the right location.

## `home_intent.play_audio_file(filename, language_dependent=False)`
This will load a `.wav` file from the filename using the [`get_file`](./home-intent-object.md#home_intentget_filefilename-language_dependenttrue) and play it back using Home Intent. It can also take in the `language_dependent` flag (but defaults to `False`) to load audio files specific to a language if needed.
