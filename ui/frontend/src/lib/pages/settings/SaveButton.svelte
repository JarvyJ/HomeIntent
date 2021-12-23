<script>
  export let menu = false;
  export let settingsList;
  export let customSettingsList;
  export let currentSetting;

  export let saveSettings;

  $: disabled =
    currentSetting in settingsList
      ? !settingsList[currentSetting].enabled
      : !customSettingsList[currentSetting].enabled;
</script>

<button
  class="rounded hover:bg-green-700 bg-hi-green px-3 py-1 disabled:opacity-50 disabled:cursor-not-allowed"
  class:mt-5={!menu}
  class:text-xl={!menu}
  on:click={saveSettings}
  {disabled}
>
  Save
</button>
{#if !menu}
  {#if disabled}
    <span class="ml-2">Ensure the integration is enabled before saving!</span>
  {/if}
{/if}
