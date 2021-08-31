#!/usr/bin/env bash
set -e
/usr/lib/rhasspy/bin/rhasspy-voltron --user-profiles /profiles --profile en &
/usr/bin/python3 -m /usr/src/app/home_intent
