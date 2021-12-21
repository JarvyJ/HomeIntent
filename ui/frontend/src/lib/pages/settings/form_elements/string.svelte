<script>
  export let title;
  export let description = '';
  export let format = '';
  export let example = '';
  export let value;
  export let required;

  import HelpText from '../HelpText.svelte';

  const style = "border dark:bg-gray-800 dark:border-gray-500 rounded-md focus:outline-none p-1.5";

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
  <label for="{id}" class="font-bold">{#if required}<span title="Required" class="text-pink-800">*</span>{/if} {title}</label>
  <HelpText>{@html description}</HelpText>
</div>

<!-- have to do this via if/else because otherwise there's an error with 2way binding -->
{#if inputType === "text"}
<input
  id="{id}"
  type="text"
  class="{style}"
  bind:value
  placeholder="{example}"
  required="{required}"
/>
{:else if inputType === "url"}
<input
  id="{id}"
  type="url"
  class="{style}"
  bind:value
  placeholder="{example}"
  required="{required}"
/>
{:else if inputType === "longtext"}
<textarea
  id="story"
  name="story"
  class="{style}"
  rows="5"
  cols="40"
  placeholder="{example}"
  required="{required}"
  bind:value
></textarea>
{/if}
