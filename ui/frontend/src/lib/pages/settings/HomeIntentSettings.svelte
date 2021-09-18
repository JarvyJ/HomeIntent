<style>
  .chevron-down{
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='%23404749' fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position-x: 94%;
    background-position-y: center;
  }
</style>

<script>
  export let userSettings
  export let currentSetting
  export let schema

  import { onMount } from "svelte";

  import { capitalize_with_underscore } from "$lib/util/capitalization";
  import PlayCircleFill from "$lib/icons/play-circle-fill.svelte";
  import BooleanInput from "./form_elements/boolean.svelte"
  import SettingsSection from "./SettingsSection.svelte";
  import Button from "$lib/components/Button.svelte";
  import SettingsTitle from "./SettingsTitle.svelte";
  import SettingsList from "./SettingsList.svelte";
  import MicFill from "$lib/icons/mic-fill.svelte";
  import HelpText from "./HelpText.svelte";

  let filesToUpload = {}
  let showAll = false
  let microphones = {}
  let speakers = {}
  let effects = {}
  let playbackMessage = "Click the play icon to test the audio device"
  let microphoneMessage = "Click the mic to test out the microphone"

  onMount(async () => {
    const mic_response = await fetch(`/api/v1/rhasspy/audio/microphones?showAll=${showAll}`);
    microphones = await mic_response.json();

    const speaker_response = await fetch(`/api/v1/rhasspy/audio/speakers?showAll=${showAll}`);
    speakers = await speaker_response.json();

    getSoundEffectInfo()
  });

  async function getSoundEffectInfo() {
    const effect_response = await fetch(`/api/v1/rhasspy/audio/effects`)
    effects = await effect_response.json()
  }

  async function playTestAudio() {
    playbackMessage = "Playing"
    let response
    if (userSettings.rhasspy.sounds_device) {
      response = await fetch(`/api/v1/rhasspy/audio/test-speakers?device=${userSettings.rhasspy.sounds_device}`)
    } else {
      response = await fetch(`/api/v1/rhasspy/audio/test-speakers`)
    }
    if (!response.ok) {
      playbackMessage = "Unable to play, try another playback device"
    } else {
      playbackMessage = "Finished Playing"
    }
  }

  async function recordAndPlayback() {
    microphoneMessage = "Recording..."
    microphoneMessage = "Playing Back..."
  }

  async function playSoundEffect(effect) {
    let response
    if (userSettings.rhasspy.sounds_device) {
      response = await fetch(`/api/v1/rhasspy/audio/play-effects?sound_effect=${effect}&device=${userSettings.rhasspy.sounds_device}`)
    } else {
      response = await fetch(`/api/v1/rhasspy/audio/play-effects?sound_effect=${effect}`)
    }
  }

  async function setDefaultSoundEffect(effect) {
    let response
      response = await fetch(`/api/v1/rhasspy/audio/set-default?sound_effect=${effect}`, {
      method: 'POST'})
    await getSoundEffectInfo()
  }

  async function uploadSoundEffect(event) {
    let data = new FormData()
    data.append('file', event.target.files[0])

    await fetch(`/api/v1/rhasspy/audio/effects?sound_effect=${event.target.name}`, {
      method: 'POST',
      body: data
    }) 
    await getSoundEffectInfo()

  }
</script>
<SettingsTitle>Home Intent Settings</SettingsTitle>

<SettingsList>
  <div>
    <label for="sounds-device" class="font-bold">Sounds Devices</label>
    <HelpText>The URL for your Home Assistant instance</HelpText>
  </div>

  <div>
    <select bind:value={userSettings.rhasspy.sounds_device} id="sounds-device" class="border chevron-down p-1.5 pr-8 border-gray-300 rounded-md appearance-none">
      {#each Object.entries(speakers) as [id, name] (id)}
      <option value="{id}">{name} ({id})</option>
      {/each}
    </select>
    <div>
      <span class="ml-3 cursor-pointer" on:click={playTestAudio}><PlayCircleFill /></span>
      <span>{playbackMessage}</span>
    </div>
  </div>

  <div>
    <label for="microphone-device" class="font-bold">Microphone Devices</label>
    <HelpText>The URL for your Home Assistant instance</HelpText>
  </div>

  <div>
    <select bind:value={userSettings.rhasspy.microphone_device} id="microphone-device" class="border chevron-down p-1.5 pr-8 border-gray-300 rounded-md appearance-none">
      {#each Object.entries(microphones) as [id, name] (id)}
      <option value="{id}">{name}</option>
      {/each}
    </select>
    <div>
      <span class="ml-3 cursor-pointer" on:click={recordAndPlayback}><MicFill /></span>
      <span>{microphoneMessage}</span>
    </div>
  </div>

  <BooleanInput title="Enable Beta Intents" description="Enable intents that are currently in beta to try out new features!"
  bind:value={userSettings.home_intent.enable_beta} />

  <BooleanInput title="Enable Dangerous Intents" description="Enable intents that are known to cause recognition issues (chaos mode)"
  bind:value={userSettings.home_intent.enable_all} />

</SettingsList>


<SettingsSection>Sound Effects</SettingsSection>

<div class="text-lg grid grid-cols-4 w-1/2 items-center gap-x-5 gap-y-6">

  {#each Object.entries(effects) as [name, meta] (name)}
    <span class="text-2xl cursor-pointer justify-self-end col-start-1" on:click="{() => playSoundEffect(name)}"><PlayCircleFill /></span>
    <div>
      <p class="">{capitalize_with_underscore(name)}</p>
      <HelpText>Using {capitalize_with_underscore(meta.custom_or_default)}</HelpText>
    </div>
    <label class="ml-auto rounded hover:bg-green-200 bg-hi-green px-3 py-1 cursor-pointer">
      <span>Upload</span>
      <input type="file" name={name}
       class="hidden" accept=".wav" on:change="{uploadSoundEffect}" />
    </label>
    {#if meta.custom_or_default === "custom"}
    <Button>
      <span on:click="{() => setDefaultSoundEffect(name)}">Use Default</span>
    </Button>
    {/if}
  {/each}

</div>
