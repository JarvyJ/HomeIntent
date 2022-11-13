<script>
  import { onMount } from "svelte";

  import RestartButton from "$lib/pages/settings/RestartButton.svelte";
  import SaveButton from "$lib/pages/satellites/SaveButton.svelte";
  import PageLayout from "$lib/PageLayout.svelte";
  import SettingsTitle from "$lib/pages/settings/SettingsTitle.svelte";
  import SettingsList from "$lib/pages/settings/SettingsList.svelte";
  import BooleanInput from "$lib/pages/settings/form_elements/boolean.svelte";
  import ArrayInput from "$lib/pages/settings/form_elements/array.svelte";

  let errors = [];
  let loaded = false;
  let userSettings;

  async function restart() {
    let response = await fetch("/api/v1/restart");
    if (response.status === 400) {
      let result = await response.json();
      console.log(result);
    }
  }

  async function reloadUserSettings() {
    loaded = false;

    const settings_response = await fetch(`/api/v1/settings`);
    if (settings_response.ok) {
      let settings = await settings_response.json();
    }

    loaded = true;
  }

  async function saveSettings() {
    // create a settings copy, so the bound userSettings doesn't get modified (and break the UI)
    // when submitting the settings. We'll do a full reload after save.
    // TODO: popup a modal to confirm save
    let settingsCopy = JSON.parse(JSON.stringify(userSettings)); // safe to do as it's all JSON
    console.log(settingsCopy);

    let response = await fetch("/api/v1/settings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
      },
      body: JSON.stringify(settingsCopy),
    });
    if (response.ok) {
      errors = [];
      let result = await response.json();
      await reloadUserSettings();
      console.log(result);
      await restart();
    } else if (response.status == 422) {
      let result = await response.json();
      let error_messages = [];
      // console.log(result)
      for (const detail of result.detail) {
        detail.loc.shift();
        let message = detail.msg;
        console.log(detail.type);
        if (detail.type === "value_error.url.scheme") {
          message = "missing http or https";
        }
        let error_message = detail.loc.join(" -> ") + ": " + message;
        error_messages.push(error_message);
      }
      errors = error_messages;
    }
  }

  onMount(async () => {
    await reloadUserSettings();
  });
</script>

<PageLayout title="Satellites">
  <svelte:fragment slot="sectionBar">
    <div class="flex items-center gap-3 ml-auto">
      <RestartButton restart={restart} />
      <SaveButton
        menu={true}
        saveSettings={saveSettings}
      />
    </div>
  </svelte:fragment>
  <div class="p-4">
    <SettingsTitle>Home Intent Settings</SettingsTitle>
    <SettingsList>      
      {#if loaded}
        <BooleanInput 
          title="Disable Audio at Base Station" 
          description="If the base station will not be handling intents, you can check this box to disable audio controls on the base. It should also be checked if there isn't a microphone plugged into the base station." />

        <ArrayInput
          title="Unmanaged Satellite IDs"
          description="A list of satellite ids for any satellites that are not managed by Home Intent. This could be for microcontrollers or a custom Rhasspy setup"
          value={["esp32_kitchen"]}
        />
      {/if}
    </SettingsList>
  </div>

  {#if errors.length > 0}
    <div class="mt-4 text-red-600">
      {#each errors as error}
        <p>{error}</p>
      {/each}
    </div>
  {/if}
</PageLayout>

<style>

</style>
