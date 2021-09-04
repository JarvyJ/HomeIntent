<script>
  import ToggleOn from "../icons/toggle-on.svelte";
  import ToggleOff from "../icons/toggle-off.svelte";
  let enabled = false;
</script>

{#if enabled}
  <span on:click="{() => enabled = !enabled}"><ToggleOff /></span>
{:else}
  <span on:click="{() => enabled = !enabled}"><ToggleOn /></span>
{/if}