# Satellites - NYI

_NOTE: Satellites are **Not Yet Implemented**_

Rhasspy supports satellites, so there can be one main instance that handles all the intents and other "satellite" instances that will listen for the wake word and stream audio.

As always, Home Intent wants to make configuring setups as easy as possible. We still need to look into and try out how we'd want this to work. There are MQTT options as well as remote rhasspy options, with options to run on an [ESP32](https://github.com/Romkabouter/ESP32-Rhasspy-Satellite), or Raspberry Pis. A while back, we even tried a Pi Zero W that seemed to do okay!

There is a lot of information in the Rhasspy [docs](https://rhasspy.readthedocs.io/en/latest/search.html?q=satellite) on various satellite configurations. If you are feeling adventurous, you can probably experiment with a [custom rhasspy profile](/getting-started/advanced-features/custom-rhasspy-profile/) and let us know how it goes!