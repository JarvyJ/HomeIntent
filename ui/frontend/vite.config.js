import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
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
};

export default config;
