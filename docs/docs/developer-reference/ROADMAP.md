# Roadmap

## Phase 1: Precision Intents

 * Figure out how the framework will work

### Home Assistant API integrations

  * Control Lights
  * Control Switches
  * Shopping List
  * Groups
  * A/C?
  * Others

### Other Integrations

  * Timer
  * Alarm
  * Calendaring?

## Phase 2: Extensible Configs

  * Ability to extend slots/sentences
  * Ability to override slots/sentences
  * Ability to alias slots/sentences
    * Provide slot entity ids for "advanced" users
  * Put this in YAML files
  * Likely a web based interface for extending/overriding config
  * Customize Rhasspy profile (load JSON file from `/config` directory)
  * Subscribe to WebSocket and auto-update when home assistant changes
    * Maybe wait a few days until an entity is gone before deleting the config. Don't want to annoy users.
  * Support the "Supported Features" and conditionally disable unused intents.
    * Ex: Your AC unit doesn't have a dehumidify option, so don't put it in Home Intent.

### Config Loading Ideals
The goal is always to keep Home Intent straightforward to get started. We want sane defaults. People shouldn't *have to* go into the web interface if they don't want to. Setting up a `config.yaml` and running the program should be all that's needed. The web interface is intended for users who want to tinker a little bit and get more configuration if needed, it should not be required for users to go to for functionality.

## Phase 3: Fuzzy Wuzzy

  * Figure out how to do Inexact Matching
    * Use Deep Speech or something if an exact match isn't found.
    * Want to avoid *only* using fuzzy matches.

### Integration Ideas

  * Wikipedia via API?
    * Person info
    * Places info
    * Ability to self host if wanted
    * https://www.dbpedia.org seems to be useful
  * Maybe Movie db?
    * TMDB as API?
  * WolframAlpha?