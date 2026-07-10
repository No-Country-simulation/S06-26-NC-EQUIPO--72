import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import {
  AlertCircle,
  Brain,
  Heart,
  SquareCheckBig,
  TriangleAlert,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  // Cell,
  // Line,
  // LineChart,
  // Scatter,
  // ScatterChart,
  XAxis,
  YAxis,
} from "recharts";
import { PriorityRegionCard } from "../components/PriorityRegionCard";
import { useSaludMental } from "../hooks/useSaludMental";
import { formatClusterName } from "@/shared/utils/format";
import { Skeleton } from "@/components/ui/skeleton";
import {
  BarChartDataSkeleton,
  HealthIndicatorsCardSkeleton,
} from "../skeletons/SaludMentalPageSkeleton";

// --- Seccion: Correlación Conectividad x Salud Mental ---
// const scatterChartConfig = {
//   saludMental: {
//     label: "Índice de Salud Mental",
//     color: "#16a34a",
//   },
// };
// const scatterData = [
//   { region: "Noroeste", conectividad: 38, saludMental: 2.9 },
//   { region: "Norte", conectividad: 45, saludMental: 3.2 },
//   { region: "Noreste", conectividad: 51, saludMental: 3.8 },
//   { region: "Occidente", conectividad: 55, saludMental: 3.5 },
//   { region: "Oriente", conectividad: 62, saludMental: 4.8 },
//   { region: "Centro", conectividad: 67, saludMental: 4.1 },
//   { region: "Sur", conectividad: 75, saludMental: 2.3 },
//   { region: "Sureste", conectividad: 82, saludMental: 2.7 },
//   { region: "Suroeste", conectividad: 89, saludMental: 3.5 },
// ];

// const getScatterColor = (value) => {
//   if (value < 3) return "#dc2626"; // crítico
//   if (value <= 3.5) return "#f59e0b"; // medio
//   return "#16a34a"; // óptimo
// };

// --- Sección: Indicadores de Riesgo ---
// const riskLineConfig = {
//   ansiedad: {
//     label: "Ansiedad",
//     color: "#dc2626",
//   },
//   depresion: {
//     label: "Depresión",
//     color: "#f59e0b",
//   },
//   burnout: {
//     label: "Burnout",
//     color: "#9333ea",
//   },
// };

// const riskLineData = [
//   { mes: "Ene", ansiedad: 38, depresion: 36, burnout: 37 },
//   { mes: "Feb", ansiedad: 36, depresion: 34, burnout: 35 },
//   { mes: "Mar", ansiedad: 35, depresion: 33, burnout: 34 },
//   { mes: "Abr", ansiedad: 34, depresion: 32, burnout: 33 },
//   { mes: "May", ansiedad: 33, depresion: 31, burnout: 32 },
//   { mes: "Jun", ansiedad: 32, depresion: 30, burnout: 31 },
//   { mes: "Jul", ansiedad: 34, depresion: 32, burnout: 33 },
//   { mes: "Ago", ansiedad: 31, depresion: 29, burnout: 30 },
//   { mes: "Sep", ansiedad: 30, depresion: 28, burnout: 29 },
//   { mes: "Oct", ansiedad: 29, depresion: 27, burnout: 28 },
//   { mes: "Nov", ansiedad: 28, depresion: 26, burnout: 27 },
//   { mes: "Dic", ansiedad: 27, depresion: 25, burnout: 26 },
// ];

//

export default function SaludMentalPage() {
  const saludMental = useSaludMental();
  const regiones = saludMental?.data?.brechas;

  const mejorRegion = saludMental?.data?.brechas?.reduce((mejor, actual) =>
    actual.congestionamento_medio < mejor.congestionamento_medio
      ? actual
      : mejor,
  );

  const barChartConfig = {
    acceso: {
      label: "Acceso",
      color: "#f3006f",
    },
    demanda: {
      label: "Demanda",
      color: "#f5bdd5",
    },
  };

  const barChartData = regiones?.map((region) => ({
    region: formatClusterName(region.cluster),
    demanda: region.congestionamento_medio * 100,
    acceso: region.indicador_social?.valor,
  }));

  const priorityRegionCards = regiones?.map((region) => ({
    region: region.cluster,
    status: region.severidad_brecha,
    mentalHealthIndex: region.indicador_social?.valor,
  }));

  const totalIndice = regiones?.reduce(
    (x, acm) => x + acm.indicador_social?.valor,
    0,
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Heart className="w-5 h-5 text-pink-600" />
            <span>Indicadores de Salud Mental</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Bienestar psicosocial, acceso a servicios y brechas regionales
          </p>
        </div>
      </div>
      {saludMental.isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {Array.from({ length: 3 }).map((_, idx) => (
            <div
              key={idx}
              className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between"
            >
              <div className="flex items-center justify-between">
                <Skeleton className="w-8 h-8 rounded-lg" />
              </div>

              <div className="mt-3 space-y-2">
                <Skeleton className="h-8 w-20" />
                <Skeleton className="h-3 w-28" />
              </div>
            </div>
          ))}
        </div>
      ) : saludMental.isError ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span>
            Error al sincronizar datos de salud mental con el servidor
          </span>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-4">
              <Brain className="w-8 h-8 text-rose-300" />
              <div className="flex flex-col items-baseline gap-1">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {totalIndice?.toFixed(2) || 12.42}
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  Objetivo: {totalIndice?.toFixed(2) * 2 || 12.42}
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">
              Índice Nacional Promedio
            </p>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-4">
              <SquareCheckBig className="shrink-0 w-8 h-8 text-green-600" />
              <div className="flex flex-col items-baseline gap-1">
                <span className="text-lg font-bold text-slate-800 tracking-tight">
                  {formatClusterName(mejorRegion?.cluster)}
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  {mejorRegion?.indicador_social?.valor} — Óptimo
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">Mejor región</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-4">
              <TriangleAlert className="w-8 h-8 text-yellow-400" />
              <div className="flex flex-col items-baseline gap-1">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {regiones?.length}
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  &lt; 3.0/5
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">
              Regiones críticas
            </p>
          </div>
          {/* <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
          <div className="flex items-center gap-4">
            <Building2 className="w-8 h-8 text-blue-600" />
            <div className="flex flex-col items-baseline gap-1">
              <span className="text-2xl font-bold text-slate-800 tracking-tight">
                43%
              </span>
              <span className="text-xs text-slate-400 font-medium">
                cobertura nacional
              </span>
            </div>
          </div>
          <p className="text-xs text-slate-500 font-medium">
            Acceso a servicios
          </p>
        </div> */}
        </div>
      )}
      {/* Nueva sección: Correlación (scatter) + Indicadores de Riesgo (líneas) */}
      {/* <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col hover:shadow-sm transition-shadow">
          <div className="border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-800">
              Correlación: Conectividad × Salud Mental
            </h3>
            <p className="flex items-center gap-1 text-xs text-slate-500 mt-1">
              <Info className="w-3.5 h-3.5" />
              <span>r = 0.87 — correlación muy fuerte</span>
            </p>
          </div>
          <div className="flex-1 mt-4">
            <ChartContainer
              config={scatterChartConfig}
              className="h-[240px] w-full"
            >
              <ScatterChart
                margin={{ top: 10, right: 10, left: -10, bottom: 10 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  type="number"
                  dataKey="conectividad"
                  name="Conectividad"
                  unit="%"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  domain={[35, 90]}
                  tick={{ fontSize: 10, fill: "#64748b" }}
                  label={{
                    value: "Conectividad (%)",
                    position: "insideBottom",
                    offset: -5,
                    fontSize: 10,
                    fill: "#64748b",
                  }}
                />
                <YAxis
                  type="number"
                  dataKey="saludMental"
                  name="Salud Mental"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  domain={[2, 5]}
                  tick={{ fontSize: 9, fill: "#64748b" }}
                />
                <ChartTooltip
                  cursor={{ strokeDasharray: "3 3" }}
                  content={({ active, payload }) => {
                    if (!active || !payload?.length) return null;

                    const data = payload[0].payload;

                    return (
                      <div className="bg-white border border-slate-200 rounded-lg p-3 shadow">
                        <p className="font-medium">{data.region}</p>
                        <p>Conectividad: {data.conectividad}%</p>
                        <p>Salud Mental: {data.saludMental}</p>
                      </div>
                    );
                  }}
                />
                <Scatter data={scatterData} dataKey="saludMental">
                  {scatterData.map((entry, index) => (
                    <Cell
                      key={`scatter-cell-${index}`}
                      fill={getScatterColor(entry.saludMental)}
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ChartContainer>
          </div>
        </div>
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col hover:shadow-sm transition-shadow">
          <div className="border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-800">
              Indicadores de Riesgo — Evolución 12 meses
            </h3>

            <span className="block h-5" />
          </div>
          <div className="flex-1 mt-4">
            <ChartContainer
              config={riskLineConfig}
              className="h-[240px] w-full"
            >
              <LineChart
                data={riskLineData}
                margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
              >
                <CartesianGrid vertical={false} strokeDasharray="3 3" />
                <XAxis
                  dataKey="mes"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tick={{ fontSize: 9, fill: "#64748b" }}
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tick={{ fontSize: 9, fill: "#64748b" }}
                  domain={[0, 40]}
                  tickFormatter={(value) => `${value}%`}
                />
                <ChartTooltip
                  content={({ active, payload }) => {
                    if (!active || !payload?.length) return null;

                    const data = payload[0].payload;

                    return (
                      <div className="rounded-lg border bg-white p-3 shadow-md">
                        <p className="font-medium text-slate-800 mb-2">
                          {data.mes}
                        </p>

                        <div className="space-y-1 text-xs">
                          <p className="text-red-500">
                            Ansiedad: {data.ansiedad}%
                          </p>
                          <p className="text-yellow-500">
                            Depresión: {data.depresion}%
                          </p>
                          <p className="text-violet-500">
                            Burnout: {data.burnout}%
                          </p>
                        </div>
                      </div>
                    );
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="ansiedad"
                  stroke="var(--color-burnout)"
                  strokeWidth={2}
                  dot={false}
                />
                <ChartLegend
                  content={() => (
                    <div className="flex justify-start gap-6 pl-5">
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-2.5 rounded-full bg-red-500" />
                        <span className="text-[10px] text-gray-500">
                          Ansiedad
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-2.5 rounded-full bg-yellow-500" />
                        <span className="text-[10px] text-gray-500">
                          Depresión
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <div className="h-1 w-2.5 rounded-full bg-violet-500" />
                        <span className="text-[10px] text-gray-500">
                          Burnout
                        </span>
                      </div>
                    </div>
                  )}
                />
              </LineChart>
            </ChartContainer>
          </div>
        </div>
      </div> */}
      {/*  */}
      {/* Visualizations Grid */}
      {saludMental.isLoading ? (
        <BarChartDataSkeleton />
      ) : saludMental.isError ? (
        <></>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">
                Brecha de Acceso a Servicios de Salud Mental
              </h3>
              <span className="flex items-center gap-1.5 bg-yellow-100 border border-yellow-200  text-orange-500 text-xs p-1 rounded-lg">
                <span>Oferta vs Demanda</span>
              </span>
            </div>
            <div className="flex-1 mt-4">
              <ChartContainer
                config={barChartConfig}
                className="h-[240px] w-full"
              >
                <BarChart
                  data={barChartData}
                  margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
                >
                  <CartesianGrid vertical={false} strokeDasharray="3 3" />
                  <XAxis
                    dataKey="region"
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    tick={{ fontSize: 9, fill: "#64748b" }}
                  />
                  <YAxis
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    tick={{ fontSize: 9, fill: "#64748b" }}
                    domain={[0, 100]}
                  />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <Bar
                    dataKey="demanda"
                    fill="var(--color-demanda)"
                    radius={[2, 2, 0, 0]}
                    barSize={25}
                  />
                  <Bar
                    dataKey="acceso"
                    fill="var(--color-acceso)"
                    radius={[2, 2, 0, 0]}
                    barSize={25}
                  />
                  <ChartLegend content={<ChartLegendContent />} />
                </BarChart>
              </ChartContainer>
            </div>
          </div>
        </div>
      )}
      {saludMental.isLoading ? (
        <HealthIndicatorsCardSkeleton />
      ) : saludMental.isError ? (
        <></>
      ) : (
        <div className="grid grid-cols-1">
          <h2 className="text-base font-semibold mb-3">
            Regiones de Atención Prioritaria
          </h2>
          <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4  max-h-[400px] overflow-y-auto">
            {priorityRegionCards?.map((region) => (
              <PriorityRegionCard key={region.region} {...region} />
            ))}
          </section>
        </div>
      )}
    </div>
  );
}
