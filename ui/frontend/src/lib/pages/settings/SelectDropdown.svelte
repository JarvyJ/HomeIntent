<style>
  .chevron-down {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='%23404749' fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position-x: 94%;
    background-position-y: center;
  }
</style>

<script>
  export let name = '';
  export let values = [];
  export let selectedValue;

  const id_name = name.replace(' ', '').toLowerCase();

  if (!selectedValue) {
    selectedValue = values[0];
  }
</script>

<label for="{id_name}">{name}</label>
<select
  id="{id_name}"
  bind:value="{selectedValue}"
  class="border chevron-down p-1.5 pr-8 border-gray-300 rounded-md appearance-none"
>
  {#each values as value}
  <option>{value}</option>
  {/each}
</select>
