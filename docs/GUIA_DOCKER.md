
# Guía de Uso de Docker para el Proyecto App BiT

Esta guía de ayuda para configurar y usar Docker tanto con Docker Desktop (Windows/macOS/Linux) como con Docker en WSL (Windows Subsystem for Linux).

---

## Prerrequisitos

Antes de empezar, asegúrate de tener:
- Git instalado
- El repositorio del proyecto clonado

---

## 1. Instalación de Docker

### Opción A: Docker Desktop (Windows/macOS/Linux)
Docker Desktop es la opción más amigable, pero consume muchos recursos:
1. Descarga Docker Desktop desde [docker.com/get-started](https://www.docker.com/get-started)
2. Instálalo siguiendo las instrucciones del asistente
3. Inicia Docker Desktop y espera a que termine de cargar (vas a ver el ícono en la barra de tareas)
4. Verifica la instalación abriendo una terminal y ejecutando:
   ```bash
   docker --version
   docker-compose --version
   ```

### Opción B: Docker en WSL (Windows)
Si prefieres usar Docker directamente en WSL (sin Docker Desktop):
1. Asegúrate de tener WSL 2 instalado (sigue la [guía oficial](https://learn.microsoft.com/es-es/windows/wsl/install))
2. Instala Docker Engine en tu distribución WSL (ej: Ubuntu):
   ```bash
   # Actualiza los paquetes
   sudo apt update && sudo apt upgrade -y

   # Instala dependencias
   sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

   # Agrega la clave GPG oficial de Docker
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

   # Agrega el repositorio de Docker
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

   # Instala Docker Engine y Docker Compose
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

   # Agrega tu usuario al grupo docker para no usar sudo
   sudo usermod -aG docker $USER

   # Cerra la terminal actual y abri una nueva terminal de WSL 2
   ```
3. Verifica la instalación:
   ```bash
   docker --version
   docker compose version
   ```

---

## 2. Primeros Pasos con el Proyecto

### Paso 1: Configurar Variables de Entorno
Copia los archivos `.env.example` de cada servicio y llénalos con las credenciales:
```bash
# Para el servicio AI
cd ai
cp .env.example .env
# Edita ai/.env con las credenciales
```


### Paso 2: Iniciar Todos los Servicios
Desde la **raíz del proyecto** (donde está el archivo `docker-compose.yml`), ejecuta:
```bash
docker-compose up --build
```

Esto hace lo siguiente:
1. Construye las imágenes de los servicios (si no existen)
2. Inicia todos los contenedores en el orden correcto (DB -> Backend -> Frontend -> AI)
3. Muestra todos los logs de cada servicio en tiempo real

Para detener los servicios, presiona **Ctrl + C** en la terminal.

### Paso 3: Verificar que los Servicios Estén Corriendo
Abre una nueva terminal y ejecuta:
```bash
docker-compose ps
```

Deberías ver los contenedores con el estado `Up`:
- `Appbitb2g_Mysql` (DB)
- `Appbitb2g` (Backend)
- `react_app` (Frontend)
- `Appbitb2g_AI` (AI)

### Paso 4: Acceder a los Servicios
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8080
- **AI (Swagger UI)**: http://localhost:8000/docs
- **AI (Redoc)**: http://localhost:8000/redoc

