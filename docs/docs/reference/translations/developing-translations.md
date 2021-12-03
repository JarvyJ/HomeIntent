# Developing Translations
All first party simple integrations will follow the rough directory structure to properly support translations. A bit of work may be needed to convert a custom component, before being accepted into the base Home Intent.

## Directory structure
```
components
	- timer
		__init__.py
		base_timer.py
		en.py
		de.py
		es.py
		... other languages
```

## `__init__.py`
The component will still be loaded from `__init__.py`, however, to properly support translations, there is a `import_module` method in the `home_intent` object that gets passed to the `setup` method that will load the component file associated with the user's language.

```python hl_lines="5"
from home_intent import HomeIntent, Intents


def setup(home_intent: HomeIntent):
    timer = home_intent.import_module(__name__) # will load the {lang}.py
    home_intent.register(timer.Timer(home_intent), timer.intents)
```

## `en.py`
The `en.py` file includes all the english (`en`) language specific sentences/code. Notably all things that can be shared across all languages should be placed in the `base_timer.py` file and imported in. This is where the `_set_timer` method is defined.
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

There is a bit of nuance here. Depending on the language the `partial_time` might not make sense, in which case it can just be omitted from the translation and not passed to `_set_timer`. On the other hand, a translation might exist for `"and a half"`, but it should still map to the english `"half"`. In the dictionary, the `half` acts more like an enum than a string. You can see that in the `get_partial_time_duration` in the `base_timer.py` code below. But in general, the value side of a dictionary slot does not need to be translated.

## `base_timer.py`
The `base_timer.py` file includes the main timer functionality and contains code that all the languages can use. In the timer constructor below, we are activating the [`humanize`](https://github.com/jmoiron/humanize) module to load the specific language settings. In this case, the `humanize` module takes care of some of the translation heavy lifting. 
```python
from datetime import timedelta
from threading import Timer as ThreadingTimer

import humanize

from home_intent import HomeIntent, Intents

intents = Intents(__name__)


class TimerException(Exception):
    pass


class BaseTimer:
    def __init__(self, home_intent: HomeIntent):
        # TODO: keep track of timers and add ability to remove timers
        # self.timers = []
        self.home_intent = home_intent

        # for some reason the activate fails for "en", I think because it's not a "translation"
        if self.home_intent.language != "en":
            humanize.i18n.activate(self.home_intent.language)

    def _set_timer(
        self,
        timer_done_message: str,
        hours: int = None,
        minutes: int = None,
        seconds: int = None,
        timer_partial_time=None,
        text_conversion_function=humanize.precisedelta,
    ):
        timer_duration = timedelta(
            hours=int(hours or 0), minutes=int(minutes or 0), seconds=int(seconds or 0),
        )
        if timer_duration == timedelta(0):
            raise TimerException("Timer has to be set for more than 0 seconds")
        if timer_partial_time:
            timer_duration = timer_duration + get_partial_time_duration(
                timer_partial_time, hours, minutes, seconds
            )
        human_timer_duration = text_conversion_function(timer_duration)
        timer = ThreadingTimer(
            timer_duration.total_seconds(),
            self.complete_timer,
            (human_timer_duration, timer_done_message),
        )
        timer.start()
        return human_timer_duration

    def complete_timer(self, human_timer_duration: str, timer_done_message: str):
        self.home_intent.play_audio_file("timer/alarm.wav")
        self.home_intent.say(timer_done_message.format(human_timer_duration))


def get_partial_time_duration(partial_time, hours=None, minutes=None, seconds=None):
    partial_of = None
    if hours:
        partial_of = "hours"
    elif minutes:
        partial_of = "minutes"
    elif seconds:
        partial_of = "seconds"

    if partial_time == "half":
        return timedelta(**{partial_of: 0.5})
    elif partial_time == "quarter":
        return timedelta(**{partial_of: 0.25})
    elif partial_time == "third":
        return timedelta(**{partial_of: 1 / 3})

```

## Language Helpers
There are a couple of things that can help with language specifics including:

### `home_intent.language`
This keeps track of the two letter ISO639-1 language code and can be used as needed. In the `base_timer.py` example above, it is used in the humanize activation step in the BaseTimer constructor.

### `home_intent.get_file`
This is further explained in the Home Intent [object reference](../api/home-intent-object.md#home_intentget_filefilename-language_dependenttrue), but to quickly summarize, the `get_file` method will load a file first looking in the Home Intent [`default_configs`](https://github.com/JarvyJ/HomeIntent/tree/main/home_intent/default_configs) directory in the appropriate language code folder. Some external files are language dependent and can get loaded from there as needed.

### `home_intent.play_audio_file`
The `play_audio_file` method has also been updated to support the `language_dependent` flag to load language specific sounds. However, it defaults to `False`, so it will not look for audio files in the language code folder in `default_configs` by default.