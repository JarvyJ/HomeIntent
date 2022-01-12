from .base_timer import intents, BaseTimer


class Timer(BaseTimer):
    @intents.dictionary_slots
    def timer_partial_time(self):
        return {
            "einhalb": "half",
            "einviertel": "quarter",
            "dreiviertel": "threequarters"            
        }

    @intents.repeatable_dictionary_slots
    def timer_number(self):
        # this is used to overwrite (or add) some numbers provided by Rhasspy's num2words package
        return {            
            "eine": "1",
            "hundert": "100",
            "hundertzehn": "110",
            "hundertzwanzig": "120",
        }
   
    @intents.satellite_id
    @intents.sentences(
        [
            "time = $timer_number | 0..120",
            "Stell (den | einen) (Wecker | Timer) auf (<time>){hours} [($timer_partial_time)] Stunden",
            "Stell (den | einen) (Wecker | Timer) auf (<time>){minutes} [($timer_partial_time)] Minuten",
            "Stell (den | einen) (Wecker | Timer) auf (<time>){seconds} [($timer_partial_time)] Sekunden",
            "Stell (den | einen) (Wecker | Timer) auf (<time>){hours} Stunden und (<time>){minutes} Minuten",
            "Stell (den | einen) (Wecker | Timer) auf (<time>){minutes} Minuten und (<time>){seconds} Sekunden",
            "Stell einen (<time>){hours} Stunden und (<time>){minutes} Minuten Timer",
            "Stell einen (<time>){minutes} Minuten und (<time>){seconds} Sekunden Timer",
            "Stell einen (<time>){hours} [($timer_partial_time)] Stunden (Wecker | Timer)",
            "Stell einen (<time>){minutes} [($timer_partial_time)] Minuten (Wecker | Timer)",
            "Stell einen (<time>){seconds} [($timer_partial_time)] Sekunden (Wecker | Timer)",
        ]
    )
    def set_timer(self, satellite_id, hours: int = None, minutes: int = None, seconds: int = None, timer_partial_time=None):
        human_timer_duration = self._set_timer(satellite_id, "Der {0} Timer ist abgelaufen", hours, minutes, seconds, timer_partial_time)
        return f"Stelle Timer auf {human_timer_duration}"