FROM python:3.9-slim
WORKDIR /usr/src/app/docs

COPY docs/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY docs .
RUN mkdocs build



FROM node:lts
WORKDIR /usr/src/app/ui/frontend

COPY ui/frontend/package.json ui/frontend/package-lock.json ./
RUN npm ci

COPY ui/frontend .
RUN npm run build



FROM rhasspy/rhasspy:2.5.10
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY --from=0 /usr/src/app/docs/site ./docs/site
COPY setup setup
COPY home_intent home_intent
COPY ui ui
COPY --from=1 /usr/src/app/ui/frontend/build ./ui/frontend/build

ENTRYPOINT [ "bash", "/usr/src/app/setup/setup.sh" ]
