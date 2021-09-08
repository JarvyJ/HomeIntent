<script>
import RhasspySettings from "$lib/pages/settings/RhasspySettings.svelte";
import ComponentList from "$lib/pages/settings/ComponentList.svelte";
import Button from "$lib/components/Button.svelte"
</script>

<nav class="flex items-center bg-gray-800 text-gray-50 px-4 py-3 border-b">
  <span class="font-semibold text-3xl">Settings</span>
  <Button>Save</Button>
</nav>

<div class="bg-gray-900 text-gray-50 grid grid-cols-5">
  <div class="h-screen">
    <ComponentList />
  </div>
  <div class="col-span-4 mt-5">
    <RhasspySettings />
  </div>
</div>