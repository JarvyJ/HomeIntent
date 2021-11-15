from datetime import datetime
from .base_weather import intents, BaseWeather, _get_forecast_time_of_day, TimeOfDay

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class Weather(BaseWeather):
    @intents.dictionary_slots
    def day_of_week(self):
        return {x[1]: x[0] for x in enumerate(DAYS_OF_WEEK)}

    @intents.on_event("register_sentences")
    def handle_forecasting(self):
        if not self.entity_with_forecast:
            intents.disable_intent(self.forecast_today)
            intents.disable_intent(self.forecast_tonight)
            intents.disable_intent(self.forecast_day)
            intents.disable_intent(self.forecast_night)

    @intents.beta
    @intents.sentences(["what is the temperature [(right now|today|outside)]"])
    def temperature_day(self):
        response = self.ha.api.get_entity(self.entity)
        return f"The temperature is currently {response['attributes']['temperature']}"

    @intents.beta
    @intents.sentences(
        [
            "what is the (weather|forecast) (right now|today|outside)",
            "what is it like (right now|outside)",
            "how does it feel outside [right now]",
        ]
    )
    def forecast_today(self):
        current_conditions = self._forecast_today()
        return _get_forecast_details(current_conditions)

    @intents.beta
    @intents.sentences(
        ["what is the (weather|forecast) tonight", "(how|what) is it going to be [like] tonight"]
    )
    def forecast_tonight(self):
        forecast = self._forecast_tonight()
        return _get_forecast_details(forecast)

    @intents.beta
    @intents.sentences(
        ["what is the (weather|forecast) [going to be] (on|for) [next] ($day_of_week:!int)"]
    )
    def forecast_day(self, day_of_week):
        forecast = self._forecast_day(day_of_week)
        return _get_forecast_details(forecast)

    @intents.beta
    @intents.sentences(
        ["what is the (weather|forecast) [going to be] (on|for) [next] ($day_of_week:!int) night"]
    )
    def forecast_night(self, day_of_week):
        forecast = self._forecast_night(day_of_week)
        return _get_forecast_details(forecast)


# yeah, this one gets a little wild. We'll see how it develops over time.
def _get_forecast_details(forecast):
    if forecast["detailed_description"]:
        return forecast["detailed_description"]

    else:
        forecast_datetime = datetime.fromisoformat(forecast["datetime"])
        time_of_day = _get_forecast_time_of_day(forecast, forecast_datetime)
        weekday = _get_weekday(forecast["datetime"])
        forecast = f"The temperature will be {forecast['temperature']} on {weekday}"
        if time_of_day == TimeOfDay.NIGHT:
            forecast = forecast + " night"
        return forecast


def _get_weekday(isodate):
    return DAYS_OF_WEEK[datetime.fromisoformat(isodate).date().weekday()]
