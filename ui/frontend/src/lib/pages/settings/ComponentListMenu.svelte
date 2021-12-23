<script>
  export let settingsList;
  export let currentSetting;
  export let customSettingsList;

  import ComponentList from "$lib/pages/settings/ComponentList.svelte";
</script>

<div>
  <ComponentList bind:settingsList bind:currentSetting />
  {#if Object.keys(customSettingsList).length !== 0}
    <h3 class="text-2xl ml-5 mt-7">Custom Components</h3>
    <ComponentList bind:settingsList={customSettingsList} bind:currentSetting />
  {/if}
</div>
