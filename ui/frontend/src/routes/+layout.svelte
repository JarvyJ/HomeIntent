<script>
  import "../app.postcss";
  import { onMount } from "svelte";

  import HomeIntentWhite from "$lib/components/HomeIntentWhite.svelte";
  import Menu from "$lib/pages/layout/Menu.svelte";

  let menuExpanded = true;
  let navWidth = 256;

  $: if (menuExpanded) {
    navWidth = 256;
  } else {
    navWidth = 55;
  }

  let isMobile = false;
  onMount(async () => {
    isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;
    if (isMobile) {
      menuExpanded = false;
    }
  });
</script>

<nav
  class="border-r dark:border-gray-700 h-screen fixed dark:bg-gray-900 dark:text-gray-50 bg-gray-50 text-gray-800"
  style="width: {navWidth}px;"
>
  <div class="py-3 px-4 bg-hi-green border-b dark:border-gray-700 text-2xl">
    <span on:click={() => (menuExpanded = !menuExpanded)}><HomeIntentWhite /></span>
    {#if menuExpanded} Home Intent {/if}
  </div>

  <Menu bind:menuExpanded />
</nav>

<main style="margin-left: {navWidth}px;">
  <div class="dark:bg-gray-900 dark:text-gray-50 text-gray-800 bg-gray-50 min-h-screen">
    <slot />
  </div>
</main>

<style>
  :global(.bi) {
    display: inline-block;
    vertical-align: -0.125em;
    width: 1em;
    height: 1em;
  }

  :global(p a) {
    color: #3c9a47;
    text-decoration: underline;
  }

</style>
