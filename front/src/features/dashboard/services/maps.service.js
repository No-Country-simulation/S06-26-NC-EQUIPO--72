class MapsService {
  API = import.meta.env.VITE_API_URL;

  async getMapsIndicators(category) {
    const response = await fetch(
      `${this.API}mapa/indicadores?categoria=${category}`,
    );

    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener los indicadores", result.message);
    }
    return result;
  }

  async getMapData(params = {}) {
    const searchParams = new URLSearchParams(params);
    const response = await fetch(
      `${this.API}mapa?${searchParams.toString()}`,
    );

    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener datos del mapa", result.message);
    }
    return result;
  }

  async getPrograms(params = {}) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, value);
      }
    });
    
    const response = await fetch(
      `${this.API}programas?${searchParams.toString()}`,
    );

    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener programas", result.message);
    }
    return result;
  }
}

export default new MapsService();
