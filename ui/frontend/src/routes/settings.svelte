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
  let settingsModel
  let componentsWithoutSettings
  let customComponents

  function setupComponentsWithoutSettings() {
    for (const settingName of componentsWithoutSettings) {

      if (customComponents.has(settingName)) {
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

  function enableSetting(setting) {
    if (customComponents.has(setting)) {
      customSettingsList[setting].enabled = true
    } else {
      settingsList[setting].enabled = true
    }
  }

  function mergeCurrentSettingsIntoModel(settings) {
    // did this setting by setting to enable them correctly
    // also could've just done a mergeDeep at the root, but it gets screwy
    // because of the `null` meaning two different things...
   for (const setting in settings) {
    if (settings[setting]) {
      mergeDeep(settingsModel[setting], settings[setting])
        if (setting === "rhasspy") { continue; } // rhasspy settings are actually lumped into home_intent
        enableSetting(setting)
      } else if (componentsWithoutSettings.has(setting)) {
        settingsModel[setting] = null
        enableSetting(setting)
      }
    } 
  }

  onMount(async () => {
    const res = await fetch(`/openapi.json`);
    openapi = await res.json();

    let fullSettings = openapi.components.schemas.FullSettings
    componentsWithoutSettings = new Set(fullSettings.additionalProperties["x-components-without-settings"])
    customComponents = new Set(fullSettings.additionalProperties["x-custom-components"])

    setupComponentsWithoutSettings()
    settingsModel = generateSettingsModel("#/components/schemas/FullSettings")
    
    const settings_response = await fetch(`/api/v1/settings`);
    if (settings_response.ok) {
      let settings = await settings_response.json();
      mergeCurrentSettingsIntoModel(settings)
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