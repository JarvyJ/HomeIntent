# Customization - NOT YET IMPLEMENTED
Users have the ability to further customize intents to provide a better experience for their individual needs. It can be useful to remove unused intents (especially if they false trigger) or modify slots (like custom shopping list items).

There are plans on having a UI to help with customizations, but currently it is handled with YAML files in `/config/customizations/<component_name>.yaml` where component name matches the intent that you are trying to modify.

## Slots

### Adding and removing custom words to slots
Adding new words to the slot list supports all the standard Rhasspy [slot](https://rhasspy.readthedocs.io/en/latest/training/#slots-lists) features like synonyms.

Removal works by reference or exact match. So, to remove a specific entity from Home Assistant, the best option is to list the entity id (for example `light.kitchen`).

```yaml
slots:
  shopping_item:
    add:
      - fruit: apple
      - (banans|naners|bananas): bananas
      - baked beans
    remove:
      - beans
```

## Sentences/Intents

### Disabling all intents in a component
To disable an entire component, add `disable_all` to the top level of the yaml file.

```yaml
disable_all: true
```

### Disabling specific intents
Under an `intents` top level config, should be the intent method name (as found in the python class) with `disable` set to `true`.

```yaml
intents:
  add_item:
    disable: true
```

### Adding and removing sentences to intents
Similar to slots, intent sentences can be added or removed. Ensure that any tags or slot names needed for the intent are present.
```yaml
intents:
  add_item:
    sentences:
      add:
        - "include ($shopping_item) on the shopping list"
      remove:
        - "add ($shopping_item) to the [shopping] list"
```

### Sentence aliasing with slot entities
```yaml
intents:
  add_item:
    alias:
      - sentence: "I want bacon"
        shopping_item: "bacon"
```

<!-- ## Full Automation
Create a sentence that kicks off multiple intents. This way you can kickoff multiple intents with a single phrase. -->

## Full Example
This file could be used as `/config/customizations/home_assistant.shopping_list.yaml`

```yaml
slots:
  shopping_item:
    add:
      - fruit: apple
      - (banans|naners|bananas): bananas
      - baked beans
    remove:
      - beans
      
intents:
  add_item:
    sentences:
      add:
        - "add ($shopping_item) to the list"
    alias:
      - sentence: "I want bacon"
        shopping_item: "bacon"
```
