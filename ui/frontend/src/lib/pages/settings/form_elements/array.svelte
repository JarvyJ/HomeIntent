<script>
  export let title;
  export let description;
  export let example;
  export let value;

  import HelpText from "../HelpText.svelte";

  let textAreaValue;

  $: value = textAreaValue.split("\n");
  if (value) {
    textAreaValue = value.join("\n");
  }
</script>

<div class="col-start-1">
  <label for="ignore-entities" class="font-bold">{title}</label>
  <HelpText>{@html description}</HelpText>
  {#if example}
    <HelpText classes="mt-3">
      Example:
      <code class="block p-2 dark:bg-gray-700 dark:text-gray-50 rounded-md">
        <pre>
{example.join("\n")}
    </pre>
      </code>
    </HelpText>
  {/if}
</div>

<textarea
  id="ignore-entities"
  name="ignore-entities"
  class="border dark:bg-gray-800 dark:border-gray-500 rounded-md focus:outline-none p-1.5"
  rows="5"
  cols="40"
  placeholder="Entities should be separated by newlines"
  bind:value={textAreaValue}
/>
