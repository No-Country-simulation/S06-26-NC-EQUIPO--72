import { useState, useMemo } from "react";
import { generarMapaOrganico } from "../utils/organicMap";
import { useMapData, useMapsIndicators } from "../hooks/useMaps";
import { AlertCircle, ChartColumn, Layers } from "lucide-react";
import { BlockMapSkeleton } from "../skeletons/BlockMapSkeleton";
import { formatClusterName } from "@/shared/utils/format";
import { normalizarRegiones } from "../utils/normalizeRegions";

const tabs = [
  { key: "EMPLEO", label: "Empleo" },
  { key: "CONECTIVIDAD", label: "Conectividad" },
  { key: "SALUD_MENTAL", label: "Salud Mental" },
  { key: "EDUCACION", label: "Educacion" },
];

const indicadorPorCategoria = {
  EMPLEO: "taxa_emprego_formal",
  SALUD_MENTAL: "cobertura_atencao_basica",
  EDUCACION: "taxa_conclusao_ensino_medio",
};

const fillColors = {
  critico: "#f87171",
  alerta: "#fcd34d",
  bueno: "#86efac",
  optimo: "#93c5fd",
};

const getStatusFromValue = (tab, value) => {
  if (tab === "CONECTIVIDAD") {
    if (value > 85) return fillColors.critico;
    if (value > 35) return fillColors.alerta;
    if (value > 15) return fillColors.bueno;
    return fillColors.optimo;
  } else {
    if (value < 30) return fillColors.critico;
    if (value < 50) return fillColors.alerta;
    if (value < 75) return fillColors.bueno;
    return fillColors.optimo;
  }
};

const tabButtonClass = (isActive) =>
  `text-[11px] px-3 py-1.5 rounded-lg font-semibold border cursor-pointer ${
    isActive
      ? "bg-blue-600 border-blue-600 text-white"
      : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
  }`;

export const BlockMap = ({ onClusterSelect }) => {
  const [activeTab, setActiveTab] = useState("EMPLEO");
  const [tooltip, setTooltip] = useState({
    visible: false,
    x: 0,
    y: 0,
    region: null,
  });

  const indicadorActivo =
    activeTab !== "CONECTIVIDAD" ? indicadorPorCategoria[activeTab] : null;

  const filterRegiones = useMapsIndicators(activeTab, indicadorActivo);
  const regiones = useMapData();

  const isConectividad = activeTab === "CONECTIVIDAD";
  const rawData = isConectividad
    ? regiones.data?.regiones
    : filterRegiones.data?.regiones;

  const dataNormalizada = normalizarRegiones(rawData);
  const regionesCompletas = generarMapaOrganico(dataNormalizada);

  const regionTextCenter = regionesCompletas.map((region) => {
    const coords = region.points.split(" ").map((p) => p.split(",").map(Number));
    const centerPositionX = coords.reduce((sum, [x]) => sum + x, 0) / coords.length;
    const centerPositionY = coords.reduce((sum, [, y]) => sum + y, 0) / coords.length;

    let valorDisplay;
    if (isConectividad) {
      valorDisplay = (region.congestionamento_medio * 100).toFixed(0);
    } else {
      const indicadorEncontrado = region.indicadores?.find(
        (i) => i.indicador === indicadorActivo
      );
      valorDisplay = indicadorEncontrado?.valor ? indicadorEncontrado.valor.toFixed(0) : 0;
    }

    return { ...region, centerPositionX, centerPositionY, valorDisplay };
  });

  const viewBoxWidth = useMemo(() => {
    let maxX = 600;
    regionTextCenter.forEach((region) => {
      if (region.points) {
        const puntosX = region.points.split(" ").map((p) => Number(p.split(",")[0]));
        const maxRegionX = Math.max(...puntosX);
        if (maxRegionX > maxX) maxX = maxRegionX;
      }
    });
    return Math.ceil(maxX + 30);
  }, [rawData]);

  const handleMouseEnter = (region, e) => {
    const svgElementRef = e.currentTarget.closest("svg");
    const containerRefRect = svgElementRef.parentElement.getBoundingClientRect();
    setTooltip({
      visible: true,
      x: e.clientX - containerRefRect.left,
      y: e.clientY - containerRefRect.top,
      region,
    });
  };

  const handleMouseMove = (e) => {
    const svgElementRef = e.currentTarget.closest("svg");
    const containerRefRect = svgElementRef.parentElement.getBoundingClientRect();
    setTooltip((prev) => ({
      ...prev,
      x: e.clientX - containerRefRect.left,
      y: e.clientY - containerRefRect.top,
    }));
  };

  if (regiones.isLoading) return <BlockMapSkeleton />;

  if (regiones.error) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-3 flex flex-col justify-between">
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span>Error al sincronizar indicadores del mapa con el servidor</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-3 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <ChartColumn height={18} width={18} className="text-blue-600" />
            <h3 className="text-sm font-bold text-slate-800">Mapa de Inclusión Social</h3>
          </div>
          <button
            onClick={() => onClusterSelect?.(regionTextCenter[0]?.cluster || "Norte", activeTab)}
            className="text-xs text-blue-600 hover:text-blue-700 font-semibold cursor-pointer"
          >
            Ver detalle →
          </button>
        </div>

        {/* Tabs */}
        <div className="flex flex-wrap items-center gap-2 mt-4">
          <Layers height={18} width={18} className="mr-2" />
          {tabs.map(({ key, label }) => (
            <button key={key} onClick={() => setActiveTab(key)} className={tabButtonClass(activeTab === key)}>
              {label}
            </button>
          ))}
        </div>

        {/* Organic Map */}
        {/* 👇 min-h-[400px] + w-full sin max-w para que ocupe todo el ancho disponible */}
        <div className="flex justify-center relative min-h-[400px]">
          <svg
            width="100%"
            height="100%"
            viewBox={`0 0 ${viewBoxWidth} 600`}
            preserveAspectRatio="xMidYMid meet"
            className="w-full"
          >
            {regionTextCenter.map((region) => (
              <g
                key={region.cluster}
                className="cursor-pointer"
                onClick={() => onClusterSelect?.(region.cluster, activeTab)}
                onMouseEnter={(e) => handleMouseEnter(region, e)}
                onMouseMove={handleMouseMove}
                onMouseLeave={() => setTooltip({ visible: false, x: 0, y: 0, region: null })}
              >
                <polygon
                  points={region.points}
                  fill={getStatusFromValue(activeTab, Number(region.valorDisplay))}
                  stroke="#fff"
                  strokeWidth="3"
                  className="transition-all hover:opacity-80"
                />
                <text x={region.centerPositionX} y={region.centerPositionY - 8} textAnchor="middle" fontSize="12" fontWeight="700" fill="#111827">
                  {formatClusterName(region.cluster)}
                </text>
                <text x={region.centerPositionX} y={region.centerPositionY + 15} textAnchor="middle" fontSize="14" fontWeight="800" fill="#111827">
                  {region.valorDisplay}%
                </text>
              </g>
            ))}
          </svg>

          {/* Custom Tooltip */}
          {tooltip.visible && tooltip.region && (
            <div
              className="pointer-events-none absolute z-50 w-56 rounded-2xl bg-white border border-slate-200 shadow-xl p-4"
              style={{ left: tooltip.x + 12, top: tooltip.y - 10, transform: "translateY(-100%)" }}
            >
              <div className="flex items-start justify-between gap-1 flex-wrap">
                <h4 className="text-xs font-bold text-slate-800">{formatClusterName(tooltip.region.cluster)}</h4>
                <span className="px-2 py-0.5 text-[11px] font-semibold rounded-md bg-slate-100 text-slate-500">
                  {tooltip.region.n_usuarios} hab.
                </span>
              </div>
              <div className="mt-3">
                <p className="text-sm text-slate-400 lowercase">
                  {activeTab === "CONECTIVIDAD" ? "congestionamento medio" :
                   activeTab === "EMPLEO" ? "tasa empleo formal" :
                   activeTab === "EDUCACION" ? "tasa conclusão ensino médio" :
                   "cobertura atenção básica"}
                </p>
                <p className="text-sm font-bold text-blue-600">{tooltip.region.valorDisplay}%</p>
              </div>
              <div className="mt-3 border-t border-slate-200 pt-3">
                <p className="text-sm text-slate-400">Clic para ver detalle <span className="ml-1">→</span></p>
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
              <span className="w-2.5 h-2.5 bg-red-400 border border-red-500 rounded-full inline-block" /> Crítico
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 bg-amber-300 border border-amber-400 rounded-full inline-block" /> Alerta
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 bg-green-200 border border-green-300 rounded-full inline-block" /> Bueno
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 bg-blue-200 border border-blue-300 rounded-full inline-block" /> Óptimo
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};