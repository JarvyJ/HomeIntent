<script>
  export let settingsList;
  export let currentSetting;

  import Toggle from "$lib/components/Toggle.svelte";
  import { capitalize_with_underscore } from "$lib/util/capitalization";

</script>

<ul class="border m-4 rounded text-xl border-b-0">
  {#each Object.entries(settingsList) as [name, setting] (name)}
    <li class="py-2 px-3 border-b flex space-x-3" class:border-r-2="{name === currentSetting}" class:border-r-hi-green="{name === currentSetting}">
      <Toggle bind:enabled={setting.enabled} /><a class="flex-grow" href="/settings/{name}">{capitalize_with_underscore(name)}</a>
    </li>
  {/each}
</ul>
