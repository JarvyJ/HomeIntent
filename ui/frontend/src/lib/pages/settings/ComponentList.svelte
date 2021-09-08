<script>
  export let settingsList;
  export let currentSetting;

  import Toggle from "$lib/components/Toggle.svelte";

  function capitalize_with_underscore(name) {
    let words = name.split("_")
    for (var i = 0; i < words.length; i++) {
      words[i] = words[i][0].toUpperCase() + words[i].substring(1)
    }
    return words.join(" ")
  }
</script>

<ul class="border m-4 rounded text-xl border-b-0">
  {#each settingsList as setting (setting.name)}
    <li class="py-2 px-3 border-b flex space-x-3" class:border-r-2="{setting.name === currentSetting}" class:border-r-hi-green="{setting.name === currentSetting}">
      <Toggle /><a class="flex-grow" href="/settings/{setting.name}">{capitalize_with_underscore(setting.name)}</a>
    </li>
  {/each}
</ul>
