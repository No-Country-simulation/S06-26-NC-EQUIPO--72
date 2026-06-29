class AiService {
  API = import.meta.env.VITE_API_URL;

  async queryAiAgent(consulta, idioma = "es") {
    const response = await fetch(`${this.API}datos`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        consulta,
        idioma,
      }),
    });

    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.message || "Error al realizar la consulta al asistente de IA");
    }
    return result;
  }
}

export default new AiService();
