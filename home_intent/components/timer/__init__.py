from collections import defaultdict
from datetime import timedelta
from threading import Timer as ThreadingTimer

from humanize import precisedelta
from pydantic import BaseModel

from home_intent import HomeIntent, Intents

intents = Intents(__name__)


class TimerSettings(BaseModel):
    max_time_days: int = 1


class Timer:
    def __init__(self, config: TimerSettings, home_intent: HomeIntent):
        self.timerssss = []
        self.max_time_days = timedelta(days=config.max_time_days)
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
            weeks=weeks or 0,
            days=days or 0,
            hours=hours or 0,
            minutes=minutes or 0,
            seconds=seconds or 0,
        )
        if partial_time:
            timer_duration = timer_duration + get_partial_time_duration(
                partial_time, weeks, days, hours, minutes, seconds
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
    home_intent.register(Timer(config, home_intent), intents)
