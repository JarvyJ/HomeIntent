<script>
  export let enabled = false;
  import ToggleOn from "$lib/icons/toggle-on.svelte";
  import ToggleOff from "$lib/icons/toggle-off.svelte";
</script>

{#if enabled}
  <span class="text-hi-green" on:click="{() => enabled = !enabled}"><ToggleOn /></span>
{:else}
  <span class="" on:click="{() => enabled = !enabled}"><ToggleOff /></span>
{/if}