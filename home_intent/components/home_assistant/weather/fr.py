from datetime import datetime

from .base_weather import BaseWeather, TimeOfDay, _get_forecast_time_of_day, intents

DAYS_OF_WEEK = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


class Weather(BaseWeather):
    @intents.dictionary_slots
    def weather_day_of_week(self):
        return {x[1]: x[0] for x in enumerate(DAYS_OF_WEEK)}

    @intents.on_event("register_sentences")
    def handle_forecasting(self):
        if not self.entity_with_forecast:
            intents.disable_intent(self.forecast_today)
            intents.disable_intent(self.forecast_tonight)
            intents.disable_intent(self.forecast_day)
            intents.disable_intent(self.forecast_night)

    @intents.beta
    @intents.sentences(["Quel [est|sera] la température [(en ce moment|aujourd'hui|extérieure)]"])
    def temperature_day(self):
        response = self._temperature_day()
        return f"La température actuelle est {response['attributes']['temperature']}"

    @intents.beta
    @intents.sentences(
        [
            "Quel est la [météo|température] (en ce moment|aujourd'hui|extérieure)",
            "Quel temps fait il [à] (maintenant|extérieure)",
            "Comment se sent on à l'extérieur [en ce moment]",
        ]
    )
    def forecast_today(self):
        current_conditions = self._forecast_today()
        return _get_forecast_details(current_conditions)

    @intents.beta
    @intents.sentences(
        ["Quel [temps|température] fait il ce soir", "Quel sera (la) (le) [température|météo] ce soir"]
    )
    def forecast_tonight(self):
        forecast = self._forecast_tonight()
        return _get_forecast_details(forecast)

    @intents.beta
    @intents.sentences(
        ["Quel (est|sera) la (météo|température) ($weather_day_of_week:!int) [prochain]"]
    )
    def forecast_day(self, weather_day_of_week):
        forecast = self._forecast_day(weather_day_of_week)
        return _get_forecast_details(forecast)

    @intents.beta
    @intents.sentences(
        [
            "Quel (est|sera) la (météo|température) ($weather_day_of_week:!int) [soir prochain]"
        ]
    )
    def forecast_night(self, weather_day_of_week):
        forecast = self._forecast_night(weather_day_of_week)
        return _get_forecast_details(forecast)


# yeah, this one gets a little wild. We'll see how it develops over time.
def _get_forecast_details(forecast):
    if forecast["detailed_description"]:
        return forecast["detailed_description"]

    else:
        forecast_datetime = datetime.fromisoformat(forecast["datetime"])
        time_of_day = _get_forecast_time_of_day(forecast, forecast_datetime)
        weekday = _get_weekday(forecast["datetime"])
        forecast = f"La température sera de {forecast['temperature']} {weekday} prochain"
        if time_of_day == TimeOfDay.NIGHT:
            forecast = forecast + " soirt"
        return forecast


def _get_weekday(isodate):
    return DAYS_OF_WEEK[datetime.fromisoformat(isodate).date().weekday()]
