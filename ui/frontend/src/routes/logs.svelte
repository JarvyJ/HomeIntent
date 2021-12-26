<script>
  import LogControl from "$lib/pages/logs/LogControl.svelte";
  import LogAreas from "$lib/pages/logs/LogAreas.svelte";
  import PageLayout from "./PageLayout.svelte";

  let horizontal_split = true;
  let word_wrap = true;
</script>

<PageLayout title="Live Logs">
  <svelte:fragment slot="sectionBar">
    <LogControl bind:horizontal_split bind:word_wrap />
  </svelte:fragment>

  <div
    class:grid-cols-2={!horizontal_split}
    class:grid-cols-1={horizontal_split}
    class="grid justify-items-stretch w-full h-screen gap-5 p-5"
  >
    <LogAreas bind:word_wrap />
  </div>
</PageLayout>
