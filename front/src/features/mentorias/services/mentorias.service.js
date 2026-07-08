class MentoriasService {
  API = import.meta.env.VITE_API_URL;

  async getProgramas(servicio = "MENTORIA") {
    const response = await fetch(
      `${this.API}programas?page=0&size=10&tipo=${servicio}&activo=true`,
    );

    const result = await response.json();
    if (!response.ok) {
      throw new Error(
        result.mensaje || "Error al obtener las brechas territoriales",
      );
    }

    return result.content;
  }
}

export default new MentoriasService();
