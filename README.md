# Home Intent
Home Intent is an open source locally hosted intent handler. Using [Rhasspy](https://rhasspy.readthedocs.io) and integrating with [Home Assistant](https://www.home-assistant.io/) it functions as an easy-to-use voice assistant for your home.

Home Intent wants to close the gap to make it easier to setup a voice assistant that integrates with Home Assistant. All you need to do is plug in a microphone/speaker, deploy the application, and pass it a Home Assistant API key to get it going. It goes through your Home Assistant configuration, finds entities, and sets up Rhasspy for you. Home Intent shows the user what it's found and how it's setup so users can either extend the configurations (like adding custom words to a shopping list), setup word aliases, or disable entities from working with voice. The goal is to have an easy to use interface to make it all happen.

Home Intent wants to avoid the problem of asking for a light to turn on and only one bulb in a fixture turns on or the fuzzy match in Home Assistant picks the wrong thing. By integrating between Home Assistant and Rhasspy, Home Intent has much better control over the entity and voice system and will hopefully work very reliably.


## Integrations
To start off we are planning to integrated heavily with Home Assistant and offer some simple local additional integrations (like setting timers). This way anything that is configured in Home Assistant can be surfaced in Home Intent.

In the future, we want to be able to integrate with various services (like Wikipedia or WolframAlpha) to create a fully featured voice assistant. Users will be able to configure which integrations are in use and we plan to indicate if the integration runs locally, connects to an API, or can be self hosted - so users will have a choice as to how Home Intent works.

## Setup
Home Intent runs alongside Rhasspy and to function. As such it is easy to get it started with a docker-compose file that runs both Home Intent and Rhasspy:

```docker-compose
version: "3"

services:
  rhasspy:
      image: "rhasspy/rhasspy"
      container_name: rhasspy
      restart: unless-stopped
      volumes:
          - "/PATH_TO_CONFIG/rhasspy:/profiles"
          - "/etc/localtime:/etc/localtime:ro"
      ports:
          - "12101:12101"
      devices:
          - "/dev/snd:/dev/snd"
      command: --user-profiles /profiles --profile en
  
  home_intent:
    image: "homeintent"
    restart: unless-stopped
    volumes:
      - "/PATH_TO_CONFIG/config:/config"
    depends_on:
      - rhasspy

```


