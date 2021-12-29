<script>
  import { onMount } from "svelte";

  import LogControl from "$lib/pages/logs/LogControl.svelte";
  import LogAreas from "$lib/pages/logs/LogAreas.svelte";
  import PageLayout from "./PageLayout.svelte";
  import SettingsTitle from "$lib/pages/settings/SettingsTitle.svelte";

  let horizontal_split = true;
  let word_wrap = false;

  let exceptions = []
  let logs = []

  let show_logs = false;

  onMount(async () => {
    const exceptions_result = await fetch(`/api/v1/exceptions`);
    exceptions = await exceptions_result.json();

    const logs_result = await fetch(`/api/v1/logs`)
    logs = await logs_result.json();
  });
</script>

<PageLayout title="Logs">
  <svelte:fragment slot="sectionBar">
    <LogControl bind:horizontal_split bind:word_wrap />
  </svelte:fragment>

  <div class="p-4">
  <SettingsTitle>Exceptions</SettingsTitle>

  {#each exceptions as exception}
  <div class="mt-4">
    <p>{exception.data}</p>
    <p class="text-gray-400 text-sm"><a href="#{exception.time}" on:click="{() => show_logs = true}">{new Date(exception.time * 1000).toLocaleString()}</a> - <span class="text-pink-700">{exception.log_level}</span></p>
  </div>
  {/each}

  <button class="rounded hover:bg-green-700 bg-hi-green px-3 py-1 my-3" on:click={() => show_logs = !show_logs}>{#if show_logs}Hide{:else}View{/if} Logs</button>

  {#if show_logs}

  <pre class="text-sm wrap-control h-screen p-2 dark:bg-gray-700 dark:text-gray-50 rounded-md" class:whitespace-pre-wrap={word_wrap} class:pre={!word_wrap}><code>
  {#each logs as log}
    <br id={log.time}>{new Date(log.time * 1000).toLocaleString()} {log.log_level} {log.logger} {log.data}
  {/each}
  </code></pre>
  {/if}
<!-- 
  <div
    class:grid-cols-2={!horizontal_split}
    class:grid-cols-1={horizontal_split}
    class="grid justify-items-stretch w-full h-screen gap-5 p-5"
  >
    <LogAreas bind:word_wrap />
  </div> -->
</div>
</PageLayout>


<style>
  .wrap-control {
    overflow-x: scroll;
    overflow-wrap: normal;
    scroll-behavior: smooth;
  }
</style>
