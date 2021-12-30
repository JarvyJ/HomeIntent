<script>
  export let currentSetting = "";
  export let customComponent;
  export let userSettings;
  export let schema;

  import DocumentationLink from "$lib/icons/file-earmark-text-link.svelte";
  import { capitalize_with_underscore } from "$lib/util/capitalization";
  import SettingsTitle from "./SettingsTitle.svelte";
  import SettingsList from "./SettingsList.svelte";
  import * as FormElement from "./form_elements";

  const humanSettingName = capitalize_with_underscore(currentSetting);
  const linkName = currentSetting.replace("_", "-");

  console.log(schema)
</script>

<SettingsTitle
  >{humanSettingName} Settings {#if !customComponent}<a
      href="/docs/integrations/{linkName}"
      target="_blank"><DocumentationLink /></a
    >{/if}</SettingsTitle
>

<SettingsList>
  {#each Object.entries(schema.properties) as [name, field] (name)}
    <svelte:component
      this={FormElement[field.type]}
      {...field}
      bind:value={userSettings[currentSetting][name]}
      required={schema.required.includes(name)}
    />
  {/each}
</SettingsList>
