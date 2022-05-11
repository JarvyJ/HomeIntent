# Satellites

Home Intent now has basic satellite support (released as of 4/2022)! It's a bit more of a manual setup at the moment, so experience with Rhasspy is recommended.


## Setting up the Satellite
You can follow the Rhasspy site's [installation](https://rhasspy.readthedocs.io/en/latest/installation/) page to get the satellite installed on a Raspberry Pi. I've successfully used satellites on Raspberry Pi 0, 3, and 4. After it's been installed, the satellite needs to be configured to point at the main Home Intent instance. The Rhasspy UI should be at the IP address of the server it's running on at port `12101`.

You can start by putting in a `siteId` at the top of the settings page. I like to name it where the satellite is (in this case `kitchen`).

![Rhasspy Settings Page with siteId visible](../../img/rhasspy-ui/settings_overall.png){width="600"}


The MQTT should point at the IP Address that Home Intent is running on, and the associated MQTT port (`12183` - ensure the port is exposed from Docker, this is the case if you're using our provided `docker-compose` file.)

![Rhasspy MQTT Settings](../../img/rhasspy-ui/settings_mqtt.png){width="300"}

From there, you can setup the microphone and UDP audio in the "Audio Recording" section. The "Test" button next to the Audio Device will narrow down the mic list if the default does't work. The UDP Audio host is set to `127.0.0.1` and the port is `12202`.

![Rhasspy Audio Recording Settings](../../img/rhasspy-ui/settings_audio-recording.png){width="600"}

Then the "Wakeword" setup. Home Intent uses "Porcupine" with the "Jarvis" wakeword, but any of the other ones should work as well. Regardless of the wakeword chosen, ensure that the `UDP Audio (input)` field matches what was in the "Audio Recording" section, so `127.0.0.1:12202` in our case. The ensures the audio is streamed correctly from the Microphone to the Wakeword service _locally_ and not over _MQTT_.

![Rhasspy Wake Word Settings](../../img/rhasspy-ui/settings_wake-word.png){width="600"}

From here, the "Speech to Text", "Intent Recognition", "Text to Speech", and "Dialogue Management" can all be set to "Hermes MQTT". The Home Intent base station will handle all of this and "Intent Handling" to **disabled** as Home Intent will handle the intents!

![the rest of the Rhasspy Settings set to Hermes MQTT and Intent Handling set to disabled](../../img/rhasspy-ui/settings_boxed.png){width="600"}


The "Audio Playing" section can be used to configure an audio playback device as needed if the default doesn't work for your setup. Below I've set it to use the USB device (a Jabra Speakerphone).

![Rhasspy Audio Playing Settings](../../img/rhasspy-ui/settings_audio-playing.png){width="600"}


From there, save and let Rhasspy restart, there's just a bit more configuration needed on the Home Intent side to finish up.

There are other ways to setup Rhasspy as a satellite, but we've found this to work well and be relatively easy to configure. It performs the Wakeword recognition on device (which works fine, even on a Raspberry Pi 0!), and then streams audio packets over MQTT to the base station. This helps the MQTT server not get bogged down with constantly streamed audio. 



## Configuring Home Intent for Satellites
Home Intent and the Satellite will run on two different servers and Home Intent needs to be aware of the Satellite id. You can add a `rhasspy` section to your `config.yaml` and specify the satellite id's in a list.


In the `config.yaml` file
```yaml
rhasspy:
  satellite_ids:
   - kitchen
  disable_audio_at_base_station: true
```

There is also the option to disable audio at the base station (`disable_audio_at_base_station`) which can be set to `true` if you are not using the base station to record and playback audio. We've noticed that Rhasspy doesn't like starting up if there isn't a microphone device detected, so be sure to disable the audio at the base station unless a microphone is plugged in.

## Testing and Troubleshooting Satellites
After Home Intent and the Rhasspy satellite are configured, you can say the wakeword and see if it all works. If not double check the site id, the UDP audio settings, and the MQTT options. It also could be an issue with the Microphone/Playback device not getting picked up correctly.

There are a couple of things you can do in order to help troubleshoot from the Rhasspy homepage:

 1. If you put type a command in the "Recognize" box (like "Turn on the living room light") and it works, that means that your MQTT settings are correct and the satellite has a connection to the base station. If it doesn't, double check the MQTT settings and make sure the port `12183` is properly mapped from the Docker container.
 2. After, if you put some words in the "Speak" box and click the "Speak" button and don't hear anything, check the "Audio Playing" settings and try a different audio device.
 3. Once you have a playback device, and you're not sure if the mic works, click the "Wake Up" on the homepage and try speaking after you hear the Wakeword sound. If it times out and doesn't pick up what you're saying, go to the "Audio Recording" setting and try another device. Also double check the "UDP Audio (Output)" `host` and `port` are correct and match what's in the "Wakeword" UDP Audio (Input).

## Future of Satellites
We'll likely get around to adding satellite id names and disabling the audio from the base station in the UI. From there I really wanted to have Home Intent do more auto-setup of Satellites (and even started creating a [dedicated OS](https://github.com/JarvyJ/Rhasspy-Satellite) for a Rhasspy base station), but with the changes coming to Rhasspy, I've dropped the dedicated OS for now. I may still go back and do auto-configuring of satellites at some point.
