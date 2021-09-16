<script>
  export let currentSetting = ""
  import SettingsTitle from "./SettingsTitle.svelte";
  import DocumentationLink from "$lib/icons/file-earmark-text-link.svelte"
  

  import { capitalize_with_underscore } from "$lib/util/capitalization";
import Button from "$lib/components/Button.svelte";

  const humanSettingName = capitalize_with_underscore(currentSetting)
  const linkName = currentSetting.replace("_", "-")

</script>
<SettingsTitle>{humanSettingName} Settings <a href="/docs/integrations/{linkName}" target="_blank"><DocumentationLink /></a></SettingsTitle>

<p>There are no settings associated with the {humanSettingName} component. It can only be enabled/disabled via the toggle.</p>
