# External Rhasspy Setup

Home Intent can work with a pre-existing Rhasspy setup. It will automatically update slots, add sentences to `intents/home_intent.ini`, and retrain Rhasspy after initialization all based on whatever integrations are enabled. It just needs to point to where the Rhasspy instance is and be connected to its MQTT instance.

Here's an example `docker-compose` setup with how to get it going:

```docker-compose
version: "3.9"

services:
  homeintent:
      image: "ghcr.io/jarvyj/homeintent-rhasspy-external:main"
      container_name: homeintent
      restart: unless-stopped
      volumes:
          - "/PATH_TO_CONFIG/config:/config"
          - "/etc/localtime:/etc/localtime:ro"
      ports:
          - "11102:11102"
```

From there, in the `rhasspy` section of `config.yaml`, you need to set `externally_managed` to `true`, and connect it to your Rhasspy and MQTT instance.

```yaml
rhasspy:
  externally_managed: true
  url: "http://my-custom-rhasspy-instance:12101"
  mqtt_host: "my-custom-mqtt-host"
  mqtt_port: 1883
```

Notably, the `microphone_device` and `sounds_device` Rhasspy settings will no longer take effect and setting custom sound effects will not work. But you can always change those with the normal Rhasspy settings.

From there you can [finish setting up](../installation.md#setup) integration via the UI or `config.yaml`.