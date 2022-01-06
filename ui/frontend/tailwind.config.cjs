const config = {
  mode: "jit",
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      colors: {
        "hi-green": "#43ae4f",
      },
    },
  },
  plugins: [],
  darkMode: "class",
};

module.exports = config;
