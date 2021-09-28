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
  import { onMount } from 'svelte';

  import HomeIntentWhite from '$lib/components/HomeIntentWhite.svelte';
  import SectionBar from '$lib/components/SectionBar.svelte';
  import DocsIcon from '$lib/icons/journal-richtext.svelte';
  import SettingsIcon from '$lib/icons/gear-fill.svelte';
  import SatellitesIcon from '$lib/icons/speaker.svelte';
  import CustomizeIcon from '$lib/icons/tools.svelte';
  import LogsIcon from '$lib/icons/card-list.svelte';
  import List from '$lib/icons/list.svelte';

  let menuExpanded = true;
  let navWidth = 256;

  $: if (menuExpanded) {
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

  let isMobile = false;
  onMount(async () => {
    isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;
    if (isMobile) {
      menuExpanded = false;
    }
  });

</script>

<nav class="border-r border-gray-700 h-screen fixed bg-gray-900 text-gray-50" style="width: {navWidth}px;">
  <div class="py-3 px-4 bg-hi-green border-b border-gray-700 text-2xl">
    <span on:click="{() => menuExpanded = !menuExpanded}"><HomeIntentWhite /></span>
    {#if menuExpanded} Home Intent {/if}
  </div>

  <div class="pt-3">
    <ul class="text-xl" class:text-center={!menuExpanded}>
      {#each pagesMeta as pageMeta}
      <li
        class="p-2 m-1 rounded-lg hover:bg-hi-green"
        class:px-4={menuExpanded}
        class:mx-2={menuExpanded}
        class:bg-gray-700="{$page.path.startsWith(pageMeta.url)}"
      >
        <a class="block" href="{pageMeta.url}"
          ><svelte:component this="{pageMeta.icon}" />
          {#if menuExpanded}
          <span class="ml-4">{pageMeta.title}</span>
          {/if}
        </a>
      </li>
      {/each}
    </ul>
  </div>
</nav>

<main style="margin-left: {navWidth}px;">
  <div class="bg-gray-900 text-gray-50">
    <slot></slot>
  </div>
</main>
