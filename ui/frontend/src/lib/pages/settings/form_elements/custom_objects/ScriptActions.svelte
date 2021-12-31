<script>
	export let title;
	export let description;
	export let value;
	export let example;
	export let required;

	import HelpText from "../../HelpText.svelte";
	import AddIcon from "$lib/icons/plus-circle.svelte";
	import ScriptAction from "./ScriptAction.svelte";

	let ui_values = [];
	if (value) {
		for (const [name, fields] of Object.entries(value)) {
			ui_values[ui_values.length] = { name: name, fields: fields };
		}
	}
	$: ui_values && updateValue();

	function updateValue() {
		value = {};
		for (const ui_value of ui_values) {
			if (ui_value.name) {
				value[ui_value.name] = ui_value.fields;
			}
		}
	}

	function addScript() {
		ui_values[ui_values.length] = { name: "", fields: { sentences: [], response: "" } };
	}

	function deleteScript(name) {
		ui_values = ui_values.filter((x) => x.name != name);
	}
</script>

<div class="col-span-2">
	<span class="font-bold"
		><span class="-ml-7 mr-2 cursor-pointer" title="Add new script" on:click="{addScript}"
			><AddIcon
		/></span>
		{title}</span
	>
	<HelpText>{@html description}</HelpText>
</div>

{#each ui_values as ui_value} <ScriptAction bind:scriptId={ui_value.name}
bind:value={ui_value.fields} on:delete={() => deleteScript(ui_value.name)} /> {/each}
