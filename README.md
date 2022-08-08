# Home Intent

![Home Intent Logo](/.github/home-intent-logo.png)

Home Intent is an open source locally hosted intent handler. Using [Rhasspy](https://rhasspy.readthedocs.io) and integrating with [Home Assistant](https://www.home-assistant.io/) it functions as an easy-to-use voice assistant for your home.

Documentation is at [https://homeintent.io](https://homeintent.io).

For discussions/support, go to [Github Discussions](https://github.com/JarvyJ/HomeIntent/discussions).

Issues are in the issue tracker!

## Installation
Home Intent can easily be installed via docker compose:
```yaml
version: "3.9"

services:
  homeintent:
    image: "ghcr.io/jarvyj/homeintent:latest"
    restart: unless-stopped
    volumes:
      - "/PATH_TO_CONFIG/rhasspy:/profiles"
      - "/PATH_TO_CONFIG/config:/config"
      - "/etc/localtime:/etc/localtime:ro"
    ports:
      - "11102:11102"  # For the Home Intent UI
      - "12183:12183"  # For communicating over MQTT/satellites
      - "12101:12101"  # For the Rhasspy UI (optional)
    devices:
      - "/dev/snd:/dev/snd"
```

From there, you can go to the UI on port `11102` and finish setting up and get going. We have full [docs](https://homeintent.io/getting-started/installation/) on getting started with more details if needed!


## Integrations

  * [Home Assistant](https://homeintent.io/integrations/home-assistant/)
    * Climate, cover, fan, group, humidifier, light, lock, media player, remote, shopping list, and switch are all supported!
    * Customizable script control!
  * [Timer](https://homeintent.io/integrations/timer/)

We have some ideas around more integrations, if you have any suggestions, feel free to throw it in the [GitHub Discussions](https://github.com/JarvyJ/HomeIntent/discussions).

## Ideology
Home Intent wants to avoid the problem of asking for a light to turn on and only one bulb in a fixture turns on because the fuzzy match picked the wrong thing. By integrating directly between Home Assistant and Rhasspy with easy customizations, Home Intent has better control over the entity and voice systems so voice interactions work more reliably.

## Translations
Home Intent now supports translations, but we don't have any yet! If you know a little python and want to help out, feel free to read up on [translating components](https://homeintent.io/reference/translations/translating-components/) and lend a hand!
