# Custom Components
Custom components can be installed in `/config/custom_components/<component_name>` and will be loaded on startup. Home Intent will go through it's `config.yaml` try to load from the builtin `components` and then load from `custom_components`.

It follows normal python importing, so either a folder with `<component_name>/__init__.py` or a file named `<component_name>.py` will be loaded. The builtin components all use the folder pattern for consistency, and prefer that for custom components as well.

More information on creating components can be found in the [example component docs](/developer-reference/example-component).

We'll publish a list of custom components here. 