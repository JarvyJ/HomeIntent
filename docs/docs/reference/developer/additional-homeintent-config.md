# Additional Home Intent Config
These settings are for globally changing how Home Intent works.

## Home Intent enable beta or all
The intent settings override all other config, so whatever is in `customization.yaml` will not take effect. These are really intended for power users who want to test beta functionality or developers during testing.

## Configuration

| Option      | Description                                                             | Required/Default |
|:------------|:------------------------------------------------------------------------|:-----------------|
| beeps       | Enable to use Home Intent beeps, disable for Rhasspy beeps              | `True`           |
| enable_beta | Enables intents in beta. Overrides `customization.yaml`                 | `False`          |
| enable_all  | Enables all intents - beta or otherwise. Overrides `customization.yaml` | `False`          |

!!!note
    To use Home Intent beeps, Rhasspy and Home Intent need to be running in the same container, which is the default setup.
    So, if you have separate Rhasspy and Home Intent instances, the Home Intent beeps and overrides will not work and should be set to `False`.


Example in `config.yaml`:
```yaml
home_intent:
  enable_beta: true
```