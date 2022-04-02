# So, how well does it work?
Pretty well, and it's only getting better!

The biggest issue we face right now is that when the wakeword mistriggers, Home Intent will always _try_ to do something, and the next thing you know there's a random timer that's been set or the foyer light has turned fuschia. This happens because the system _only_ knows the words from the sentence structures and slot names.

The second issue we currently face is that it works well if the sentences programmed in line up with what you say, but if you start deviating it can cause issues.

However if it does hear you correctly, and the intents line up, it'll perform the action just fine!

## How are we planning to make it better?
Newer versions of Rhasspy support some fun options around detecting unknown words, so an intent can still trigger if it gets most of the words right or will fail if the sentence is too far off. It works by adding everyday words to the model so the intent recognizer can better determine if an intent needs to be handled or not. This should help both of the problems above by hopefully allowing some deviation and better recognition overall.

Finally, one of the easier things to change the wakeword sensitivity. Ideally we would have a database that matches up microphones to what sensitivity to use, but that requires a bit of tuning. Maybe this will end up being a Rhasspy setting down the road and we could have an interface to help tune it.

Regardless, Home Intent relies on a lot of different underlying software to keep it going, and as they get better and more mature, so does Home Intent. We are always trying out the latest features and want to push the envelope and provide the best experience we can.

## What else is planned?
We're also excited about "stop" words, so the user can say "cancel" or "nevermind" and Home Intent will just stop trying to execute on an intent. This will definitely come in a future version. **1/2022 Update:** We tried this out and with default settings, it slowed down intent recognition to below acceptable levels. We'll try it again in the future and spend some time tweaking it to see what happens!

Apart from intent handling, we want to create a UI to make it easier to set up and get going like helping to choose microphone/speakers, edit settings, and maybe even support some of the wilder customization options. **1/2022 Update:** the UI can now set mic/speakers and edit component settings!

Eventually we'll have Satellite support and make Home Intent installable as a hass.io addon. This will allow a lot of folks to easily get up and running and create a whole home voice automation solution.

And finally, while Home Intent is great for controlling things around the smart home, it currently doesn't do a lot on getting statuses back. It's a bit of a delicate balance of adding in things that are useful without compromising the ability to change things. I could see maybe getting back what temperature the HVAC is at would be useful, but a light bulbs not as much. Home Assistant also keeps track of _A LOT_ of things informationally (air quality, sensors, device\_trackers, etc), so knowing what to add can be kind've hard as we're always trying to keep system confusion to a minimum.

So stay tuned, there's a lot of work to be done!
