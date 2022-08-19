# Translating a Component
Currently only a few languages are supported in Home Intent. We've designed the [structure](./developing-translations.md) of the code to support multiple languages and hope that people can contribute.

Currently translating requires a bit of Docker, docker-compose, and git knowledge. We know this is a high bar for contributing, but have decided to go for it to allow Python to be fully used in the translation environment. Knowing Python is not strictly needed to help with translations, but it would be useful as translators may have to refer back to the base classes during translation. 

The [developing translations guide](./developing-translations.md) and [local Home Intent development](../developer/local-development.md) would be good to read beforehand to understand how it all fits together.

If you want to contribute a translation, feel free to create a new issue in our [GitHub repository](https://github.com/JarvyJ/HomeIntent/issues) so we know who is working on it and any questions related to the translation can be asked.

## Enabling another language
To get stated with translations, you will need to pull down the latest version of the repo, and [setup the `config.yaml`](../developer/local-development.md#basic-development-setup). From there you can update the development [`docker-compose.yaml`](https://github.com/JarvyJ/HomeIntent/blob/main/docker-compose.yaml) file to set the ISO639-1 language codes in Home Intent and Rhasspy. The current supported codes are the following:

 - en - English
 - de - German
 - es - Spanish
 - fr - French
 - it - Italian
 - nl - Dutch
 - ru - Russian
 - vi - Vietnamese
 - sv - Swedish
 - cs - Czech

You can set the language in Home Intent with the `LANGUAGE` environment variable:
```yaml hl_lines="15"
# the other containers...

  homeintent:
    restart: unless-stopped
    build:
      context: .
      dockerfile: "development-env/Dockerfile.python"
    depends_on:
      - rhasspy
    volumes:
      - "./home_intent:/usr/src/app/home_intent"
      - "./development-env/config:/config"
    environment:
      - DOCKER_DEV=True
      - LANGUAGE=de
    command: python3 home_intent

# some more containers...
```

In Rhasspy, the `command`'s `profile` argument also needs to be updated to the match the language code:
```yaml hl_lines="12"
  rhasspy:
    image: "rhasspy/rhasspy:2.5.11"
    restart: unless-stopped
    volumes:
      - "./development-env/rhasspy:/profiles"
      - "/etc/localtime:/etc/localtime:ro"
    ports:
      - "12101:12101"
      - "12183:12183"
    devices:
      - "/dev/snd:/dev/snd"
    command: --user-profiles /profiles --profile de
```

Doing this will load the different language option in Rhasspy and tell Home Intent to try and load the translated version of a component. If it can't do that it will fallback to English. This might not be the long term behavior, but is currently how it is setup as very few things have been translated.


## Translating Components
To translate a component, in the components folder (which should exist after kicking off the container for the first time), there are component folders with `en.py` files. You can start by copying the `en.py` file to the language you are translating to (ex: `de.py`, `es.py`, etc), and going through and translating the sentencs/structures to the other language.

```python
from .base_timer import intents, BaseTimer


class Timer(BaseTimer):
    @intents.dictionary_slots
    def timer_partial_time(self):
        return {
            "and [a] half": "half",
            "and [a] quarter": "quarter",
            "and [a] third": "third",
        }

    @intents.sentences(
        [
            "time = 0..128",
            "set timer [(<time>){hours} hours] [(<time>){minutes} minutes] [(<time>){seconds} seconds]",
            "set timer (<time>){hours} [($timer_partial_time)] hours",
            "set timer (<time>){minutes} [($timer_partial_time)] minutes",
            "set timer (<time>){seconds} [($timer_partial_time)] seconds",
            "set a [(<time>){hours} hour] [(<time>){minutes} minute] [(<time>){seconds} second] timer",
            "set a (<time>){hours} [($timer_partial_time)] hour timer",
            "set a (<time>){minutes} [($timer_partial_time)] minute timer",
            "set a (<time>){seconds} [($timer_partial_time)] second timer",
        ]
    )
    def set_timer(
        self, hours: int = None, minutes: int = None, seconds: int = None, timer_partial_time=None
    ):
        human_timer_duration = self._set_timer(
            "Your timer {0} has ended", hours, minutes, seconds, timer_partial_time
        )
        return f"Setting timer {human_timer_duration}"

```

This is the `en.py` file from the Timer component. Rhasspy uses a [simplified JSGF](https://rhasspy.readthedocs.io/en/latest/training/#sentencesini) grammar for its sentence structure. This is the most complex component in terms of grammer:

 - Most of the time there will be a `($slot_name)` which will do a substitution with a slot (dictionary or regular).
 - Some of the sentences include things in brackets which are considered `[optional]`.
 - A couple of the sentences use sentence "rules". You can see that with the `time = 0..128` which later gets referenced in the sentence by `(<time>){variable_name}`

These can be mixed and matched to create various types of sentence structures.

When a sentence is spoken, Rhasspy parses out specific types of variables - the `($slot_name)` and `{curly_bracket}`, which then Home Intent picks up and calls the associated function with. In the example above, `set_timer` takes in `hours`, `minutes`, and `seconds` from the `{curly_bracket}` and `partial_time` from the `($slot_name)`

## Testing Translations

After making changes to the codebase, you can start Home Intent in the Docker container:
```
docker-compose up homeintent
```

After it's running, you can go to the Rhasspy UI ([`http://localhost:12101`](http://localhost:12101)), click on the `Sentences` tab and select `intents/home_intent.ini` from the file dropdown to see the sentences and `Slots` tab to see any language specific slots.

Sentences Tab:
![sentences tab in Rhasspy](../../../img/rhasspy-ui/sentences.png)

Slots Tab:
![slots tab in Rhasspy](../../../img/rhasspy-ui/slots.png)

From there, you can verbally test the translations and see how well they work. If changes are needed, you can stop running Home Intent with `ctrl+c`, make further changes, and start the container again. Once they are working as expected, the files can be Pull Requested back in, and we can work on getting it merged!


## Translation Considerations
We always want to keep Home Intent working well and feeling professional, so we have some considerations that might help.

### Common Sentence Structure
In English all the sentences try to start with verbs ("Turn on the kitchen light", "Set timer 5 minutes", "Open the garage door", etc). The main idea behind this is to have a sentence structure that is consistent across all types of intents and makes the sentence usage "guessable". So the idea with any of the translations is that once folks understand the sentence structure, they should be able to guess all the variations without much effort.


### Understanding the on/off types of issues
One of the issues we run into in English voice recognition is that "on" and "off" sound very similar and mean very different things. To get around this, for (at least) Home Assistant, there's a [`prefer_toggle`](../../integrations/home-assistant.md#on-prefer_toggle) setting that toggles instead of directly performing the action that was requested. This gets Home Intent to perform the correct action even if it misheard the sentence.

I'm sure this will affect other languages. If they follow the `prefer_toggle` convention, they can use it. But if another language quirk causes "system confusion", please put an issue into the tracker so we can work to resolve it.

### Others
I'm sure while translating we may come across other language considerations that can be used to further improve the quality of Home Intent. Feel free to start a discussion or open an issue to discuss. We'd love to hear about it!
