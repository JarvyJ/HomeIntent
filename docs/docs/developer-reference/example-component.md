# Example Component
Let's take a look at a simplified example component and break it down.

```python
from collections import defaultdict
from datetime import timedelta
from pydantic import BaseModel
from home_intent import Intents, HomeIntent

intents = Intents(__name__)


class TimerSettings(BaseModel):
    max_time_days: int = 1


class Timer:
    def __init__(self, config: TimerSettings):
        self.timers = []
        self.max_time_days = timedelta(days=config.max_time_days)

    @intents.dictionary_slots
    def partial_time(self):
        return {
            "and [a] half": "half",
            "and [a] quarter": "quarter",
            "and [a] third": "third",
        }

    @intents.sentences(
        [
            "time = 0..128",
            "set timer [<time>{hours:!int} (hour | hours)] [<time>{minutes:!int} (minute | minutes)] [<time>{seconds:!int} (second | seconds)]"
            "set timer <time>{hours:!int} [($partial_time)] (hour | hours)",
            "set timer <time>{minutes:!int} [($partial_time)] (minute | minutes)",
            "set timer <time>{seconds:!int} [($partial_time)] (second | seconds)",
        ]
    )
    def set_timer(self, hours=None, minutes=None, seconds=None, partial_time=None):
        timer_duration = timedelta(
            weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
        )
        if partial_time:
            timer_duration = timer_duration + get_partial_time_duration(
                partial_time, hours, minutes, seconds
            )
        create_timer(timer_duration)


def setup(home_intent: HomeIntent):
    config = home_intent.get_config(TimerSettings)
    home_intent.register(Timer(config), intents)

```

## The Intents Object
```python hl_lines="4"
from pydantic import BaseModel
from home_intent import Intents, HomeIntent

intents = Intents(__name__)


class TimerSettings(BaseModel):
    max_time_days: int = 1
```

The intents object holds on to all the `slots` and `sentences` function references related to the intent class (in this case `Timer`). In the `setup` call it also gets passed to `home_intent.register` when setting up a component.

### Dictionary Slots
```python
    @intents.dictionary_slots
    def partial_time(self):
        return {
            "and [a] half": "half",
            "and [a] quarter": "quarter",
            "and [a] third": "third",
        }
```
Dictionary slots are a dictionary of words and their references that get used as a Rhasspy [slot](https://rhasspy.readthedocs.io/en/latest/training/#slots-lists). They make defining intents more modular as a sentence can just refer to a slot name instead of creating a bunch of variations. This is a rather small example, but slots can have hundreds of potential options. With slots defined in Home Intent, the slot name is the same as the function name - here it's `partial_time` and that will be used in the sentence definition below.

The `intents.dictionary_slots` expects a `Dict[str, str]` to be returned. There is also an `intents.slots` which can be used if what is spoken matches the reference. It expects a `List[str]`.

### Sentences
```python
    @intents.sentences(
        [
            "time = 0..128",
            "set timer [<time>{hours:!int} (hour | hours)] [<time>{minutes:!int} (minute | minutes)] [<time>{seconds:!int} (second | seconds)]"
            "set timer <time>{hours:!int} [($partial_time)] (hour | hours)",
            "set timer <time>{minutes:!int} [($partial_time)] (minute | minutes)",
            "set timer <time>{seconds:!int} [($partial_time)] (second | seconds)",
        ]
    )
    def set_timer(self, hours=None, minutes=None, seconds=None, partial_time=None):
        timer_duration = timedelta(
            weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
        )
        if partial_time:
            timer_duration = timer_duration + get_partial_time_duration(
                partial_time, hours, minutes, seconds
            )
        create_timer(timer_duration)

```
The sentence function (`set_timer`) is what gets called when a matching sentence is spoken to the voice assistant. These all get published to Rhasspy's [sentences.ini](https://rhasspy.readthedocs.io/en/latest/training/#sentencesini) file and use its syntax. Home Intent will parse the sentences defined in the decorator and pull out the slots and tags. Slots are defined with `($slot_name)` and tags are defined by `{tag_name}`. The slot names need to be defined in the same `Intents` object and are referred to by the method name. These are what get passed to the method to perform an action.


### Setup

```python
class TimerSettings(BaseModel):
    max_time_days: int = 1

###### ... ######

def setup(home_intent: HomeIntent):
    config = home_intent.get_config(TimerSettings)
    home_intent.register(Timer(config), intents)
```

This function gets called when loading from `config.yaml`, as long as the component name is present. It will be loaded from `/config/custom_components/<component_name>`.

The `home_intent.get_config` function will load the `TimerSettings` from `config.yaml` and pass back the [pydantic](https://pydantic-docs.helpmanual.io/) model that can be used for initialization. This is only required if the custom component requires any settings passed in from the user.

The `home_intent.register` function will keep track of the instantiated object and associated intents. When the the register function is called, the slots and sentences are verified, and a bit later on in the Home Intent setup all the slot functions are called to get the slot values.