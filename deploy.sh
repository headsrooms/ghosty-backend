#!/usr/bin/env bash


set -e     # Stop on first error
set -u     # Stop if an unbound variable is referenced

curl -X POST https://api.digitalocean.com/v2/droplets \
-H "Authorization: Bearer a963fd011e73b202b7ba125c4740796f1a06a845f8c1ce77b06c1de8c4634787"

cd ghosty-backend/
git pull
sh redocker.sh