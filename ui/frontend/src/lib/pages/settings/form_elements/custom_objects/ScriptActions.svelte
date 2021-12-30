<script>
	export let title;
	export let description;
	export let value;
	export let example;
	export let required;

	import HelpText from "../../HelpText.svelte";

	const style = "border dark:bg-gray-800 dark:border-gray-500 rounded-md focus:outline-none p-1.5";
</script>

<div class="col-span-2">
	<span class="font-bold"> {title}</span>
	<HelpText>{@html description}</HelpText>
</div>

<div>
	<div>
		<label class="font-bold block mb-2">Script ID</label>
		<input type="text" class="{style}" placeholder="ex: script.test_script" />
	</div>

	<div class="mt-3">
		<label class="font-bold block mb-2">Response</label>
		<input type="text" class="{style} w-full" />
	</div>
</div>

<div>
	<label class="font-bold block mb-2">Sentences</label>
	<textarea
		class="{style} w-full"
		rows="4"
		cols="40"
		placeholder="Sentences should be separated by newlines"
	/>
</div>
