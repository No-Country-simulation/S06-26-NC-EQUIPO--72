class FormacionesService {
  API = import.meta.env.VITE_API_URL;

  async getProgramas(tipo = "FORMACION", municipio = "Florianopolis") {
    const response = await fetch(`${this.API}programas?size=100&tipo=${tipo}&municipio=${municipio}`);

    const result = await response.json();
    if (!response.ok) {
      throw new Error(
        result.mensaje || "Error al obtener la lista de programas",
      );
    }

    return result.content || result || [];
  }


  async getBrechas(servicio = "FORMACION", municipio = "Florianopolis") {
    const response = await fetch(`${this.API}brechas?servicio=${servicio}&municipio=${municipio}`);

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
