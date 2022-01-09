The Home Assistant API returns certain attributes/states in english, that a user may have to translate across multiple components. The json files in this directory translate the specific english words in API responses to the corresponding languages.

This includes things like "on" and "off" as well as "high", "medium", and "low".

The json file will get auto-loaded based on language and is used in the HA API code to handle the translation.
