<script>
  export let word_wrap;

  import { onMount } from "svelte";

  import { capitalize_with_underscore } from "$lib/util/capitalization";
  import SettingsTitle from "$lib/pages/settings/SettingsTitle.svelte";

  let sockets = {
    home_intent: { socket: null, status: "Connecting...", messages: [] },
    rhasspy: { socket: null, status: "Connecting...", messages: [] },
  };

  let socketElements = { rhasspy: null, home_intent: null };

  onMount(() => {
    const location = window.location;
    setupSocket("rhasspy", `ws://${location.hostname}:12101/api/events/log`);
    setupSocket("home_intent", `ws://${location.host}/ws/logs`);
  });

  function setupSocket(name, url) {
    sockets[name].socket = new WebSocket(url);

    sockets[name].socket.onopen = function (event) {
      sockets[name].status = "Connected";
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
        sockets[name].status = "Connection died";
      }
    };

    sockets[name].socket.onerror = function (error) {
      sockets[name].status = `Error: ${error.message}`;
    };
  }
</script>

{#each Object.entries(sockets) as [name, info] (name)}
  <div class="justify-self-stretch pb-9">
    <SettingsTitle>{capitalize_with_underscore(name)} Logs ({info.status})</SettingsTitle>
    <textarea
      readonly
      class:dont-word-wrap={!word_wrap}
      bind:this={socketElements[name]}
      class="w-full h-full p-2 dark:bg-gray-700 rounded-md font-mono text-sm"
    >
      {info.messages.join("\n")}</textarea
    >
  </div>
{/each}

<style>
  .dont-word-wrap {
    overflow-x: scroll;
    overflow-wrap: normal;
    white-space: pre;
  }
</style>
