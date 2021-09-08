<script>
  import PlayCircleFill from "../../icons/play-circle-fill.svelte";
  import Button from "../../components/Button.svelte";
  import SettingsSection from "./SettingsSection.svelte";
import Checkbox from "./Checkbox.svelte";

</script>
<h2 class="text-3xl mb-3">Home Intent Settings</h2>

<style>
  .chevron-down{
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='%23404749' fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position-x: 94%;
  background-position-y: center;
}
</style>


<div class="mx-auto w-4/5">
  <div class="mt-5 flex items-center space-x-3">
  <label for="sounds-devices">Sounds Device</label>
  <select id="sounds-devices" class="border chevron-down p-1.5 pr-8 border-gray-300 rounded-md appearance-none">
    <option>default:CARD=USB</option>
    <option>default:CARD=Headphones</option>
    <option>jack</option>
  </select>
  <span class=""><PlayCircleFill /></span>
  </div>

  <progress class="bg-gray-300 w-96 mt-3 text-xs rounded-full" max="100" value="90">90%</progress>

  <div class="mt-5 flex items-center space-x-3">
  <label for="microphone-devices">Microphone Device</label>
  <select id="sounds-devices" class="border chevron-down p-1.5 pr-8 border-gray-300 rounded-md appearance-none">
    <option>plughw</option>
    <option>Default device</option>
    <option>Something else</option>
  </select>
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
    <p class="text-xs text-gray-500">Using Default</p>
  </div>
  <Button>
    Upload
  </Button>

  <span class="justify-self-end col-start-1"><PlayCircleFill /></span>
  <div>
    <p class="">Beep Low</p>
    <p class="text-xs text-gray-500">Using Default</p>
  </div>
  <Button>
    Upload
  </Button>

  <span class="justify-self-end col-start-1"><PlayCircleFill /></span>
  <div>
    <p class="">Error</p>
    <p class="text-xs text-gray-500">Using Custom</p>
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