# Home Assistant
Example Config:

```yaml
home_assistant:
  url: "http://my-home-assistant-url:8123" 
  bearer_token: "eyJ0eXAiOiJKV1QiLCJhbGci..."

```

!!! note
    The `url` is the URL that you use to access Home Assistant. It supports `https` if using a common certificate provider (like Let's Encrypt). Currently there is no support for a self-signed certificate.

## Getting a bearer token
In Home Assistant, if you go to your "Profile" page (by clicking your username) and scroll to the bottom, there is a section called "Long-Lived Access Tokens". Click on "Create" and give your token a name like "HomeIntent". Copy the token and place it in the config. It will last 10 years. NOTE: I've truncated the token above, but they are quite long.

## Configuration

| Option        | Description                                                                       | Required/Default |
|:--------------|:----------------------------------------------------------------------------------|:-----------------|
| url           | The URL for your Home Assistant instance                                          | REQUIRED         |
| bearer_token  | The long-lived access token that Home Intent uses to interact with Home Assistant | REQUIRED         |
| prefer_toggle | Prefer to `toggle` instead using `on` or `off` when handling intents              | `true`           |

### On `prefer_toggle`
After a few years of running various voice assistants, I've noticed that they can really struggle with "on" and "off". It's particularly annoying when you're trying to turn off a light at night and nothing happens. At some point I played with switching it over to "toggle" instead of doing an "on" or "off" and everything works a lot better. This is why `prefer_toggle` defaults to `True`.

Currently `prefer_toggle` is only used for the following:

 * lights
 * switches

## Example Sentences
### Lights
### Shopping List
### Groups
### Switches