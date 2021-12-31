<script>
	export let scriptId;
	export let value = {sentences: [], response: ""}

	import { createEventDispatcher } from "svelte";
	import DeleteIcon from "$lib/icons/trash.svelte";
  
  	const dispatch = createEventDispatcher();
	const style = "border dark:bg-gray-800 dark:border-gray-500 rounded-md focus:outline-none p-1.5";
	let textAreaValue;

	$: value.sentences = textAreaValue.split("\n");
	if (value.sentences) {
		textAreaValue = value.sentences.join("\n");
	}

	function deleteScript() {
		dispatch("delete")
	}
</script>

<div>
	<div>
		<label class="font-bold block mb-2"
			><span class="-ml-7 mr-2 cursor-pointer" title="Delete script" on:click={deleteScript}><DeleteIcon /></span> Script
			ID</label
		>
		<input type="text" class="{style}" placeholder="ex: script.movietime" bind:value="{scriptId}" />
	</div>

	<div class="mt-3">
		<label class="font-bold block mb-2">Response</label>
		<input
			type="text"
			class="{style} w-full"
			placeholder="ex: You are now ready to watch a movie"
			bind:value="{value.response}"
		/>
	</div>
</div>

<div>
	<label class="font-bold block mb-2">Sentences</label>
	<textarea
		class="{style} w-full"
		rows="4"
		cols="40"
		placeholder="Sentences should be separated by newlines"
		bind:value="{textAreaValue}"
	/>
</div>
