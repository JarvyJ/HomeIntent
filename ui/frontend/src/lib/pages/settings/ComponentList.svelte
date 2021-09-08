<script>
  import Toggle from "$lib/components/Toggle.svelte";
</script>

<div class="border m-4 rounded text-xl">
  <div class="py-2 px-3 border-r-2 border-r-hi-green border-b">
    <a class="" href="/settings">
      <span class="block">Home Intent</span>
    </a>
  </div>

  <div class="py-2 px-3 border-b">
    <Toggle /><a class="ml-3" href="/settings/home_assistant">Home Assistant</a>
  </div>

  <div class="py-2 px-3">
    <Toggle /><a class="ml-3" href="/settings/timer">
      Timer
    </a>
  </div>
</div>
