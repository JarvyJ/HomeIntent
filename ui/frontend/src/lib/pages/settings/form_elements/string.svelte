<script>
  export let title;
  export let description = '';
  export let format = '';
  export let example = '';
  export let value;

  import HelpText from '../HelpText.svelte';

  let id = `${title}-id`;
  let inputType;

  switch (format) {
    case 'uri':
      inputType = 'url';
      break;

    default:
      inputType = 'text';
  }

  $: if (value && value.length > 50) {
    inputType = 'longtext';
  }
</script>

<div>
  <label for="{id}" class="font-bold">{title}</label>
  <HelpText>{@html description}</HelpText>
</div>

<!-- have to do this via if/else because otherwise there's an error with 2way binding -->
{#if inputType === "text"}
<input
  id="{id}"
  type="text"
  class="border bg-gray-800 border-gray-500 rounded-md focus:outline-none p-1.5"
  bind:value
  placeholder="{example}"
/>
{:else if inputType === "url"}
<input
  id="{id}"
  type="url"
  class="border bg-gray-800 border-gray-500 rounded-md focus:outline-none p-1.5"
  bind:value
  placeholder="{example}"
/>
{:else if inputType === "longtext"}
<textarea
  id="story"
  name="story"
  class="text-area border bg-gray-800 border-gray-500 rounded-md focus:outline-none p-1.5"
  rows="5"
  cols="40"
  placeholder="{example}"
  bind:value
></textarea>
{/if}
