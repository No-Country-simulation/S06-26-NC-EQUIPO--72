// Servicio de comunicación con el backend para la sección de Experiencias.
// Proporciona métodos para listar, obtener brechas y registrar nuevas experiencias en la base de datos.
class ExperienciasService {
  // Obtenemos la URL de la API desde las variables de entorno de Vite
  API = import.meta.env.VITE_API_URL;

  /**
   * Obtiene la lista de programas filtrada por tipo.
   * Por defecto solicita "EXPERIENCIA" al backend.
   * 
   * @param {string} tipo - Tipo de programa a filtrar
   * @returns {Promise<Array>} Listado de experiencias del backend
   */
  async getProgramas(tipo = "EXPERIENCIA") {
    // Realizamos la llamada GET especificando un tamaño de página grande para traer todas las experiencias
    const response = await fetch(`${this.API}programas?size=100&tipo=${tipo}`);

    const result = await response.json();
    
    // Si la respuesta no es exitosa (código HTTP 4xx o 5xx), lanzamos un error con el mensaje del servidor
    if (!response.ok) {
      throw new Error(
        result.mensaje || "Error al obtener la lista de experiencias",
      );
    }

    // Devolvemos el array 'content' que contiene los registros de la base de datos o un array vacío por seguridad
    return result.content || [];
  }

  /**
   * Obtiene el análisis de brechas territoriales y de cobertura de servicios.
   * Por defecto se consulta para "EXPERIENCIA".
   * 
   * @param {string} servicio - Identificador del servicio de brechas
   * @returns {Promise<Object>} Datos de brechas territoriales
   */
  async getBrechas(servicio = "EXPERIENCIA") {
    // Solicitamos al endpoint /brechas el análisis territorial para el tipo de servicio especificado
    const response = await fetch(`${this.API}brechas?servicio=${servicio}`);

    const result = await response.json();
    
    if (!response.ok) {
      throw new Error(
        result.mensaje || "Error al obtener las brechas territoriales",
      );
    }

    return result;
  }

  /**
   * Envía una petición POST al servidor para dar de alta una nueva experiencia.
   * 
   * @param {Object} payload - Datos de la experiencia a crear
   * @returns {Promise<Object>} Respuesta de éxito de la operación
   */
  async createProgram(payload) {
    // Hacemos un POST a /programas mandando el payload serializado como JSON
    const response = await fetch(`${this.API}programas`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    
    if (!response.ok) {
      throw new Error(result.mensaje || "Error al registrar la experiencia");
    }

    return result;
  }
}

// Exportamos una única instancia del servicio para ser utilizada de manera global
export default new ExperienciasService();
