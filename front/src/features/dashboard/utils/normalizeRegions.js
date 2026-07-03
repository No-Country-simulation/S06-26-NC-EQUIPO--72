// utils/normalizeRegion.js
function normalizeCongestion(valor) {
  // redondeo consistente sin importar de qué endpoint venga
  return Math.round(valor * 100) / 100;
}

export function normalizarRegiones(regiones = []) {
  return regiones.map((r) => ({
    ...r,
    congestionamento_medio: normalizeCongestion(r.congestionamento_medio),
  }));
}
