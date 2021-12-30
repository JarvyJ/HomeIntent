<script>
  export let word_wrap;
  export let horizontal_split;

  import Checkbox from "$lib/components/Checkbox.svelte";
</script>

<span class="flex items-center ml-auto gap-4">
  <Checkbox title="Word Wrap" bind:value={word_wrap} />
</span>
