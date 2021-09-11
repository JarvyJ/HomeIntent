<script>
  import { onMount } from 'svelte';

  import ComponentList from "$lib/pages/settings/ComponentList.svelte";
  import Button from "$lib/components/Button.svelte"

  import HomeIntentSettings from "$lib/pages/settings/HomeIntentSettings.svelte";
  import HomeAssistantSettings from "$lib/pages/settings/HomeAssistantSettings.svelte";
  import NoSettings from "$lib/pages/settings/NoSettings.svelte";


  let settingsList = { 
    "home_intent": {component: HomeIntentSettings, enabled: false},
    "home_assistant": {component: HomeAssistantSettings, enabled: false},
  }

  let currentSetting = "home_intent"

  let openapi = {}
  let settings = {}

  let loaded = false

  // this does get re-called after the SPA is loaded
  // so it ends up calling this methods twice.
  // i could probably move them to a store and get only if they don't exist.
  // TODO: I might do that later.
  onMount(async () => {
    const res = await fetch(`/openapi.json`);
    openapi = await res.json();

    const settings_response = await fetch(`/api/v1/settings`);
    settings = await settings_response.json();

    let fullSettings = openapi.components.schemas.FullSettings
    for (const settingName of fullSettings.additionalProperties["x-components-without-settings"]) {
      settingsList[settingName] = {component: NoSettings, enabled: false}
    }
    loaded = true
  });

</script>

<nav class="flex items-center bg-gray-800 text-gray-50 px-4 py-3 border-b">
  <span class="font-semibold text-3xl">Settings</span>
  <Button>Save</Button>
</nav>

{#if loaded}
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
{/if}