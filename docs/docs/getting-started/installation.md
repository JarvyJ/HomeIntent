# Getting Started

## Supported Configs
Home Intent currently is designed to run in a docker container running on a Raspberry Pi 3B or 4 (armv7/arm64). We also offer a "server" build (amd64). Future installation options may be available in the future.

## Installation
It is easy to get it started with a `docker-compose.yaml` file that runs Home Intent:

```docker-compose
version: "3.9"

services:
  homeintent:
      image: "ghcr.io/jarvyj/homeintent:main"
      container_name: homeintent
      restart: unless-stopped
      volumes:
          - "/PATH_TO_CONFIG/rhasspy:/profiles"
          - "/PATH_TO_CONFIG/config:/config"
          - "/etc/localtime:/etc/localtime:ro"
      ports:
          - "12101:12101"
      devices:
          - "/dev/snd:/dev/snd"

```

The `/profiles` directory is where Rhasspy stores its configs/downloads. The ports expose the Rhasspy web interface, which is useful during debugging and for advanced users.

In your config folder, all you need to do is add a `config.yaml`, pointing to your Home Assistant URL and a "Long Lived Access" (bearer) token you can get from your [Home Assistant profile page](https://homeintent.jarvy.io/integrations/home-assistant/#getting-a-bearer-token):

```yaml
home_assistant:
  url: "https://home-assistant-url:8123"
  bearer_token: "eyJ0eXAiOiJKV1Q...**THE REST OF THE TOKEN**"

timer:

```

and just like that you have Home Intent setup and connected to Home Assistant! Plug in a USB Microphone, startup the containers, and you are good to go! The wakeword Home Intent uses is "Jarvis". We have [example sentences](https://homeintent.jarvy.io/integrations/home-assistant/#example-sentences) on the integration page for all the components, but here are a few to get you started:

 * Jarvis, set timer one minute
 * Jarvis, turn on the kitchen light
 * Jarvis, add milk to the shopping list
 * Jarvis, set the bedroom light to red at 80% brightness

## Audio Config
Home Intent will use the system defaults for speaker and microphone. However, if it's not responding or you don't hear any sounds, you may need to add the microphone or speaker to your `config.yaml`.

When Home Intent starts it will verify sentences and log out Rhasspy's microphone and sounds' devices:
```
 These are the attached microphones (the default has an asterisk):
 {
  "0": "HDA Intel PCH: CX8070 Analog (hw:0,0)",
  "1": "sysdefault",
  "10": "vdownmix",
  "11": "default*",
  "12": "dmix",
  "2": "Jabra SPEAK 410 USB: Audio (hw:1,0)",
  "3": "surround40",
  "4": "surround51",
  "5": "surround71",
  "6": "lavrate",
  "7": "samplerate",
  "8": "speexrate",
  "9": "upmix"
 }
```

```
 These are the attached sounds devices:
 {
  "default:CARD=PCH": "Default Audio Device",
  "default:CARD=Headphones": "Default Audio Device",
  "default:CARD=USB": "Default Audio Device",
  "default:CARD=vc4hdmi": "Default Audio Device",
  "dmix:CARD=PCH,DEV=0": "Direct sample mixing device",
  "dsnoop:CARD=PCH,DEV=0": "Direct sample snooping device",
  "front:CARD=PCH,DEV=0": "Front speakers",
  "hw:CARD=PCH,DEV=0": "Direct hardware device without any conversions",
  "jack": "JACK Audio Connection Kit",
  "null": "Discard all samples (playback) or generate zero samples (capture)*",
  "plughw:CARD=PCH,DEV=0": "Hardware device with all software conversions",
  "pulse": "PulseAudio Sound Server",
  "surround21:CARD=PCH,DEV=0": "2.1 Surround output to Front and Subwoofer speakers",
  "surround40:CARD=PCH,DEV=0": "4.0 Surround output to Front and Rear speakers",
  "surround41:CARD=PCH,DEV=0": "4.1 Surround output to Front, Rear and Subwoofer speakers",
  "surround50:CARD=PCH,DEV=0": "5.0 Surround output to Front, Center and Rear speakers",
  "surround51:CARD=PCH,DEV=0": "5.1 Surround output to Front, Center, Rear and Subwoofer speakers",
  "surround71:CARD=PCH,DEV=0": "7.1 Surround output to Front, Center, Side, Rear and Woofer speakers",
  "sysdefault:CARD=PCH": "Default Audio Device"
 }
```

!!!note
    For the sounds devices, you likely want one of the "default" devices. However, the `plughw` can sometimes make a fun chipmunk effect!

From the output above, you could change the microphone/speaker in the `rhasspy` config section in `config.yaml`. It uses the 'key' as the identifier:

```yaml
rhasspy:
  microphone_device: "2" # the 2 represents the "Jabra SPEAK 410 USB" above
  sounds_device: "default:CARD=USB"
```