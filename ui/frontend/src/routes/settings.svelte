<script>
import RhasspySettings from "../pages/settings/RhasspySettings.svelte";
import ComponentList from "../pages/settings/ComponentList.svelte";
</script>

<!-- Main container -->
<nav class="level is-mobile">
  <!-- Left side -->
  <div class="level-left">
    <div class="level-item">
      <p class="subtitle is-5">
        Settings
      </p>
    </div>
  </div>

  <!-- Right side -->
  <div class="level-right">
    <p class="level-item"><a class="button is-success">Save</a></p>
  </div>
</nav>


<div class="columns">
  <div class="column is-2">
    <ComponentList />
  </div>
  <div class="column">
    <RhasspySettings />
  </div>
</div>