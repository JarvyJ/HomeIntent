import ciso8601
from home_intent import Intents

intents = Intents(__name__)

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class Weather:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("weather.")]
        self.entity = self.entities[0]  # just going to pick the first weather entity for now
        self.entity_with_forecast = [
            x for x in self.entities if x["attribute"].get("forecast") is not None
        ]

    @intents.slots
    def day_of_week(self):
        return DAYS_OF_WEEK

    @intents.sentences(["what is the temperature (right now|today|outside)"])
    def weather_day(self):
        response = self.ha.api.get_entity(self.entity)
        return f"The temperature is currently {response['attributes']['temperature']}"

    @intents.on_event("register_sentences")
    def handle_forecasting(self):
        if not self.entity_with_forecast:
            intents.disable_intent(self.forecast_today)
            intents.disable_intent(self.forecast_tonight)
            intents.disable_intent(self.forecast_day)
            intents.disable_intent(self.forecast_night)

    @intents.sentences(["what is the (weather|forecast) (right now|today|outside)"])
    def forecast_today(self):
        response = self.ha.api.get_entity(self.entity_with_forecast)
        current_conditions = response["attributes"]["forecast"][0]
        return _get_forecast(current_conditions)

    @intents.sentences(["what is the (weather|forecast) tonight"])
    def forecast_tonight(self):
        response = self.ha.api.get_entity(self.entity_with_forecast)
        forecasts = response["attributes"]["forecast"]
        for forecast in forecasts:
            if "daytime" in forecast:
                if not forecast["daytime"]:
                    return _get_forecast(forecast)

            else:
                hour = ciso8601.parse_datetime(forecast["datetime"]).time().hour
                if hour > 12:
                    return _get_forecast(forecast)

    @intents.sentences(
        ["what is the (weather|forecast) [going to be] (on|for) [next] ($day_of_week)"]
    )
    def forecast_day(self, day_of_week):
        response = self.ha.api.get_entity(self.entity_with_forecast)

    @intents.sentences(
        ["what is the (weather|forecast) [going to be] (on|for) [next] ($day_of_week) night"]
    )
    def forecast_night(self, day_of_week):
        response = self.ha.api.get_entity(self.entity_with_forecast)


def _get_forecast(forecast):
    if forecast["detailed_description"]:
        return forecast["detailed_description"]


def _get_weekday(isodate):
    return DAYS_OF_WEEK[ciso8601.parse_datetime(isodate).date().weekday()]
