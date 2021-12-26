<script>
  export let title;
  export let value;
</script>

<label class="flex items-center space-x-2">
  <input
    type="checkbox"
    class="form-tick appearance-none h-6 w-6 border dark:border-gray-500 rounded-md checked:bg-blue-600 dark:checked:border-transparent focus:outline-none"
    bind:checked={value}
  />
  <span>{title}</span>
</label>

<style>
  .form-tick:checked {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z'/%3E%3C/svg%3E");
  }
</style>
