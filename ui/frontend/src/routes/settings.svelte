<script>
  import { onMount } from 'svelte';

  import ComponentList from "$lib/pages/settings/ComponentList.svelte";
  import Button from "$lib/components/Button.svelte"

  import HomeIntentSettings from "$lib/pages/settings/HomeIntentSettings.svelte";
  import HomeAssistantSettings from "$lib/pages/settings/HomeAssistantSettings.svelte";
  import NoSettings from "$lib/pages/settings/NoSettings.svelte";


  let loaded = false
  let customSettingsList = {}

  let settingsList = { 
    "home_intent": {component: HomeIntentSettings, enabled: false},
    "home_assistant": {component: HomeAssistantSettings, enabled: false},
  }
  let currentSetting = "home_intent"

  let openapi = {}
  let settings = {}
  let settingsModel

  function setupComponentsWithoutSettings() {
    let fullSettings = openapi.components.schemas.FullSettings

    for (const settingName of fullSettings.additionalProperties["x-components-without-settings"]) {
     
      if (fullSettings.additionalProperties["x-custom-components"].includes(settingName)) {
        customSettingsList[settingName] = {component: NoSettings, enabled:false}
      } else {
        settingsList[settingName] = {component: NoSettings, enabled: false}
      }
    }
  }

  function generateSettingsModel(full_schema_name) {
    let schema_name = full_schema_name.split("/").pop()
    let schema = openapi.components.schemas[schema_name]
    let model = {}
    for (const name in schema.properties) {
      if ("$ref" in schema.properties[name]) {
        model[name] = generateSettingsModel(schema.properties[name]["$ref"])
      } else if ("default" in schema.properties[name]) {
        model[name] = schema.properties[name]["default"]
      } else {
        model[name] = null
      }
    }

    return model
  }

  // The following functions are from stack overflow https://stackoverflow.com/a/34749873
  /**
   * Simple object check.
   * @param item
   * @returns {boolean}
   */
  function isObject(item) {
    return (item && typeof item === 'object' && !Array.isArray(item));
  }

  /**
   * Deep merge two objects.
   * @param target
   * @param ...sources
   */
  function mergeDeep(target, ...sources) {
    if (!sources.length) return target;
    const source = sources.shift();

    if (isObject(target) && isObject(source)) {
      for (const key in source) {
        if (isObject(source[key])) {
          if (!target[key]) Object.assign(target, { [key]: {} });
          mergeDeep(target[key], source[key]);
        } else {
          Object.assign(target, { [key]: source[key] });
        }
      }
    }

    return mergeDeep(target, ...sources);
  }

  // this does get re-called after the SPA is loaded
  // so it ends up calling this methods twice.
  // i could probably move them to a store and get only if they don't exist.
  // TODO: I might do that later.
  onMount(async () => {
    const res = await fetch(`/openapi.json`);
    openapi = await res.json();

    setupComponentsWithoutSettings()
    settingsModel = generateSettingsModel("#/components/schemas/FullSettings")
    console.log(settingsModel)
    
    const settings_response = await fetch(`/api/v1/settings`);
    if (settings_response.ok) {
      settings = await settings_response.json();
      // mergeDeep(settingsModel, settings)
    }
    
    // console.log(settingsModel)

    for (const setting in settingsModel) {
      if (setting in settingsList) {
        settingsList[setting].enabled = true
      } else if (setting in customSettingsList) {
        customSettingsList[setting].enabled = true
      }
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
    {#if Object.keys(customSettingsList).length !== 0}
    <h3 class="text-2xl ml-5 mt-7">Custom Components</h3>
    <ComponentList bind:settingsList={customSettingsList} bind:currentSetting/>
    {/if}
  </div>
  <div class="col-span-4 mt-5">
    {#key currentSetting}
    {#if currentSetting in settingsList}
      <svelte:component this={settingsList[currentSetting].component} bind:currentSetting bind:settingsModel/>
    {:else if currentSetting in customSettingsList}
      <svelte:component this={customSettingsList[currentSetting].component} bind:currentSetting/>
    {/if}
    {/key}
  </div>
</div>
{/if}