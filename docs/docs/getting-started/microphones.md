# Microphones
Home Intent can work with any USB powered microphone, however, it'll work best with microphones designed to pick up voice that can do some amount of background noise cancellation. A lot of times these are conference microphone "pucks" or custom built mic arrays.

Here are a few microphone options that are known to do well:

 * Jabra Speak 410 (the 510 has bluetooth, but will work wired just fine)
 * Playstation Eye Camera

Some older jabra firmwares have issues with muting/being found on Linux, but upgrading the firmware (using [Jabra Direct](https://www.jabra.com/software-and-services/jabra-direct)) will solve the problem. The irony being that Jabra Direct only runs on Mac/Windows, but the firmware fixes problems on Linux...

If you find any other microphones that perform well, let us know! I want to try out a microphone comparison at some point, and see what performs well at various price points.

## Pi Hat Support - Advanced
Home Intent can support some of the Raspberry Pi Hats. However, it can be a lot harder to setup and maintain a Pi hat (like a ReSpeaker) setup. They generally will use a kernel module to get the driver support working, but a lot of times on operating system will update the kernel and potentially break compatibility.

A lot of times the drivers aren't updated very frequently, so you have to try and find alternatives out on the internet. From there you will also need to configure audio settings (like microphone gain) more carefully (using alsa) to get the microphone working. If they support any leds, that will also have to be setup using something like [Hermes Led Control](https://github.com/project-alice-assistant/HermesLedControl)).

After setting all that up, you can now add the `sounds_device` and maybe `microphone_device` to the Rhasspy section in `config.yaml`.

```yaml
rhasspy:
    sounds_device: plughw:CARD=seeed2micvoicec,DEV=0 # if using a ReSpeaker, look for the device name with 'seeed'
```

If we ever end up shipping a full Operating System image for Home Intent, and I acquire a Pi hat microphone, I'll try to get some of this stuff baked in, but until then, you are on your own. Good luck!

Special thanks to Daenara for calling out some of the [complexities](https://community.rhasspy.org/t/how-im-integrating-between-rhasspy-and-home-assistant/3090/7) around using a microphone hat.
