<script>
	export let settingsList;
	export let currentSetting;

	import Toggle from '$lib/components/Toggle.svelte';
	import { capitalize_with_underscore } from '$lib/util/capitalization';
</script>

<ul class="border m-4 rounded text-xl border-b-0 dark:border-gray-600">
	{#each Object.entries(settingsList) as [name, setting] (name)}
		{#if name !== 'rhasspy'}
			<!-- Small hack to not show rhasspy in the list, as the settings in it are only for advanced users -->
			<li
				class="py-2 px-3 border-b flex space-x-3 dark:border-gray-600"
				class:border-r-2={name === currentSetting}
				class:dark:border-r-hi-green={name === currentSetting}
			>
				{#if name !== 'home_intent'}<Toggle
						bind:enabled={settingsList[name].enabled}
						on:change={() => (currentSetting = name)}
					/>{/if}<span
					class="flex-grow cursor-pointer"
					on:click|preventDefault={() => (currentSetting = name)}
					>{capitalize_with_underscore(name)}</span
				>
			</li>
		{/if}
	{/each}
</ul>
