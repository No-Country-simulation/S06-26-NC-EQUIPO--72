# 🛰️ App BiT Backend - Sistema de Gestión de Brechas Digitales e Inclusión (B2G)

## 📂 Anatomía de las Capas (Estructura de Directorios)
El código fuente se organiza de la siguiente manera dentro del paquete raíz `com.example.appbitb2g`:
     
### 📥 Capa de Controladores (controller)
Es la puerta de entrada de la aplicación. Expone las rutas de la `API REST`, define los métodos 
`HTTP (GET, POST, PUT, DELETE),` habilita políticas de CORS para el Frontend y valida la consistencia 
de los datos recibidos mediante Query Params o Request Bodies.


### 📦Capa de Objetos de Transferencia de Datos (dto)
### ⚙️ Capa de Servicios (service e service.impl)
### 💾 Capa de Persistencia y Modelos (model y repository)


## 🚦Endpoints de la API y Contratos de Datos

### 📘 Documentación Swagger
La API cuenta con documentación interactiva generada automáticamente con Swagger/OpenAPI. Una vez que el servicio esté corriendo (ya sea en local o en producción), puedes explorar los endpoints, ver los esquemas de datos y realizar peticiones de prueba desde tu navegador.

- URL de Producción: https://s06-26-nc-equipo-72.onrender.com/api/swagger-ui/index.html

- URL Local (por defecto): http://localhost:8080/api/swagger-ui/index.html (Asegúrate de ajustar el puerto si tu configuración local difiere).

## 🚀Instrucciones para Correr el Proyecto Localmente


  ### Prerrequisitos
  - Java JDK 21 o superior.
  - Maven 3.8+.
  - Spring Boot
  - Docker

## ☁️ Despliegue en Producción (Render + Aiven)

El entorno de producción de este backend está configurado para desplegarse como un contenedor en la Plataforma como Servicio (PaaS) __Render__, conectándose a una base de datos MySQL gestionada por __Aiven__.

Si necesitas replicar este despliegue o configurar un entorno de staging, sigue estas instrucciones exactas:

### 1. Configuración del Servicio en Render

- Crea un nuevo Web Service en Render y conéctalo al repositorio de GitHub.
- Llena los campos de configuración principales con los siguientes valores:
  - Branch: elegir la rama del repositorio remoto (`main`, `develop`, etc).
  - Root Directory: `back` (⚠️ Crítico: Esto le indica a Render que solo debe leer la carpeta del backend y su `Dockerfile`).
  - Runtime: Docker (⚠️ Crítico: No usar entornos nativos, seleccionar Docker).
  - Instance Type: Free (o la capa requerida).

Nota: Los campos de "Build Command" y "Start Command" serán ignorados o desaparecerán al elegir Docker, ya que el Dockerfile interno se encarga de empaquetar con Maven y arrancar el servidor.

### 2. Variables de Entorno (Environment Variables)
Para que el contenedor de Spring Boot logre comunicarse con la base de datos externa y el servicio de IA, debes agregar estrictamente las siguientes variables de entorno en el panel de Render (pestaña Environment).

Spring Boot utilizará la característica de Relaxed Binding para sobrescribir los valores locales de application.properties.

| **Nombre dela Variable (Key)** | **Valor Esperado (Value)** | **Descripción** | 
| --- | --- | --- |
| `AI_SERVICE_URL` | `url_ia_service` | URL del servicio de IA |
| `SPRING_DATASOURCE_URL` | `jdbc:mysql://[HOST_AIVEN]:[PUERTO]/[DB_NAME]?ssl-mode=REQUIRED&serverTimezone=UTC` | La URL de conexión JDBC. Debe incluir ssl-mode=REQUIRED por seguridad y separar las credenciales. |
| `SPRING_DATASOURCE_USERNAME` | Usuario de Aiven (normalmente `avnadmin`) | El usuario de la base de datos de producción. |
| `SPRING_DATASOURCE_PASSWORD` | `********` | La contraseña asignada por Aiven. |
<br>

__Importante sobre el Puerto:__ No es necesario configurar una variable PORT manual. Render inyecta dinámicamente el puerto, y el Dockerfile del proyecto está preparado para leerlo y asignar Spring Boot al puerto correcto de forma automática.

### 3. Base de Datos Externa (Aiven)
La instancia de MySQL no corre dentro de Render por motivos de persistencia de disco. Las credenciales insertadas en el paso anterior deben obtenerse del panel de control de tu clúster de MySQL en Aiven Console o del entorno web de Aiven.

Para conectarte localmente a esta base de datos de producción (ej. usando DBeaver o MySQL Workbench), recuerda que debes configurar la conexión requiriendo SSL (Use SSL: Require).