import { useState, useMemo, useRef, useEffect } from "react";
import { useAiAgent } from "../hooks/useAiAgent";
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
  Loader2,
  AlertCircle,
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
import { useMapData, usePrograms, useMapsIndicators } from "../hooks/useMaps";

function ClusterDetailPage({ clusterName, onBack, activeTab = "EMPLEO" }) {
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: `Hola, soy el asistente de IA del APP BiT. He analizado la Región ${clusterName} y puedo ayudarte a identificar brechas y generar recomendaciones basadas en evidencia. ¿Qué te gustaría explorar hoy?`,
    },
  ]);
  const [chatInput, setChatInput] = useState("");
  const chatContainerRef = useRef(null);

  const aiMutation = useAiAgent();

  const handleSendMessage = (text) => {
    const messageToSend = text || chatInput;
    if (!messageToSend.trim() || aiMutation.isPending) return;

    setMessages((prev) => [...prev, { sender: "user", text: messageToSend }]);
    setChatInput("");

    let queryWithContext = messageToSend;
    const lowerMessage = messageToSend.toLowerCase();
    const regionNameLower = clusterName.toLowerCase();
    if (!lowerMessage.includes(regionNameLower)) {
      queryWithContext = `En la región ${clusterName}: ${messageToSend}`;
    }

    aiMutation.mutate(
      { consulta: queryWithContext, idioma: "es" },
      {
        onSuccess: (data) => {
          setMessages((prev) => [
            ...prev,
            { sender: "ai", text: data.respuesta_ia },
          ]);
        },
        onError: (error) => {
          setMessages((prev) => [
            ...prev,
            {
              sender: "ai",
              text: "Lo siento, ocurrió un error al procesar tu consulta. Por favor, intenta de nuevo más tarde.",
            },
          ]);
        },
      }
    );
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages]);

  // Fetch data desde backend
  const { data: mapData, isLoading: loadingMap, error: errorMap } = useMapData();
  const { data: empleoData } = useMapsIndicators("EMPLEO");
  const { data: educacionData } = useMapsIndicators("EDUCACION");
  const { data: saludData } = useMapsIndicators("SALUD_MENTAL");
  const { data: programsData } = usePrograms({ cluster: clusterName });

  // Mapeo de tabs a títulos y datos
  const tabConfig = {
    EMPLEO: {
      title: "Empleo vs. Otras Regiones",
      dataSource: empleoData,
      getValue: (reg) => 100 - parseFloat(reg.indicadores?.[0]?.valor || 0),
      displaySuffix: "%",
    },
    EDUCACION: {
      title: "Educación vs. Otras Regiones",
      dataSource: educacionData,
      getValue: (reg) => {
        const val = parseFloat(reg.indicadores?.[0]?.valor || 0);
        return val < 2 ? val * 100 : val;
      },
      displaySuffix: "%",
    },
    SALUD_MENTAL: {
      title: "Salud Mental vs. Otras Regiones",
      dataSource: saludData,
      getValue: (reg) => {
        const val = parseFloat(reg.indicadores?.[0]?.valor || 0);
        return Math.min(5, Math.max(0, (val / 15) * 4.8));
      },
      displaySuffix: "/5",
    },
  };

  const currentTabConfig = tabConfig[activeTab] || tabConfig.EMPLEO;

  // Buscar la región seleccionada en los datos disponibles
  const selectedRegion = useMemo(() => {
    if (!clusterName) return null;

    // Primero buscar en mapData (endpoint /mapa)
    let found = mapData?.regiones?.find((r) => 
      r.cluster.toUpperCase() === clusterName.toUpperCase()
    );

    // Si no está en mapData, buscar en los datos de indicadores que SÍ lo tienen
    if (!found) {
      const allIndicatorRegions = [
        ...(empleoData?.regiones || []),
        ...(educacionData?.regiones || []),
        ...(saludData?.regiones || []),
      ];
      
      found = allIndicatorRegions.find((r) => 
        r.cluster.toUpperCase() === clusterName.toUpperCase()
      );
    }

    return found;
  }, [mapData, empleoData, educacionData, saludData, clusterName]);

  // Obtener indicadores para esta región
  const regionIndicators = useMemo(() => {
    const indicators = {};
    
    if (empleoData?.regiones) {
      const reg = empleoData.regiones.find(
        (r) => r.cluster.toUpperCase() === clusterName?.toUpperCase()
      );
      if (reg?.indicadores?.[0]) {
        indicators.empleo = 100 - parseFloat(reg.indicadores[0].valor);
      }
    }

    if (educacionData?.regiones) {
      const reg = educacionData.regiones.find(
        (r) => r.cluster.toUpperCase() === clusterName?.toUpperCase()
      );
      if (reg?.indicadores?.[0]) {
        const val = parseFloat(reg.indicadores[0].valor);
        indicators.inclusion = val < 2 ? val * 100 : val;
      }
    }

    if (saludData?.regiones) {
      const reg = saludData.regiones.find(
        (r) => r.cluster.toUpperCase() === clusterName?.toUpperCase()
      );
      if (reg?.indicadores?.[0]) {
        indicators.saludMental = parseFloat(reg.indicadores[0].valor);
      }
    }

    return indicators;
  }, [empleoData, educacionData, saludData, clusterName]);

  // Contar programas por tipo
  const programCounts = useMemo(() => {
    const programs = programsData?.programs || [];
    return {
      courses: programs.filter((p) => p.tipo === "FORMACION").length,
      mentorings: programs.filter((p) => p.tipo === "MENTORIA").length,
      experiences: programs.filter((p) => p.tipo === "EXPERIENCIA").length,
    };
  }, [programsData]);

  // Obtener todas las regiones para el gráfico de comparación (dinámico según activeTab)
  const allRegionsForComparison = useMemo(() => {
    if (!currentTabConfig.dataSource?.regiones) return [];
    return currentTabConfig.dataSource.regiones.map((r) => {
      const value = currentTabConfig.getValue(r);
      return {
        id: r.cluster,
        name: r.cluster,
        value: Math.max(0, Math.min(100, Math.round(value))),
      };
    }).sort((a, b) => b.value - a.value);
  }, [currentTabConfig]);

  // Generar datos del gráfico radar (solo con datos reales disponibles)
  const radarData = useMemo(() => {
    const empleo = regionIndicators.empleo || 0;
    const conectividad = selectedRegion?.congestionamento_medio 
      ? Math.round(100 - selectedRegion.congestionamento_medio * 100) 
      : 0;
    const inclusion = regionIndicators.inclusion || 0;
    const saludMentalPercent = regionIndicators.saludMental 
      ? Math.max(0, Math.min(100, Math.round((regionIndicators.saludMental / 15) * 100))) 
      : 0;

    const data = [
      { subject: "Empleo", A: Math.round(empleo), fullMark: 100 },
      { subject: "Conectividad", A: conectividad, fullMark: 100 },
      { subject: "Salud Mental", A: saludMentalPercent, fullMark: 100 },
    ];
    
    if (inclusion > 0) {
      data.push({ subject: "Inclusión", A: Math.round(inclusion), fullMark: 100 });
    }
    
    return data;
  }, [regionIndicators, selectedRegion]);

  // Estados de carga y error
  if (loadingMap) {
    return (
      <div className="flex items-center justify-center h-full py-20">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (errorMap || !selectedRegion) {
    return (
      <div className="flex items-center justify-center h-full py-20">
        <div className="text-center">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto mb-2" />
          <p className="text-red-600 font-medium">
            {errorMap ? "Error al cargar los datos de la región" : "Región no encontrada"}
          </p>
        </div>
      </div>
    );
  }

  // Preparar valores para mostrar
  const displayName = selectedRegion.cluster;
  const populationValue = selectedRegion.n_usuarios 
    ? selectedRegion.n_usuarios >= 1000000 
      ? `${(selectedRegion.n_usuarios / 1000000).toFixed(1)}M` 
      : `${(selectedRegion.n_usuarios / 1000).toFixed(1)}K`
    : "0";
  
  const empleoValue = regionIndicators.empleo 
    ? `${regionIndicators.empleo.toFixed(0)}%` 
    : "60%";
  
  const conectividadValue = selectedRegion.congestionamento_medio 
    ? `${Math.round(100 - selectedRegion.congestionamento_medio * 100)}%` 
    : "50%";
  
  const saludMentalValue = regionIndicators.saludMental 
    ? `${Math.min(5, Math.max(0, (regionIndicators.saludMental / 15) * 4.8)).toFixed(1)}/5` 
    : "3.0/5";
  
  const inclusionValue = regionIndicators.inclusion 
    ? `${regionIndicators.inclusion.toFixed(0)}%` 
    : "50%";

  const hasAlerts = selectedRegion.congestionamento_medio && selectedRegion.congestionamento_medio > 0.7;

  return (
    <div className="space-y-6">
      {/* Encabezado y navegación de regreso */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="w-9 h-9 rounded-lg bg-[#2563eb] hover:bg-blue-600 flex items-center justify-center cursor-pointer transition-colors shadow-xs"
          >
            <ArrowLeft className="font-bold text-white w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h2 className="text-xl font-bold text-slate-800 leading-tight">
                {displayName}
              </h2>
              {hasAlerts ? (
                <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full border bg-red-50 text-red-700 border-red-200 animate-pulse">
                  1 alerta
                </span>
              ) : (
                <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full border bg-green-50 text-green-700 border-green-200">
                  Sin alertas
                </span>
              )}
            </div>
            <p className="text-xs text-slate-500 mt-1">
              {populationValue} usuarios • {programCounts.courses + programCounts.mentorings + programCounts.experiences} programas • Actualizado: {selectedRegion.fecha || new Date().toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>

      {/* Grid de Tarjetas de Métricas */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Tarjeta 1: Tasa de Empleo */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-xl bg-amber-50 border border-amber-100 flex items-center justify-center">
              <Briefcase className="w-4.5 h-4.5 text-amber-600" />
            </div>
          </div>
          <div className="mt-4">
            <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
              {empleoValue}
            </h4>
            <p className="text-[11px] text-slate-500 mt-1 font-semibold">
              Tasa de Empleo
            </p>
          </div>
        </div>

        {/* Tarjeta 2: Conectividad */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-xl bg-orange-50 border border-orange-100 flex items-center justify-center">
              <Wifi className="w-4.5 h-4.5 text-orange-600" />
            </div>
          </div>
          <div className="mt-4">
            <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
              {conectividadValue}
            </h4>
            <p className="text-[11px] text-slate-500 mt-1 font-semibold">
              Conectividad
            </p>
          </div>
        </div>

        {/* Tarjeta 3: Salud Mental */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-xl bg-red-50 border border-red-100 flex items-center justify-center">
              <Activity className="w-4.5 h-4.5 text-red-600" />
            </div>
          </div>
          <div className="mt-4">
            <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
              {saludMentalValue}
            </h4>
            <p className="text-[11px] text-slate-500 mt-1 font-semibold">
              Salud Mental
            </p>
          </div>
        </div>

        {/* Tarjeta 4: Inclusión Digital */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center">
              <TrendingUp className="w-4.5 h-4.5 text-blue-600" />
            </div>
          </div>
          <div className="mt-4">
            <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
              {inclusionValue}
            </h4>
            <p className="text-[11px] text-slate-500 mt-1 font-semibold">
              Inclusión Digital
            </p>
          </div>
        </div>
      </div>

      {/* Grid Principal: gráficos y asistente */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Columna izquierda: Gráficos (ocupa 2 espacios) */}
        <div className="lg:col-span-2 space-y-6">

          {/* Subgrid: radar de indicadores y comparación de empleo */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Perfil de Indicadores en Radar */}
            <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <h3 className="text-sm font-bold text-slate-800">
                  Perfil de Indicadores
                </h3>
              </div>
              <div className="h-[200px] mt-4 flex items-center justify-center w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" tick={{ fontSize: 9, fill: "#475569" }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 8 }} />
                    <Radar
                      name={displayName}
                      dataKey="A"
                      stroke="#2563eb"
                      fill="#3b82f6"
                      fillOpacity={0.2}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Indicador comparado con otras regiones (dinámico) */}
            <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                <h3 className="text-sm font-bold text-slate-800">
                  {currentTabConfig.title}
                </h3>
              </div>
              <div className="flex-1 space-y-2.5 overflow-y-auto max-h-[200px] pr-1">
                {allRegionsForComparison.map((item, idx) => {
                  const isCurrent = item.id.toUpperCase() === clusterName?.toUpperCase();
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
                          {item.value}{currentTabConfig.displaySuffix}
                        </span>
                      </div>
                      <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${isCurrent ? "bg-blue-600" : "bg-slate-300"}`}
                          style={{ width: `${item.value}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Fila de resumen de programas */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-slate-800">
              Resumen de Programas — {displayName}
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Tarjeta Formaciones */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <h4 className="text-2xl font-bold text-slate-850">{programCounts.courses}</h4>
                  <p className="text-[10px] text-slate-500 font-semibold mt-0.5">Programas de Formación</p>
                </div>
                <div className="w-9 h-9 rounded-xl bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center">
                  <BookOpen className="w-4.5 h-4.5" />
                </div>
              </div>

              {/* Tarjeta Mentorías */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <h4 className="text-2xl font-bold text-slate-850">{programCounts.mentorings}</h4>
                  <p className="text-[10px] text-slate-500 font-semibold mt-0.5">Mentorías Activas</p>
                </div>
                <div className="w-9 h-9 rounded-xl bg-purple-50 border border-purple-100 text-purple-600 flex items-center justify-center">
                  <GraduationCap className="w-4.5 h-4.5" />
                </div>
              </div>

              {/* Tarjeta Experiencias */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <h4 className="text-2xl font-bold text-slate-850">{programCounts.experiences}</h4>
                  <p className="text-[10px] text-slate-500 font-semibold mt-0.5">Experiencias</p>
                </div>
                <div className="w-9 h-9 rounded-xl bg-yellow-50 border border-yellow-100 text-yellow-600 flex items-center justify-center">
                  <Star className="w-4.5 h-4.5" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Columna derecha: Asistente IA interactivo */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between min-h-[450px]">
          <div className="flex flex-col h-full w-full justify-between flex-1">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-slate-100 pb-3 flex-shrink-0">
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

            {/* Chat Messages Log */}
            <div ref={chatContainerRef} className="flex-1 overflow-y-auto my-4 space-y-4 pr-1 text-xs min-h-[180px] max-h-[300px]">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex gap-2.5 items-start ${
                    msg.sender === "user" ? "flex-row-reverse" : ""
                  }`}
                >
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center font-bold text-[10px] shrink-0 ${
                      msg.sender === "user"
                        ? "bg-slate-200 text-slate-700"
                        : "bg-[#2563eb] text-white"
                    }`}
                  >
                    {msg.sender === "user" ? "Tú" : <Bot className="w-3.5 h-3.5" />}
                  </div>
                  <div
                    className={`rounded-xl p-3 border leading-relaxed max-w-[80%] ${
                      msg.sender === "user"
                        ? "bg-blue-600 text-white border-blue-600"
                        : "bg-slate-50 text-slate-700 border-slate-150"
                    }`}
                  >
                    <p className="whitespace-pre-line">{msg.text}</p>
                  </div>
                </div>
              ))}

              {aiMutation.isPending && (
                <div className="flex gap-2.5 items-start">
                  <div className="w-7 h-7 rounded-full bg-[#2563eb] text-white flex items-center justify-center shrink-0">
                    <Bot className="w-3.5 h-3.5" />
                  </div>
                  <div className="bg-slate-50 text-slate-500 border border-slate-100 rounded-xl p-3 flex items-center gap-1.5">
                    <Loader2 className="w-3 h-3 animate-spin text-blue-600" />
                    <span>IA escribiendo...</span>
                  </div>
                </div>
              )}
            </div>

            {/* Sugerencias estáticas */}
            {messages.length === 1 && !aiMutation.isPending && (
              <div className="space-y-2 mb-4 flex-shrink-0">
                <button
                  onClick={() => handleSendMessage(`¿Qué alertas críticas hay activas en la Región ${clusterName}?`)}
                  className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2 rounded-lg font-medium shadow-2xs transition-colors cursor-pointer leading-tight truncate"
                >
                  ¿Qué alertas críticas hay activas en la Región {clusterName}?
                </button>
                <button
                  onClick={() => handleSendMessage(`¿Dónde faltan programas de formación en la Región ${clusterName}?`)}
                  className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2 rounded-lg font-medium shadow-2xs transition-colors cursor-pointer leading-tight truncate"
                >
                  ¿Dónde faltan programas de formación en la Región {clusterName}?
                </button>
                <button
                  onClick={() => handleSendMessage(`¿Qué zonas de la Región ${clusterName} son prioridad para inversión social?`)}
                  className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2 rounded-lg font-medium shadow-2xs transition-colors cursor-pointer leading-tight truncate"
                >
                  ¿Qué zonas son prioridad para inversión social?
                </button>
                <button
                  onClick={() => handleSendMessage(`¿Cómo impacta la conectividad en la salud mental de la Región ${clusterName}?`)}
                  className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2 rounded-lg font-medium shadow-2xs transition-colors cursor-pointer leading-tight truncate"
                >
                  ¿Cómo impacta la conectividad en la salud mental?
                </button>
              </div>
            )}

            {/* AI Chat Input */}
            <div className="mt-auto flex-shrink-0 pt-2 border-t border-slate-100">
              <div className="relative w-full">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                  placeholder="Haga una pregunta sobre los datos de la región..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-3 pr-10 py-2.5 text-xs focus:outline-none focus:border-blue-500"
                  disabled={aiMutation.isPending}
                />
                <button
                  onClick={() => handleSendMessage()}
                  disabled={aiMutation.isPending}
                  className="absolute right-1.5 top-1/2 -translate-y-1/2 w-7 h-7 text-blue-600 hover:text-blue-800 hover:bg-blue-50 flex items-center justify-center rounded-md cursor-pointer transition-colors disabled:opacity-50"
                >
                  <Send className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ClusterDetailPage;
