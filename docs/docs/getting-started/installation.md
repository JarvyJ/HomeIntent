# Getting Started

## Installation
Home Intent runs alongside Rhasspy to function. As such it is easy to get it started with a `docker-compose.yaml` file that runs both Home Intent and Rhasspy:

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
    image: "ghcr.io/jarvyj/homeintent:main"
    restart: unless-stopped
    volumes:
      - "/PATH_TO_CONFIG/config:/config"
    depends_on:
      - rhasspy

```

In your config folder, all you need to do is add a `config.yaml`, pointing to your Home Assistant URL and a "Long Lived Access" (bearer) token you can get from your [Home Assistant profile page](https://homeintent.jarvy.io/integrations/home-assistant/#getting-a-bearer-token):

```yaml
home_assistant:
  url: "https://home-assistant-url:8123"
  bearer_token: "eyJ0eXAiOiJKV1Q...**THE REST OF THE TOKEN**"

timer:

```

and just like that you have Home Intent setup and connected to Home Assistant! The wakeword Home Intent uses is "Jarvis". We have [example sentences](https://homeintent.jarvy.io/integrations/home-assistant/#example-sentences) on the integration page for all the components, but here are a few to get you started:

 * Jarvis, set timer one minute
 * Jarvis, turn on the kitchen light
 * Jarvis, add milk to the shopping list
 * Jarvis, set the bedroom light to red at 80%

