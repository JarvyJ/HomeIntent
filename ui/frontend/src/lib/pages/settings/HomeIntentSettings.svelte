<style>
  .chevron-down{
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='%23404749' fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position-x: 94%;
    background-position-y: center;
  }
</style>

<script>
  import PlayCircleFill from "$lib/icons/play-circle-fill.svelte";
  import Button from "$lib/components/Button.svelte";
  import SettingsSection from "./SettingsSection.svelte";
  import Checkbox from "./Checkbox.svelte";
  import SettingsTitle from "./SettingsTitle.svelte";
  import SelectDropdown from "./SelectDropdown.svelte";
  import HelpText from "./HelpText.svelte";

  let selectedSoundsDevice = ""
  let selectedMicrophoneDevice = ""

</script>
<SettingsTitle>Home Intent Settings</SettingsTitle>

<div class="grid grid-cols-2 w-3/4 gap-6">
  <div>
    <label for="sounds-device" class="font-bold">Sounds Devices</label>
    <HelpText>The URL for your Home Assistant instance</HelpText>
  </div>

  <div>
    <select id="sounds-device" class="border chevron-down p-1.5 pr-8 border-gray-300 rounded-md appearance-none">
      <option>default:CARD=USB</option>
      <option>default:CARD=Headphones</option>
      <option>jack</option>
    </select>
    <span class="ml-3"><PlayCircleFill /></span>
    <progress class="bg-gray-300 w-96 mt-3 text-xs rounded-full" max="100" value="70">70%</progress>
  </div>

  <div>
    <label for="microphone-device" class="font-bold">Microphone Devices</label>
    <HelpText>The URL for your Home Assistant instance</HelpText>
  </div>

  <div>
    <select id="microphone-device" class="border chevron-down p-1.5 pr-8 border-gray-300 rounded-md appearance-none">
      <option>plughw</option>
      <option>Default device</option>
      <option>Something Else</option>
    </select>
    <progress class="bg-gray-300 w-96 mt-3 text-xs rounded-full" max="100" value="70">70%</progress>
  </div>

  <div>
    <label for="story" class="font-bold">Enable Beta Intents</label>
    <HelpText>Enable intents that are currently in beta to try out new features!</HelpText>
  </div>
  <Checkbox>Enable Beta Intents</Checkbox>


  <div>
    <label for="story" class="font-bold">Enable Dangerous Intents</label>
    <HelpText>Enable intents that are known to cause recognition issues (chaos mode)</HelpText>
  </div>
  <Checkbox>Enable Dangerous Intents</Checkbox>

</div>


<SettingsSection>Sound Effects</SettingsSection>

<div class="text-lg grid grid-cols-4 w-1/2 items-center gap-x-5 gap-y-6">
  <span class="justify-self-end"><PlayCircleFill /></span>
  <div>
    <p class="">Beep High</p>
    <HelpText>Using Default</HelpText>
  </div>
  <Button>
    Upload
  </Button>

  <span class="justify-self-end col-start-1"><PlayCircleFill /></span>
  <div>
    <p class="">Beep Low</p>
    <HelpText>Using Default</HelpText>    
  </div>
  <Button>
    Upload
  </Button>

  <span class="justify-self-end col-start-1"><PlayCircleFill /></span>
  <div>
    <p class="">Error</p>
    <HelpText>Using Custom</HelpText>
  </div>
  <Button>
    Upload
  </Button>
  <Button>
    Use Default
  </Button>

</div>


<div class="mt-5 text-xl">
  <Button>
    Save
  </Button>
</div>