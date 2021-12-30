<script>
  export let title;

  import { slide } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { tweened } from "svelte/motion";
  import { onMount } from "svelte";

  let sockets = {
    restart: { socket: null, status: "Connecting...", messages: [] },
    exceptions: { socket: null, status: "Connecting...", messages: [] },
  };

  const progress = tweened(0, {
    duration: 400,
    easing: cubicOut,
  });

  setInterval(() => {
    if ($progress < 1) {
      progress.update((n) => n + 0.005);
    }
    if (
      sockets["restart"].messages[sockets["restart"].messages.length - 1] ===
      "Ready to handle intents!"
    ) {
      if ($progress < 1) {
        progress.set(1.0);
      } else {
        sockets["restart"].messages = [];
      }
    } else if (
      sockets["restart"].messages.length > 1 &&
      sockets["restart"].messages[sockets["restart"].messages.length - 1].startsWith("Error")
    ) {
      progress.set(0);
    }
  }, 1500);

  onMount(async () => {
    const location = window.location;
    

    setupSocket("restart", `ws://${location.host}/ws/jobs/restart`);
    sockets.restart.socket.onmessage = function (event) {
      if (event.data === "Restarting the Home Intent process...") {
        sockets.restart.messages = [event.data];
        sockets.exceptions.messages = [];
      } else {
        sockets.restart.messages[sockets.restart.messages.length] = event.data;
      }
      progress.set(sockets.restart.messages.length / 9);
    };

    setupSocket("exceptions", `ws://${location.host}/ws/exceptions`);
    sockets.exceptions.socket.onmessage = function (event) {
      const json_data = JSON.parse(event.data);
      if (json_data.log_level === "ERROR") {
        sockets.exceptions.messages[sockets.exceptions.messages.length] = json_data
        sockets.restart.messages[sockets.restart.messages.length] = "Error during startup. See the errors below and make the appropriate changes";
      }
    };
  });

  function setupSocket(name, url) {
    sockets[name].socket = new WebSocket(url);

    sockets[name].socket.onopen = function (event) {
      sockets[name].status = "Connected";
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

<nav class="flex items-center px-4 py-3 border-b dark:border-gray-700">
  <span class="font-semibold text-3xl">{title}</span>
  <slot />
</nav>

{#if sockets.restart.messages.length > 0}
<div class="m-4 py-4 px-5 border rounded dark:bg-gray-800 dark:border-gray-500" transition:slide>
  <div class="text-2xl mb-3">{sockets.restart.messages[sockets.restart.messages.length - 1]}</div>
  <progress value="{$progress}" class="w-full" />
  {#if sockets.exceptions.messages.length > 0}
  <p class="mt-4 mb-2">Errors:</p>
  {#each sockets.exceptions.messages as exception}
  <div class="mb-4">
    <p>{exception.data}</p>
    <p class="text-gray-400 text-sm">
      {new Date(exception.time * 1000).toLocaleString()} -
      <span class="text-pink-700">{exception.log_level}</span> - <a href="/logs/">Go to Logs</a>
    </p>
  </div>
  {/each} {/if}
</div>
{/if}
