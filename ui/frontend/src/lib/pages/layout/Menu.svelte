<script>
  export let menuExpanded;

  import { page } from "$app/stores";

  import DocsIcon from "$lib/icons/journal-richtext.svelte";
  import SettingsIcon from "$lib/icons/gear-fill.svelte";
  import SatellitesIcon from "$lib/icons/speaker.svelte";
  // import CustomizeIcon from "$lib/icons/tools.svelte";
  import LogsIcon from "$lib/icons/card-list.svelte";

  const pagesMeta = [
    { title: "Settings", url: "/settings/", icon: SettingsIcon },
    // {title: "Customize", url: "/customize", icon: CustomizeIcon},
    //{title: "Satellites", url: "/satellites", icon: SatellitesIcon},
    { title: "Logs", url: "/logs/", icon: LogsIcon },
  ];
</script>

<div class="pt-3">
  <ul class="text-xl" class:text-center={!menuExpanded}>
    {#each pagesMeta as pageMeta}
      <li
        class="p-2 m-1 rounded-lg hover:bg-hi-green"
        class:px-4={menuExpanded}
        class:mx-2={menuExpanded}
        class:dark:bg-gray-700={$page.url.pathname.startsWith(pageMeta.url.slice(0, -1))}
      >
        <a class="block" href={pageMeta.url}
          ><svelte:component this={pageMeta.icon} />
          {#if menuExpanded}
            <span class="ml-4">{pageMeta.title}</span>
          {/if}
        </a>
      </li>
    {/each}

    <li
      class="p-2 m-1 rounded-lg hover:bg-hi-green"
      class:px-4={menuExpanded}
      class:mx-2={menuExpanded}
    >
      <a class="block" href="/docs/" rel="external" target="_blank"
        ><DocsIcon />
        {#if menuExpanded}
          <span class="ml-4">Docs</span>
        {/if}
      </a>
    </li>
  </ul>
</div>
