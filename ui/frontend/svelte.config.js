import preprocess from "svelte-preprocess";
import adapter from "@sveltejs/adapter-static";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],

  kit: {
    adapter: adapter(),
    prerender: {
      crawl: true,
      entries: ["/settings", "/"], //enough to trigger a full crawl!
      onError: "continue",
    },
    vite: {
      server: {
        proxy: {
          // string shorthand
          "/openapi.json": {
            target: "http://api:11102",
            secure: false,
            changeOrigin: true,
          },
          "/api": {
            target: "http://api:11102",
            secure: false,
            changeOrigin: true,
          },
          "/ws": {
            target: "ws://api:11102",
            secure: false,
            changeOrigin: true,
            ws: true,
          },
        },
      },
    },
  },
};

export default config;
