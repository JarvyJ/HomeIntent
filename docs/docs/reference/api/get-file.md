# Get File Function

!!! warning "Deprecation Notice"

    This method has been moved into the [Home Intent object](./home-intent-object.md#home_intentget_file) and will be removed in Home Intent 2022.02.0. The new version follows the same semantics, but supports internationalization.


Home Intent uses a custom file loading function that will first check if a file exists in `/config` otherwise it'll load the file from the [`default_configs`](https://github.com/JarvyJ/HomeIntent/tree/main/home_intent/default_configs) folder in the source code.

This allows users to easily replace parts of components like lists of colors or sounds. This can also be useful when creating custom components, as users can add component code to `/config/custom_components` and any associated files to `/config`.

```python hl_lines="7"
from home_intent import get_file

#### OTHER COMPONENT CODE #####

@intents.dictionary_slots
def color(self):
    color_file = get_file("home_assistant/colors.txt")
    colors = color_file.read_text().strip().split("\n")
    return {color: color.replace(" ", "") for color in colors}

```

## Conventions
When loading a file related to a component, it's best to put it in a folder that references the component's name. In the example above, files will be loaded from the `home_assistant` folder in `/config` or Home Intent's `default_configs` folder.