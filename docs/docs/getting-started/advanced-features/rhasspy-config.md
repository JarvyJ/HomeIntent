# Advanced Rhasspy Config
The default Rhasspy configuration is designed to work with the default [docker based installation](/getting-started/installation/#installation). The config most likely needed to be changed are the `microphone_device` and `sounds_device` options. However, Home Intent can be setup to work with an external Rhasspy instance via the config.

Setting up the `microphone_device` and `sounds_device` is described in the [audio config section](/getting-started/installation/#audio-config).

## Connecting to an external Rhasspy instance
Home Intent manages Rhasspy via the REST API and interacts with the intents via MQTT. The default configuration is setup to use docker-compose, however, if Home Intent is pointed at the Rhasspy URL and MQTT server that Rhasspy uses it can interact with the external system.

This can also be helpful for doing local development on Home Intent itself.

## Configuration

| Option            | Description                                             | Required/Default         |
|:------------------|:--------------------------------------------------------|:-------------------------|
| url               | The URL for your Rhasspy instance                       | `"http://rhasspy:12101"` |
| mqtt_host         | External MQTT host hooked up to Rhasspy and Home Intent | `"rhasspy"`              |
| mqtt_port         | External MQTT port                                      | `12183`                  |
| mqtt_username     | External MQTT username                                  |                          |
| mqtt_password     | External MQTT password                                  |                          |
| microphone_device | The pyaudio device number representing the microphone   |                          |
| sounds_device     | The aplay device identifier for playing back sounds     |                          |

Example:
```yaml
rhasspy:
  microphone_device: 11
  sounds_device: "default:CARD=PCH"
  url: "http://localhost:12101"
  mqtt_host: "localhost"
  mqtt_port: 1883

```