#!/bin/bash

echo "iniciando monitoreo de cambios en src/main/java y src/main/resources..."

# Monitorea cambios en directorios fuente y recompila automáticamente
while inotifywait -r -e modify,create,delete,move /app/src/main/java /app/src/main/resources; do
  echo "Cambios detectados - Recompilando..."
  ./mvnw compile -DskipTests
  echo "Compilación completada! Spring DevTools reiniciará la app automáticamente."
done
