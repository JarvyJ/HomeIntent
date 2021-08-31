from datetime import datetime
from enum import Enum, auto

from home_intent import Intents

intents = Intents(__name__)

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class TimeOfDay(Enum):
    DAY = auto()
    NIGHT = auto()


class Weather:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("weather.")]
        self.entity = self.entities[0][
            "entity_id"
        ]  # just going to pick the first weather entity for now
        self.entity_with_forecast = next(
            x["entity_id"] for x in self.entities if x["attributes"].get("forecast") is not None
        )

    @intents.dictionary_slots
    def day_of_week(self):
        return {x[1]: x[0] for x in enumerate(DAYS_OF_WEEK)}

    @intents.beta
    @intents.sentences(["what is the temperature [(right now|today|outside)]"])
    def temperature_day(self):
        response = self.ha.api.get_entity(self.entity)
        return f"The temperature is currently {response['attributes']['temperature']}"

    @intents.on_event("register_sentences")
    def handle_forecasting(self):
        if not self.entity_with_forecast:
            intents.disable_intent(self.forecast_today)
            intents.disable_intent(self.forecast_tonight)
            intents.disable_intent(self.forecast_day)
            intents.disable_intent(self.forecast_night)

    @intents.beta
    @intents.sentences(
        [
            "what is the (weather|forecast) (right now|today|outside)",
            "what is it like (right now|outside)",
            "how does it feel outside [right now]",
        ]
    )
    def forecast_today(self):
        response = self.ha.api.get_entity(self.entity_with_forecast)
        current_conditions = response["attributes"]["forecast"][0]
        return _get_forecast_details(current_conditions)

    @intents.beta
    @intents.sentences(
        ["what is the (weather|forecast) tonight", "(how|what) is it going to be [like] tonight"]
    )
    def forecast_tonight(self):
        response = self.ha.api.get_entity(self.entity_with_forecast)
        forecasts = response["attributes"]["forecast"]
        for forecast in forecasts:
            forecast_datetime = datetime.fromisoformat(forecast["datetime"])
            day_or_night = _get_forecast_time_of_day(forecast, forecast_datetime)
            if day_or_night == TimeOfDay.NIGHT:
                return _get_forecast_details(forecast)

    @intents.beta
    @intents.sentences(
        ["what is the (weather|forecast) [going to be] (on|for) [next] ($day_of_week:!int)"]
    )
    def forecast_day(self, day_of_week):
        day_of_week = int(day_of_week)
        response = self.ha.api.get_entity(self.entity_with_forecast)
        forecast = _get_forecast(response["attributes"]["forecast"], TimeOfDay.DAY, day_of_week)
        return _get_forecast_details(forecast)

    @intents.beta
    @intents.sentences(
        ["what is the (weather|forecast) [going to be] (on|for) [next] ($day_of_week:!int) night"]
    )
    def forecast_night(self, day_of_week):
        day_of_week = int(day_of_week)
        response = self.ha.api.get_entity(self.entity_with_forecast)
        forecast = _get_forecast(response["attributes"]["forecast"], TimeOfDay.NIGHT, day_of_week)
        return _get_forecast_details(forecast)


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
