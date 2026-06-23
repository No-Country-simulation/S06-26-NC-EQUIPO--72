class FormacionesService {
  API = import.meta.env.VITE_API_URL;

  async getProgramas(tipo = "FORMACION") {
    const response = await fetch(`${this.API}programas?size=100&tipo=${tipo}`);

    const result = await response.json();
    if (!response.ok) {
      throw new Error(
        result.mensaje || "Error al obtener la lista de programas",
      );
    }

    return result.content || [];
  }


  async getBrechas(servicio = "FORMACION") {
    const response = await fetch(`${this.API}brechas?servicio=${servicio}`);

    const result = await response.json();
    if (!response.ok) {
      throw new Error(
        result.mensaje || "Error al obtener las brechas territoriales",
      );
    }

    return result;
  }

  async createProgram(payload) {
    const response = await fetch(`${this.API}programas`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.mensaje || "Error al registrar el programa");
    }

    return result;
  }
}

export default new FormacionesService();
