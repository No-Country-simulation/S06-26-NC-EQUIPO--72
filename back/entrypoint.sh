#!/bin/bash
set -e

echo "Iniciando backend con hot reload..."

get_hash() {
  find ./src -name "*.java" -exec md5sum {} \; 2>/dev/null | sort | md5sum
}

watch_and_compile() {
  echo "Watcher iniciado con PID $$"
  local last_hash
  last_hash=$(get_hash)

  while true; do
    sleep 2
    current_hash=$(get_hash)

    if [ "$current_hash" != "$last_hash" ]; then
      echo "Cambio detectado, recompilando..."
      if ./mvnw compile -q 2>&1; then
        echo "Recompilado OK"
      else
        echo "Error al compilar"
      fi
      last_hash="$current_hash"
    fi
  done
}

echo "Compilación inicial..."
./mvnw compile -q

# Arranca watcher en background y guardamos PID
watch_and_compile &
WATCHER_PID=$!
echo "Watcher PID: $WATCHER_PID"

# Mata el watcher si la app muere
trap "echo 'Deteniendo watcher...'; kill $WATCHER_PID 2>/dev/null" EXIT

echo "Arrancando Spring Boot..."
./mvnw spring-boot:run -Dspring-boot.run.fork=false