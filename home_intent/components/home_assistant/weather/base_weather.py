from datetime import datetime
from enum import Enum, auto

from home_intent import Intents

intents = Intents(__name__)


class TimeOfDay(Enum):
    DAY = auto()
    NIGHT = auto()


class BaseWeather:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("weather.")]
        self.entity = self.entities[0][
            "entity_id"
        ]  # just going to pick the first weather entity for now
        self.entity_with_forecast = next(
            x["entity_id"] for x in self.entities if x["attributes"].get("forecast") is not None
        )

    def _temperature_day(self):
        response = self.ha.api.get_entity(self.entity)
        return response

    def _forecast_today(self):
        response = self.ha.api.get_entity(self.entity_with_forecast)
        current_conditions = response["attributes"]["forecast"][0]
        return current_conditions

    def _forecast_tonight(self):
        response = self.ha.api.get_entity(self.entity_with_forecast)
        forecasts = response["attributes"]["forecast"]
        for forecast in forecasts:
            forecast_datetime = datetime.fromisoformat(forecast["datetime"])
            day_or_night = _get_forecast_time_of_day(forecast, forecast_datetime)
            if day_or_night == TimeOfDay.NIGHT:
                return forecast

    def _forecast_day(self, day_of_week):
        day_of_week = int(day_of_week)
        response = self.ha.api.get_entity(self.entity_with_forecast)
        forecast = _get_forecast(response["attributes"]["forecast"], TimeOfDay.DAY, day_of_week)
        return forecast

    def _forecast_night(self, day_of_week):
        day_of_week = int(day_of_week)
        response = self.ha.api.get_entity(self.entity_with_forecast)
        forecast = _get_forecast(response["attributes"]["forecast"], TimeOfDay.NIGHT, day_of_week)
        return forecast


def _get_forecast(forecasts, when: TimeOfDay, iso_weekday: int):
    for forecast in forecasts:
        forecast_datetime = datetime.fromisoformat(forecast["datetime"])
        if forecast_datetime.weekday() == iso_weekday:
            if _get_forecast_time_of_day(forecast, forecast_datetime) == when:
                return forecast


def _get_forecast_time_of_day(forecast, forecast_datetime) -> TimeOfDay:
    if "daytime" in forecast:
        if forecast["daytime"]:
            return TimeOfDay.DAY
        else:
            return TimeOfDay.NIGHT

    hour = forecast_datetime.time().hour
    if hour < 12:
        return TimeOfDay.DAY
    else:
        return TimeOfDay.NIGHT
