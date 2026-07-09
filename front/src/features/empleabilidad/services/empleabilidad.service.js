class EmpleabilidadService {
  API = import.meta.env.VITE_API_URL;

  async getEmpleabilidad(categoria = "EMPLEO") {
    const response = await fetch(`${this.API}mapa/indicadores?categoria=${categoria}`);

    const result = await response.json();
        console.log("resultado es ", result);

    if (!response.ok) {
      throw new Error("Error al obtener los indicadores de empleabilidad", result.message);
    }
    return result;
  }

  async getIndicadoresEvolucion(categoria = "EMPLEO", indicador = "taxa_emprego_formal", municipio = null) {
    let url = `${this.API}mapa/indicadores/evolucion?categoria=${categoria}&indicador=${indicador}`;
    if (municipio) {
      url += `&municipio=${municipio}`;
    }
    const response = await fetch(url);

    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener la evolución de indicadores", result.message);
    }
    return result;
  }
}

export default new EmpleabilidadService();
