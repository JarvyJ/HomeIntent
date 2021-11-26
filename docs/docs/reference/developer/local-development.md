# Local Home Intent Development
Home Intent can be developed locally by using a series of containers that have all been defined in the [`docker-compose.yaml`](https://github.com/JarvyJ/HomeIntent/blob/main/docker-compose.yaml). So now, with just a little bit of Docker knowledge, developing on Home Intent should be a lot easier.

NOTE: The examples are using `docker-compose`, newer versions of the Docker cli can use `docker compose` on Mac/Windows.

## Basic Development Setup
The development environment is setup to run from the `development-env` directory. Inside there there is a `config` folder that includes `config.example.yaml`. This is a starting `config.yaml` intended for development. Feel free to copy `config.examples.yaml` to `config.yaml` and enable integrations or add customizations to the folder.

After you have a `config.yaml` in the `development-env` directory, you can start a full development environment you can spin up by doing the following:

```
docker-compose up
```

Below mentions some of the caveats of containerized development and how to do run certain components as needed. We want to make the local development experience better, and will look for ways to do that in the future!

## Docs Development
The docs container will spin up a local mkdocs server and will hot reload as the Markdown files in the `docs` directory are changed. If you want to only work on docs, you can spin it up with the following command:

```
docker-compose up docs
```

This will start a server at [`http://localhost:8000`](http://localhost:8000) where you can see the rendered docs.

## Frontend Development
Frontend development will spin up a local node server that runs [SvelteKit](https://kit.svelte.dev/) and will hot reload as the Svelte files in `ui/frontend` are changed. It relies on the API development container to run and will spin it up automatically if it's not specified.

```
docker-compose up api frontend
```

This will start a server at [`http://localhost:3000`](http://localhost:3000) where you can see the rendered frontend.

Notably some of the Frontend/API features do not work in the containerized development environment as they rely on being deployed in the same location as Home Intent. This includes restarts and testing some of the sound functionality (which is disabled for externally managed Rhasspy in the UI).

## API Development
The API is built using [FastAPI](https://fastapi.tiangolo.com) and supports hot reload as Python files in the `ui` folder are changed.

```
docker-compose up api
```

This will start a server at [`http://localhost:11102/openapi`](http://localhost:11102/openapi)

It has the same caveats as mentioned in the Frontend Development section above. Also, if the docs/frontend are built in their respective directories, the API should host them and will be available at [`http://localhost:11102`](http://localhost:11102).

## Home Intent Development
Home Intent development is done in Python and currently **does not** support hot reload. We want to enable it, but haven't had enough time to get it working.

To start Home Intent in a container:
```
docker-compose up homeintent
```

If you make changes, you will have to `ctrl+c` out and then restart using the command above. Also, if you have spun up the entire development environment with `docker-compose up`, you can manually stop Home Intent with the following:
```
docker-compose stop homeintent
```

The Home Intent development container has the one issue of not sharing the filesystem with Rhasspy, so custom Rhasspy intent/error sounds can't be loaded. It's why `beeps` is set to `false` under `home_intent` in the development `config.yaml`.

## General Development Recommendations
When you are done doing any local development, you should probably stop whatever development containers may have been started by doing the following:

```
docker-compose stop
```

The last thing that's worth noting is that if you pull in updates from GitHub, you should run the `docker-compose up` command with the `--build` flag to rebuild any of the underlying containers.
