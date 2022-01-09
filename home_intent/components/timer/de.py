from .base_timer import intents, BaseTimer


class Timer(BaseTimer):
    @intents.dictionary_slots
    def timer_partial_time(self):
        return {
            "einhalb": "half",
            "einviertel": "quarter",
            "[und] dreiviertel": "threequarters"
            #"and [a] third": "third", # no one says this
        }

    @intents.repeatable_dictionary_slots
    def timer_number(self):
        # this is used to overwrite (or add) some numbers provided by Rhasspy's num2words package
        return {            
            "hundert": "100",
            "hunderteins": "101",
            "hundertzwei": "102",
            "hundertdrei": "103",
            "hundertvier": "104",
            "hundertfünf": "105",
        }
   

    @intents.sentences(
        [
            "time = ($timer_number | 0..120)",
            "Stell (den | einen) (Wecker | Timer) auf [(<time>){hours} Stunden] [(<time>){minutes} Minuten] [(<time>){seconds} Sekunden]",
            "Stell (den | einen) (Wecker | Timer)  auf (<time>){hours} [($timer_partial_time)] Stunden",
            "Stell (den | einen) (Wecker | Timer)  auf (<time>){minutes} [($timer_partial_time)] Minuten",
            "Stell (den | einen) (Wecker | Timer)  (<time>){seconds} [($timer_partial_time)] Sekunden",
            "Stell einen [(<time>){hours} Stunden] [(<time>){minutes} Minuten] [(<time>){seconds} Sekunden] (Wecker | Timer)",
            "Stell einen (<time>){hours} [($timer_partial_time)] Stunden (Wecker | Timer)",
            "Stell einen (<time>){minutes} [($timer_partial_time)] Minuten (Wecker | Timer)",
            "Stell einen (<time>){seconds} [($timer_partial_time)] Sekunden (Wecker | Timer)",
        ]
    )
    def set_timer(
        self, hours: int = None, minutes: int = None, seconds: int = None, timer_partial_time=None
    ):
        human_timer_duration = self._set_timer(
            "Der Timer {0} ist abgelaufen", hours, minutes, seconds, timer_partial_time
        )
        return f"Stelle Timer auf {human_timer_duration}"

    @intents.sentences(["Lösche den letzten Timer"])
    def delete_timer(self):
        self.delete_timer()
        return f"lösche Timer"


        