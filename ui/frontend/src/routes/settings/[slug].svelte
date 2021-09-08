<script>
import {page} from '$app/stores';

import ComponentList from "$lib/pages/settings/ComponentList.svelte";
import Button from "$lib/components/Button.svelte"

import HomeIntentSettings from "$lib/pages/settings/HomeIntentSettings.svelte";
import HomeAssistantSettings from "$lib/pages/settings/HomeAssistantSettings.svelte";
import NoSettings from "$lib/pages/settings/NoSettings.svelte";


let settingsList = { 
  "home_intent": {component: HomeIntentSettings, enabled: true},
  "home_assistant": {component: HomeAssistantSettings, enabled: false},
  "timer": {component: NoSettings, enabled: true},
}

$: currentSetting = $page.params.slug

</script>

<nav class="flex items-center bg-gray-800 text-gray-50 px-4 py-3 border-b">
  <span class="font-semibold text-3xl">Settings</span>
  <Button>Save</Button>
</nav>

<div class="bg-gray-900 text-gray-50 grid grid-cols-5">
  <div class="h-screen">
    <ComponentList bind:settingsList bind:currentSetting/>
  </div>
  <div class="col-span-4 mt-5">
    {#key currentSetting}
    <svelte:component this={settingsList[currentSetting].component} bind:currentSetting/>
    {/key}
  </div>
</div>
