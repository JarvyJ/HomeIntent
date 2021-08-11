# API Reference
This is a quick reference for anyone who wants to build their own Home Intent components. There are two main classes developers will utilize while building a component - the `Intents` class and a `HomeIntent` object. Home Intent is designed to work as a class based system. We strongly recommend taking a look at the [Example Component](example-component.md) to get a feel for how it works. This is just a reference for all the methods that are available.

Home Intent's speech abilities are built on top of Rhasspy. It is highly recommended to read the page on [training sentences](https://rhasspy.readthedocs.io/en/latest/training/), as Home Intent builds upon them.

## `Intents` class

The intents class is generally initiated at the top level of a component and has a bunch of decorators that make it easier to create intents and their components.

Example initialization:
```python
intents = Intents(__name__)
```

### `@intents.dictionary_slots`
Dictionary slots expect a dictionary of what is spoken to what is returned to the sentence method. It can be really useful to use entity id's to make for quick manipulation.

Example:
```python
@intents.dictionary_slots
def partial_time(self):
    return {
        "Bedroom Light": "light.bedroom",
        "Kitchen": "light.kitchen",
        "Office Light": "light.office",
    }
```


### `@intents.slots`
The regular slots are useful when the text that is spoken is the same as the text that is returned to the sentence method.

Example:
```python
@intents.slots
def shopping_item(self):
    return ["apples", "applesauce", "asparagus", "bacon"]
```

### `@intents.sentences(List[str])`
This decorator takes in a list of strings that can be spoken to trigger an intent. After the intent is triggered, the method that is decorated will execute. The sentences follow the [sentence structure](https://rhasspy.readthedocs.io/en/latest/training/) Rhasspy uses. 

Home Intent will parse out the slot name (in the form `($slotName)`) and tag name (in the form `{tagName}`) and verify they are parameters in the method. When an intent triggers, those values are then passed in to the method.

Example:
```python
@intents.sentences(["add ($shopping_item) to the [shopping] list"])
def add_item_to_shopping_list(self, shopping_item):
    self.ha.api.call_service("shopping_list", "add_item", {"name": shopping_item})
    return f"Adding {shopping_item} to the shopping list."
```

In the example `shopping_item` is expected to be passed in to the `add_item_to_shopping_list` based on the sentence.

### `@intents.on_event("register")` - NOT YET IMPLEMENTED
This method registers a callback method that will be executed after the slot methods have been executed. It can come in handy for disabling an intent if there are no slots to execute on, which can help the overall experience as a sentence that can't do anything shouldn't be registered in Rhasspy. To aid in disabling intents, there are two helper methods `intents.disable_intent` and `intents.disable_all`.

!!!note "System Integrations"
    For system integrations (like Home Assistant), intents can also be disabled before calling `register` if it is known ahead of time if the group of intents is not going to be used.
    ```python
    if "shopping_list" in home_assistant_component.domains:
        home_intent.register(
            shopping_list.ShoppingList(home_assistant_component), shopping_list.intents
        )
    ```

#### `intents.disable_intent(method)`
Disables a specific intent method. Takes in the actual method and will stop it from being registered in Rhasspy.

#### `intents.disable_all()`
Disables the entire intent. Can come in handy if there are no slots associated.

Example:
```python
@intents.on_event("register")
def conditionally_remove_intents(self):
    if len(self.controllable_entites) == 0:
        intents.disable_intent(self.toggle_group)

    if len(self.all_entities) == 0:
        intents.disable_all_intents()
```

## On Slots and Sentences
One thing that is currently a little odd is that slot names (either regular or dictionary) have to be unique across Home Intent. Technically slots can be used across multiple intents. Sentences, on the other hand, do **not** need to be unique across Home Intent.

You will get a runtime error if multiple slots are found with the same name.

## `HomeIntent` object
An instantiated `HomeIntent` object gets passed in to the `setup` function when setting up components.

Example:
```python hl_lines="4"
class TimerSettings(BaseModel):
    max_time_days: int = 1

def setup(home_intent: HomeIntent):
    config = home_intent.get_config(TimerSettings)
    home_intent.register(Timer(config), intents)
```

### `home_intent.get_config(pydantic.BaseModel)`
Home Intent uses [pydantic](https://pydantic-docs.helpmanual.io/) models for handling configuration. The `get_config` method will parse the config from `config.yaml` given the pydantic BaseModel object and return it for use.

### `home_intent.register(Class(), Intents)`
The `register` method expects an instantiated intent class object and an `Intents` object. This method registers the class and verifies all the slots and sentences are setup correctly. Later in the Home Intent initialization process, the registered intents are used to configure Rhasspy and setup the Intent Handler.