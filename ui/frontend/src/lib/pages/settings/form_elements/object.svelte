<script>
  export let title;
  export let description;
  export let value;
  export let example;
  export let required;
  export let additionalProperties;

  import * as CustomObjects from "./custom_objects";

  const customObject = additionalProperties["$ref"].split("/").pop()
</script>

<svelte:component
  this={CustomObjects[customObject]}
  bind:title
  bind:description
  bind:value
  bind:example
  bind:required
/>