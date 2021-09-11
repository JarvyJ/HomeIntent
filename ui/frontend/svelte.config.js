import preprocess from 'svelte-preprocess';
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://github.com/sveltejs/svelte-preprocess
	// for more information about preprocessors
	preprocess: [preprocess({
		"postcss": true
	})],

	kit: {
		// hydrate the <div id="svelte"> element in src/app.html
		target: '#svelte',
		adapter: adapter(),
		prerender: {
			crawl: true,
			pages: ["/settings/home_intent", "/"], //enough to trigger a full crawl!
			onError: "continue"
		},
		vite: {
			server: {
				proxy: {
					// string shorthand
					'/openapi.json': {
						target: 'http://localhost:11102',
						secure: false,
						changeOrigin: true
	  				},
	  				'/api': {
						target: 'http://localhost:11102',
						secure: false,
						changeOrigin: true
	  				}

				}
			}
		}
	},
};

export default config;
