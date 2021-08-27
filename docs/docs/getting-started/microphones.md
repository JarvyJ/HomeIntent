# Microphones
Home Intent can work with any USB powered microphone, however, it'll work best with microphones designed to pick up voice that can do some amount of background noise cancellation. A lot of times these are conference microphone "pucks" or custom built mic arrays.

Here are a few microphone options that are known to do well:

 * Jabra Speak 410 (the 510 and other bluetooth options are more trouble than they are worth)
 * Playstation Eye Camera

## Pi Hat Support
Home Intent can support the following Raspberry Pi Hats.
 
 * ReSpeaker 4 Mic Array
 * ReSpeaker 2 Mics Pi HAT

You need to install the ReSpeaker [drivers](https://rhasspy.readthedocs.io/en/latest/tutorials/#respeaker-drivers) on your main Raspberry Pi and set the microphone device to `plughw:CARD=seeed2micvoicec,DEV=0` in the Rhasspy section in `config.yaml`

```yaml
rhasspy:
    sounds_device: plughw:CARD=seeed2micvoicec,DEV=0
```

We haven't tested the settings personally, but they are known to work well with Rhasspy. Let us know if they do or don't work with Home Intent!

If you find any other microphones that can do well, let us know! I want to try out a microphone comparison at some point, but that will likely come a bit later.
