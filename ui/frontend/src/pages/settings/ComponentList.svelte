<script>
  import Toggle from "../../components/Toggle.svelte";
</script>

<ul class="menu-list is-bordere"d>
  <li><a class="" href="/settings">
    <span class="menu-text is-size-5">Home Intent</span>
  </a></li>

  <li><a class="" href="/settings/home_assistant">
    <span class="menu-text is-size-5"><Toggle /> Home Assistant</span>
  </a></li>

  <li><a class="" href="/settings/timer">
    <span class="menu-text is-size-5"><Toggle /> Timer</span>
  </a></li>
</ul>
