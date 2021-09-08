<style>
  :global(.bi) {
    display: inline-block;
    vertical-align: -.125em;
    width: 1em;
    height: 1em;
  }
</style>

<script>
  import "../app.postcss";
  import { page } from '$app/stores';

  import SettingsIcon from "../icons/gear-fill.svelte"
  import CustomizeIcon from "../icons/tools.svelte"
  import SatellitesIcon from "../icons/speaker.svelte"
  import LogsIcon from "../icons/card-list.svelte"
  import DocsIcon from "../icons/journal-richtext.svelte"
  import HomeIntentWhite from "../components/HomeIntentWhite.svelte"

  let visible = true;
  let navWidth = 256;

  $: if (visible) {
    navWidth = 256;
  } else {
    navWidth = 55;
  }

</script>

<nav class="border-r h-screen fixed bg-gray-800 text-gray-50" style="width: {navWidth}px;">    

  <div class="py-3 px-4 bg-hi-green border-b text-2xl">
    <span on:click="{() => visible = !visible}"><HomeIntentWhite /></span>
  {#if visible}
    Home Intent
  {/if}
  </div>

  <div class="pt-3">

    <ul class="text-xl">
      <li class="py-2 px-4 mx-2 rounded-lg hover:bg-hi-green" class:bg-gray-700="{$page.path === "/settings"}"><a class="block" href="/settings"><SettingsIcon />
        {#if visible}
          <span class="ml-4">Settings</span>
        {/if}
      </a></li>

      <li class="py-2 px-4 mx-2 rounded-lg hover:bg-hi-green" class:bg-gray-700="{$page.path === "/customize"}"><a class="block" href="/customize"><CustomizeIcon />
        {#if visible}
          <span class="ml-4">Customize</span>
        {/if}
      </a></li>

      <li class="py-2 px-4 mx-2 rounded-lg hover:bg-hi-green" class:bg-gray-700="{$page.path === "/satellites"}"><a class="block" href="/satellites"><SatellitesIcon />
        {#if visible}
          <span class="ml-4">Satellites</span>
        {/if}
      </a></li>

      <li class="py-2 px-4 mx-2 rounded-lg hover:bg-hi-green" class:bg-gray-700="{$page.path === "/logs"}"><a class="block" href="/logs"><LogsIcon />
        {#if visible}
          <span class="ml-4">Logs</span>
        {/if}
      </a></li>

      <li class="py-2 px-4 mx-2 rounded-lg hover:bg-hi-green" class:bg-gray-700="{$page.path === "/docs"}"><a class="block" href="/docs" target="_blank"><DocsIcon />
        {#if visible}
          <span class="ml-4">Docs</span>
        {/if}
      </a></li>
    </ul>
  </div>

</nav>


<main style="margin-left: {navWidth}px;">
<slot></slot>
</main>
