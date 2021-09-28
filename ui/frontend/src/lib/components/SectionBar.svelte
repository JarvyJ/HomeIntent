<script>
  export let title;

  import { slide } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import { tweened } from 'svelte/motion';
  import { onMount } from 'svelte';

  let restartSocket = { socket: null, status: 'Connecting...', messages: [] };

  const progress = tweened(0, {
    duration: 400,
    easing: cubicOut
  });

  setInterval(() => {
    if ($progress < 1) {
      progress.update((n) => n + 0.005);
    }
    if (restartSocket.messages[restartSocket.messages.length - 1] === 'Ready to handle intents!') {
      if ($progress < 1) {
        progress.set(1.0);
      } else {
        restartSocket.messages = [];
      }
    } else if (
      restartSocket.messages.length > 1 &&
      restartSocket.messages[restartSocket.messages.length - 1].startsWith('Error')
    ) {
      progress.set(0);
    }
  }, 1500);

  onMount(async () => {
    setupSocket('ws://localhost:11102/ws/jobs/restart');
  });

  function setupSocket(url) {
    restartSocket.socket = new WebSocket(url);

    restartSocket.socket.onopen = function (event) {
      restartSocket.status = 'Connected';
    };

    restartSocket.socket.onmessage = function (event) {
      if (event.data === 'Restarting the Home Intent process...') {
        restartSocket.messages = [event.data];
      } else {
        restartSocket.messages[restartSocket.messages.length] = event.data;
      }
      progress.set(restartSocket.messages.length / 9);
    };

    restartSocket.socket.onclose = function (event) {
      if (event.wasClean) {
        restartSocket.status = `Connection closed cleanly, code=${event.code} reason=${event.reason}`;
      } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        restartSocket.status = 'Connection died';
      }
    };

    restartSocket.socket.onerror = function (error) {
      restartSocket.status = `Error: ${error.message}`;
    };
  }
</script>

<nav class="flex items-center px-4 py-3 border-b dark:border-gray-700">
  <span class="font-semibold text-3xl">{title}</span>
  <slot></slot>
</nav>

{#if restartSocket.messages.length > 0}
<div class="m-4 py-4 px-5 border rounded dark:bg-gray-800 dark:border-gray-500" transition:slide>
  <div class="text-2xl mb-3">{restartSocket.messages[restartSocket.messages.length - 1]}</div>
  <progress value="{$progress}" class="w-full"></progress>
</div>
{/if}
