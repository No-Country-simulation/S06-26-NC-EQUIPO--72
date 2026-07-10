const bordeIzquierdoMapa = [
  [80, 60],
  [60, 140],
  [80, 300],
  [40, 360],
];

const pared0 = [
  [220, 50],
  [250, 140],
  [180, 280],
  [210, 390],
];

const pared1 = [
  [380, 50],
  [380, 150],
  [430, 270],
  [420, 400],
];

export function generarMapaOrganico(data = []) {
  const paredes = [bordeIzquierdoMapa, pared0, pared1];

  // Función para autogenerar la siguiente pared irregular (paredX)
  const obtenerParedX = (colIndex) => {
    while (paredes.length <= colIndex) {
      const prevPared = paredes[paredes.length - 1];
      const nuevoIndice = paredes.length;

      const newPared = prevPared.map((punto, i) => {
        const anchoPromedio = 145;

        // Magia Orgánica: Alternamos las coordenadas matemáticas para crear polígonos asimétricos.
        // Hacemos que los puntos "reboten" ligeramente en X y Y.
        const waveX =
          (i % 2 === 0 ? 18 : -14) * (nuevoIndice % 2 === 0 ? 1 : -1);
        const waveY =
          (i % 2 === 0 ? -12 : 16) * (nuevoIndice % 2 === 0 ? -1 : 1);

        return [punto[0] + anchoPromedio + waveX, punto[1] + waveY];
      });
      paredes.push(newPared);
    }
    return paredes[colIndex];
  };

  return data.map((regio, index) => {
    const colIndex = Math.floor(index / 3);
    const rowIndex = index % 3;

    const leftPared = obtenerParedX(colIndex);
    const rightPared = obtenerParedX(colIndex + 1);

    const iTop = rowIndex;
    const iBottom = rowIndex + 1;

    const generatePoints = `${leftPared[iTop].join(",")} ${rightPared[iTop].join(",")} ${rightPared[iBottom].join(",")} ${leftPared[iBottom].join(",")}`;

    return { ...regio, points: generatePoints };
  });
}
