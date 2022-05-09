#!/bin/bash
#
# SPDX-License-Identifier: Apache-2.0
#
# Usage: $ ./seed.sh
# courtesy of the Marquez Repo
# https://github.com/MarquezProject/marquez

set -e

if [[ -z "${MARQUEZ_CONFIG}" ]]; then
  MARQUEZ_CONFIG='marquez.dev.yml'
  echo "WARNING 'MARQUEZ_CONFIG' not set, using development configuration."
fi

java -jar marquez-api-*.jar seed --host "${MARQUEZ_HOST:-localhost}" --port "${MARQUEZ_PORT:-5000}" "${MARQUEZ_CONFIG}"
