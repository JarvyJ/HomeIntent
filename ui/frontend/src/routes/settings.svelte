<script>
  import { onMount } from 'svelte';

  import ComponentList from '$lib/pages/settings/ComponentList.svelte';
  import Button from '$lib/components/Button.svelte';
  import Spinner from '$lib/icons/spinner.svelte';

  import HomeIntentSettings from '$lib/pages/settings/HomeIntentSettings.svelte';
  import NoSettings from '$lib/pages/settings/NoSettings.svelte';
  import AutoSettings from '$lib/pages/settings/AutoSettings.svelte';
  import SectionBar from '$lib/components/SectionBar.svelte';
  import { mergeDeep } from '$lib/util/merge.js';
  import PageLayout from './PageLayout.svelte';

  let loaded = false;
  let customSettingsList = {};

  let settingsList = {
    home_intent: { component: HomeIntentSettings, enabled: true, schema: null }
  };
  let currentSetting = 'home_intent';

  let openapi = {};
  let userSettings;
  let componentsWithoutSettings;
  let customComponents;

  onMount(async () => {
    const res = await fetch(`/openapi.json`);
    openapi = await res.json();

    let fullSettings = openapi.components.schemas.FullSettings;
    componentsWithoutSettings = new Set(
      fullSettings.additionalProperties['x-components-without-settings']
    );
    customComponents = new Set(fullSettings.additionalProperties['x-custom-components']);

    setupComponentList('#/components/schemas/FullSettings');
    setupComponentsWithoutSettings();

    await reloadUserSettings();
  });

  function setupComponentList(fullSchemaName) {
    let schemaName = getSchemaName(fullSchemaName);
    let schema = openapi.components.schemas[schemaName];

    for (const name in schema.properties) {
      if ('$ref' in schema.properties[name]) {
        let settingSchemaName = getSchemaName(schema.properties[name]['$ref']);
        let settingSchema = openapi.components.schemas[settingSchemaName];
        if (name in settingsList) {
          settingsList[name].schema = settingSchema;
        } else {
          if (customComponents.has(name)) {
            // hopefully this will work for folks.
            customSettingsList[name] = {
              component: AutoSettings,
              enabled: false,
              schema: settingSchema
            };
          } else {
            settingsList[name] = { component: AutoSettings, enabled: false, schema: settingSchema };
            // rhasspy is default enabled
            if (name === 'rhasspy') {
              settingsList[name].enabled = true;
            }
          }
        }
      }
    }
  }

  function getSchemaName(fullSchemaName) {
    return fullSchemaName.split('/').pop();
  }

  function setupComponentsWithoutSettings() {
    for (const settingName of componentsWithoutSettings) {
      if (customComponents.has(settingName)) {
        customSettingsList[settingName] = { component: NoSettings, enabled: false, schema: null };
      } else {
        settingsList[settingName] = { component: NoSettings, enabled: false, schema: null };
      }
    }
  }

  async function reloadUserSettings() {
    loaded = false;
    userSettings = generateDefaultUserSettings('#/components/schemas/FullSettings');

    const settings_response = await fetch(`/api/v1/settings`);
    if (settings_response.ok) {
      let settings = await settings_response.json();
      mergeUserSettings(settings);
      enableUsersSettings(settings);
    }

    loaded = true;
  }

  function generateDefaultUserSettings(fullSchemaName) {
    let schemaName = getSchemaName(fullSchemaName);
    let schema = openapi.components.schemas[schemaName];
    let model = {};
    for (const name in schema.properties) {
      if ('$ref' in schema.properties[name]) {
        model[name] = generateDefaultUserSettings(schema.properties[name]['$ref']);
      } else if ('default' in schema.properties[name]) {
        model[name] = schema.properties[name]['default'];
      } else {
        model[name] = null;
      }
    }

    return model;
  }

  function mergeUserSettings(settings) {
    // did this setting by setting to enable them correctly
    // also could've just done a mergeDeep at the root, but it gets screwy
    // because of the `null` meaning two different things...
    for (const setting in settings) {
      if (settings[setting]) {
        mergeDeep(userSettings[setting], settings[setting]);
      } else if (componentsWithoutSettings.has(setting)) {
        userSettings[setting] = null;
      }
    }
  }

  function enableUsersSettings(settings) {
    for (const setting in settings) {
      enableSetting(setting);
    }
  }

  function enableSetting(setting) {
    if (customComponents.has(setting)) {
      customSettingsList[setting].enabled = true;
    } else {
      settingsList[setting].enabled = true;
    }
  }

  async function restart() {
    let response = await fetch('/api/v1/restart');
    if (response.status === 400) {
      let result = await response.json();
      console.log(result);
    }
  }

  async function saveSettings() {
    // create a settings copy, so the bound userSettings doesn't get modified (and break the UI)
    // when submitting the settings. We'll do a full reload after save.
    // TODO: popup a modal to confirm save
    let settingsCopy = JSON.parse(JSON.stringify(userSettings)); // safe to do as it's all JSON
    disableUnusedSettings(settingsCopy);
    enableComponentsWithoutSettings(settingsCopy);
    console.log(settingsCopy);

    let response = await fetch('/api/v1/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(settingsCopy)
    });
    if (response.ok) {
      let result = await response.json();
      await reloadUserSettings();
      console.log(result);
      await restart();
    }
  }

  function disableUnusedSettings(settings) {
    for (const setting in settings) {
      if (customComponents.has(setting)) {
        if (customSettingsList[setting].enabled === false) {
          delete settings[setting];
        }
      } else {
        if (settingsList[setting].enabled === false) {
          delete settings[setting];
        }
      }
    }
  }

  function enableComponentsWithoutSettings(settings) {
    for (const [name, meta] of Object.entries(settingsList)) {
      if (componentsWithoutSettings.has(name) && meta.enabled) {
        settings[name] = null;
      }
    }

    for (const [name, meta] of Object.entries(customSettingsList)) {
      if (componentsWithoutSettings.has(name) && meta.enabled) {
        settings[name] = null;
      }
    }
  }
</script>

<PageLayout title="Settings">
  <svelte:fragment slot="sectionBar">
    <div class="flex items-center gap-3 ml-auto">
      <span
        class="rounded hover:bg-red-700 bg-red-500 px-3 py-1 cursor-pointer"
        on:click="{restart}"
        >Restart</span
      >
      <button
        class="rounded hover:bg-green-700 bg-hi-green px-3 py-1 disabled:opacity-50 disabled:cursor-not-allowed"
        on:click="{saveSettings}"
        disabled={currentSetting in settingsList ? !settingsList[currentSetting].enabled : !customSettingsList[currentSetting].enabled}
      >
        Save
      </button>
    </div>
  </svelte:fragment>

  {#if loaded}
  <div class="grid grid-cols-5">
    <div>
      <ComponentList bind:settingsList bind:currentSetting />
      {#if Object.keys(customSettingsList).length !== 0}
      <h3 class="text-2xl ml-5 mt-7">Custom Components</h3>
      <ComponentList bind:settingsList="{customSettingsList}" bind:currentSetting />
      {/if}
    </div>
    <div class="col-span-4 mt-5">
      {#if currentSetting in settingsList}
      <svelte:component
        this="{settingsList[currentSetting].component}"
        bind:currentSetting
        bind:userSettings
        bind:schema="{settingsList[currentSetting].schema}"
        customComponent="{false}"
      />
      <button
        class="rounded hover:bg-green-700 bg-hi-green px-3 py-1 mt-5 text-xl disabled:opacity-50 disabled:cursor-not-allowed"
        on:click="{saveSettings}"
        disabled={!settingsList[currentSetting].enabled}
      >
        Save
      </button>
      {#if !settingsList[currentSetting].enabled}
        <span class="ml-2">Ensure the integration is enabled before saving!</span>
      {/if}
      {:else if currentSetting in customSettingsList}
      <svelte:component
        this="{customSettingsList[currentSetting].component}"
        bind:currentSetting
        bind:userSettings
        bind:schema="{customSettingsList[currentSetting].schema}"
        customComponent="{true}"
      />
      <button
        class="rounded hover:bg-green-700 bg-hi-green px-3 py-1 mt-5 text-xl disabled:opacity-50 disabled:cursor-not-allowed"
        on:click="{saveSettings}"
        disabled={!customSettingsList[currentSetting].enabled}
      >
        Save
      </button>
      {#if !customSettingsList[currentSetting].enabled}
        <span class="ml-2">Ensure the integration is enabled before saving!</span>
      {/if}
      {/if}
    </div>
  </div>
  {/if}
</PageLayout>
