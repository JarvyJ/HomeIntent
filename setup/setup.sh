#!/usr/bin/env bash
set -e
/usr/lib/rhasspy/bin/rhasspy-voltron --user-profiles /profiles --profile en &
supervisord --configuration /usr/src/app/setup/supervisord.conf