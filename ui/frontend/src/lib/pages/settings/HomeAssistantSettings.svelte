<script>
  export let currentSetting = ""
  export let settingsModel

  import DocumentationLink from "$lib/icons/file-earmark-text-link.svelte"
  import SettingsTitle from "./SettingsTitle.svelte";
  import StringInput from "./form_elements/string.svelte"
  import BooleanInput from "./form_elements/boolean.svelte"
  import ArrayInput from "./form_elements/array.svelte"

  import { capitalize_with_underscore } from "$lib/util/capitalization";
  import Button from "$lib/components/Button.svelte";
import SettingsList from "./SettingsList.svelte";

  const humanSettingName = capitalize_with_underscore(currentSetting)
  const linkName = currentSetting.replace("_", "-")

</script>
<SettingsTitle>{humanSettingName} Settings <a href="/docs/integrations/{linkName}" target="_blank"><DocumentationLink /></a></SettingsTitle>

<SettingsList>
  <StringInput title="URL" description="The URL for your Home Assistant instance" format="uri" bind:value={settingsModel.home_assistant.url} />

  <StringInput title="Bearer Token" description="The long-lived access token that Home Intent uses to interact with Home Assistant"
    bind:value={settingsModel.home_assistant.bearer_token} />

  <BooleanInput title="Prefer Toggle" description="Prefer to toggle instead using on or off when handling intents" bind:checked="{settingsModel.home_assistant.prefer_toggle}" />

  <ArrayInput title="Entities to Ignore" description="A list of entities that shouldn't be controlled via Home Intent"
  example="{['light.kitchen', 'fan.attic', 'switch.tv']}" bind:value={settingsModel.home_assistant.ignore_entities} />

  <ArrayInput title="Domains to Ignore" description="A list of domains that shouldn't be controlled via Home Intent."
  example="{['shopping_list', 'light', 'remote']}" bind:value={settingsModel.home_assistant.ignore_domains} />
</SettingsList>

<div class="mt-5 text-xl">
  <Button>
    Save
  </Button>
</div>