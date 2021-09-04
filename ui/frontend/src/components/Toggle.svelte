<script>
  import ToggleOn from "../icons/toggle-on.svelte";
  import ToggleOff from "../icons/toggle-off.svelte";
  let enabled = false;
</script>

{#if enabled}
  <span class="" on:click="{() => enabled = !enabled}"><ToggleOff /></span>
{:else}
  <span class="text-hi-green" on:click="{() => enabled = !enabled}"><ToggleOn /></span>
{/if}