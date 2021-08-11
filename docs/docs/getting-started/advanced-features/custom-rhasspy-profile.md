# Custom Rhasspy Profile
A custom Rhasspy profile can be loaded for use in Home Intent. If there is a `/config/rhasspy_profile.json` file, Home Intent will load that, otherwise it'll use the default Rhasspy profile provided by Home Intent.

This can be useful if you want to change any of the internal Rhasspy settings, for example if testing different components for speech to text, intent recognition, text to speech, wakeword, etc that could become the defaults that Home Intent could use.

The profile is found by going to the Rhasspy advanced configuration page and pulling the json blob that is present there.
![rhasspy advanced profile](/img/rhasspy-advanced.png)