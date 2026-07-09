import { useState } from "react";
import {
  Briefcase,
  ArrowUpRight,
  MapPin,
  Award,
  AlertTriangle,
  AlertCircle,
} from "lucide-react";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ReferenceLine,
} from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart";
import { useEmpleabilidad, useIndicadoresEvolucion } from "../hooks/useEmpleabilidad";
import { formatClusterName } from "@/shared/utils/format";
import {
  BarChartSkeleton,
  RankingListSkeleton,
} from "../skeletons/EmpleabilidadPageSkeleton";
import { useLanguage } from "@/context/useLenguage";

const tooltipFormatter = (value, name, item) => {
  const color = item.color || item.payload?.fill;
  return (
    <div className="flex items-center gap-1.5 w-full text-xs">
      <div
        className="h-2.5 w-2.5 shrink-0 rounded-[2px]"
        style={{ backgroundColor: color }}
      />
      <div className="flex flex-1 justify-between items-center leading-none gap-4">
        <span className="text-muted-foreground">{name}</span>
        <span className="font-mono font-medium text-foreground tabular-nums">
          {value}%
        </span>
      </div>
    </div>
  );
};

// Function to format date (YYYY-MM-DD) to month abbreviation
const formatMes = (dateStr, isPortugues) => {
  const date = new Date(dateStr);
  const monthsEs = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
  const monthsPt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
  return isPortugues ? monthsPt[date.getMonth()] : monthsEs[date.getMonth()];
};

// Bottom Section: Ranking de Empleabilidad

function EmpleabilidadPage() {
  const { lenguage } = useLanguage();
  const isPortugues = lenguage === "pt";

  const [activeTab, setActiveTab] = useState("evolucion");

  const empleo = useEmpleabilidad();
  const evolucion = useIndicadoresEvolucion();

  // Helper function to get taxa_emprego_formal from a region
  const getTasaEmpleo = (region) =>
    region.indicadores?.find((i) => i.indicador === "taxa_emprego_formal")?.valor ?? 0;

  // Get mejor/peor region based on taxa_emprego_formal
  const mejorRegion = empleo?.data?.regiones?.reduce((mejor, actual) =>
    getTasaEmpleo(actual) > getTasaEmpleo(mejor) ? actual : mejor,
  );

  const peorRegion = empleo?.data?.regiones?.reduce((peor, actual) =>
    getTasaEmpleo(actual) < getTasaEmpleo(peor) ? actual : peor,
  );

  // Calculate tasa promedio
  const tasaPromedio = empleo?.data?.regiones
    ? (
        empleo.data.regiones.reduce((sum, r) => sum + getTasaEmpleo(r), 0) /
        empleo.data.regiones.length
      ).toFixed(1)
    : 0;

  // Get progress bar styling for ranking list
  const getRankBarColors = (rate) => {
    if (rate >= 0.7) return { text: "text-green-600", bar: "bg-green-500" };
    if (rate >= 0.5) return { text: "text-amber-600", bar: "bg-amber-500" };
    return { text: "text-red-600", bar: "bg-red-500" };
  };

  const comparisonConfig = {
    formal: {
      label: isPortugues ? "Emprego Formal" : "Empleo Formal",
      color: "#2563eb",
    },
    desempleo: {
      label: isPortugues ? "Desemprego" : "Desempleo",
      color: "#f87171",
    },
  };

  // Process evolution data
  const evolutionData = evolucion?.data?.evolucion?.map((item) => ({
    mes: formatMes(item.fecha_referencia, isPortugues),
    tasa: item.valor_promedio,
  })) || [];

  const evolutionConfig = {
    tasa: {
      label: isPortugues ? "Taxa de Emprego" : "Tasa de Empleo",
      color: "#2563eb",
    },
  };

  // Process comparison data (formal vs desempleo)
  const comparisonData = empleo?.data?.regiones?.map((region) => ({
    region: formatClusterName(region.cluster),
    formal:
      region.indicadores?.find((i) => i.indicador === "taxa_emprego_formal")
        ?.valor ?? 0,
    desempleo:
      region.indicadores?.find((i) => i.indicador === "taxa_desemprego")
      ?.valor ?? 0,
  }));

  return (
    <div className="space-y-6">
      {/* Title & Header Row */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-blue-600" />
            <span>
              {isPortugues
                ? "Empregabilidade Regional"
                : "Empleabilidad Regional"}
            </span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            {isPortugues
              ? "Análise de emprego, desemprego e participação no trabalho"
              : "Análisis de empleo, desempleo y participación laboral"}
          </p>
        </div>
        {/* <div>
          <span className="inline-flex items-center gap-1.5 bg-green-50 text-green-700 border border-green-200 px-3 py-1 rounded-full text-xs font-semibold shadow-xs">
            <TrendingUp className="w-4 h-4 text-green-600" />
            <span>Tendencia nacional: +2.3%</span>
          </span>
        </div> */}
      </div>

      {/* Average Metrics Cards Row */}
      {empleo.isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="bg-white border border-slate-200 rounded-xl p-4 h-[135px] flex flex-col justify-between animate-pulse"
            >
              <div className="flex items-center justify-between">
                <div className="w-8 h-8 rounded-lg bg-slate-100" />
                <div className="w-12 h-4 rounded-full bg-slate-105" />
              </div>
              <div className="space-y-2 mt-4">
                <div className="h-6 w-16 bg-slate-100 rounded" />
                <div className="h-3 w-24 bg-slate-100 rounded" />
              </div>
            </div>
          ))}
        </div>
      ) : empleo.error ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span>
            {isPortugues
              ? "Erro ao sincronizar dados de empregabilidade com o servidor"
              : "Error al sincronizar datos de empleabilidad con el servidor"}
          </span>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Card 1: Tasa de Empleo Promedio */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                {isPortugues
                  ? "Taxa de Emprego Média"
                  : "Tasa de Empleo Promedio"}
              </p>
              <h3 className="text-2xl font-bold text-slate-800 tracking-tight mt-1.5">
                {tasaPromedio}%
              </h3>
            </div>
            <div className="flex items-center gap-1 text-[10px] text-green-600 font-bold mt-2">
              <ArrowUpRight className="w-3.5 h-3.5" />
              <span>+2.3%</span>
            </div>
          </div>

          {/* Card 2: Mejor Región */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                {isPortugues ? "Melhor Região" : "Mejor Región"}
              </p>
              <h3 className="text-2xl font-bold text-slate-800 tracking-tight mt-1.5">
                {mejorRegion?.municipio}
              </h3>
            </div>
            <div className="flex items-center gap-1 text-[10px] text-green-600 font-bold mt-2">
              <Award className="w-3.5 h-3.5" />
              <span>
                {getTasaEmpleo(mejorRegion)}{isPortugues ? "% de emprego" : "% de empleo"}
              </span>
            </div>
          </div>

          {/* Card 3: Región Crítica */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                {isPortugues ? "Região Crítica" : "Región Crítica"}
              </p>
              <h3 className="text-2xl font-bold text-slate-800 tracking-tight mt-1.5">
                {peorRegion?.municipio}
              </h3>
            </div>
            <div className="flex items-center gap-1 text-[10px] text-red-600 font-bold mt-2">
              <AlertTriangle className="w-3.5 h-3.5" />
              <span>
                {getTasaEmpleo(peorRegion)}{isPortugues ? "% de emprego" : "% de empleo"}
              </span>
            </div>
          </div>

          {/* Card 4: Participación Laboral */}
          {/* <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div>
            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
              Participación Laboral
            </p>
            <h3 className="text-2xl font-bold text-slate-800 tracking-tight mt-1.5">
              63.1%
            </h3>
          </div>
          <div className="flex items-center gap-1 text-[10px] text-green-600 font-bold mt-2">
            <ArrowUpRight className="w-3.5 h-3.5" />
            <span>+1.1%</span>
          </div>
        </div> */}
        </div>
      )}

      {/* Tabs Switcher Navigation */}
      <div className="bg-slate-100/60 p-1 rounded-xl flex items-center gap-1 w-fit border border-slate-200/50">
        <button
          onClick={() => setActiveTab("evolucion")}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer ${
            activeTab === "evolucion"
              ? "bg-blue-600 text-white shadow-xs"
              : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/40"
          }`}
        >
          {isPortugues ? "Evolução Temporal" : "Evolución Temporal"}
        </button>
        {!empleo.error && (
          <button
            onClick={() => setActiveTab("comparacion")}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer ${
              activeTab === "comparacion"
                ? "bg-blue-600 text-white shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/40"
            }`}
          >
            {isPortugues ? "Comparação Regional" : "Comparación Regional"}
          </button>
        )}
      </div>

      {/* Interactive Chart Container */}
      <div>
        {activeTab === "evolucion" ? (
          evolucion.isLoading ? (
            <BarChartSkeleton />
          ) : evolucion.error ? (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
              <AlertCircle className="w-4 h-4 text-red-500" />
              <span>
                {isPortugues ? "Erro ao sincronizar dados de evolução" : "Error al sincronizar datos de evolución"}
              </span>
            </div>
          ) : (
            <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-slate-800">
                    {isPortugues ? "Evolução do Emprego" : "Evolución de Empleo"}
                  </h3>
                </div>

                <ChartContainer
                  config={evolutionConfig}
                  className="h-[280px] w-full"
                >
                  <AreaChart
                    data={evolutionData}
                    margin={{ top: 15, right: 10, left: -20, bottom: 0 }}
                  >
                    <defs>
                      <linearGradient id="colorTasa" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#2563eb" stopOpacity={0.2} />
                        <stop offset="95%" stopColor="#2563eb" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
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
                    />
                    <ChartTooltip
                      content={<ChartTooltipContent formatter={tooltipFormatter} />}
                    />
                    <Area
                      type="monotone"
                      dataKey="tasa"
                      stroke="#2563eb"
                      strokeWidth={2.5}
                      fillOpacity={1}
                      fill="url(#colorTasa)"
                    />
                    <ChartLegend content={<ChartLegendContent />} />
                  </AreaChart>
                </ChartContainer>
              </div>
            </div>
          )
        ) : (
          !empleo.error && (
            empleo.isLoading ? (
              <BarChartSkeleton />
            ) : (
              <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow">
                {activeTab === "comparacion" && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-bold text-slate-800">
                        {isPortugues ? "Emprego Formal vs Desempleo por Região" : "Empleo Formal vs Desempleo en Región"}
                      </h3>
                    </div>

                    <ChartContainer
                      config={comparisonConfig}
                      className="h-[280px] w-full"
                    >
                      <BarChart
                        data={comparisonData}
                        margin={{ top: 15, right: 10, left: -20, bottom: 0 }}
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
                        <ChartTooltip
                          content={
                            <ChartTooltipContent formatter={tooltipFormatter} />
                          }
                        />
                        <Bar
                          dataKey="formal"
                          stackId="a"
                          fill="var(--color-formal)"
                          radius={[0, 0, 0, 0]}
                          barSize={14}
                        />
                        <Bar
                          dataKey="desempleo"
                          stackId="a"
                          fill="var(--color-desempleo)"
                          radius={[2, 2, 0, 0]}
                          barSize={14}
                        />
                        <ChartLegend content={<ChartLegendContent />} />
                      </BarChart>
                    </ChartContainer>
                  </div>
                )}
              </div>
            )
          )
        )}
      </div>

      {/* Bottom Ranking List Section */}
      {empleo.isLoading ? (
        <RankingListSkeleton />
      ) : empleo.isError ? (
        <></>
      ) : (
        <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow">
          <h3 className="text-sm font-bold text-slate-800 mb-4 pb-3 border-b border-slate-100">
            {isPortugues
              ? "Ranking de Empregabilidade por Região"
              : "Ranking de Empleabilidad por Región"}
          </h3>

          <div className="divide-y divide-slate-100">
            {empleo?.data?.regiones
              ?.slice()
              .sort((a, b) => getTasaEmpleo(b) - getTasaEmpleo(a))
              .slice(0, 10)
              .map((item, index) => {
              const tasa = getTasaEmpleo(item) / 100;
              const colors = getRankBarColors(tasa);
              return (
                <div
                  key={item.cluster + item.municipio}
                  className="flex items-center gap-4 py-3 text-xs font-semibold"
                >
                  {/* Position Badge */}
                  <div className="w-6 h-6 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center text-[10px] shrink-0">
                    {index + 1}
                  </div>

                  {/* Region details */}
                  <div className="flex-1 flex flex-col sm:flex-row sm:items-center gap-4 min-w-0">
                    <div className="flex items-center gap-2 w-48 min-w-0 shrink-0">
                      <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span className="text-slate-700 truncate">
                        {formatClusterName(item.cluster)}
                      </span>
                    </div>

                    <div className="flex-1 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${colors.bar}`}
                        style={{
                          width: `${tasa * 100}%`,
                        }}
                      />
                    </div>

                    <div className="flex items-center gap-6 shrink-0">
                      <span className={`w-10 text-right ${colors.text}`}>
                        {(tasa * 100).toFixed(1)}%
                      </span>
                      <span className="text-slate-400 font-medium text-[11px] w-20 text-right">
                        {item.n_usuarios} hab.
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

export default EmpleabilidadPage;
