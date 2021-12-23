<script>
  export let word_wrap;
  export let horizontal_split;

  import LayoutHSplit from "$lib/icons/layout-h-split.svelte";
  import LayoutSplit from "$lib/icons/layout-split.svelte";
  import Checkbox from "$lib/components/Checkbox.svelte";
</script>

<span class="flex items-center ml-auto gap-4">
  <Checkbox title="Word Wrap" bind:value={word_wrap} />
  <ul class="flex items-center gap-2">
    <li>
      <span
        class:cursor-pointer={horizontal_split}
        class:hover:bg-green-200={horizontal_split}
        class:bg-hi-green={!horizontal_split}
        class="rounded px-2 py-1 text-lg"
        on:click={() => (horizontal_split = false)}><LayoutSplit /></span
      >
    </li>
    <li>
      <span
        class:cursor-pointer={!horizontal_split}
        class:hover:bg-green-200={!horizontal_split}
        class:bg-hi-green={horizontal_split}
        class="rounded px-2 py-1 text-lg"
        on:click={() => (horizontal_split = true)}><LayoutHSplit /></span
      >
    </li>
  </ul>
</span>
