class EmpleabilidadService {
  API = import.meta.env.VITE_API_URL;

  async getEmpleabilidad(service = "EMPLEO") {
    const response = await fetch(`${this.API}brechas?servicio=${service}`);

    const result = await response.json();
    if (!response.ok) {
      throw new Error("Error al obtener las brechas", result.message);
    }
    return result;
  }
}

export default new EmpleabilidadService();
