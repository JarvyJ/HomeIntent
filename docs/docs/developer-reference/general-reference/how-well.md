# So, how well does it work?
Pretty well, and we are trying to get better!

The biggest issue we face right now is that when the wakeword mistriggers, Home Intent will always _try_ to do something, and the next thing you know there's a random timer that's been set or the foyer light has turned fuschia. This happens because the system _only_ knows the words from the sentence structures and slot names.

However if it does hear you correctly, and the intents line up, it'll perform the action just fine. Honestly, sometimes we're surprised at how well it works.

## How are planning to make it better?
Newer versions of Rhasspy support some fun options around detecting unknown words, so an intent might not trigger if it doesn't hear it properly. This adds everyday words to the model so the intent recognizer can better determine if an intent needs to be handled.

There is also support for "stop" words, so the user can say "cancel" or "nevermind" and Home Intent will just stop trying to execute on an intent.

Finally, one of the easier things is to change the wakeword sensitivity. Ideally we would have a database that matches up microphones to what sensitivity to use, but that requires a bit of tuning. Maybe this will end up being a Rhasspy setting down the road or maybe we'll have an interface to help tune it.

Regardless, Home Intent relies on a lot of different underlying software to keep it going, and as they get better and more mature, so does Home Intent. We always want to push the envelope and provide the best experience we can.
