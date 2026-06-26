#!/bin/bash

echo "Iniciando monitoreo de cambios..."

get_checksum() {
  find /app/src/main/java /app/src/main/resources -type f \
    \( -name "*.java" -o -name "*.xml" -o -name "*.properties" -o -name "*.yml" \) \
    -exec stat -c "%Y %n" {} \; 2>/dev/null | sort | md5sum
}

LAST_CHECKSUM=$(get_checksum)

while true; do
  sleep 3
  CURRENT_CHECKSUM=$(get_checksum)

  if [ "$CURRENT_CHECKSUM" != "$LAST_CHECKSUM" ]; then
    echo "Cambios detectados - Recompilando..."
    ./mvnw compile -DskipTests -q
    echo "Compilación completada! Spring DevTools reiniciará la app."
    LAST_CHECKSUM="$CURRENT_CHECKSUM"
  fi
done