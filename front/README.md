# App BiT Frontend - Sistema de Gestión de Brechas Digitales e Inclusión (B2G)

Este directorio contiene la aplicación del lado del cliente (Frontend) del proyecto **App BiT**, un panel de datos públicos para la gestión de brechas digitales e inclusión (B2G).

---

## Tecnologías Utilizadas

El frontend está desarrollado sobre un stack de tecnologías modernas enfocadas en el rendimiento, accesibilidad y una estética visual de primer nivel:

- **React 19**
- **Vite 8**
- **Tailwind CSS v4**
- **TanStack React Query v5**
- **Recharts v3**
- **Radix UI**
- **Shadcn UI / Tailwind CSS**
- **Lucide React**

---

## Anatomía de la Aplicación (Estructura de Directorios)

El código fuente está estructurado de forma modular y organizada en base a características de negocio (feature-based):

```text
front/
├── public/                 # Recursos estáticos globales (imágenes, logos)
└── src/
    ├── app/                # Configuración transversal del proyecto
    │   ├── layouts/        # Layouts principales de las páginas (ej: MainLayout con sidebar)
    │   ├── providers/      # Proveedores de contexto globales (React Query, etc.)
    │   └── router/         # Rutas e intercambio de vistas principales
    ├── components/         # Componentes transversales del diseño
    │   └── ui/             # Componentes base e interactivos reutilizables (Shadcn/UI)
    ├── context/            # Contextos globales de React
    ├── features/           # Módulos de funcionalidad y negocio
    │   ├── ai-assistant/   # Chat interactivo con el Agente de Inteligencia Artificial (Text-to-SQL)
    │   ├── alertas/        # Panel de alertas de brechas y novedades
    │   ├── configuracion/  # Ajustes de idioma y panel de control
    │   ├── dashboard/      # Vista de Landing y panel general con Clusters territoriales
    │   ├── empleabilidad/  # Indicadores, evolución y brechas de empleo formal
    │   ├── experiencias/   # Experiencias estructurantes y programas de inclusión
    │   ├── formaciones/    # Programas formativos, educación e indicadores
    │   ├── mapa/           # Mapeo y análisis geográfico/indicadores territoriales
    │   ├── mentorias/      # Registro e indicadores de programas de mentorías
    │   ├── reportes/       # Exportación de reportes ejecutivos
    │   └── salud-mental/   # Indicadores y tasas de internaciones psiquiátricas
    ├── hooks/              # Custom hooks globales
    ├── shared/             # Recursos, servicios y constantes comunes compartidos
    │   ├── services/       # Clientes de API globales (Vacíos en favor de servicios de feature)
    │   ├── utils/          # Utilidades y funciones helper
    │   └── styles/         # Estilos globales y variables de tema
    ├── index.css           # Punto de entrada de Tailwind CSS y estilos base
    ├── App.jsx             # Componente raíz con el selector de vistas principal
    └── main.jsx            # Punto de entrada y renderizado del árbol React
```

### Modularidad por Features

Cada módulo dentro de `src/features/` sigue un patrón modular limpio, aislando sus componentes, páginas, hooks y llamadas de red específicas:

- `hooks/`: Lógica personalizada y hooks reactivos propios del módulo (ej: `useEmpleabilidad.js`).
- `pages/`: Vistas de página principales del módulo (ej: `EmpleabilidadPage.jsx`).
- `components/`: Subcomponentes específicos de esa feature.
- `services/`: Llamadas HTTP y servicios para comunicarse con la API de ese módulo.
- `skeletons/`: Vistas de carga adaptadas al diseño del módulo.

---

## Integración con la API y Variables de Entorno

El frontend se conecta con el servicio Backend de App BiT mediante solicitudes HTTP (fetch/React Query) guiadas por variables de entorno locales o del servidor:

Crea un archivo `.env` en la raíz de la carpeta `front/` (puedes tomar como base .env.example):

```env
# URL de conexión al backend de App BiT
VITE_API_URL=http://localhost:8080/api/
```

_Nota: Todas las variables expuestas en el código del cliente mediante Vite deben llevar el prefijo `VITE_`.\_

---

## Instrucciones para Ejecutar el Proyecto Localmente

### Prerrequisitos

Asegúrate de tener instalados los siguientes componentes:

1.  **Node.js** (Versión `20.x` o superior recomendada)
2.  **npm** (O gestor de paquetes de tu preferencia como `pnpm` o `yarn`)

### Paso 1: Instalación de Dependencias

Dentro del directorio `front/`, ejecuta el comando para descargar los paquetes necesarios:

```bash
npm install
```

### Paso 2: Configurar las Variables de Entorno

Copia el archivo de ejemplo y edita el archivo resultante:

```bash
cp .env.example .env
```

_(Modifica la variable `VITE_API_URL` si el puerto o la dirección de tu backend local cambian)._

### Paso 3: Levantar el Servidor de Desarrollo

Para correr la aplicación en local con recarga rápida (HMR), ejecuta:

```bash
npm run dev
```

La aplicación estará disponible por defecto en: [http://localhost:5173](http://localhost:5173).

---

## Despliegue en Producción

La compilación optimizada de la aplicación está preparada para ser desplegada en plataformas PaaS o de hosting estático (Render, Vercel, Netlify, AWS S3, etc.).

### Compilar para Producción

Ejecuta el siguiente comando para empaquetar y optimizar la app:

```bash
npm run build
```

Este proceso generará una carpeta `dist/` en la raíz del frontend.

### Configuración sugerida para Despliegue Estático (ej: Render)

1.  Crea un nuevo **Static Site** en la plataforma de Render.
2.  Conéctalo a tu repositorio de GitHub.
3.  Establece la siguiente configuración:
    - **Branch**: Elegir la rama correspondiente (ej: `develop` o `main`).
    - **Root Directory**: `front` (Indica que solo debe leer esta carpeta).
    - **Build Command**: `npm run build`.
    - **Publish Directory**: `dist`.
4.  Agrega la variable de entorno en el panel correspondiente:
    - `VITE_API_URL`: La dirección pública HTTPS de tu backend (ej: `https://s06-26-nc-equipo-72.onrender.com/api/`).