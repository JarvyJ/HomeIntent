<style>
  :global(.bi) {
    display: inline-block;
    vertical-align: -0.125em;
    width: 1em;
    height: 1em;
  }
</style>

<script>
  import '../app.postcss';
  import { page } from '$app/stores';

  import SettingsIcon from '$lib/icons/gear-fill.svelte';
  import CustomizeIcon from '$lib/icons/tools.svelte';
  import SatellitesIcon from '$lib/icons/speaker.svelte';
  import LogsIcon from '$lib/icons/card-list.svelte';
  import DocsIcon from '$lib/icons/journal-richtext.svelte';
  import HomeIntentWhite from '$lib/components/HomeIntentWhite.svelte';
  import SectionBar from '$lib/components/SectionBar.svelte';

  let visible = true;
  let navWidth = 256;

  $: if (visible) {
    navWidth = 256;
  } else {
    navWidth = 55;
  }

  const pagesMeta = [
    { title: 'Settings', url: '/settings', icon: SettingsIcon },
    // {title: "Customize", url: "/customize", icon: CustomizeIcon},
    // {title: "Satellites", url: "/satellites", icon: SatellitesIcon},
    { title: 'Live Logs', url: '/logs', icon: LogsIcon },
    { title: 'Docs', url: '/docs/', icon: DocsIcon }
  ];

  $: currentPage = pagesMeta.filter((meta) => $page.path.startsWith(meta.url))[0].title;
</script>

<nav class="border-r h-screen fixed bg-gray-800 text-gray-50" style="width: {navWidth}px;">
  <div class="py-3 px-4 bg-hi-green border-b text-2xl">
    <span on:click="{() => visible = !visible}"><HomeIntentWhite /></span>
    {#if visible} Home Intent {/if}
  </div>

  <div class="pt-3">
    <ul class="text-xl">
      {#each pagesMeta as pageMeta}
      <li
        class="py-2 px-4 mx-2 rounded-lg hover:bg-hi-green"
        class:bg-gray-700="{$page.path.startsWith(pageMeta.url)}"
      >
        <a class="block" href="{pageMeta.url}"
          ><svelte:component this="{pageMeta.icon}" />
          {#if visible}
          <span class="ml-4">{pageMeta.title}</span>
          {/if}
        </a>
      </li>
      {/each}
    </ul>
  </div>
</nav>

<main style="margin-left: {navWidth}px;">
  <slot></slot>
</main>
