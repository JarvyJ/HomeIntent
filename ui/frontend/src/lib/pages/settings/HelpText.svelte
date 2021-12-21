<script>
	export let classes = '';
</script>

<p class="text-sm dark:text-gray-400 {classes}"><slot /></p>

<style>
	p :global(a) {
		color: #3c9a47;
		text-decoration: underline;
	}
</style>
