import { useMemo } from "react";
import {
  ArrowLeft,
  Briefcase,
  Wifi,
  Activity,
  TrendingUp,
  Bot,
  Send,
  Star,
  GraduationCap,
  BookOpen,
  ArrowUpRight,
  Sparkles,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";

// Deterministic mockup data by region
const REGION_MOCKS = {
  NORTE: {
    name: "Norte",
    population: "2.1M",
    courses: 18,
    mentorings: 14,
    experiences: 7,
    alerts: 2,
    metrics: {
      employment: { value: "62%", change: "+1.8%" },
      connectivity: { value: "45%", change: "+3.2%" },
      mentalHealth: { value: "3.2/5", change: "+0.1" },
      digitalInclusion: { value: "38%", change: "+0.9%" },
    },
    radarData: [
      { subject: "Empleo", A: 62, fullMark: 100 },
      { subject: "Conectividad", A: 45, fullMark: 100 },
      { subject: "Salud Mental", A: 64, fullMark: 100 }, // 3.2/5 is 64%
      { subject: "Inclusión", A: 38, fullMark: 100 },
      { subject: "Formación", A: 75, fullMark: 100 },
      { subject: "Mentoría", A: 70, fullMark: 100 },
    ],
  },
  SUR: {
    name: "Sur",
    population: "1.8M",
    courses: 12,
    mentorings: 8,
    experiences: 5,
    alerts: 1,
    metrics: {
      employment: { value: "54%", change: "+0.5%" },
      connectivity: { value: "50%", change: "+1.1%" },
      mentalHealth: { value: "3.8/5", change: "-0.2" },
      digitalInclusion: { value: "44%", change: "+1.5%" },
    },
    radarData: [
      { subject: "Empleo", A: 54, fullMark: 100 },
      { subject: "Conectividad", A: 50, fullMark: 100 },
      { subject: "Salud Mental", A: 76, fullMark: 100 },
      { subject: "Inclusión", A: 44, fullMark: 100 },
      { subject: "Formación", A: 50, fullMark: 100 },
      { subject: "Mentoría", A: 40, fullMark: 100 },
    ],
  },
  ORIENTE: {
    name: "Oriente",
    population: "2.4M",
    courses: 22,
    mentorings: 16,
    experiences: 10,
    alerts: 0,
    metrics: {
      employment: { value: "74%", change: "+2.1%" },
      connectivity: { value: "78%", change: "+4.0%" },
      mentalHealth: { value: "4.1/5", change: "+0.3" },
      digitalInclusion: { value: "68%", change: "+2.4%" },
    },
    radarData: [
      { subject: "Empleo", A: 74, fullMark: 100 },
      { subject: "Conectividad", A: 78, fullMark: 100 },
      { subject: "Salud Mental", A: 82, fullMark: 100 },
      { subject: "Inclusión", A: 68, fullMark: 100 },
      { subject: "Formación", A: 90, fullMark: 100 },
      { subject: "Mentoría", A: 85, fullMark: 100 },
    ],
  },
  OCCIDENTE: {
    name: "Occidente",
    population: "1.9M",
    courses: 15,
    mentorings: 11,
    experiences: 6,
    alerts: 3,
    metrics: {
      employment: { value: "65%", change: "+1.2%" },
      connectivity: { value: "52%", change: "+2.5%" },
      mentalHealth: { value: "3.5/5", change: "+0.0" },
      digitalInclusion: { value: "49%", change: "+1.1%" },
    },
    radarData: [
      { subject: "Empleo", A: 65, fullMark: 100 },
      { subject: "Conectividad", A: 52, fullMark: 100 },
      { subject: "Salud Mental", A: 70, fullMark: 100 },
      { subject: "Inclusión", A: 49, fullMark: 100 },
      { subject: "Formación", A: 65, fullMark: 100 },
      { subject: "Mentoría", A: 55, fullMark: 100 },
    ],
  },
  NORESTE: {
    name: "Noreste",
    population: "1.5M",
    courses: 10,
    mentorings: 7,
    experiences: 4,
    alerts: 4,
    metrics: {
      employment: { value: "71%", change: "+1.5%" },
      connectivity: { value: "60%", change: "+1.8%" },
      mentalHealth: { value: "3.6/5", change: "+0.2" },
      digitalInclusion: { value: "55%", change: "+1.3%" },
    },
    radarData: [
      { subject: "Empleo", A: 71, fullMark: 100 },
      { subject: "Conectividad", A: 60, fullMark: 100 },
      { subject: "Salud Mental", A: 72, fullMark: 100 },
      { subject: "Inclusión", A: 55, fullMark: 100 },
      { subject: "Formación", A: 45, fullMark: 100 },
      { subject: "Mentoría", A: 38, fullMark: 100 },
    ],
  },
  NOROESTE: {
    name: "Noroeste",
    population: "1.2M",
    courses: 8,
    mentorings: 5,
    experiences: 3,
    alerts: 1,
    metrics: {
      employment: { value: "58%", change: "+0.8%" },
      connectivity: { value: "48%", change: "+1.2%" },
      mentalHealth: { value: "3.0/5", change: "-0.1" },
      digitalInclusion: { value: "41%", change: "+0.7%" },
    },
    radarData: [
      { subject: "Empleo", A: 58, fullMark: 100 },
      { subject: "Conectividad", A: 48, fullMark: 100 },
      { subject: "Salud Mental", A: 60, fullMark: 100 },
      { subject: "Inclusión", A: 41, fullMark: 100 },
      { subject: "Formación", A: 35, fullMark: 100 },
      { subject: "Mentoría", A: 30, fullMark: 100 },
    ],
  },
  SURESTE: {
    name: "Sureste",
    population: "2.0M",
    courses: 16,
    mentorings: 12,
    experiences: 8,
    alerts: 2,
    metrics: {
      employment: { value: "61%", change: "+1.1%" },
      connectivity: { value: "58%", change: "+2.0%" },
      mentalHealth: { value: "3.4/5", change: "+0.1" },
      digitalInclusion: { value: "50%", change: "+1.0%" },
    },
    radarData: [
      { subject: "Empleo", A: 61, fullMark: 100 },
      { subject: "Conectividad", A: 58, fullMark: 100 },
      { subject: "Salud Mental", A: 68, fullMark: 100 },
      { subject: "Inclusión", A: 50, fullMark: 100 },
      { subject: "Formación", A: 70, fullMark: 100 },
      { subject: "Mentoría", A: 62, fillMark: 100 },
    ],
  },
  SUROESTE: {
    name: "Suroeste",
    population: "1.6M",
    courses: 11,
    mentorings: 9,
    experiences: 5,
    alerts: 3,
    metrics: {
      employment: { value: "49%", change: "+0.4%" },
      connectivity: { value: "42%", change: "+0.9%" },
      mentalHealth: { value: "2.8/5", change: "-0.3" },
      digitalInclusion: { value: "35%", change: "+0.5%" },
    },
    radarData: [
      { subject: "Empleo", A: 49, fullMark: 100 },
      { subject: "Conectividad", A: 42, fullMark: 100 },
      { subject: "Salud Mental", A: 56, fullMark: 100 },
      { subject: "Inclusión", A: 35, fullMark: 100 },
      { subject: "Formación", A: 48, fullMark: 100 },
      { subject: "Mentoría", A: 42, fullMark: 100 },
    ],
  },
  CENTRO: {
    name: "Centro",
    population: "3.2M",
    courses: 30,
    mentorings: 25,
    experiences: 15,
    alerts: 1,
    metrics: {
      employment: { value: "80%", change: "+2.5%" },
      connectivity: { value: "85%", change: "+3.8%" },
      mentalHealth: { value: "4.3/5", change: "+0.4" },
      digitalInclusion: { value: "78%", change: "+3.0%" },
    },
    radarData: [
      { subject: "Empleo", A: 80, fullMark: 100 },
      { subject: "Conectividad", A: 85, fullMark: 100 },
      { subject: "Salud Mental", A: 86, fullMark: 100 },
      { subject: "Inclusión", A: 78, fullMark: 100 },
      { subject: "Formación", A: 95, fullMark: 100 },
      { subject: "Mentoría", A: 90, fullMark: 100 },
    ],
  },
};

// All regions reference list for sorted comparison chart
const ALL_REGIONS_BASE = [
  { id: "ORIENTE", name: "Oriente", employmentVal: 74 },
  { id: "NORESTE", name: "Noreste", employmentVal: 71 },
  { id: "OCCIDENTE", name: "Occidente", employmentVal: 65 },
  { id: "NORTE", name: "Norte", employmentVal: 62 },
  { id: "SURESTE", name: "Sureste", employmentVal: 61 },
  { id: "NOROESTE", name: "Noroeste", employmentVal: 58 },
  { id: "SUR", name: "Sur", employmentVal: 54 },
  { id: "SUROESTE", name: "Suroeste", employmentVal: 49 },
  { id: "CENTRO", name: "Centro", employmentVal: 80 },
];

function ClusterDetailPage({ clusterName, onBack }) {
  // Normalize key to uppercase (e.g., "Norte" -> "NORTE")
  const key = useMemo(() => {
    if (!clusterName) return "NORTE";
    const upper = clusterName.toUpperCase();
    return REGION_MOCKS[upper] ? upper : "NORTE";
  }, [clusterName]);

  const data = useMemo(() => REGION_MOCKS[key], [key]);

  // Generate dynamic comparison list where the active region is placed in order and highlighted
  const comparisonList = useMemo(() => {
    const parsedEmployment = parseInt(data.metrics.employment.value);
    const updatedBase = ALL_REGIONS_BASE.map((item) => {
      if (item.id === key) {
        return { ...item, employmentVal: parsedEmployment };
      }
      return item;
    });
    // Sort descending
    return updatedBase.sort((a, b) => b.employmentVal - a.employmentVal);
  }, [data, key]);

  // Generate dynamic double line chart data based on region metrics
  const lineChartData = useMemo(() => {
    const parsedEmp = parseInt(data.metrics.employment.value);
    const parsedConn = parseInt(data.metrics.connectivity.value);
    const months = [
      { mes: "Ene", empOffset: -8, connOffset: -7 },
      { mes: "Feb", empOffset: -6, connOffset: -5 },
      { mes: "Mar", empOffset: -5, connOffset: -4 },
      { mes: "Abr", empOffset: -6, connOffset: -3 },
      { mes: "May", empOffset: -4, connOffset: -3 },
      { mes: "Jun", empOffset: -3, connOffset: -2 },
      { mes: "Jul", empOffset: -4, connOffset: -1 },
      { mes: "Ago", empOffset: -2, connOffset: 0 },
      { mes: "Sep", empOffset: -1, connOffset: -1 },
      { mes: "Oct", empOffset: -2, connOffset: -2 },
      { mes: "Nov", empOffset: -1, connOffset: -1 },
      { mes: "Dic", empOffset: 0, connOffset: 0 },
    ];
    return months.map((m) => ({
      mes: m.mes,
      Empleo: Math.max(0, parsedEmp + m.empOffset),
      Conectividad: Math.max(0, parsedConn + m.connOffset),
    }));
  }, [data]);

  return (
    <div className="space-y-6">
      {/* Header and Back navigation */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="w-9 h-9 rounded-lg bg-white border border-slate-200 hover:bg-slate-50 flex items-center justify-center cursor-pointer transition-colors shadow-xs"
          >
            <ArrowLeft className="w-4 h-4 text-slate-600" />
          </button>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h2 className="text-xl font-bold text-slate-800 leading-tight">
                Región {data.name}
              </h2>
              {data.alerts > 0 ? (
                <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full border bg-red-50 text-red-700 border-red-200 animate-pulse">
                  {data.alerts} {data.alerts === 1 ? "alerta" : "alertas"}
                </span>
              ) : (
                <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full border bg-green-50 text-green-700 border-green-200">
                  Sin alertas
                </span>
              )}
            </div>
            <p className="text-xs text-slate-500 mt-1">
              {data.population} habitantes • {data.courses} programas de formación • Actualizado: 10 dic 2024
            </p>
          </div>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Tasa de Empleo */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-xl bg-amber-50 border border-amber-100 flex items-center justify-center">
              <Briefcase className="w-4.5 h-4.5 text-amber-600" />
            </div>
            <div className="flex items-center gap-1 text-[11px] text-green-600 font-bold">
              <ArrowUpRight className="w-3.5 h-3.5" />
              <span>{data.metrics.employment.change}</span>
            </div>
          </div>
          <div className="mt-4">
            <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
              {data.metrics.employment.value}
            </h4>
            <p className="text-[11px] text-slate-500 mt-1 font-semibold">
              Tasa de Empleo
            </p>
          </div>
        </div>

        {/* Card 2: Conectividad */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-xl bg-orange-50 border border-orange-100 flex items-center justify-center">
              <Wifi className="w-4.5 h-4.5 text-orange-600" />
            </div>
            <div className="flex items-center gap-1 text-[11px] text-green-600 font-bold">
              <ArrowUpRight className="w-3.5 h-3.5" />
              <span>{data.metrics.connectivity.change}</span>
            </div>
          </div>
          <div className="mt-4">
            <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
              {data.metrics.connectivity.value}
            </h4>
            <p className="text-[11px] text-slate-500 mt-1 font-semibold">
              Conectividad
            </p>
          </div>
        </div>

        {/* Card 3: Salud Mental */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-xl bg-red-50 border border-red-100 flex items-center justify-center">
              <Activity className="w-4.5 h-4.5 text-red-600" />
            </div>
            <div className="flex items-center gap-1 text-[11px] text-green-600 font-bold">
              <ArrowUpRight className="w-3.5 h-3.5" />
              <span>{data.metrics.mentalHealth.change}</span>
            </div>
          </div>
          <div className="mt-4">
            <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
              {data.metrics.mentalHealth.value}
            </h4>
            <p className="text-[11px] text-slate-500 mt-1 font-semibold">
              Salud Mental
            </p>
          </div>
        </div>

        {/* Card 4: Inclusión Digital */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center">
              <TrendingUp className="w-4.5 h-4.5 text-blue-600" />
            </div>
            <div className="flex items-center gap-1 text-[11px] text-green-600 font-bold">
              <ArrowUpRight className="w-3.5 h-3.5" />
              <span>{data.metrics.digitalInclusion.change}</span>
            </div>
          </div>
          <div className="mt-4">
            <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
              {data.metrics.digitalInclusion.value}
            </h4>
            <p className="text-[11px] text-slate-500 mt-1 font-semibold">
              Inclusión Digital
            </p>
          </div>
        </div>
      </div>

      {/* Main Grid: charts and assistant */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column: Charts (Grid span 2) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Historical Trend line chart */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">
                Tendencia Histórica — {data.name}
              </h3>
              <span className="text-[10px] font-bold bg-slate-50 px-2 py-0.5 rounded-full border border-slate-200 text-slate-500">
                12 meses
              </span>
            </div>
            <div className="h-[240px] mt-4 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={lineChartData}
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
                    domain={[0, 100]}
                  />
                  <Tooltip
                    contentStyle={{ fontSize: 11, borderRadius: 8, borderColor: "#cbd5e1" }}
                  />
                  <Line
                    type="monotone"
                    dataKey="Empleo"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    dot={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="Conectividad"
                    stroke="#0d9488"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            {/* Custom chart legend */}
            <div className="flex items-center justify-center gap-4 text-[10px] text-slate-500 font-bold mt-2">
              <div className="flex items-center gap-1">
                <span className="w-2.5 h-1 bg-blue-500 inline-block rounded-full"></span>
                <span>Empleo</span>
              </div>
              <div className="flex items-center gap-1">
                <span className="w-2.5 h-1 bg-teal-600 inline-block rounded-full"></span>
                <span>Conectividad</span>
              </div>
            </div>
          </div>

          {/* Sub grid: radar indicators & employment compared */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Radar Indicators profile */}
            <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <h3 className="text-sm font-bold text-slate-800">
                  Perfil de Indicadores
                </h3>
              </div>
              <div className="h-[200px] mt-4 flex items-center justify-center w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data.radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" tick={{ fontSize: 9, fill: "#475569" }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 8 }} />
                    <Radar
                      name={data.name}
                      dataKey="A"
                      stroke="#2563eb"
                      fill="#3b82f6"
                      fillOpacity={0.2}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Employment compared to other regions list */}
            <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                <h3 className="text-sm font-bold text-slate-800">
                  Empleo vs. Otras Regiones
                </h3>
              </div>
              <div className="flex-1 space-y-2.5 overflow-y-auto max-h-[200px] pr-1">
                {comparisonList.map((item, idx) => {
                  const isCurrent = item.id === key;
                  return (
                    <div key={item.id} className="space-y-1">
                      <div className="flex items-center justify-between text-[11px] font-bold text-slate-700">
                        <span className="flex items-center gap-1.5">
                          <span className="text-slate-400 w-3.5 text-right">{idx + 1}</span>
                          <span className={isCurrent ? "text-blue-600 font-extrabold" : "text-slate-600"}>
                            {item.name}
                          </span>
                        </span>
                        <span className={isCurrent ? "text-blue-600 font-extrabold" : "text-slate-800"}>
                          {item.employmentVal}%
                        </span>
                      </div>
                      <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${isCurrent ? "bg-blue-600" : "bg-slate-300"}`}
                          style={{ width: `${item.employmentVal}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Program summaries row */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-slate-800">
              Resumen de Programas — {data.name}
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Card Formaciones */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <h4 className="text-2xl font-bold text-slate-850">{data.courses}</h4>
                  <p className="text-[10px] text-slate-500 font-semibold mt-0.5">Programas de Formación</p>
                </div>
                <div className="w-9 h-9 rounded-xl bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center">
                  <BookOpen className="w-4.5 h-4.5" />
                </div>
              </div>

              {/* Card Mentorías */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <h4 className="text-2xl font-bold text-slate-850">{data.mentorings}</h4>
                  <p className="text-[10px] text-slate-500 font-semibold mt-0.5">Mentorías Activas</p>
                </div>
                <div className="w-9 h-9 rounded-xl bg-purple-50 border border-purple-100 text-purple-600 flex items-center justify-center">
                  <GraduationCap className="w-4.5 h-4.5" />
                </div>
              </div>

              {/* Card Experiencias */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <h4 className="text-2xl font-bold text-slate-850">{data.experiences}</h4>
                  <p className="text-[10px] text-slate-500 font-semibold mt-0.5">Experiencias</p>
                </div>
                <div className="w-9 h-9 rounded-xl bg-yellow-50 border border-yellow-100 text-yellow-600 flex items-center justify-center">
                  <Star className="w-4.5 h-4.5" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right column: Non-functional Visual‑Only AI Assistant */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded bg-[#2563eb] text-white flex items-center justify-center">
                  <Bot className="w-3.5 h-3.5" />
                </div>
                <h3 className="text-sm font-bold text-slate-800">
                  Asistente IA
                </h3>
              </div>
              <span className="flex items-center gap-1.5 text-[10px] text-green-600 font-bold bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                <span>En línea</span>
              </span>
            </div>

            {/* AI Welcome Message with Bot Avatar inside a blue circle */}
            <div className="mt-4 flex gap-3 items-start bg-slate-50 rounded-xl p-3 border border-slate-100">
              <div className="w-8 h-8 rounded-full bg-[#2563eb] text-white flex items-center justify-center shrink-0">
                <Bot className="w-4.5 h-4.5" />
              </div>
              <p className="text-xs text-slate-700 leading-relaxed">
                Hola, soy el asistente de IA del APP BiT. Puedo ayudarle a
                analizar datos sociales, identificar brechas regionales y
                generar recomendaciones basadas en evidencia. ¿Qué le gustaría
                explorar hoy?
              </p>
            </div>

            {/* Static suggestions matching main panel style but non-functional */}
            <div className="mt-4 space-y-2">
              <button className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer leading-tight">
                ¿Qué regiones tienen alto desempleo y baja conectividad?
              </button>
              <button className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer leading-tight">
                ¿Dónde faltan programas de formación?
              </button>
              <button className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer leading-tight">
                ¿Qué zonas son prioridad para inversión social?
              </button>
              <button className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer leading-tight">
                ¿Cómo impacta la conectividad en la salud mental?
              </button>
            </div>
          </div>

          {/* AI Chat Input - Static, non-functional */}
          <div className="mt-6 relative">
            <input
              type="text"
              placeholder="Haga una pregunta sobre los datos..."
              className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-3 pr-10 py-2.5 text-xs focus:outline-none focus:border-blue-500"
              readOnly
            />
            <button className="absolute right-2 top-1/2 -translate-y-1/2 w-7 h-7 bg-blue-100 text-blue-600 flex items-center justify-center rounded-md cursor-default">
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ClusterDetailPage;
