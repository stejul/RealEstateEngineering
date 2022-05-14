
#!/bin/bash
#
# SPDX-License-Identifier: Apache-2.0
#
# Usage: $ ./init-db.sh
# courtesy of the Marquez Repo
# https://github.com/MarquezProject/marquez

set -eu

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" > /dev/null <<-EOSQL
  CREATE USER ${MARQUEZ_USER};
  ALTER USER ${MARQUEZ_USER} WITH PASSWORD '${MARQUEZ_PASSWORD}';
  CREATE DATABASE ${MARQUEZ_DB};
  GRANT ALL PRIVILEGES ON DATABASE ${MARQUEZ_DB} TO ${MARQUEZ_USER};
EOSQL

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" > /dev/null <<-EOSQL
  CREATE USER ${AIRFLOW_USER};
  ALTER USER ${AIRFLOW_USER} WITH PASSWORD '${AIRFLOW_PASSWORD}';
  CREATE DATABASE ${AIRFLOW_DB};
  GRANT ALL PRIVILEGES ON DATABASE ${AIRFLOW_DB} TO ${AIRFLOW_USER};
EOSQL
