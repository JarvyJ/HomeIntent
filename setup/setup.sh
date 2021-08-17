#!/usr/bin/env bash
set -e
/usr/lib/rhasspy/bin/voltron-run python3 -m rhasspysupervisor \
        --profile "en" \
        --user-profiles "/profiles" \
        --docker-compose ''

sed -i -e 's/ --debug//g' /profiles/en/supervisord.conf
cat /usr/src/app/setup/home_intent.conf >> /profiles/en/supervisord.conf 
bash /usr/lib/rhasspy/bin/rhasspy-voltron --nogenerate-conf --user-profiles /profiles --profile en
