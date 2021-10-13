#!/usr/bin/env bash
set -e

# clears the default (example) sentences.ini file for folks using the embedded system
mkdir -p /profiles/en && touch /profiles/en/sentences.ini

/usr/lib/rhasspy/bin/rhasspy-voltron --user-profiles /profiles --profile en &
supervisord --configuration /usr/src/app/setup/supervisord.conf