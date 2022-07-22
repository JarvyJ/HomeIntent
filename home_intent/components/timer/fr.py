from .base_timer import intents, BaseTimer


class Timer(BaseTimer):
    @intents.dictionary_slots
    def timer_partial_time(self):
        return {
            "demi": "half",
            "quart": "quarter",
            "tiers": "third",
            "deuxtiers": "twothirds",
            "troisquarts": "threequarters"
        }

    @intents.satellite_id
    @intents.sentences(
        [
            "time = 0..120",
            "Régler (le | un) (minuteur | Timer) à (<time>){hours} (un) [($timer_partial_time)] (de) secondes",
            "Régler (le | un) (minuteur | Timer) à (<time>){minutes} (un) [($timer_partial_time)] (de) minutes",
            "Régler (le | un) (minuteur | Timer) à (<time>){seconds} (un) [($timer_partial_time)] (de) secondes",
            "Régler (le | un) (minuteur | Timer) à (<time>){hours} heures et (<time>){minutes} Minutes",
            "Régler (le | un) (minuteur | Timer) à (<time>){minutes} minutes et (<time>){seconds} Secondes",
            "Régler un (minuteur | Timer) (d'une | de) (<time>){hours} heures et (<time>){minutes} minutes",
            "Régler un (minuteur | Timer) (d'une | de) (<time>){minutes} minutes et (<time>){seconds} secondes",
            "Régler un (minuteur | Timer) (d'un | d'une | de) (<time>){seconds} [($timer_partial_time)] (de) secondes",
            "Régler un (minuteur | Timer) (d'un | d'une | de) (<time>){minutes} [($timer_partial_time)] (de) minutes",
            "Régler un (minuteur | Timer) (d'un | d'une | de) (<time>){hours} [($timer_partial_time)] (d') heures",
        ]
    )
    def set_timer(
        self,
        satellite_id,
        hours: int = None,
        minutes: int = None,
        seconds: int = None,
        timer_partial_time=None,
    ):
        human_timer_duration = self._set_timer(
            satellite_id, "Votre minuteur {0} s'est écoulé", hours, minutes, seconds, timer_partial_time
        )
        return f"Réglage du minuteur {human_timer_duration}"
