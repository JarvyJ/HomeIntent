<style>
  .navbar-burger {
    margin-left: 0;
    display: block;
  }

  :global(.bi) {
    display: inline-block;
    vertical-align: -.125em;
    width: 1em;
    height: 1em;
  }

  .menu {
    height: 100%;
    overflow: hidden;
    position: fixed;
    background-color: rgb(76, 174, 79);
  }

  .menu-text {
    padding-left: 1em;
  }

  hr {
    margin: 0;
  }

  main {
    padding: .5em .75em;
    background-color: whitesmoke;
    height: 100%;
  }

  :global(html, body, #svelte) {
    height: 100%;
  }

  :global(.label) {
    font-weight: 400;
  }

  :global(h1, h2, h3, h4, h5, h6) {
    font-weight: 300 !important;
  }

</style>

<script>
  import "../global.scss";
  import { page } from '$app/stores';

  import SettingsIcon from "../icons/gear-fill.svelte"
  import CustomizeIcon from "../icons/tools.svelte"
  import SatellitesIcon from "../icons/speaker.svelte"
  import LogsIcon from "../icons/card-list.svelte"
  import DocsIcon from "../icons/journal-richtext.svelte"

  let visible = true;
  let navWidth = 256;

  $: if (visible) {
    navWidth = 256;
  } else {
    navWidth = 52;
  }

</script>

<nav class="menu">

  <div class="navbar-brand" style="width: {navWidth}px;">
    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample" on:click="{() => visible = !visible}">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>

    {#if visible}
    <a class="navbar-item" href="/" >
      Home Intent
    </a>
    {/if}
  </div>

  <hr />

  <ul class="menu-list">
    <li><a class="is-size-5 has-text-light" class:is-active="{$page.path == '/settings'}" href="/settings"><SettingsIcon />
      {#if visible}
      <span class="menu-text">Settings</span>
      {/if}
    </a></li>

    <li><a class="is-size-5 has-text-light" class:is-active="{$page.path == '/customize'}" href="/customize"><CustomizeIcon />
      {#if visible}
      <span class="menu-text">Customize</span>
      {/if}
    </a></li>

    <li><a class="is-size-5 has-text-light" class:is-active="{$page.path == '/satellites'}" href='/satellites'><SatellitesIcon />
      {#if visible}
      <span class="menu-text">Satellites</span>
      {/if}
    </a></li>

    <li><a class="is-size-5 has-text-light" class:is-active="{$page.path == '/logs'}" href="/logs"><LogsIcon />
      {#if visible}
      <span class="menu-text">Logs</span>
      {/if}
    </a></li>

    <li><a class="is-size-5 has-text-light" href="/docs" target="_blank"><DocsIcon />
      {#if visible}
      <span class="menu-text">Docs</span>
      {/if}
    </a></li>
  </ul>

</nav>


<main style="margin-left: {navWidth}px;">
<slot></slot>
</main>