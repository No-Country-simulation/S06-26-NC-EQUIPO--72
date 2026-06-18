import {
  AlertCircle,
  Bell,
  Brain,
  Funnel,
  MoveRight,
  TriangleAlert,
} from "lucide-react";
import { useState } from "react";
import { AlertCard } from "../components/AlertCard";

export default function AlertasPage() {
  const alerts = [
    {
      id: 1,
      type: "critical",
      title: "Desconectividad crítica en Suroeste",
      description:
        "La región Suroeste registra 27% de cobertura de conectividad — mínimo histórico.",
      region: "Suroeste",
      date: "2024-12-10",
      action: "Revisar infraestructura de red",
    },
    {
      id: 2,
      type: "critical",
      title: "Índice de desempleo en zona Sur supera 50%",
      description:
        "Tasa de desempleo alcanza 46%, superando un umbral crítico.",
      region: "Sur",
      date: "2024-12-09",
      action: "Activar programa de emergencia laboral",
    },
    {
      id: 3,
      type: "warning",
      title: "Deterioro de indicadores de salud mental",
      description: "El índice de bienestar mental bajó a 2.3/5.",
      region: "Suroeste",
      date: "2024-12-08",
      action: "Asignar equipos de apoyo psicosocial",
    },
    {
      id: 4,
      type: "warning",
      title: "Brechas de formación en región Norte",
      description: "Solo 45% de cobertura en programas de capacitación.",
      region: "Norte",
      date: "2024-12-07",
      action: "Ampliar centros de capacitación",
    },
    {
      id: 5,
      type: "info",
      title: "Aumento de demanda de mentoría",
      description: "Se registró un incremento del 34% en solicitudes.",
      region: "Noroeste",
      date: "2024-12-06",
      action: "Evaluar ampliación de capacidad",
    },
    {
      id: 6,
      type: "info",
      title: "Baja participación laboral femenina — Sur",
      description:
        "La participación femenina en el mercado laboral es de solo 38% en la región Sur.",
      region: "Sur",
      date: "2024-12-05",
      action: "Implementar programa de equidad laboral",
    },
    {
      id: 7,
      type: "info",
      title: "Expansión de conectividad en Noreste",
      description:
        "Infraestructura de conectividad en Noreste avanza bien — 67% de cobertura alcanzada.",
      region: "Noreste",
      date: "2024-12-04",
      action: "Continuar con el plan de expansión",
    },
  ];

  const FILTERS = {
    all: "Todos",
    critical: "Crítica",
    warning: "Alerta",
    info: "Aviso",
  };

  const [selectedFilter, setSelectedFilter] = useState("all");

  const filteredAlerts =
    selectedFilter === "all"
      ? alerts
      : alerts.filter((alert) => alert.type === selectedFilter);

  const getCount = (type) => alerts.filter((a) => a.type === type).length;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Bell className="w-5 h-5 text-red-600" />
            <span>Centro de Alertas</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Monitoreo inteligente de riesgos e indicadores críticos
          </p>
        </div>
        <div>
          <span className="flex items-center gap-1.5 bg-red-50 border border-red-200  text-red-500 font-medium text-sm px-4 py-2.5 rounded-lg">
            <AlertCircle className="w-4 h-4" />
            <span>2 alertas criticas</span>
          </span>
        </div>
      </div>
      {/*  */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-white border border-red-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <span className="text-2xl font-semibold text-red-600">2</span>
          </div>
          <div className="flex flex-col gap-0.5">
            <h2 className="text-sm font-semibold">Críticas</h2>
            <p className="text-xs text-slate-500">Requieren acción inmediata</p>
          </div>
        </div>
        <div className="bg-white border border-amber-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
          <div className="flex items-center gap-2">
            <TriangleAlert className="w-5 h-5 text-amber-600" />
            <span className="text-2xl font-semibold text-amber-600">2</span>
          </div>
          <div className="flex flex-col gap-0.5">
            <h2 className="text-sm font-semibold">Alertas</h2>
            <p className="text-xs text-slate-500">Monitoreo intensivo</p>
          </div>
        </div>
        <div className="bg-white border border-blue-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-blue-600" />
            <span className="text-2xl font-semibold text-blue-600">3</span>
          </div>
          <div className="flex flex-col gap-0.5">
            <h2 className="text-sm font-semibold">Avisos</h2>
            <p className="text-xs text-slate-500">Información relevante</p>
          </div>
        </div>
      </div>
      {/* Visualizations Grid */}
      <div className="grid grid-cols-1 gap-6">
        <div className="bg-white rounded-xl p-5 lg:col-span-2 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between pb-3">
            <div className="flex items-center gap-2">
              <Brain className="w-4.5 h-4.5 text-blue-800" />
              <h3 className="text-sm font-semibold">Análisis IA de Alertas</h3>
            </div>
            <span className="flex items-center gap-1.5 bg-blue-100 text-blue-500 text-xs p-1 px-2 rounded-lg">
              <span>Actualizado hace 5 min</span>
            </span>
          </div>
          <div className="flex flex-col gap-2">
            <div className="flex gap-2 item-start p-3 bg-red-50 rounded-lg">
              <MoveRight className="shrink-0 font-bold h-4 w-4 text-red-600" />
              <p className="text-sm">
                Las regiones críticas (Suroeste y Sur) comparten un patrón de
                baja conectividad + alto desempleo. Intervención conjunta
                recomendada.
              </p>
            </div>
            <div className="flex gap-2 item-start p-3 bg-yellow-100 rounded-lg">
              <MoveRight className="shrink-0 font-bold h-4 w-4 text-amber-600" />
              <p className="text-sm">
                El deterioro de salud mental en Suroeste muestra aceleración en
                los últimos 60 días. Riesgo de escalada si no hay intervención
                psicosocial.
              </p>
            </div>
            <div className="flex gap-2 item-start p-3 bg-blue-50 rounded-lg">
              <MoveRight className="shrink-0 font-bold h-4 w-4 text-blue-600" />
              <p className="text-sm">
                La alerta de formación en Norte puede atenderse con
                redistribución de recursos existentes de la región Centro.
              </p>
            </div>
          </div>
        </div>
      </div>
      {/*  */}
      <section className="bg-white rounded-xl border border-slate-200 p-6">
        <div className="flex flex-wrap items-center gap-2 mb-6">
          <Funnel className="w-4 h-4 text-slate-500" />
          {Object.entries(FILTERS).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setSelectedFilter(key)}
              className={`flex items-center px-3 py-1 rounded-lg text-sm font-medium transition cursor-pointer
              ${selectedFilter === key && "bg-slate-900 text-white"}`}
            >
              <p>{label}</p>
              {key !== "all" && (
                <span
                  className={`ml-2 text-xs w-6 h-6 rounded-full grid place-items-center
                  ${
                    selectedFilter === key
                      ? "bg-white/40 text-white"
                      : "bg-slate-200 text-slate-600 hover:bg-slate-200"
                  }`}
                >
                  {getCount(key)}
                </span>
              )}
            </button>
          ))}
          <span className="ml-auto text-xs text-slate-400">
            {filteredAlerts.length} alertas
          </span>
        </div>
        <div className="space-y-4">
          {filteredAlerts.map((alert) => (
            <AlertCard key={alert.id} alert={alert} />
          ))}
        </div>
      </section>
    </div>
  );
}
