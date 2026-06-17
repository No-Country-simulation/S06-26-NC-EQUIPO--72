----
name: "Reporte de Bug"
about: Plantilla avanzada de QA con severidad, prioridad y datos de prueba.
title: "[BUG] "
labels: bug
---

###ID
*Ej: BUG-001 (o dejar vacío si se usa el número correlativo de GitHub)*

### Título
*Breve y descriptivo (Ej: Error 404 al llamar al endpoint /datos con consulta vacía)*

### Descripción / Resumen
*Una explicación concisa de qué está fallando y cuándo ocurre.*

### Entorno
* **Dispositivo / Sistema Operativo:** (Ej: PC Windows 11 / iPhone 14)
* **Navegador y Versión:** (Ej: Chrome v125 / Safari)
* **Tipo de pantalla:** (Ej: Desktop / Mobile)

### Precondiciones
1. 
2. 

### Datos de Prueba
*Variables o inputs específicos que usaste (Ej: Texto ingresado = "", Región = "São Paulo")*

### Pasos para Reproducir
1. 
2. 
3. 

### Resultado Esperado
*¿Qué debería pasar en el sistema según el Criterio de Aceptación?*

### Resultado Obtenido
*¿Qué pasó realmente? (El comportamiento fallido).*

### Severidad
*Impacto técnico del error en la aplicación (Marcar con una 'X'):*
- [ ] **Bloqueante (Blocker):** La app se cae, pantalla en blanco, no se puede seguir probando nada.
- [ ] **Crítica (Critical):** Falla una funcionalidad principal sin camino alternativo.
- [ ] **Mayor (Major):** Falla una función importante, pero hay una alternativa para avanzar.
- [ ] **Menor (Minor):** Error estético, visual, un desbordamiento leve de UI o un texto mal escrito.

### Prioridad
*Urgencia para el negocio/desarrollo (Marcar con una 'X'):*
- [ ] **Alta:** Se tiene que resolver en este Sprint obligatoriamente.
- [ ] **Media:** Se puede resolver en el Sprint actual si hay tiempo, si no, pasa al siguiente.
- [ ] **Baja:** No urge, se puede resolver más adelante.

### Evidencia
*Arrastrá y soltá acá tus capturas de pantalla, videos o mensajes de la consola de desarrollo.*
