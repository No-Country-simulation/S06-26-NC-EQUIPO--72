
<img width="768" height="260" alt="logoo" src="https://github.com/user-attachments/assets/6ebed2a1-bd5e-4d61-8349-00fecfeb7d99" />


<h2 align="left"> Sistema de Gestión de Brechas Digitales e Inclusión (B2G)</h2>


![Static Badge](https://img.shields.io/badge/Equipo_72-No_Country-blue)
![Badge en Desarollo](https://img.shields.io/badge/STATUS-%20FINALIZADO-green)

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=spring&logoColor=white)
![Maven](https://img.shields.io/badge/Apache_Maven-C71A36?style=flat-square&logo=apache-maven&logoColor=white)
![TiDB](https://img.shields.io/badge/TiDB-00758F?style=flat-square&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white)
![Static Badge](https://img.shields.io/badge/MySQL-00758F)
![Swagger](https://img.shields.io/badge/-Swagger-%2385EA2D?style=flat-square&logo=swagger&logoColor=black)
![Spring Data JPA](https://img.shields.io/badge/Spring_Data_JPA-6DB33F?style=flat-square&logo=spring&logoColor=white)
![Hibernate](https://img.shields.io/badge/Hibernate-59666C?style=flat-square&logo=hibernate&logoColor=white)



## 📝 Descripción del Proyecto
El **Sistema de Gestión de Brechas Digitales e Inclusión (B2G)** es una plataforma de analítica territorial diseñada para gobiernos y organizaciones. Su objetivo es centralizar, cruzar y visualizar datos críticos como la infraestructura de red móvil (antenas) y los indicadores socioeconómicos locales (empleo, educación y salud mental). 

A través de este motor, los tomadores de decisiones pueden identificar qué regiones sufren de exclusión digital y coordinar planes de acción basados en datos reales.

## ⚡ Características Principales
* **Mapeo de Infraestructura:** Consulta y procesamiento geográfico de datos de antenas y niveles de congestión de red en tiempo real.
* **Tendencias Históricas Cruzadas:** Endpoints optimizados que unifican estadísticas de empleo mensuales con la calidad de conectividad por clusters.
* **Arquitectura de Alto Rendimiento:** Consultas nativas eficientes (CTEs y JSON) que delegan el procesamiento pesado a la base de datos para respuestas en milisegundos.
* **Documentación Interactiva:** Contratos de API totalmente integrados con Swagger para facilitar el trabajo en paralelo con el Frontend.


## 📂 Arquitectura y Estructura de Capas
El código fuente se organiza bajo una arquitectura modular y limpia dentro del paquete raíz `com.example.appbitb2g`, dividiendo las responsabilidades de forma estricta:
* **Controladores (`controller`):** Puerta de entrada que expone los endpoints de la API REST, gestiona los métodos HTTP, políticas de CORS y validaciones iniciales.
* **DTOs (`dto`):** Objetos de transferencia de datos inmutables definidos mediante **Records de Java**, encargados de transportar la información blindando las entidades de la base de datos y cumpliendo el contrato JSON con el Frontend.
* **Servicios (`service` e `service.impl`):** Núcleo de la lógica de negocio donde se procesan, unifican y filtran los flujos de datos (usando Java Streams y manejo seguro de nulos) antes de enviarlos a la vista.
* **Persistencia y Modelos (`model` y `repository`):** Capa encargada del mapeo de entidades con Hibernate y la comunicación con MySQL/TiDB mediante Spring Data JPA, incluyendo las consultas nativas optimizadas.

## 🚦Endpoints de la API y Contratos de Datos

### Documentación Swagger
La API cuenta con documentación interactiva generada automáticamente con Swagger/OpenAPI. Una vez que el servicio esté corriendo (ya sea en local o en producción), puedes explorar los endpoints, ver los esquemas de datos y realizar peticiones de prueba desde tu navegador.

- URL de Producción: https://s06-26-nc-equipo-72.onrender.com/api/swagger-ui/index.html

- URL Local (por defecto): http://localhost:8080/api/swagger-ui/index.html (Asegúrate de ajustar el puerto si tu configuración local difiere).

## 🚀 Instrucciones para Correr el Proyecto Localmente

### Prerrequisitos
* Docker y Docker Compose instalados.
* Git.

### 🛠️ Pasos para la Ejecución con Docker

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/ginaCapuchina/S06-26-NC-EQUIPO72.git](https://github.com/ginaCapuchina/S06-26-NC-EQUIPO72.git)
   cd S06-26-NC-EQUIPO72/back

2. **Configurar las variables de entorno:**
    ```bash
    Asegúrate de configurar las credenciales de tu base de datos y servicios en el archivo .env local
    (o pasarlas como variables al contenedor) respetando las llaves
    requeridas (SPRING_DATASOURCE_URL, SPRING_DATASOURCE_USERNAME, etc.) *(Mas detalle siguiente sección)
3. **Construir y levantar el contenedor:**
   ```bash
    # Si usan Docker Compose para levantar el entorno completo:
     docker compose up --build

     # O si construyen la imagen individualmente:
     docker build -t app-b2g-back .
     docker run -p 8080:8080 --env-file .env app-b2g-back
   
El servidor web se compilará y empaquetará automáticamente dentro del contenedor, quedando disponible en el puerto 8080.

## Despliegue en Producción

Este servicio backend está preparado para ser desplegado en cualquier plataforma de tipo PaaS que acepte archivos de tipo __Dockerfile__.
En este caso el servicio se encuentra desplegado en la plataforma __Render__ mediante el archivo `Dockerfile` que se encuentra en la raíz del proyecto.

Si necesitas replicar este despliegue o configurar un entorno de staging, sigue estas instrucciones:

### 1. Configuración del Servicio en Render

- Crea un nuevo Web Service en Render y conéctalo al repositorio de GitHub.
- Llena los campos de configuración principales con los siguientes valores:
  - Branch: elegir la rama del repositorio remoto (`main`, `develop`, etc).
  - Root Directory: `back` (Crítico: Esto le indica a Render que solo debe leer la carpeta del backend y su `Dockerfile`).
  - Runtime: Docker (Crítico: No usar entornos nativos, seleccionar Docker).
  - Instance Type: Free (o la capa requerida).

Nota: Los campos de "Build Command" y "Start Command" serán ignorados o desaparecerán al elegir Docker, ya que el Dockerfile interno se encarga de empaquetar con Maven y arrancar el servidor. Si se elige la capa gratuita que ofrece Render, el servicio desplegado sufrirá de un cold-start debido a que la plataforma suele poner en suspención los servicios desplegados de forma gratuita. El tiempo de inicialización del servicio luego de la suspensión automática suele rondar lo 4 o 5 min.

### 2. Variables de Entorno (Environment Variables)
Para que el contenedor de Spring Boot logre comunicarse con la base de datos externa y el servicio de IA del cual depende, se deben agregar estrictamente las siguientes variables de entorno en el panel de Render (pestaña Environment).

Spring Boot utilizará la característica de Relaxed Binding para sobrescribir los valores locales de application.properties.

| **Nombre dela Variable (Key)** | **Valor Esperado (Value)** | **Descripción** | 
| --- | --- | --- |
| `AI_SERVICE_URL` | `url_ia_service` | URL del servicio de IA |
| `SPRING_DATASOURCE_URL` | `jdbc:mysql://[DB_HOST]:[DB_PORT]/[DB_NAME]??sslMode=VERIFY_IDENTITY&serverTimezone=UTC` | La URL de conexión JDBC. Debe incluir `sslMode=VERIFY_IDENTITY` por seguridad y separar las credenciales. |
| `SPRING_DATASOURCE_USERNAME` | `db_user_example` | El usuario de la base de datos de producción. |
| `SPRING_DATASOURCE_PASSWORD` | `********` | La contraseña asignada por el proveedor de la base de datos. |
<br>

__Importante sobre el Puerto:__ No es necesario configurar una variable PORT manual. En este caso Render inyecta dinámicamente el puerto, y el Dockerfile del proyecto está preparado para leerlo y asignar Spring Boot al puerto correcto de forma automática.

### 3. Base de Datos Externa
La instancia de MySQL no corre dentro de Render por motivos de persistencia de disco y cuota de espacio. Las credenciales insertadas en el paso anterior deben obtenerse del panel de control del clúster de MySQL del proveedor que se haya seleccionado.
En nuestro caso se ha elegido __TiDB__ como proveedor de servicio para almacenar los datos en una instancia de MySQL.

Para conectarte localmente a esta base de datos de producción (ej. usando DBeaver o MySQL Workbench), recuerda que se debe configurar la conexión requiriendo SSL (Use SSL: Require).

## Autores

| [<img src="https://github.com/ginaCapuchina.png" width=115><br><sub><b>Georgina Bosque</b></sub>](https://github.com/ginaCapuchina) | [<img src="https://github.com/Malmaraz1.png" width=115><br><sub><b>Matías Almaraz</b></sub>](https://github.com/Malmaraz1) | [<img src="https://github.com/CoraYako.png" width=115><br><sub><b>Héctor Cortez</b></sub>](https://github.com/CoraYako) | [<img src="https://github.com/Barreratomas.png" width=115><br><sub><b>Tomás Barrera</b></sub>](https://github.com/Barreratomas) |
| :---: | :---: | :---: | :---: |
