# S06-26-NC-EQUIPO--72

Panel de Datos Públicos - App BiT (B2G)

## Integrantes del Equipo

### 🎨 Frontend

| Nombre               | Rol                | GitHub                                             |
| -------------------- | ------------------ | -------------------------------------------------- |
| Juan Ramirez         | Frontend Developer | [@juanRCoder](https://github.com/juanRCoder)       |
| Lorenzo Segada Lopez | Frontend Developer | [@lorenzosegada](https://github.com/lorenzosegada) |

### 📋 Project Management

| Nombre                      | Rol             | GitHub                               |
| --------------------------- | --------------- | ------------------------------------ |
| Jonathan Axel Zappa Verardi | Project Manager | [@AxelJZ](https://github.com/AxelJZ) |

### 🧪 QA

| Nombre                     | Rol       | GitHub                                                       |
| -------------------------- | --------- | ------------------------------------------------------------ |
| Maria Grillo               | QA Tester | [@Mgrillo348](https://github.com/Mgrillo348)                 |
| Victoria Paula Del Giovine | QA Tester | [@victoriadelgiovine](https://github.com/victoriadelgiovine) |

### ⚙️ Backend e Infraestructura

| Nombre                | Rol                       | GitHub                                             |
| --------------------- | ------------------------- | -------------------------------------------------- |
| Héctor Armando Cortez | Backend Developer & Infra | [@CoraYako](https://github.com/CoraYako)           |
| Matias Almaraz        | Backend Developer         | [@Malmaraz1](https://github.com/Malmaraz1)         |
| Georgina Bosque       | Backend Developer         | [@GinaCapuchina](https://github.com/GinaCapuchina) |

### 🤖 Data e IA

| Nombre                      | Rol                                                | GitHub                                                       |
| --------------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| Rider Renato Manrique Cueto | Data  Developer                                    | [@ridermanriquecueto](https://github.com/ridermanriquecueto) |
| Tomás Barrera               | Líder Técnico - Fullstack (Back, Front, Data & IA) | [@Barreratomas](https://github.com/Barreratomas)             |

***

## Introducción y Contexto del Negocio

### ¿Qué es App BiT?

App BiT es una plataforma B2G (Business to Government) diseñada para transformar la gestión de políticas públicas de movilidad en ciudades inteligentes. Nace de la necesidad de los gestores públicos de acceder a datos complejos (más de 18 millones de datos) que hoy están atrapados en archivos dificiles de analizar (Excels).

### El problema que resuelve

Los equipos técnicos y analistas pierden horas buscando datos dispersos, mientras que los decisores políticos no pueden consultarlos sin intermediarios. App BiT elimina esta fricción: permite a un gestor preguntar en lenguaje natural (ej: "¿Cuál es el índice de movilidad en esta región?") y obtener una respuesta precisa en segundos, apoyada por el cruce de datos reales.

### Contexto del MVP

Para esta primera versión del producto, tomamos decisiones estratégicas de alcance estricto ("Trade-offs") para garantizar la viabilidad del proyecto dentro de un plazo acotado (5 semanas), priorizando la validación de la Inteligencia Artificial generativa sobre funcionalidades periféricas de software tradicional.

## Cómo Levantar el Proyecto con Docker

### Prerrequisitos

- Docker y Docker Compose instalados en tu sistema.

### Pasos para Levantar el Proyecto

1. **Preparar los datasets:**
   - Descarga los datasets CSV desde este [Google Drive](https://drive.google.com/drive/folders/1nXCg4Il5vmBI_5aldhNMPfAdp_dQyobE?usp=sharing)
   - Colócalos en la carpeta `ai/data/`:
     ```
     ai/data/
     ├── antenas_flp.csv
     ├── assinantes.csv
     ├── tensor_concentracao.csv
     ├── tensor_mobilidade.csv
     ├── tensor_od.csv
     └── tensor_fluxo_vias.csv
     ```
2. **Configurar variables de entorno del proyecto:**
   ```bash
   cp .env.example .env
   ```
   El archivo `.env` ya viene configurado con valores por defecto. Podes editarlo si necesitas cambiar credenciales o puertos.
3. **Configurar variables de entorno del AI Service:**
   ```bash
   cd ai
   cp .env.example .env
   ```
   Edita `ai/.env` con tus credenciales (necesarias para el agente de IA).
4. **Levantar todos los servicios con Docker Compose:**
   ```bash
   cd ..  # Volver a la raíz del proyecto
   docker-compose up --build
   ```

### Servicios Disponibles

- **Frontend**: <http://localhost:5173>
- **Backend (Spring Boot)**: <http://localhost:8080/api/swagger-ui/index.html>
- **AI Service**: <http://localhost:8000/docs>
- **phpMyAdmin**: <http://localhost:8081> (usuario: `root`, contraseña: `root`)

## Documentación técnica

- [Frontend](front/README.md)
- [Backend (Spring Boot)](back/README.md)
- [AI / DATA](ai/README.md)

