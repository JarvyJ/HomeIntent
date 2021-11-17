#!/usr/bin/env bash
set -e

# clears the default (example) sentences.ini file for folks using the embedded system
mkdir -p /profiles/${LANGUAGE} && echo -n > /profiles/${LANGUAGE}/sentences.ini

/usr/lib/rhasspy/bin/rhasspy-voltron --user-profiles /profiles --profile ${LANGUAGE} &
supervisord --configuration /usr/src/app/setup/supervisord.conf
