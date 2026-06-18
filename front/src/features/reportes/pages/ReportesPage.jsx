import { useState, useRef, useEffect } from "react";
import {
  FileText,
  Calendar,
  ChevronDown,
  Sparkles,
  Loader2,
  FileDown,
  Activity,
  Check,
  Wifi,
  Briefcase,
  Heart,
  TrendingUp,
  AlertTriangle,
} from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart";

// Mock Data for the generated report chart (3 series)
const reportChartData = [
  { region: "Noroeste", empleo: 58, conectividad: 38, inclusion: 30 },
  { region: "Norte", empleo: 62, conectividad: 45, inclusion: 36 },
  { region: "Noreste", empleo: 71, conectividad: 68, inclusion: 52 },
  { region: "Occidente", empleo: 65, conectividad: 52, inclusion: 45 },
  { region: "Centro", empleo: 82, conectividad: 90, inclusion: 78 },
  { region: "Oriente", empleo: 74, conectividad: 72, inclusion: 61 },
];

const reportChartConfig = {
  empleo: {
    label: "Empleo",
    color: "#2563eb",
  },
  conectividad: {
    label: "Conectividad",
    color: "#0d9488",
  },
  inclusion: {
    label: "Inclusión",
    color: "#a855f7",
  },
};

const templates = [
  {
    id: 1,
    title: "Informe Ejecutivo Mensual",
    description: "Resumen de todos los indicadores del período seleccionado",
    tags: ["KPIs", "Mapa", "Tendencias", "Alertas"],
    icon: FileText,
    iconColor: "text-blue-600 bg-blue-50 border-blue-100",
  },
  {
    id: 2,
    title: "Análisis de Empleabilidad",
    description: "Informe detallado de empleo, desempleo y brechas laborales",
    tags: ["Empleo Regional", "Tendencias", "Brecha Género"],
    icon: Briefcase,
    iconColor: "text-emerald-600 bg-emerald-50 border-emerald-100",
  },
  {
    id: 3,
    title: "Informe de Conectividad",
    description: "Cobertura digital, brechas e iniciativas de acceso",
    tags: ["Cobertura", "Brechas", "Inversiones"],
    icon: Wifi,
    iconColor: "text-purple-600 bg-purple-50 border-purple-100",
  },
  {
    id: 4,
    title: "Salud Mental y Bienestar",
    description: "Indicadores de bienestar psicosocial por región",
    tags: ["Índices", "Correlaciones", "Recomendaciones"],
    icon: Heart,
    iconColor: "text-pink-600 bg-pink-50 border-pink-100",
  },
];

const sectionsToIncludeList = [
  { id: "resumen", label: "Resumen ejecutivo" },
  { id: "mapa", label: "Mapa interactivo" },
  { id: "graficos", label: "Gráficos analíticos" },
  { id: "recomendaciones", label: "Recomendaciones IA" },
  { id: "alertas", label: "Alertas activas" },
  { id: "comparacion", label: "Comparación regional" },
];

function ReportesPage() {
  const [selectedPeriod, setSelectedPeriod] = useState("Diciembre 2024");
  const [selectedTemplate, setSelectedTemplate] = useState(1);
  const [checkedSections, setCheckedSections] = useState({
    resumen: true,
    mapa: true,
    graficos: true,
    recomendaciones: true,
    alertas: true,
    comparacion: true,
  });

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedReport, setGeneratedReport] = useState(null);

  const dropdownRef = useRef(null);

  // Handle click outside for dropdown closure
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Toggle checkbox state
  const handleCheckboxChange = (id) => {
    setCheckedSections((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // Handle generating report simulation
  const handleGenerateReport = () => {
    setIsGenerating(true);
    setGeneratedReport(null);

    // Simulate IA loading duration
    setTimeout(() => {
      setIsGenerating(false);
      setGeneratedReport({
        period: selectedPeriod,
        templateName: templates.find((t) => t.id === selectedTemplate)?.title,
        sections: { ...checkedSections },
      });
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Title & Header Row */}
      <div>
        <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
          <FileText className="w-5 h-5 text-blue-600" />
          <span>Generador de Reportes</span>
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          Cree informes ejecutivos con IA y exporte en PDF o Excel
        </p>
      </div>

      {/* Main Grid Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Left Column: Configure Report (2/5 size) */}
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow space-y-6 flex flex-col justify-between">
          <div className="space-y-5">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Configurar Reporte
            </h3>

            {/* Period selector */}
            <div className="space-y-2">
              <label className="text-[11px] font-bold text-slate-500 uppercase">
                Periodo
              </label>
              <div className="relative" ref={dropdownRef}>
                <button
                  onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                  className="w-full flex items-center justify-between gap-2 bg-white border border-slate-200 text-xs font-semibold text-slate-700 px-3.5 py-2.5 rounded-lg hover:bg-slate-50 cursor-pointer select-none text-left"
                >
                  <span className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-slate-400" />
                    {selectedPeriod}
                  </span>
                  <ChevronDown
                    className={`w-4 h-4 text-slate-400 transition-transform duration-150 ${isDropdownOpen ? "rotate-180" : ""}`}
                  />
                </button>

                {isDropdownOpen && (
                  <div className="absolute left-0 right-0 top-full mt-1.5 bg-white border border-slate-200 rounded-lg shadow-md py-1 z-50 animate-in fade-in slide-in-from-top-1 duration-100">
                    {[
                      "Noviembre 2024",
                      "Diciembre 2024",
                      "Q4 2024",
                      "Año 2024",
                    ].map((opt) => (
                      <button
                        key={opt}
                        onClick={() => {
                          setSelectedPeriod(opt);
                          setIsDropdownOpen(false);
                        }}
                        className={`w-full text-left px-3 py-2 text-xs hover:bg-slate-50 cursor-pointer flex items-center justify-between ${selectedPeriod === opt ? "bg-blue-50/50 text-blue-600 font-bold" : "text-slate-700"}`}
                      >
                        <span>{opt}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Template select cards */}
            <div className="space-y-2">
              <label className="text-[11px] font-bold text-slate-500 uppercase">
                Plantilla de Reporte
              </label>
              <div className="space-y-3">
                {templates.map((tpl) => {
                  const Icon = tpl.icon;
                  const isSelected = selectedTemplate === tpl.id;
                  return (
                    <div
                      key={tpl.id}
                      onClick={() => setSelectedTemplate(tpl.id)}
                      className={`border p-3 rounded-lg flex gap-3 cursor-pointer transition-all duration-200 relative select-none ${
                        isSelected
                          ? "border-blue-600 bg-blue-50/10"
                          : "border-slate-200 hover:border-slate-300 bg-white"
                      }`}
                    >
                      <div
                        className={`w-8 h-8 rounded-lg flex items-center justify-center border shrink-0 ${tpl.iconColor}`}
                      >
                        <Icon className="w-4 h-4" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="text-xs font-bold text-slate-800 leading-snug">
                          {tpl.title}
                        </h4>
                        <p className="text-[10px] text-slate-400 mt-1 leading-normal">
                          {tpl.description}
                        </p>

                        {/* Tags list */}
                        <div className="flex flex-wrap gap-1 mt-2">
                          {tpl.tags.map((tag) => (
                            <span
                              key={tag}
                              className="text-[9px] font-semibold text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200/50"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* Selected green indicator check */}
                      {isSelected && (
                        <div className="absolute top-3 right-3 w-4 h-4 rounded-full bg-emerald-500 text-white flex items-center justify-center shrink-0">
                          <Check className="w-2.5 h-2.5 stroke-[3]" />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Sections checklist */}
            <div className="space-y-2">
              <label className="text-[11px] font-bold text-slate-500 uppercase">
                Secciones a Incluir
              </label>
              <div className="grid grid-cols-2 gap-3">
                {sectionsToIncludeList.map((sec) => {
                  const isChecked = checkedSections[sec.id];
                  return (
                    <div
                      key={sec.id}
                      onClick={() => handleCheckboxChange(sec.id)}
                      className="flex items-center gap-2.5 cursor-pointer text-xs text-slate-600 font-semibold select-none"
                    >
                      <div
                        className={`w-4.5 h-4.5 border rounded flex items-center justify-center shrink-0 transition-colors ${
                          isChecked
                            ? "bg-blue-600 border-blue-600 text-white"
                            : "border-slate-300 hover:border-slate-400 bg-white"
                        }`}
                      >
                        {isChecked && <Check className="w-3 h-3 stroke-[3]" />}
                      </div>
                      <span>{sec.label}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Action Generate Button */}
          <div className="pt-4 border-t border-slate-100 mt-4">
            <button
              onClick={handleGenerateReport}
              disabled={isGenerating}
              className="w-full flex items-center justify-center gap-1.5 bg-[#2563eb] hover:bg-blue-600 text-white font-medium text-xs py-2.5 rounded-lg transition-colors cursor-pointer shadow-sm disabled:opacity-50 disabled:pointer-events-none"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Generar Reporte</span>
            </button>
          </div>
        </div>

        {/* Right Column: Preview Panel (3/5 size) */}
        <div className="lg:col-span-3 bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow min-h-[450px] flex flex-col relative overflow-hidden">
          {/* Loading state overlay */}
          {isGenerating && (
            <div className="absolute inset-0 bg-white/95 z-40 flex flex-col items-center justify-center gap-3 animate-in fade-in duration-200">
              <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
              <p className="text-xs text-slate-500 font-bold tracking-wider animate-pulse">
                Generando con IA...
              </p>
            </div>
          )}

          {/* 1. Empty State (Initial) */}
          {!generatedReport && !isGenerating && (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8 space-y-4">
              <div className="flex items-center justify-between w-full border-b border-slate-100 pb-3 absolute top-5 left-5 right-5 pr-10">
                <h3 className="text-xs font-bold text-slate-800">
                  Vista Previa del Reporte
                </h3>
              </div>
              <div className="w-16 h-16 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-300">
                <FileText className="w-8 h-8" />
              </div>
              <div className="max-w-xs space-y-1">
                <h4 className="text-xs font-bold text-slate-700">
                  Seleccione una plantilla y haga clic en "Generar Reporte"
                </h4>
                <p className="text-[10px] text-slate-400 font-medium leading-relaxed">
                  El reporte se generará con datos en tiempo real y análisis de
                  IA
                </p>
              </div>
            </div>
          )}

          {/* 2. Generated Report Preview State */}
          {generatedReport && !isGenerating && (
            <div className="flex-1 flex flex-col justify-between space-y-4">
              {/* Preview top header bar */}
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 flex-shrink-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-xs font-bold text-slate-800">
                    Vista Previa del Reporte
                  </h3>
                  <span className="inline-flex items-center gap-1 bg-green-50 text-green-700 border border-green-200 px-2.5 py-0.5 rounded-full text-[9px] font-bold">
                    <Check className="w-2.5 h-2.5" />
                    <span>Generado</span>
                  </span>
                </div>

                {/* Actions (Excel / PDF) */}
                <div className="flex items-center gap-2">
                  <button className="flex items-center gap-1 bg-white border border-slate-200 text-[10px] font-semibold text-slate-600 px-2.5 py-1.5 rounded hover:bg-slate-50 cursor-pointer">
                    <FileDown className="w-3 h-3 text-slate-400" />
                    <span>Excel</span>
                  </button>
                  <button className="flex items-center gap-1 bg-blue-600 text-white border border-blue-600 text-[10px] font-semibold px-2.5 py-1.5 rounded hover:bg-blue-700 cursor-pointer">
                    <FileDown className="w-3 h-3" />
                    <span>PDF</span>
                  </button>
                </div>
              </div>

              {/* Preview Document Paper Sheet */}
              <div className="flex-1 overflow-y-auto space-y-4 border border-slate-100 rounded-lg p-4 bg-slate-50/40">
                {/* Main Dark Document Header block */}
                <div className="bg-[#0f172a] text-white rounded-lg p-5 space-y-4 relative overflow-hidden">
                  <div>
                    <span className="text-[9px] font-bold text-blue-400 uppercase tracking-widest">
                      APP BIT — INFORME EJECUTIVO
                    </span>
                    <h4 className="text-sm font-bold text-white mt-1 leading-snug">
                      Plataforma de Inteligencia Pública
                    </h4>
                    <p className="text-[10px] text-slate-400 mt-1">
                      Periodo: {generatedReport.period} · Generado con IA · 9
                      regiones
                    </p>
                  </div>

                  {/* Top banner Mini KPI Summary */}
                  <div className="flex items-center gap-8 pt-3 border-t border-slate-800">
                    <div>
                      <h5 className="text-sm font-bold text-white leading-none">
                        68.4%
                      </h5>
                      <span className="text-[9px] text-slate-400 mt-1 inline-block">
                        Empleo
                      </span>
                    </div>
                    <div>
                      <h5 className="text-sm font-bold text-white leading-none">
                        54.2%
                      </h5>
                      <span className="text-[9px] text-slate-400 mt-1 inline-block">
                        Conectividad
                      </span>
                    </div>
                    <div>
                      <h5 className="text-sm font-bold text-white leading-none">
                        3.4/5
                      </h5>
                      <span className="text-[9px] text-slate-400 mt-1 inline-block">
                        Salud Mental
                      </span>
                    </div>
                  </div>
                </div>

                {/* Resumen Ejecutivo block (if checked) */}
                {generatedReport.sections.resumen && (
                  <div className="bg-blue-50/30 border border-blue-100 rounded-lg p-4 space-y-2">
                    <div className="flex items-center gap-2 text-blue-800 font-bold text-[11px]">
                      <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                      <span>Resumen Ejecutivo (Generado por IA)</span>
                    </div>
                    <p className="text-[10px] text-slate-700 leading-relaxed font-medium">
                      El análisis integral del periodo{" "}
                      <span className="font-bold text-slate-800">
                        {generatedReport.period.toLowerCase()}
                      </span>{" "}
                      revela avances significativos en los indicadores de empleo
                      (+2.3%) y conectividad (+5.1%), sin embargo persisten{" "}
                      <span className="text-red-700 font-bold">
                        brechas críticas en las regiones Sur y Suroeste
                      </span>
                      . La correlación empleo-conectividad continúa siendo el
                      factor determinante para el bienestar social regional. Se
                      recomienda priorizar inversión en infraestructura digital
                      para las regiones con índice de conectividad por debajo
                      del 40%.
                    </p>
                  </div>
                )}

                {/* Indicadores por Región Chart block (if checked) */}
                {generatedReport.sections.graficos && (
                  <div className="bg-white border border-slate-100 rounded-lg p-4 space-y-3">
                    <h5 className="text-[11px] font-bold text-slate-700">
                      Indicadores por Región
                    </h5>

                    <ChartContainer
                      config={reportChartConfig}
                      className="h-[200px] w-full"
                    >
                      <BarChart
                        data={reportChartData}
                        margin={{ top: 10, right: 10, left: -25, bottom: 0 }}
                      >
                        <CartesianGrid vertical={false} strokeDasharray="3 3" />
                        <XAxis
                          dataKey="region"
                          tickLine={false}
                          axisLine={false}
                          tickMargin={8}
                          tick={{ fontSize: 8, fill: "#64748b" }}
                        />
                        <YAxis
                          tickLine={false}
                          axisLine={false}
                          tickMargin={8}
                          tick={{ fontSize: 8, fill: "#64748b" }}
                          domain={[0, 100]}
                        />
                        <ChartTooltip content={<ChartTooltipContent />} />
                        <Bar
                          dataKey="empleo"
                          fill="var(--color-empleo)"
                          radius={[1, 1, 0, 0]}
                          barSize={8}
                        />
                        <Bar
                          dataKey="conectividad"
                          fill="var(--color-conectividad)"
                          radius={[1, 1, 0, 0]}
                          barSize={8}
                        />
                        <Bar
                          dataKey="inclusion"
                          fill="var(--color-inclusion)"
                          radius={[1, 1, 0, 0]}
                          barSize={8}
                        />
                        <ChartLegend content={<ChartLegendContent />} />
                      </BarChart>
                    </ChartContainer>
                  </div>
                )}

                {/* Recomendaciones Estratégicas block (if checked) */}
                {generatedReport.sections.recomendaciones && (
                  <div className="bg-white border border-slate-100 rounded-lg p-4 space-y-3">
                    <h5 className="text-[11px] font-bold text-slate-700">
                      Recomendaciones Estratégicas
                    </h5>

                    <div className="space-y-2">
                      <div className="flex items-start gap-2.5 bg-red-50/30 border border-red-100 p-2.5 rounded text-[10px] text-slate-700 font-medium leading-normal">
                        <span className="bg-red-500 text-white text-[8px] font-bold px-1.5 py-0.5 rounded shrink-0">
                          Alta
                        </span>
                        <span>
                          Expansión urgente de infraestructura de
                          telecomunicaciones en Suroeste y Sur
                        </span>
                      </div>

                      <div className="flex items-start gap-2.5 bg-red-50/30 border border-red-100 p-2.5 rounded text-[10px] text-slate-700 font-medium leading-normal">
                        <span className="bg-red-500 text-white text-[8px] font-bold px-1.5 py-0.5 rounded shrink-0">
                          Alta
                        </span>
                        <span>
                          Activación de programas de emergencia laboral en
                          regiones con desempleo &gt;45%
                        </span>
                      </div>

                      <div className="flex items-start gap-2.5 bg-amber-50/30 border border-amber-100 p-2.5 rounded text-[10px] text-slate-700 font-medium leading-normal">
                        <span className="bg-amber-500 text-white text-[8px] font-bold px-1.5 py-0.5 rounded shrink-0">
                          Media
                        </span>
                        <span>
                          Ampliación de programas de formación digital en zonas
                          rurales con baja cobertura
                        </span>
                      </div>

                      <div className="flex items-start gap-2.5 bg-amber-50/30 border border-amber-100 p-2.5 rounded text-[10px] text-slate-700 font-medium leading-normal">
                        <span className="bg-amber-500 text-white text-[8px] font-bold px-1.5 py-0.5 rounded shrink-0">
                          Media
                        </span>
                        <span>
                          Refuerzo de equipos de salud mental en regiones con
                          índice &lt;3.0/5
                        </span>
                      </div>

                      <div className="flex items-start gap-2.5 bg-emerald-50/30 border border-emerald-100 p-2.5 rounded text-[10px] text-slate-700 font-medium leading-normal">
                        <span className="bg-emerald-500 text-white text-[8px] font-bold px-1.5 py-0.5 rounded shrink-0">
                          Baja
                        </span>
                        <span>
                          Replicación del modelo del Laboratorio de Innovación
                          Social de Centro en 3 regiones
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ReportesPage;
