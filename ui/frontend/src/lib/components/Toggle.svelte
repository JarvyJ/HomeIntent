<script>
	export let enabled = false;
	import ToggleOn from '$lib/icons/toggle-on.svelte';
	import ToggleOff from '$lib/icons/toggle-off.svelte';

	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	function click() {
		enabled = !enabled;
		dispatch('change', {
			enabled: enabled
		});
	}
</script>

{#if enabled}
	<span class="text-hi-green cursor-pointer" on:click={click}><ToggleOn /></span>
{:else}
	<span class="cursor-pointer" on:click={click}><ToggleOff /></span>
{/if}
