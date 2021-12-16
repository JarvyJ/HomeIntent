import logging

LOGGER = logging.getLogger(__name__)


def run(home_intent):
    slot_update = {
        "color": [],
        "color_temperature": [],
        "cover_close": [],
        "cover_close_tilt": [],
        "cover_open": [],
        "cover_open_tilt": [],
        "cover_set_position": [],
        "cover_set_tilt_position": [],
        "cover_stop": [],
        "day_of_week": [],
        "directional_fan": [],
        "openable_lock": [],
        "oscillating_fan": [],
        "preset_fan": [],
        "preset_mode": [],
        "shopping_item": [],
        "speed_fan": [],
        "timer_partial_time": [],
    }

    if "home_assistant" in home_intent.settings:
        LOGGER.info("Found previous version using Home Assistant. Clearing up unused values")
        home_intent.rhasspy_api.post("/api/slots?overwriteAll=true", body=slot_update)
    else:
        LOGGER.info("Nothing to do. Moving on!")
