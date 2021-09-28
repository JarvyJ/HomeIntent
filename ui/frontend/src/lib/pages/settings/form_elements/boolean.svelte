<script>
  export let title;
  export let description;
  export let value;

  import Checkbox from '$lib/components/Checkbox.svelte';
  import HelpText from '../HelpText.svelte';
</script>

<div>
  <label for="story" class="font-bold">{title}</label>
  <HelpText>{@html description}</HelpText>
</div>
<Checkbox title="{title}" bind:value />
