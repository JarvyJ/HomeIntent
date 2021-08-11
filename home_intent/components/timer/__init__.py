from collections import defaultdict
from datetime import timedelta
from threading import Timer as ThreadingTimer

from humanize import precisedelta
from pydantic import BaseModel

from home_intent import HomeIntent, Intents

intents = Intents(__name__)


class Timer:
    def __init__(self, home_intent: HomeIntent):
        # TODO: keep track of timers and add ability to remove timers
        self.timers = []
        self.home_intent = home_intent

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
            "set timer [(<time>){hours:!int} hours] [(<time>){minutes:!int} minutes] [(<time>){seconds:!int} seconds]",
            "set timer (<time>){hours:!int} [($partial_time)] hours",
            "set timer (<time>){minutes:!int} [($partial_time)] minutes",
            "set timer (<time>){seconds:!int} [($partial_time)] seconds",
        ]
    )
    def set_timer(self, hours=None, minutes=None, seconds=None, partial_time=None):
        timer_duration = timedelta(hours=hours or 0, minutes=minutes or 0, seconds=seconds or 0,)
        if partial_time:
            timer_duration = timer_duration + get_partial_time_duration(
                partial_time, hours, minutes, seconds
            )
        human_timer_duration = precisedelta(timer_duration)
        timer = ThreadingTimer(
            timer_duration.total_seconds(), self.complete_timer, (human_timer_duration,),
        )
        timer.start()
        return f"Timer set {human_timer_duration}"

    def complete_timer(self, human_timer_duration: str):
        self.home_intent.say("BWEEP bip bip BWEEP " * 4)
        self.home_intent.say(f"Your timer {human_timer_duration} has ended")


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


def setup(home_intent: HomeIntent):
    home_intent.register(Timer(home_intent), intents)
