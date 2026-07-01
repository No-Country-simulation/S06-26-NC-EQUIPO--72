#!/bin/bash
set -e

# Crea un usuario de solo lectura para el agente de IA
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<-EOSQL
    CREATE USER IF NOT EXISTS '${DB_READONLY_USER}'@'%' IDENTIFIED BY '${DB_READONLY_PASSWORD}';
    GRANT SELECT ON ${MYSQL_DATABASE}.* TO '${DB_READONLY_USER}'@'%';
    FLUSH PRIVILEGES;
EOSQL
