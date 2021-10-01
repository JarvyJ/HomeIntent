<style>
	p :global(a) {
		color: #3c9a47;
		text-decoration: underline;
	}
</style>

<script>
	export let classes = '';
</script>

<p class="text-sm dark:text-gray-400 {classes}"><slot></slot></p>
