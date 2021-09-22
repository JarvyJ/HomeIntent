<script>
  export let title
</script>

<nav class="flex items-center bg-gray-800 text-gray-50 px-4 py-3 border-b">
  <span class="font-semibold text-3xl">{title}</span>
  <slot></slot>
</nav>