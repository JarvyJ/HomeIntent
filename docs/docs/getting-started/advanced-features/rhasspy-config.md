# Advanced Rhasspy Config
The default Rhasspy configuration is designed to work with the default [docker based installation](/getting-started/installation/#installation). The config most likely needed to be changed are the `microphone_device` and `sounds_device` options. However, Home Intent can be setup to work with an external Rhasspy instance via the config.

Setting up the `microphone_device` and `sounds_device` is described in the [audio config section](/getting-started/installation/#audio-config).

## Rhasspy web interface
The Rhasspy web interface can be accessed at `http://localhost:12101` by default. It can be useful for debugging to see how things are configured.

## Home Intent Sound Effects (Beeps)
Home Intent uses custom beep sound effects for interaction. You can override them with your own beep sounds by adding the sound files to your config folder.

 * Beep high: `/config/beep-high.wav`
 * Beep low: `/config/beep-low.wav`
 * Error: `/config/error.wav`


## Connecting to an external Rhasspy instance
Home Intent manages Rhasspy via the REST API and interacts with the intents via MQTT. The default configuration is setup to use docker-compose, however, if Home Intent is pointed at the Rhasspy URL and MQTT server that Rhasspy uses it can interact with the external system.

This can also be helpful for doing local development on Home Intent itself.

## Configuration

| Option            | Description                                             | Required/Default           |
|:------------------|:--------------------------------------------------------|:---------------------------|
| url               | The URL for your Rhasspy instance                       | `"http://localhost:12101"` |
| mqtt_host         | External MQTT host hooked up to Rhasspy and Home Intent | `"localhost"`              |
| mqtt_port         | External MQTT port                                      | `12183`                    |
| mqtt_username     | External MQTT username                                  |                            |
| mqtt_password     | External MQTT password                                  |                            |
| microphone_device | The pyaudio device number representing the microphone   |                            |
| sounds_device     | The aplay device identifier for playing back sounds     |                            |
| homeintent_beeps  | Whether to use homeintent beeps (True) or Rhasspy beeps | `True`                     |

!!!note
    To use Home Intent beeps, Rhasspy and Home Intent need to be running in the same container.
    So, if you have separate Rhasspy and Home Intent instances, the Home Intent beeps will not work and should be set to `False`.

Example:
```yaml
rhasspy:
  microphone_device: 11
  sounds_device: "default:CARD=PCH"
  url: "http://my-custom-rhasspy-instance:12101"
  mqtt_host: "my-custom-mqtt-host"
  mqtt_port: 1883

```