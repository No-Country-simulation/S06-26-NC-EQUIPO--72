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
}

export default new MapsService();
