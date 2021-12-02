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
