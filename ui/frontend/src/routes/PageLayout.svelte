<script>
	// this is a little temporary. I really want it to persist in the layout, so you can navigate to other
	// pages and have the restart status be correct

	// Waiting on this: https://github.com/sveltejs/kit/issues/627
	export let title;

	import SectionBar from '$lib/components/SectionBar.svelte';
</script>

<SectionBar title="{title}"><slot name="sectionBar"></slot></SectionBar>
<slot></slot>
