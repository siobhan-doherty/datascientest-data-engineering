#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# clear out any leftover logs
rm -rf api_output && mkdir api_output

# ensure API image is present
docker pull datascientest/fastapi:1.0.0

# build all and run tests (will leave API running, tests exit automatically)
docker-compose up --build --abort-on-container-exit

echo
echo "──── All tests complete; here's your consolidated log ────"
cat api_output/api_test.log
