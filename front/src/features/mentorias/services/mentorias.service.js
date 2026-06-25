class MentoriasService {
  API = import.meta.env.VITE_API_URL;

  async getBrechas(servicio = "MENTORIA") {
    const response = await fetch(`${this.API}brechas?servicio=${servicio}`);

    const result = await response.json();
    if (!response.ok) {
      throw new Error(
        result.mensaje || "Error al obtener las brechas territoriales",
      );
    }

    return result;
  }
}

export default new MentoriasService();
