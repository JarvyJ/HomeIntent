<script>
  export let currentSetting = ""
  export let settingsModel
  export let schema

  import DocumentationLink from "$lib/icons/file-earmark-text-link.svelte"
  import { capitalize_with_underscore } from "$lib/util/capitalization";
  import SettingsTitle from "./SettingsTitle.svelte";
  import Button from "$lib/components/Button.svelte";
  import SettingsList from "./SettingsList.svelte";
  import * as FormElement from "./form_elements"
  

  const humanSettingName = capitalize_with_underscore(currentSetting)
  const linkName = currentSetting.replace("_", "-")
</script>

<SettingsTitle>{humanSettingName} Settings <a href="/docs/integrations/{linkName}" target="_blank"><DocumentationLink /></a></SettingsTitle>

<SettingsList>
{#each Object.entries(schema.properties) as [name, field] (name)}
  <svelte:component this={FormElement[field.type]} {...field} bind:value="{settingsModel[currentSetting][name]}"/>
{/each}
</SettingsList>