<script>
  import { onMount } from "svelte";

  import PageLayout from "$lib/PageLayout.svelte";
  import Checkbox from "$lib/components/Checkbox.svelte";

  let word_wrap = false;

  let exceptions = []
  let logs = []

  let sockets = {
    logs: { socket: null, status: "Connecting...", messages: [] },
    exceptions: { socket: null, status: "Connecting...", messages: [] },
  };

  let show_logs = false;

  function setupSocket(name, url) {
    sockets[name].socket = new WebSocket(url);

    sockets[name].socket.onopen = function (event) {
      sockets[name].status = "Connected";
    };

    sockets[name].socket.onmessage = function (event) {
      sockets[name].messages[sockets[name].messages.length] = JSON.parse(event.data);
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

  async function clearExceptions() {
    await fetch(`/api/v1/exceptions`, {method: 'DELETE'})
    const exceptions_result = await fetch(`/api/v1/exceptions`);
    exceptions = await exceptions_result.json();
  }

  onMount(async () => {
    const exceptions_result = await fetch(`/api/v1/exceptions`);
    exceptions = await exceptions_result.json();

    const logs_result = await fetch(`/api/v1/logs`)
    logs = await logs_result.json();

    setupSocket("logs", `ws://${window.location.host}/ws/logs`)
    setupSocket("exceptions", `ws://${window.location.host}/ws/exceptions`)
  });
</script>

<PageLayout title="Logs">
  <div class="p-4">
    <div class="flex items-center">
      <h2 class="text-3xl">Exceptions</h2>
      {#if exceptions.length > 0}
      <span class="ml-auto">
        <button title="Clear Exceptions" class="rounded hover:bg-red-700 bg-red-500 px-3 py-1 my-3" on:click={clearExceptions}>Clear</button>
      </span>
      {/if}
    </div>

  {#each exceptions as exception}
  <div class="mb-4">
    <p>{exception.data}</p>
    <p class="text-gray-400 text-sm"><a href="#{exception.time}" on:click="{() => show_logs = true}">{new Date(exception.time * 1000).toLocaleString()}</a> - <span class="text-pink-700">{exception.log_level}</span></p>
  </div>
  {:else}
  <p class="mb-4 mt-2">There are no issues</p>
  {/each}

  {#each sockets.exceptions.messages as exception}
  <div class="mb-4">
    <p>{exception.data}</p>
    <p class="text-gray-400 text-sm"><a href="#{exception.time}" on:click="{() => show_logs = true}">{new Date(exception.time * 1000).toLocaleString()}</a> - <span class="text-pink-700">{exception.log_level}</span></p>
  </div>
  {/each}


  {#if !show_logs}
  <button class="rounded hover:bg-green-700 bg-hi-green px-3 py-1 my-3 text-xl" on:click={() => show_logs = !show_logs}>{#if show_logs}Hide{:else}View{/if} Logs</button>
  {/if}

  {#if show_logs}
  <div class="flex">
    <div>
      <h2 class="text-3xl">Logs</h2>
      <p class="dark:text-gray-500 mb-1">Status: {sockets.logs.status}</p>
    </div>

    <span class="flex items-center ml-auto gap-4">
      <Checkbox title="Word Wrap" bind:value={word_wrap} />
    </span>
  </div>

  <pre class="text-sm wrap-control h-screen p-2 pt-0 dark:bg-gray-700 dark:text-gray-50 rounded-md" class:whitespace-pre-wrap={word_wrap} class:pre={!word_wrap}><code>
  {#each logs as log}
    <br id={log.time}>{new Date(log.time * 1000).toLocaleString()} {log.log_level} {log.logger} {log.data}
  {/each}
  {#each sockets.logs.messages as socketLog}
    <br id={socketLog.time}>{new Date(socketLog.time * 1000).toLocaleString()} {socketLog.log_level} {socketLog.logger} {socketLog.data}
  {/each}
  </code></pre>
  {/if}
</div>
</PageLayout>


<style>
  .wrap-control {
    overflow-x: scroll;
    overflow-wrap: normal;
    scroll-behavior: smooth;
  }
</style>
