class MapsService {
  API = import.meta.env.VITE_API_URL;

  async getMapsIndicators(category, indicator = null) {
    const url = new URL(`${this.API}mapa/indicadores`);
    url.searchParams.set("categoria", category);
    if (indicator) {
      url.searchParams.set("indicador", indicator);
    }
    const response = await fetch(url.toString());

    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener los indicadores", result.message);
    }
    return result;
  }

  async getRegions() {
    const response = await fetch(`${this.API}regiones`);
    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener las regiones", result.message);
    }
    return result;
  }

  async getMapData(params = {}) {
    const url = new URL(`${this.API}mapa`);
    Object.entries(params).forEach(([key, value]) => {
      if (value) url.searchParams.set(key, value);
    });
    const response = await fetch(url.toString());
    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener datos del mapa", result.message);
    }
    return result;
  }

  async getPrograms(params = {}) {
    const url = new URL(`${this.API}programas`);
    Object.entries(params).forEach(([key, value]) => {
      if (value) url.searchParams.set(key, value);
    });
    const response = await fetch(url.toString());
    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener programas", result.message);
    }
    return result;
  }
}

export default new MapsService();
