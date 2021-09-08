<script>
  import ToggleOn from "$lib/icons/toggle-on.svelte";
  import ToggleOff from "$lib/icons/toggle-off.svelte";
  let enabled = false;
</script>

{#if enabled}
  <span class="" on:click="{() => enabled = !enabled}"><ToggleOff /></span>
{:else}
  <span class="text-hi-green" on:click="{() => enabled = !enabled}"><ToggleOn /></span>
{/if}