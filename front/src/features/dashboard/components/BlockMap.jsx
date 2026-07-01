import { useState, useMemo } from "react";
import { generarMapaOrganico } from "../utils/organicMap";
import { useRegions } from "../hooks/useMaps";
import { AlertCircle, ChartColumn, Layers } from "lucide-react";
import { BlockMapSkeleton } from "../skeletons/BlockMapSkeleton";
import { formatClusterName } from "@/shared/utils/format";

const tabs = [
  { key: "EMPLEO", label: "Tasa de Empleo" },
  { key: "EDUCACION", label: "Educacion" },
  { key: "SALUD_MENTAL", label: "Salud Mental" },
];

// const labelByKey = new Map(tabs.map((t) => [t.key, t.label]));

const fillColors = {
  critico: "#f87171",
  alerta: "#fcd34d",
  bueno: "#86efac",
  optimo: "#93c5fd",
};

const getStatusFromCongestion = (value) => {
  if (value > 11) return fillColors.critico;
  if (value > 8) return fillColors.alerta;
  if (value > 5) return fillColors.bueno;
  return fillColors.optimo;
};

const tabButtonClass = (isActive) =>
  `text-[11px] px-3 py-1.5 rounded-lg font-semibold border cursor-pointer ${
    isActive
      ? "bg-blue-600 border-blue-600 text-white"
      : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
  }`;

export const BlockMap = ({
  onClusterSelect,
  activeMapTab,
  onActiveMapTabChange,
}) => {
  const [tooltip, setTooltip] = useState({
    visible: false,
    x: 0,
    y: 0,
    region: null,
  });

  // const regiones = useMapsIndicators(activeMapTab);
  const regiones = useRegions();

  const regionesCompletas = generarMapaOrganico(regiones.data?.regiones);

  const regionTextCenter = regionesCompletas.map((region) => {
    const coords = region.points
      .split(" ")
      .map((p) => p.split(",").map(Number));
    const centerPositionX =
      coords.reduce((sum, [x]) => sum + x, 0) / coords.length;
    const centerPositionY =
      coords.reduce((sum, [, y]) => sum + y, 0) / coords.length;
    return { ...region, centerPositionX, centerPositionY };
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
  }, [regiones.data?.regiones]);

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

  if (regiones.isLoading) {
    return <BlockMapSkeleton />;
  }

  if (regiones.error) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col justify-between">
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span>Error al sincronizar indicadores del mapa con el servidor</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <ChartColumn height={18} width={18} className="text-blue-600" />
            <h3 className="text-sm font-bold text-slate-800">
              Mapa de Inclusión Social
            </h3>
          </div>
          <button
            onClick={() =>
              onClusterSelect?.(regionTextCenter[0]?.cluster || "Norte")
            }
            className="text-xs text-blue-600 hover:text-blue-700 font-semibold cursor-pointer"
          >
            Ver detalle →
          </button>
        </div>
        {/* Tabs */}
        <div className="flex flex-wrap items-center gap-2 mt-4">
          <Layers height={18} width={18} className="mr-2" />
          {tabs.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => onActiveMapTabChange(key)}
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
                onClick={() => onClusterSelect?.(region.cluster)}
                onMouseEnter={(e) => handleMouseEnter(region, e)}
                onMouseMove={handleMouseMove}
                onMouseLeave={() =>
                  setTooltip({ visible: false, x: 0, y: 0, region: null })
                }
              >
                <polygon
                  points={region.points}
                  fill={getStatusFromCongestion(region.n_antenas)}
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
                  {formatClusterName(region.cluster)}
                </text>

                <text
                  x={region.centerPositionX}
                  y={region.centerPositionY + 15}
                  textAnchor="middle"
                  fontSize="14"
                  fontWeight="800"
                  fill="#111827"
                >
                  {region.n_antenas} Ant.
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
                  {formatClusterName(tooltip.region.cluster)}
                </h4>

                <span className="px-2 py-0.5 text-[11px] font-semibold rounded-md bg-slate-100 text-slate-500">
                  {/* {(tooltip.region.n_usuarios / 10000).toFixed(1)}M hab. */}
                  {tooltip.region.n_antenas} Antenas
                </span>
              </div>
              {/* <div className="mt-3">
                <p className="text-sm text-slate-400 lowercase">
                  {labelByKey.get(tooltip.region.indicadores[0].categoria)}
                </p>

                <p className="text-sm font-bold text-blue-600">
                  {tooltip.region.indicadores[0].valor.toFixed(1)}%
                </p>
              </div> */}

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
