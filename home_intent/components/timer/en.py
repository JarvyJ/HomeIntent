from .base_timer import intents, BaseTimer


class Timer(BaseTimer):
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
            "set timer [(<time>){hours} hours] [(<time>){minutes} minutes] [(<time>){seconds} seconds]",
            "set timer (<time>){hours} [($partial_time)] hours",
            "set timer (<time>){minutes} [($partial_time)] minutes",
            "set timer (<time>){seconds} [($partial_time)] seconds",
            "set a [(<time>){hours} hour] [(<time>){minutes} minute] [(<time>){seconds} second] timer",
            "set a (<time>){hours} [($partial_time)] hour timer",
            "set a (<time>){minutes} [($partial_time)] minute timer",
            "set a (<time>){seconds} [($partial_time)] second timer",
        ]
    )
    def set_timer(
        self, hours: int = None, minutes: int = None, seconds: int = None, partial_time=None
    ):
        human_timer_duration = self._set_timer(
            "Your timer {0} has ended", hours, minutes, seconds, partial_time
        )
        return f"Setting timer {human_timer_duration}"
