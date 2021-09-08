<script>
  export let currentSetting = ""
  import SettingsTitle from "./SettingsTitle.svelte";

  import { capitalize_with_underscore } from "$lib/util/capitalization";

  const humanSettingName = capitalize_with_underscore(currentSetting)
  const linkName = currentSetting.replace("_", "-")

</script>
<SettingsTitle>{humanSettingName} Settings</SettingsTitle>

<p>There are no settings associated with the {humanSettingName} component. It can only be enabled/disabled via the toggle.</p>
<p><a href="/docs/integrations/{linkName}">Documentation for the {humanSettingName} component</a></p>