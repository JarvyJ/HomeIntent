<style>
  .text-area {

  }
</style>

<script>
  export let currentSetting = ""
  import DocumentationLink from "$lib/icons/file-earmark-text-link.svelte"
  import SettingsTitle from "./SettingsTitle.svelte";
  import InputText from "./InputText.svelte";

  import { capitalize_with_underscore } from "$lib/util/capitalization";
  import HelpText from "./HelpText.svelte";
  import Checkbox from "./Checkbox.svelte";

  const humanSettingName = capitalize_with_underscore(currentSetting)
  const linkName = currentSetting.replace("_", "-")

</script>
<SettingsTitle>{humanSettingName} Settings <a href="/docs/integrations/{linkName}" target="_blank"><DocumentationLink /></a></SettingsTitle>


<div class="grid grid-cols-2 w-3/4 gap-6">
  <div>
    <label for="input" class="font-bold">URL</label>
    <HelpText>The URL for your Home Assistant instance</HelpText>
  </div>
  <input id="url" type="text" class="border border-gray-300 rounded-md focus:outline-none p-1.5">

  <div>
    <label for="story" class="font-bold">Bearer Token</label>
    <HelpText>The long-lived access token that Home Intent uses to interact with Home Assistant</HelpText>
    <HelpText classes="mt-3">Instructions on <a href="/docs/integrations/home-assistant/#getting-a-bearer-token" target="_blank">getting a bearer token</a></HelpText>
  </div>

  <textarea id="story" name="story" class="text-area border border-gray-300 rounded-md focus:outline-none p-1.5"
  rows="5" cols="40" placeholder="Paste your bearer token here. It should start with 'ey'"></textarea>

  <div>
    <label for="story" class="font-bold">Prefer Toggle</label>
    <HelpText>Prefer to toggle instead using on or off when handling intents</HelpText>
    <HelpText classes="mt-3">Reason to use <a href="/docs/integrations/home-assistant/#on-prefer_toggle" target="_blank">prefer toggle</a></HelpText>
  </div>
  <Checkbox>Prefer Toggle</Checkbox>

  <div class="col-start-1">
    <label for="ignore-entities" class="font-bold">Entities to Ignore</label>
    <HelpText>A list of entities that shouldn't be controlled via Home Intent</HelpText>
    <HelpText classes="mt-3">
      Example:
      <code class="block p-2 bg-gray-300 rounded-md"><pre>
light.kitchen
fan.attic
switch.tv
      </pre></code>
    </HelpText>
  </div>

  <textarea id="ignore-entities" name="ignore-entities" class="text-area border border-gray-300 rounded-md focus:outline-none p-1.5"
  rows="5" cols="40" placeholder="Entities should be separated by newlines"></textarea>

  <div>
    <label for="ignore-domains" class="font-bold">Domains to Ignore</label>
    <HelpText>A list of domains that shouldn't be controlled via Home Intent.</HelpText>
    <HelpText classes="mt-3">
      Example:
      <code class="block p-2 bg-gray-300 rounded-md"><pre>
shopping_list
light
remote
      </pre></code>
    </HelpText>
  </div>

  <textarea id="ignore-domains" name="ignore-domains" class="text-area border border-gray-300 rounded-md focus:outline-none p-1.5"
  rows="5" cols="40" placeholder="Domains should be separated by newlines"></textarea>


</div>
