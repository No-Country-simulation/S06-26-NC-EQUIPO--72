# === ETAPA 1: Compilación y construcción ===
FROM eclipse-temurin:21-jdk-jammy AS build
WORKDIR /app

# Instalamos dos2unix para corregir los saltos de línea de Windows (CRLF a LF)
RUN apt-get update && apt-get install -y dos2unix

COPY .mvn/ .mvn
COPY mvnw pom.xml ./

# Convertimos el archivo al formato Linux y asignamos permisos de ejecución
RUN dos2unix mvnw && chmod +x mvnw

# Descargamos dependencias y plugins (el || true evita que falle si un plugin da problemas)
RUN ./mvnw dependency:resolve-plugins dependency:go-offline -B || true

COPY src ./src
RUN ./mvnw clean package -DskipTests

# === ETAPA 2: Imagen final de ejecución ===
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app

# Creamos un usuario de sistema no-root por seguridad
RUN addgroup --system spring && adduser --system spring --ingroup spring
USER spring

# Copiamos el archivo .jar generado en la etapa anterior
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["sh", "-c", "java -Dserver.port=${PORT:-8080} -jar app.jar"]