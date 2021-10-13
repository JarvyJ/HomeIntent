from pathlib import Path

RHASSPY_VERSION = "2.5.10"

BUILD_DOCS = """
FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app/docs

COPY docs/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY docs .
RUN mkdocs build
"""

BUILD_FRONTEND = """
FROM node:lts
WORKDIR /usr/src/app/ui/frontend

COPY ui/frontend/package.json ui/frontend/package-lock.json ./
RUN npm ci

COPY ui/frontend .
RUN npm run build
"""


BUILD_VENV = """
FROM python:3.7
WORKDIR /usr/src/app

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH="/venv/bin:$PATH"

RUN python -m venv /venv --copies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
"""


FINAL_BULD = """
FROM {build_image}
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

{extra}

COPY {venv_location} /venv
COPY {docs_location} ./docs/site
COPY setup setup
COPY home_intent home_intent
COPY ui ui
COPY {frontend_location} ./ui/frontend/build

ENTRYPOINT {entrypoint}
"""

WARNING = """### NOTE: THIS FILE IS AUTOGENERATED FROM generate_dockerfiles.py ###"""


def main():
    make_local_dockerfile()
    make_gh_actions_dockerfiles()


def write_dockerfile(filename: str, contents: str):
    file = Path(filename)
    if file.is_file():
        file.chmod(0o644)

    file.write_text(contents)
    file.chmod(0o444)


def make_local_dockerfile():
    final_build = FINAL_BULD.format(
        build_image=f"rhasspy/rhasspy:{RHASSPY_VERSION}",
        venv_location="--from=1 /venv",
        docs_location="--from=0 /usr/src/app/docs/site",
        frontend_location="--from=2 /usr/src/app/ui/frontend/build",
        extra="",
        entrypoint='[ "bash", "/usr/src/app/setup/setup.sh" ]',
    )

    dockerfile = f"""
{WARNING}

{BUILD_DOCS}

{BUILD_VENV}

{BUILD_FRONTEND}

{final_build}
"""
    write_dockerfile("Dockerfile", dockerfile)


def make_gh_actions_dockerfiles():
    make_static_dockerfile()
    make_rhasspy_external_dockerfile()
    make_gh_build_dockerfile()


def make_static_dockerfile():
    dockerfile = f"""
{WARNING}

{BUILD_DOCS}

{BUILD_FRONTEND}

FROM scratch
COPY --from=0 /usr/src/app/docs/site /docs/site
COPY --from=1 /usr/src/app/ui/frontend/build /ui/frontend/build
"""

    write_dockerfile("Dockerfile.static", dockerfile)


def make_rhasspy_external_dockerfile():
    final_build = FINAL_BULD.format(
        build_image="python:3.7-slim",
        venv_location="--from=0 /venv",
        docs_location="tmp/static/docs/site",
        frontend_location="tmp/static/ui/frontend/build",
        extra="RUN pip3 install --no-cache-dir supervisor",
        entrypoint='[ "supervisord", "--configuration", "/usr/src/app/setup/supervisord.conf" ]',
    )

    dockerfile = f"""
{WARNING}

{BUILD_VENV}

{final_build}
"""
    write_dockerfile("Dockerfile.rhasspy-external", dockerfile)


def make_gh_build_dockerfile():
    final_build = FINAL_BULD.format(
        build_image=f"rhasspy/rhasspy:{RHASSPY_VERSION}",
        venv_location="--from=0 /venv",
        docs_location="tmp/static/docs/site",
        frontend_location="tmp/static/ui/frontend/build",
        extra="",
        entrypoint='[ "bash", "/usr/src/app/setup/setup.sh" ]',
    )

    dockerfile = f"""
{WARNING}

{BUILD_VENV}

{final_build}
"""
    write_dockerfile("Dockerfile.gh-build", dockerfile)


if __name__ == "__main__":
    main()
