FROM rhasspy/rhasspy:2.5.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY setup setup
COPY home_intent home_intent

ENTRYPOINT [ "bash", "/usr/src/app/setup/setup.sh" ]
