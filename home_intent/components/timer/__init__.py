from collections import defaultdict
from datetime import timedelta

from pydantic import BaseModel

from home_intent import HomeIntent, Intents

intents = Intents(__name__)


class TimerSettings(BaseModel):
    max_time_days: int = 1


class Timer:
    def __init__(self, config: TimerSettings):
        self.timerssss = []
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
            "set timer [<time>{days:!int} (day | days)] [<time>{hours:!int} (hour | hours)] [<time>{minutes:!int} (minute | minutes)] [<time>{seconds:!int} (second | seconds)]",
            "set timer <time>{days:!int} [($partial_time)] (day | days)",
            "set timer <time>{hours:!int} [($partial_time)] (hour | hours)",
            "set timer <time>{minutes:!int} [($partial_time)] (minute | minutes)",
            "set timer <time>{seconds:!int} [($partial_time)] (second | seconds)",
        ]
    )
    def set_timer(
        self, weeks=None, days=None, hours=None, minutes=None, seconds=None, partial_time=None
    ):
        timer_duration = timedelta(
            weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
        )
        if partial_time:
            timer_duration = timer_duration + get_partial_time_duration(
                partial_time, weeks, days, hours, minutes, seconds
            )
        # create_timer(timer_duration)


def get_partial_time_duration(
    partial_time, weeks=None, days=None, hours=None, minutes=None, seconds=None
):
    partial_of = None
    if days:
        partial_of = "days"
    elif hours:
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
    config = home_intent.get_config(TimerSettings)
    home_intent.register(Timer(config), intents)
