import { useState } from "react";
import {
  Briefcase,
  ArrowUpRight,
  MapPin,
  Award,
  AlertTriangle,
} from "lucide-react";
import {
  // AreaChart,
  // Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  // ReferenceLine,
} from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart";
import { useEmpleabilidad } from "../hooks/useEmpleabilidad";

// Mock Data

// Tab 1: Evolución Temporal
// const evolutionData = [
//   { mes: "Ene", tasa: 64.0 },
//   { mes: "Feb", tasa: 65.0 },
//   { mes: "Mar", tasa: 66.5 },
//   { mes: "Abr", tasa: 66.0 },
//   { mes: "May", tasa: 67.5 },
//   { mes: "Jun", tasa: 68.0 },
//   { mes: "Jul", tasa: 67.6 },
//   { mes: "Ago", tasa: 69.0 },
//   { mes: "Sep", tasa: 69.5 },
//   { mes: "Oct", tasa: 68.8 },
//   { mes: "Nov", tasa: 69.8 },
//   { mes: "Dic", tasa: 70.2 },
// ];

// const evolutionConfig = {
//   tasa: {
//     label: "Tasa de Empleo",
//     color: "#2563eb",
//   },
// };

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

// Tab 3: Brecha de Género
// const genderGapData = [
//   { region: "Centro", masculino: 87, femenino: 77 },
//   { region: "Oriente", masculino: 79, femenino: 69 },
//   { region: "Noreste", masculino: 76, femenino: 66 },
//   { region: "Occidente", masculino: 70, femenino: 60 },
//   { region: "Norte", masculino: 68, femenino: 56 },
//   { region: "Sureste", masculino: 66, femenino: 56 },
//   { region: "Noroeste", masculino: 64, femenino: 52 },
//   { region: "Sur", masculino: 59, femenino: 49 },
//   { region: "Suroeste", masculino: 54, femenino: 44 },
// ];

// const genderGapConfig = {
//   masculino: {
//     label: "Masculino",
//     color: "#2563eb",
//   },
//   femenino: {
//     label: "Femenino",
//     color: "#ec4899",
//   },
// };

// Bottom Section: Ranking de Empleabilidad

function EmpleabilidadPage() {
  const [activeTab, setActiveTab] = useState("comparacion");

  const empleo = useEmpleabilidad();
  const brechaEmpleo = empleo?.data?.brechas?.[0];

  const peorCongestionamiento = empleo?.data?.brechas?.reduce((peor, actual) =>
    actual.congestionamento_medio > peor.congestionamento_medio ? actual : peor,
  );

  const mejorCongestionamiento = empleo?.data?.brechas?.reduce(
    (mejor, actual) =>
      actual.congestionamento_medio < mejor.congestionamento_medio
        ? actual
        : mejor,
  );

  // Get progress bar styling for ranking list
  const getRankBarColors = (rate) => {
    if (rate >= 0.7) return { text: "text-green-600", bar: "bg-green-500" };
    if (rate >= 0.5) return { text: "text-amber-600", bar: "bg-amber-500" };
    return { text: "text-red-600", bar: "bg-red-500" };
  };

  const comparisonConfig = {
    formal: {
      label: "Empleo Formal",
      color: "#2563eb",
    },
    informal: {
      label: "Empleo Informal",
      color: "#38bdf8",
    },
  };

  const comparisonData = empleo?.data?.brechas?.map((brecha) => ({
    region: brecha.municipio,
    formal: Math.round((10 - brecha.indicador_social?.valor) * 10),
    informal: Math.round(brecha.indicador_social?.valor * 10),
  }));

  return (
    <div className="space-y-6">
      {/* Title & Header Row */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-blue-600" />
            <span>Empleabilidad Regional</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Análisis de empleo, desempleo y participación laboral
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
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Tasa de Empleo Promedio */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div>
            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
              Tasa de Empleo Promedio
            </p>
            <h3 className="text-2xl font-bold text-slate-800 tracking-tight mt-1.5">
              {brechaEmpleo?.indicador_social?.valor.toFixed(1)}%
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
              Mejor Región
            </p>
            <h3 className="text-2xl font-bold text-slate-800 tracking-tight mt-1.5">
              {mejorCongestionamiento?.municipio}
            </h3>
          </div>
          <div className="flex items-center gap-1 text-[10px] text-green-600 font-bold mt-2">
            <Award className="w-3.5 h-3.5" />
            <span>
              {mejorCongestionamiento?.indicador_social?.valor}% de empleo
            </span>
          </div>
        </div>

        {/* Card 3: Región Crítica */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div>
            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
              Región Crítica
            </p>
            <h3 className="text-2xl font-bold text-slate-800 tracking-tight mt-1.5">
              {peorCongestionamiento?.municipio}
            </h3>
          </div>
          <div className="flex items-center gap-1 text-[10px] text-red-600 font-bold mt-2">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>
              {peorCongestionamiento?.indicador_social?.valor}% de empleo
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

      {/* Tabs Switcher Navigation */}
      <div className="bg-slate-100/60 p-1 rounded-xl flex items-center gap-1 w-fit border border-slate-200/50">
        {/* <button
          onClick={() => setActiveTab("evolucion")}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer ${
            activeTab === "evolucion"
              ? "bg-blue-600 text-white shadow-xs"
              : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/40"
          }`}
        >
          Evolución Temporal
        </button> */}
        <button
          onClick={() => setActiveTab("comparacion")}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer ${
            activeTab === "comparacion"
              ? "bg-blue-600 text-white shadow-xs"
              : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/40"
          }`}
        >
          Comparación Regional
        </button>
        {/* <button
          onClick={() => setActiveTab("brecha")}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer ${
            activeTab === "brecha"
              ? "bg-blue-600 text-white shadow-xs"
              : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/40"
          }`}
        >
          Brecha de Género
        </button> */}
      </div>

      {/* Interactive Chart Container */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow">
        {/* {activeTab === "evolucion" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-800">
                Evolución de Empleo — 12 meses
              </h3>
              <span className="text-[10px] font-bold text-green-700 bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
                +6% anual
              </span>
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
                  domain={[60, 75]}
                />
                <ChartTooltip
                  content={<ChartTooltipContent formatter={tooltipFormatter} />}
                />
                <ReferenceLine
                  y={65}
                  stroke="#f97316"
                  strokeDasharray="3 3"
                  label={{
                    value: "Meta 65%",
                    position: "insideBottomLeft",
                    fill: "#f97316",
                    fontSize: 9,
                    fontWeight: "bold",
                  }}
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
        )} */}

        {activeTab === "comparacion" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-800">
                Empleo Formal vs Informal por Región
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
                  domain={[0, 120]}
                />
                <ChartTooltip
                  content={<ChartTooltipContent formatter={tooltipFormatter} />}
                />
                <Bar
                  dataKey="formal"
                  stackId="a"
                  fill="var(--color-formal)"
                  radius={[0, 0, 0, 0]}
                  barSize={14}
                />
                <Bar
                  dataKey="informal"
                  stackId="a"
                  fill="var(--color-informal)"
                  radius={[2, 2, 0, 0]}
                  barSize={14}
                />
                <ChartLegend content={<ChartLegendContent />} />
              </BarChart>
            </ChartContainer>
          </div>
        )}

        {/* {activeTab === "brecha" && (
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <h3 className="text-sm font-bold text-slate-800">
                Brecha de Género en Empleabilidad
              </h3>
              <span className="text-[10px] font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full border border-slate-200">
                Brecha promedio: -10.4pp
              </span>
            </div>

            <ChartContainer
              config={genderGapConfig}
              className="h-[300px] w-full"
            >
              <BarChart
                data={genderGapData}
                layout="vertical"
                margin={{ top: 10, right: 10, left: -5, bottom: 5 }}
              >
                <CartesianGrid horizontal={false} strokeDasharray="3 3" />
                <XAxis
                  type="number"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tick={{ fontSize: 9, fill: "#64748b" }}
                  domain={[0, 100]}
                />
                <YAxis
                  type="category"
                  dataKey="region"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tick={{ fontSize: 9, fill: "#64748b" }}
                />
                <ChartTooltip
                  content={<ChartTooltipContent formatter={tooltipFormatter} />}
                />
                <Bar
                  dataKey="masculino"
                  fill="var(--color-masculino)"
                  radius={[0, 2, 2, 0]}
                  barSize={8}
                />
                <Bar
                  dataKey="femenino"
                  fill="var(--color-femenino)"
                  radius={[0, 2, 2, 0]}
                  barSize={8}
                />
                <ChartLegend content={<ChartLegendContent />} />
              </BarChart>
            </ChartContainer>
          </div>
        )} */}
      </div>

      {/* Bottom Ranking List Section */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow">
        <h3 className="text-sm font-bold text-slate-800 mb-4 pb-3 border-b border-slate-100">
          Ranking de Empleabilidad por Región
        </h3>

        <div className="divide-y divide-slate-100">
          {empleo?.data?.brechas?.map((item, index) => {
            const colors = getRankBarColors(item.congestionamento_medio);
            return (
              <div
                key={item.congestionamento_medio}
                className="flex items-center gap-4 py-3 text-xs font-semibold"
              >
                {/* Position Badge */}
                <div className="w-6 h-6 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center text-[10px] shrink-0">
                  {index + 1}
                </div>

                {/* Region details */}
                <div className="flex-1 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2 max-w-[200px] truncate">
                    <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <span className="text-slate-700 truncate">
                      {item.cluster}
                    </span>
                  </div>

                  {/* Horizontal progress bar */}
                  <div className="flex-1 max-w-md mx-0 sm:mx-8 bg-slate-100 rounded-full h-1.5 overflow-hidden shrink-0">
                    <div
                      className={`h-full rounded-full ${colors.bar}`}
                      style={{ width: `${item.congestionamento_medio * 100}%` }}
                    />
                  </div>

                  {/* Value and population details */}
                  <div className="flex items-center justify-between sm:justify-end gap-6 shrink-0">
                    <span className={`w-10 text-right ${colors.text}`}>
                      {item.congestionamento_medio * 100}%
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
    </div>
  );
}

export default EmpleabilidadPage;
