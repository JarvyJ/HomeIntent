<script>
  export let menu = false;
  export let saveSettings;
</script>

<button
  class="rounded hover:bg-green-700 bg-hi-green px-3 py-1 disabled:opacity-50 disabled:cursor-not-allowed"
  class:mt-5={!menu}
  class:text-xl={!menu}
  on:click={saveSettings}
>
  Save
</button>