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

<div class="mx-auto w-4/5">
  <div class="mt-5 flex items-center space-x-3">
    <SelectDropdown name="Sounds Device" values={["default:CARD=USB", "default:CARD=Headphones", "jack"]} bind:selectedValue={selectedSoundsDevice}/>
    <span class=""><PlayCircleFill /></span>
  </div>

  <progress class="bg-gray-300 w-96 mt-3 text-xs rounded-full" max="100" value="90">90%</progress>

  <div class="mt-5 flex items-center space-x-3">
    <SelectDropdown name="Microphone Device" values={["plughw", "Default device", "Something else"]} bind:selectedValue={selectedMicrophoneDevice}/>
  </div>
  
  <progress class="bg-gray-300 w-96 mt-3 text-xs rounded-full" max="100" value="70">70%</progress>


</div>

<Checkbox>Enable All Intents</Checkbox>
<Checkbox>Enable Beta Intents</Checkbox>

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