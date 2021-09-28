<style>
  .dont-word-wrap {
    overflow-x: scroll;
    overflow-wrap: normal;
    white-space: pre;
  }
</style>

<script>
  import { onMount } from 'svelte';

  import SectionBar from '$lib/components/SectionBar.svelte';
  import SettingsTitle from '$lib/pages/settings/SettingsTitle.svelte';
  import LayoutSplit from '$lib/icons/layout-split.svelte';
  import LayoutHSplit from '$lib/icons/layout-h-split.svelte';
  import Checkbox from '$lib/components/Checkbox.svelte';
  import { capitalize_with_underscore } from '$lib/util/capitalization';
  import PageLayout from './PageLayout.svelte';

  let horizontal_split = true;
  let word_wrap = true;

  let sockets = {
    rhasspy: { socket: null, status: 'Connecting...', messages: [] },
    home_intent: { socket: null, status: 'Connecting...', messages: [] }
  };

  let socketElements = { rhasspy: null, home_intent: null };

  onMount(() => {
    setupSocket('rhasspy', 'ws://localhost:12101/api/events/log');
    setupSocket('home_intent', 'ws://localhost:11102/ws/logs');
  });

  function setupSocket(name, url) {
    sockets[name].socket = new WebSocket(url);

    sockets[name].socket.onopen = function (event) {
      sockets[name].status = 'Connected';
    };

    sockets[name].socket.onmessage = function (event) {
      sockets[name].messages[sockets[name].messages.length] = event.data;
      socketElements[name].scrollTop = socketElements[name].scrollHeight;
    };

    sockets[name].socket.onclose = function (event) {
      if (event.wasClean) {
        sockets[
          name
        ].status = `Connection closed cleanly, code=${event.code} reason=${event.reason}`;
      } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        sockets[name].status = 'Connection died';
      }
    };

    sockets[name].socket.onerror = function (error) {
      sockets[name].status = `Error: ${error.message}`;
    };
  }
</script>

<PageLayout title="Live Logs">
  <svelte:fragment slot="sectionBar">
    <span class="flex items-center ml-auto gap-4">
      <Checkbox title="Word Wrap" bind:value="{word_wrap}" />
      <ul class="flex items-center gap-2">
        <li>
          <span
            class:cursor-pointer="{horizontal_split}"
            class:hover:bg-green-200="{horizontal_split}"
            class:bg-hi-green="{!horizontal_split}"
            class="rounded px-2 py-1 text-lg"
            on:click="{() => horizontal_split = false }"
            ><LayoutSplit
          /></span>
        </li>
        <li>
          <span
            class:cursor-pointer="{!horizontal_split}"
            class:hover:bg-green-200="{!horizontal_split}"
            class:bg-hi-green="{horizontal_split}"
            class="rounded px-2 py-1 text-lg"
            on:click="{() => horizontal_split = true }"
            ><LayoutHSplit
          /></span>
        </li>
      </ul>
    </span>
  </svelte:fragment>

  <div
    class:grid-cols-2="{!horizontal_split}"
    class:grid-cols-1="{horizontal_split}"
    class="grid justify-items-stretch w-full h-screen gap-5 p-5"
  >
    {#each Object.entries(sockets) as [name, info] (name)}
    <div class="justify-self-stretch pb-9">
      <SettingsTitle>{capitalize_with_underscore(name)} Logs ({info.status})</SettingsTitle>
      <textarea
        readonly
        class:dont-word-wrap="{!word_wrap}"
        bind:this="{socketElements[name]}"
        class="w-full h-full p-2 bg-gray-700 rounded-md font-mono text-sm"
      >
{info.messages.join("\n")}</textarea
      >
    </div>
    {/each}
  </div>
</PageLayout>
