# Advanced Rhasspy Config
The default Rhasspy configuration is designed to work with the default [docker based installation](../installation.md#installation). The config most likely needed to be changed are the `microphone_device` and `sounds_device` options. However, Home Intent can be setup to work with an [external Rhasspy instance](./external-rhasspy.md).

Setting up the `microphone_device` and `sounds_device` is described in the [audio config section](../installation.md#audio-config).

## Rhasspy web interface
The Rhasspy web interface can be accessed at `http://localhost:12101` by default. It can be useful for debugging to see how things are configured.


## Configuration

| Option             | Description                                                          | Required/Default           |
|:-------------------|:---------------------------------------------------------------------|:---------------------------|
| url                | The URL for your Rhasspy instance                                    | `"http://localhost:12101"` |
| mqtt_host          | External MQTT host hooked up to Rhasspy and Home Intent              | `"localhost"`              |
| mqtt_port          | External MQTT port                                                   | `12183`                    |
| mqtt_username      | External MQTT username                                               |                            |
| mqtt_password      | External MQTT password                                               |                            |
| microphone_device  | The pyaudio device number representing the microphone                |                            |
| sounds_device      | The aplay device identifier for playing back sounds                  |                            |
| externally_managed | A boolean value to set if the Rhasspy instance is externally managed | `false`                    |


Example in `config.yaml`:
```yaml
rhasspy:
  microphone_device: 11
  sounds_device: "default:CARD=PCH"
```