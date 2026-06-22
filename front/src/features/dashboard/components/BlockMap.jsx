import { useState, useMemo } from "react";
import { generarMapaOrganico } from "../utils/organicMap";

// ENDPOINT: /mapa/indicadores
// {
//   "regiones": [
//     {
//       "cluster": "SAO_JOSE_KOBRASOL",
//       "municipio": "São José",
//       "lat": -27.5935,
//       "lon": -48.6358,
//       "n_usuarios": 12400,
//       "congestionamento_medio": 0.72,
//       "indicadores": [
//         {
//           "categoria": "SALUD_MENTAL",
//           "indicador": "taxa_internacao_psiquiatrica",
//           "valor": 14.2,
//           "unidad": "porcentaje",
//           "fonte": "DATASUS",
//           "fecha_referencia": "2025-12-01"
//         }
//       ]
//     }
//   ]
// }

const regiones = [
  {
    cluster: "AEROPORTO_HLZ",
    municipio: "Florianopolis",
    congestionamento_medio: 0.6,
    n_usuarios: 12400,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
  {
    cluster: "CAMPECHE",
    municipio: "Florianopolis",
    congestionamento_medio: 0.6,
    n_usuarios: 12300,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
  {
    cluster: "CANASVIEIRAS",
    municipio: "Florianopolis",
    congestionamento_medio: 0.7,
    n_usuarios: 12200,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
  {
    cluster: "CBD_BEIRAMAR",
    municipio: "Florianopolis",
    congestionamento_medio: 0.65,
    n_usuarios: 12100,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
  {
    cluster: "CENTRO_HISTORICO",
    municipio: "Florianopolis",
    congestionamento_medio: 0.82,
    n_usuarios: 13000,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
  {
    cluster: "COQUEIROS",
    municipio: "Florianopolis",
    congestionamento_medio: 0.52,
    n_usuarios: 13100,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
  {
    cluster: "ESTREITO_CAPOEIRAS",
    municipio: "Florianopolis",
    congestionamento_medio: 0.35,
    n_usuarios: 13200,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
  {
    cluster: "INGLESES",
    municipio: "Florianopolis",
    congestionamento_medio: 0.62,
    n_usuarios: 13200,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
  {
    cluster: "JURERE",
    municipio: "Florianopolis",
    congestionamento_medio: 0.2,
    n_usuarios: 13000,
    indicadores: [
      {
        categoria: "SALUD_MENTAL",
        indicador: "taxa_internacao_psiquiatrica",
        valor: 14.2,
        unidad: "porcentaje",
        fonte: "DATASUS",
        fecha_referencia: "2025-12-01",
      },
    ],
  },
];

const tabs = [
  { key: "empleo", label: "Tasa de Empleo" },
  { key: "conectividad", label: "Conectividad" },
  { key: "salud", label: "Salud Mental" },
  { key: "digital", label: "Inclusión Digital" },
];

const fillColors = {
  critico: "#f87171",
  alerta: "#fcd34d",
  bueno: "#86efac",
  optimo: "#93c5fd",
};

const regionesCompletas = generarMapaOrganico(regiones);

const regionTextCenter = regionesCompletas.map((region) => {
  const coords = region.points.split(" ").map((p) => p.split(",").map(Number));
  const centerPositionX =
    coords.reduce((sum, [x]) => sum + x, 0) / coords.length;
  const centerPositionY =
    coords.reduce((sum, [, y]) => sum + y, 0) / coords.length;
  return { ...region, centerPositionX, centerPositionY };
});

const getStatusFromCongestion = (value) => {
  if (value >= 0.75) return fillColors.optimo;
  if (value >= 0.55) return fillColors.bueno;
  if (value >= 0.35) return fillColors.alerta;
  return fillColors.critico;
};

const tabButtonClass = (isActive) =>
  `text-[11px] px-3 py-1.5 rounded-lg font-semibold border cursor-pointer ${
    isActive
      ? "bg-blue-600 border-blue-600 text-white"
      : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
  }`;

export const BlockMap = () => {
  const [activeMapTab, setActiveMapTab] = useState("empleo");
  const [tooltip, setTooltip] = useState({
    visible: false,
    x: 0,
    y: 0,
    region: null,
  });

  const viewBoxWidth = useMemo(() => {
    let maxX = 600;

    regionTextCenter.forEach((region) => {
      if (region.points) {
        const puntosX = region.points
          .split(" ")
          .map((p) => Number(p.split(",")[0]));

        const maxRegionX = Math.max(...puntosX);
        if (maxRegionX > maxX) {
          maxX = maxRegionX;
        }
      }
    });

    return Math.ceil(maxX + 30);
  }, []);

  const handleMouseEnter = (region, e) => {
    const svgElementRef = e.currentTarget.closest("svg");
    const containerRefRect =
      svgElementRef.parentElement.getBoundingClientRect();
    setTooltip({
      visible: true,
      x: e.clientX - containerRefRect.left,
      y: e.clientY - containerRefRect.top,
      region,
    });
  };

  const handleMouseMove = (e) => {
    const svgElementRef = e.currentTarget.closest("svg");
    const containerRefRect =
      svgElementRef.parentElement.getBoundingClientRect();
    setTooltip((prev) => ({
      ...prev,
      x: e.clientX - containerRefRect.left,
      y: e.clientY - containerRefRect.top,
    }));
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <h3 className="text-sm font-bold text-slate-800">
            Mapa de Inclusión Social
          </h3>
          <button className="text-xs text-blue-600 hover:text-blue-700 font-semibold">
            Ver detalle →
          </button>
        </div>
        {/* Tabs */}
        <div className="flex flex-wrap gap-1 mt-4">
          {tabs.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setActiveMapTab(key)}
              className={tabButtonClass(activeMapTab === key)}
            >
              {label}
            </button>
          ))}
        </div>
        {/* Organic Map */}
        <div className="flex justify-center relative">
          <svg
            width="100%"
            height="100%"
            viewBox={`0 0 ${viewBoxWidth} 450`}
            className="w-full max-w-2xl"
          >
            {regionTextCenter.map((region) => (
              <g
                key={region.cluster}
                className="cursor-pointer"
                onClick={() => console.log(`ver detalles de ${region.cluster}`)}
                onMouseEnter={(e) => handleMouseEnter(region, e)}
                onMouseMove={handleMouseMove}
                onMouseLeave={() =>
                  setTooltip({ visible: false, x: 0, y: 0, region: null })
                }
              >
                <polygon
                  points={region.points}
                  fill={getStatusFromCongestion(region.congestionamento_medio)}
                  stroke="#fff"
                  strokeWidth="3"
                  className="transition-all hover:opacity-80"
                />

                <text
                  x={region.centerPositionX}
                  y={region.centerPositionY - 8}
                  textAnchor="middle"
                  fontSize="10"
                  fontWeight="700"
                  fill="#111827"
                >
                  {region.cluster}
                </text>

                <text
                  x={region.centerPositionX}
                  y={region.centerPositionY + 15}
                  textAnchor="middle"
                  fontSize="14"
                  fontWeight="800"
                  fill="#111827"
                >
                  {`${region.congestionamento_medio * 100}%`}
                </text>
              </g>
            ))}
          </svg>

          {/* Custom Tooltip */}
          {tooltip.visible && tooltip.region && (
            <div
              className="pointer-events-none absolute z-50 w-56 rounded-2xl bg-white border border-slate-200 shadow-xl p-4"
              style={{
                left: tooltip.x + 12,
                top: tooltip.y - 10,
                transform: "translateY(-100%)",
              }}
            >
              <div className="flex items-start justify-between gap-1 flex-wrap">
                <h4 className="text-xs font-bold text-slate-800">
                  {tooltip.region.cluster}
                </h4>

                <span className="px-2 py-0.5 text-[11px] font-semibold rounded-md bg-slate-100 text-slate-500">
                  {(tooltip.region.n_usuarios / 10000).toFixed(1)}M hab.
                </span>
              </div>

              <div className="mt-3">
                <p className="text-sm text-slate-400">Empleo</p>

                <p className="text-sm font-bold text-blue-600">
                  {(tooltip.region.congestionamento_medio * 100).toFixed(0)}%
                </p>
              </div>
              <div className="mt-3">
                <p className="text-sm text-slate-400">Salud M.</p>

                <p className="text-sm font-bold text-blue-600">
                  {tooltip.region.indicadores[0].valor.toFixed(1)}%
                </p>
              </div>

              <div className="mt-3 border-t border-slate-200 pt-3">
                <p className="text-sm text-slate-400">
                  Clic para ver detalle
                  <span className="ml-1">→</span>
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Map Legend */}
      <div className="mt-6 border-t border-slate-100 pt-4 flex items-center justify-between text-[11px] text-slate-500 font-semibold">
        <div className="flex items-center gap-1.5">
          <span>Escala:</span>
          <div className="flex items-center gap-3 ml-2">
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 bg-red-400 border border-red-500 rounded-full inline-block" />{" "}
              Crítico
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 bg-amber-300 border border-amber-400 rounded-full inline-block" />{" "}
              Alerta
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 bg-green-200 border border-green-300 rounded-full inline-block" />{" "}
              Bueno
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 bg-blue-200 border border-blue-300 rounded-full inline-block" />{" "}
              Óptimo
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
