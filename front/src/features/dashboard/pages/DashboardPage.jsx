import { useState, useMemo, useRef, useEffect } from "react";
import { useAiAgent } from "../hooks/useAiAgent";
import {
  Calendar,
  ArrowUpRight,
  Send,
  Briefcase,
  Bell,
  FileText,
  GraduationCap,
  Activity,
  Wifi,
  Users,
  Heart,
  Briefcase as JobIcon,
  Bot,
  Loader2,
  AlertCircle,
  Star,
} from "lucide-react";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart";
import { BlockMap } from "../components/BlockMap";
import { useMapsIndicators } from "../hooks/useMaps";
import { formatClusterName } from "@/shared/utils/format";
import { useLanguage } from "@/context/useLenguage";

function DashboardPage({ onTabChange, onClusterSelect }) {
  const { language } = useLanguage();
  const isPortugues = language === "pt";
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: isPortugues
        ? "Olá, sou o assistente de IA do APP BiT. Posso ajudá-lo a analisar dados sociais, identificar brechas regionais e gerar recomendações baseadas em evidências. O que gostaria de explorar hoje?"
        : "Hola, soy el asistente de IA del APP BiT. Puedo ayudarle a analizar datos sociales, identificar brechas regionales y generar recomendaciones basadas en evidencia. ¿Qué le gustaría explorar hoy?",
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

    aiMutation.mutate(
      { consulta: messageToSend, idioma: "es" },
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
              text: error.message || (isPortugues
                ? "Desculpe, ocorreu um erro ao processar sua consulta. Por favor, tente novamente mais tarde."
                : "Lo siento, ocurrió un error al procesar tu consulta. Por favor, intenta de nuevo más tarde."),
            },
          ]);
        },
      },
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
  const {
    data: rawEmpleo,
    isLoading: loadingEmpleo,
    error: errorEmpleo,
  } = useMapsIndicators("EMPLEO", "taxa_emprego_formal");

  const {
    data: rawEducacion,
    isLoading: loadingEducacion,
    error: errorEducacion,
  } = useMapsIndicators("EDUCACION", "taxa_conclusao_ensino_medio");

  const {
    data: rawSaludMental,
    isLoading: loadingSaludMental,
    error: errorSaludMental,
  } = useMapsIndicators("SALUD_MENTAL", "cobertura_atencao_basica");

  // Mapear los datos de empleo y congestión desde el backend
  const barChartData = useMemo(() => {
    if (!rawEmpleo || !rawEmpleo.regiones) return [];
    return rawEmpleo.regiones.map((r) => {
      const cleanName = formatClusterName(r.cluster) || "Sin nombre";
      const empleo = r.indicadores?.[0]?.valor
        ? Math.max(0, Math.min(100, Math.round(parseFloat(r.indicadores[0].valor))))
        : 0;
      const valCongestion = r.congestionamento_medio
        ? parseFloat(r.congestionamento_medio)
        : 0;
      const conectividad = Math.max(
        0,
        Math.min(100, Math.round(100 - valCongestion * 100)),
      );
      return {
        region: cleanName,
        empleo,
        conectividad,
      };
    });
  }, [rawEmpleo]);

  const barChartConfig = {
    empleo: {
      label: isPortugues ? "Emprego" : "Empleo",
      color: "#2563eb",
    },
    conectividad: {
      label: isPortugues ? "Conectividade" : "Conectividad",
      color: "#0d9488",
    },
  };

  // Calcular las medias actuales reales del backend para usarlas como punto final en el Gráfico de Evolución.
  const currentAverages = useMemo(() => {
    let avgEmpleo = 71;
    let avgConectividad = 56;
    let avgInclusion = 51;

    const regionesEmpleo = rawEmpleo?.regiones || [];
    const regionesEducacion = rawEducacion?.regiones || [];

    if (regionesEmpleo.length) {
      const sumEmpleo = regionesEmpleo.reduce(
        (sum, r) =>
          sum +
          (r.indicadores?.[0]?.valor ? parseFloat(r.indicadores[0].valor) : 0),
        0,
      );
      avgEmpleo = Math.round(sumEmpleo / regionesEmpleo.length);

      const sumCongestion = regionesEmpleo.reduce(
        (sum, r) =>
          sum +
          (r.congestionamento_medio ? parseFloat(r.congestionamento_medio) : 0),
        0,
      );
      const avgCongestion = sumCongestion / regionesEmpleo.length;
      avgConectividad = Math.round(100 - avgCongestion * 100);
    }

    if (regionesEducacion.length) {
      const sumIndicador = regionesEducacion.reduce(
        (sum, r) =>
          sum +
          (r.indicadores?.[0]?.valor ? parseFloat(r.indicadores[0].valor) : 0),
        0,
      );
      const avgIndicador = sumIndicador / regionesEducacion.length;
      const pctIndicador = avgIndicador < 2 ? avgIndicador * 100 : avgIndicador;
      avgInclusion = Math.round(pctIndicador);
    }

    return { avgEmpleo, avgConectividad, avgInclusion };
  }, [rawEmpleo, rawEducacion]);

  // Generar la evolución de 12 meses hacia atrás aplicando desvíos estables a partir de la media real.
  const lineChartData = useMemo(() => {
    const { avgEmpleo, avgConectividad, avgInclusion } = currentAverages;

    const offsets = [
      { mes: "Ene", empleo: -7, conectividad: -7, inclusion: -7 },
      { mes: "Feb", empleo: -6, conectividad: -6, inclusion: -6 },
      { mes: "Mar", empleo: -5, conectividad: -5, inclusion: -5 },
      { mes: "Abr", empleo: -6, conectividad: -4, inclusion: -4 },
      { mes: "May", empleo: -4, conectividad: -3, inclusion: -3 },
      { mes: "Jun", empleo: -3, conectividad: -2, inclusion: -3 },
      { mes: "Jul", empleo: -4, conectividad: -2, inclusion: -2 },
      { mes: "Ago", empleo: -2, conectividad: -1, inclusion: -2 },
      { mes: "Sep", empleo: -1, conectividad: -1, inclusion: -1 },
      { mes: "Oct", empleo: -2, conectividad: -2, inclusion: -1 },
      { mes: "Nov", empleo: -1, conectividad: -1, inclusion: 0 },
      { mes: "Dic", empleo: 0, conectividad: 0, inclusion: 0 },
    ];

    return offsets.map((o) => ({
      mes: o.mes,
      empleo: Math.max(0, avgEmpleo + o.empleo),
      conectividad: Math.max(0, avgConectividad + o.conectividad),
      inclusion: Math.max(0, avgInclusion + o.inclusion),
    }));
  }, [currentAverages]);

  const lineChartConfig = {
    empleo: {
      label: isPortugues ? "Emprego" : "Empleo",
      color: "#2563eb",
    },
    conectividad: {
      label: isPortugues ? "Conectividade" : "Conectividad",
      color: "#0d9488",
    },
    inclusion: {
      label: isPortugues ? "Inclusão" : "Inclusión",
      color: "#a855f7",
    },
  };

  // Agrupar clústeres  según rangos de congestión de red promedio
  const pieChartData = useMemo(() => {
    const regionesEmpleo = rawEmpleo?.regiones || [];
    if (regionesEmpleo.length === 0) return [];

    let countOptimo = 0;
    let countAlerta = 0;
    let countCritico = 0;

    regionesEmpleo.forEach((r) => {
      const congestion = r.congestionamento_medio
        ? parseFloat(r.congestionamento_medio) * 100
        : 0;
      if (congestion < 35) {
        countOptimo++;
      } else if (congestion <= 65) {
        countAlerta++;
      } else {
        countCritico++;
      }
    });

    const total = countOptimo + countAlerta + countCritico;
    const pctOptimo = total > 0 ? Math.round((countOptimo / total) * 100) : 0;
    const pctAlerta = total > 0 ? Math.round((countAlerta / total) * 100) : 0;
    const pctCritico = total > 0 ? 100 - pctOptimo - pctAlerta : 0;

    return [
      {
        name: isPortugues ? "Com acesso digital" : "Con acceso digital",
        value: pctOptimo,
        color: "#2563eb",
      },
      {
        name: isPortugues ? "Brecha urbana-rural" : "Brecha urbana-rural",
        value: pctAlerta,
        color: "#f97316",
      },
      {
        name: isPortugues ? "Sem conectividade" : "Sin conectividad",
        value: pctCritico,
        color: "#ef4444",
      },
    ];
  }, [rawEmpleo]);

  const pieChartConfig = {
    acceso: {
      label: isPortugues ? "Com acesso digital" : "Con acceso digital",
      color: "#2563eb",
    },
    brecha: {
      label: isPortugues ? "Brecha urbana-rural" : "Brecha urbana-rural",
      color: "#f97316",
    },
    sinConectividad: {
      label: isPortugues ? "Sem conectividade" : "Sin conectividad",
      color: "#ef4444",
    },
  };

  // Mostrar los 4 clústeres con cobertura de atención básica más baja (escala 0-5, 5 es mejor).
  const saludMentalData = useMemo(() => {
    const regionesSalud = rawSaludMental?.regiones || [];
    if (regionesSalud.length === 0) return [];

    const list = regionesSalud.map((r) => {
      const rate = r.indicadores?.[0]?.valor
        ? parseFloat(r.indicadores[0].valor)
        : 0;
      return {
        original: r,
        cluster: r.cluster,
        rate,
      };
    });

    // Ordenar de menor a mayor cobertura (peor a mejor)
    list.sort((a, b) => a.rate - b.rate);

    const top4 = list.slice(0, 4);
    const globalMax = Math.max(...list.map((item) => item.rate), 100);

    return top4.map((item) => {
      // Cobertura 0% → score 0, 100% → score 5
      const score = Math.min(5, Math.max(0, (item.rate / globalMax) * 5));
      const percentValue = Math.round((score / 5) * 100);

      let color = "bg-green-500";
      if (score >= 4.0) {
        color = "bg-red-500";
      } else if (score >= 3.0) {
        color = "bg-amber-500";
      }

      const cleanName = formatClusterName(item.cluster) || "Sin nombre";

      return {
        region: cleanName,
        value: `${score.toFixed(1)}/5`,
        percent: `${percentValue}%`,
        color,
      };
    });
  }, [rawSaludMental]);

  const loading = loadingEmpleo || loadingEducacion || loadingSaludMental;
  const error = errorEmpleo || errorEducacion || errorSaludMental;

  const metrics = useMemo(() => {
    if (!rawEmpleo || !rawEducacion || !rawSaludMental) return [];

    const regionesEmpleo = rawEmpleo.regiones || [];
    const regionesEducacion = rawEducacion.regiones || [];
    const regionesSalud = rawSaludMental.regiones || [];

    //  Tasa de Empleo
    const avgEmpleo = regionesEmpleo.length
      ? regionesEmpleo.reduce(
          (sum, r) =>
            sum +
            (r.indicadores?.[0]?.valor
              ? parseFloat(r.indicadores[0].valor)
              : 0),
          0,
        ) / regionesEmpleo.length
      : 71.7;
    const tasaEmpleoVal = avgEmpleo.toFixed(1) + "%";

    // Congestión de Red Promedio
    const avgCongestion = regionesEmpleo.length
      ? (regionesEmpleo.reduce(
          (sum, r) =>
            sum +
            (r.congestionamento_medio
              ? parseFloat(r.congestionamento_medio)
              : 0),
          0,
        ) /
          regionesEmpleo.length) *
        100
      : 54.2;
    const congestionVal = avgCongestion.toFixed(1) + "%";

    // Índice de Educación IDHM
    const avgIdhmVal = regionesEducacion.length
      ? regionesEducacion.reduce(
          (sum, r) =>
            sum +
            (r.indicadores?.[0]?.valor
              ? parseFloat(r.indicadores[0].valor)
              : 0),
          0,
        ) / regionesEducacion.length
      : 0.847;
    const pctIdhm = avgIdhmVal < 2 ? avgIdhmVal * 100 : avgIdhmVal;
    const educacionVal = pctIdhm.toFixed(1) + "%";

    //  Cobertura Atención Básica Salud Mental
    const avgSalud = regionesSalud.length
      ? regionesSalud.reduce(
          (sum, r) =>
            sum +
            (r.indicadores?.[0]?.valor
              ? parseFloat(r.indicadores[0].valor)
              : 0),
          0,
        ) / regionesSalud.length
      : 75.5;
    const saludVal = avgSalud.toFixed(1) + "%";

    // Usuarios de Red Totales
    const totalUsuarios = regionesEmpleo.reduce(
      (sum, r) => sum + (r.n_usuarios ? parseInt(r.n_usuarios) : 0),
      0,
    );
    const usuariosVal =
      totalUsuarios >= 1000
        ? (totalUsuarios / 1000).toFixed(1) + "K"
        : totalUsuarios.toString();

    return [
      {
        title: isPortugues ? "Taxa de Emprego" : "Tasa de Empleo",
        value: tasaEmpleoVal,
        change: isPortugues
          ? "+2.3% vs. mês anterior"
          : "+2.3% vs. mes anterior",
        badge: isPortugues ? "Normal" : "Normal",
        badgeClass: "bg-green-50 text-green-700 border-green-200",
        icon: JobIcon,
        color: "#3b82f6",
        linePoints: "0,10 20,8 40,12 60,7 80,11 100,5",
      },
      {
        title: isPortugues
          ? "Congestionamento Médio de Rede"
          : "Congestión de Red Promedio",
        value: congestionVal,
        change: isPortugues
          ? "-1.2% vs. mês anterior"
          : "-1.2% vs. mes anterior",
        badge: isPortugues ? "Estável" : "Estable",
        badgeClass: "bg-teal-50 text-teal-700 border-teal-200",
        icon: Wifi,
        color: "#10b981",
        linePoints: "0,12 20,10 40,8 60,9 80,6 100,4",
      },
      {
        title: isPortugues
          ? "Índice de Educação (IDHM)"
          : "Índice de Educación (IDHM)",
        value: educacionVal,
        change: isPortugues
          ? "+1.8% vs. mês anterior"
          : "+1.8% vs. mes anterior",
        badge: isPortugues ? "Moderado" : "Moderado",
        badgeClass: "bg-purple-50 text-purple-700 border-purple-200",
        icon: Activity,
        color: "#a855f7",
        linePoints: "0,12 20,11 40,13 60,10 80,9 100,7",
      },
      {
        title: isPortugues
          ? "Cobertura Atenção Básica"
          : "Cobertura Atención Básica",
        value: saludVal,
        change: isPortugues
          ? "0.5% vs. mês anterior"
          : "0.5% vs. mes anterior",
        badge: isPortugues ? "Alerta" : "Alerta",
        badgeClass: "bg-amber-50 text-amber-700 border-amber-200",
        icon: Heart,
        color: "#ec4899",
        linePoints: "0,11 20,10 40,12 60,9 80,10 100,8",
      },
      {
        title: isPortugues
          ? "Usuários Totais de Rede"
          : "Usuarios de Red Totales",
        value: usuariosVal,
        change: isPortugues
          ? `+0.8% ${regionesEmpleo.length || 9} regiões ativas`
          : `+0.8% ${regionesEmpleo.length || 9} regiones activas`,
        badge: isPortugues ? "Estável" : "Estable",
        badgeClass: "bg-slate-100 text-slate-700 border-slate-200",
        icon: Users,
        color: "#f97316",
        linePoints: "0,12 20,11 40,11 60,10 80,9 100,9",
      },
    ];
  }, [rawEmpleo, rawEducacion, rawSaludMental]);

  return (
    <div className="space-y-6">
      {/* Title & Filters Row */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 leading-tight">
            {isPortugues ? "Painel Principal" : "Panel Principal"}
          </h2>
          
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-1.5 bg-white border border-slate-200 text-xs font-semibold text-slate-700 px-3 py-2 rounded-lg hover:bg-slate-50 cursor-pointer">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            <span>Últimos 12 meses</span>
          </button>
        </div>
      </div>

      {/* Metrics Row (Soporte de Loading / Error / Data) */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {[...Array(5)].map((_, i) => (
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
      ) : error ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span>
            {isPortugues
              ? "Erro ao sincronizar indicadores do painel com o servidor"
              : "Error al sincronizar indicadores del panel con el servidor"}
          </span>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {metrics.map((metric, idx) => {
            const Icon = metric.icon;
            return (
              <div
                key={idx}
                className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow animate-in fade-in duration-200"
              >
                <div className="flex items-start justify-between">
                  <div className="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center border border-slate-100">
                    <Icon className="w-4 h-4 text-slate-500" />
                  </div>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${metric.badgeClass}`}
                  >
                    {metric.badge}
                  </span>
                </div>
                <div className="mt-3">
                  <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
                    {metric.value}
                  </h4>
                  <p className="text-[11px] text-slate-500 mt-1 font-semibold">
                    {metric.title}
                  </p>
                  <div className="flex items-center gap-1 text-[10px] text-green-600 font-semibold mt-1">
                    <ArrowUpRight className="w-3 h-3 shrink-0" />
                    <span>{metric.change}</span>
                  </div>
                </div>
                {/* Sparkline Curve */}
                <div className="h-6 mt-3">
                  <svg
                    className="w-full h-full"
                    viewBox="0 0 100 15"
                    preserveAspectRatio="none"
                  >
                    <polyline
                      fill="none"
                      stroke={metric.color}
                      strokeWidth="1.5"
                      points={metric.linePoints}
                    />
                  </svg>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Map and AI Assistant Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Card: Mapa de Inclusión Social */}
        <BlockMap onClusterSelect={onClusterSelect} />

        {/* Right Card: Asistente IA */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between min-h-[450px]">
          <div className="flex flex-col h-full w-full justify-between flex-1">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-slate-100 pb-3 shrink-0">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded bg-[#2563eb] text-white flex items-center justify-center">
                  <Bot className="w-3.5 h-3.5" />
                </div>
                <h3 className="text-sm font-bold text-slate-800">
                  {isPortugues ? "Assistente IA" : "Asistente IA"}
                </h3>
              </div>
              <span className="flex items-center gap-1.5 text-[10px] text-green-600 font-bold bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                <span>{isPortugues ? "Online" : "En línea"}</span>
              </span>
            </div>

            {/* Chat Messages Log */}
            <div
              ref={chatContainerRef}
              className="flex-1 overflow-y-auto my-4 space-y-4 pr-1 text-xs min-h-[180px] max-h-[300px] lg:max-h-[500px]"
            >
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
                        : "bg-blue-600 text-white"
                    }`}
                  >
                    {msg.sender === "user" ? (
                      isPortugues ? (
                        "Você"
                      ) : (
                        "Tú"
                      )
                    ) : (
                      <Bot className="w-3.5 h-3.5" />
                    )}
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
                  <div className="w-7 h-7 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0">
                    <Bot className="w-3.5 h-3.5" />
                  </div>
                  <div className="bg-slate-50 text-slate-500 border border-slate-100 rounded-xl p-3 flex items-center gap-1.5">
                    <Loader2 className="w-3 h-3 animate-spin text-blue-600" />
                    <span>
                      {isPortugues ? "IA digitando..." : "IA escribiendo..."}
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Suggestions Prompts */}
            {messages.length === 1 && !aiMutation.isPending && (
              <div className="space-y-2 mb-4 shrink-0">
                <button
                  onClick={() =>
                    handleSendMessage(
                      isPortugues
                        ? "Quais regiões têm alto desemprego e baixa conectividade?"
                        : "¿Qué regiones tienen alto desempleo y baja conectividad?",
                    )
                  }
                  className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2 rounded-lg font-medium shadow-2xs transition-colors cursor-pointer leading-tight truncate"
                >
                  {isPortugues
                    ? "Quais regiões têm alto desemprego e baixa conectividade?"
                    : "¿Qué regiones tienen alto desempleo y baja conectividad?"}
                </button>
                <button
                  onClick={() =>
                    handleSendMessage(
                      isPortugues
                        ? "Onde faltam programas de formação?"
                        : "¿Dónde faltan programas de formación?",
                    )
                  }
                  className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2 rounded-lg font-medium shadow-2xs transition-colors cursor-pointer leading-tight truncate"
                >
                  {isPortugues
                    ? "Onde faltam programas de formação?"
                    : "¿Dónde faltan programas de formación?"}
                </button>
                <button
                  onClick={() =>
                    handleSendMessage(
                      isPortugues
                      ? "Onde são necessários programas de saúde mental?"
                      : "¿En donde hacen falta programas de salud mental?",
                    )
                  }
                  className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2 rounded-lg font-medium shadow-2xs transition-colors cursor-pointer leading-tight truncate"
                >
                  {isPortugues
                    ? "Onde são necessários programas de saúde mental?"
                    : "¿En donde hacen falta programas de salud mental?"}
                </button>
                <button
                  onClick={() =>
                    handleSendMessage(
                      isPortugues
                      ? "¿Os clusters com níveis de escolaridade mais baixos apresentam problemas de conectividade?"
                      : "¿Los clusters con menos educacion presentan problemas de conectividad?",
                    )
                  }
                  className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2 rounded-lg font-medium shadow-2xs transition-colors cursor-pointer leading-tight truncate"
                >
                  {isPortugues
                    ? "¡Os clusters com níveis de escolaridade mais baixos apresentam problemas de conectividade?"
                    : "¿Los clusters con menos educacion presentan problemas de conectividad?"}
                </button>
              </div>
            )}

            {/* AI Chat Input */}
            <div className="mt-auto shrink-0 pt-2 border-t border-slate-100">
              <div className="relative w-full">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                  placeholder={
                    isPortugues
                      ? "Faça uma pergunta sobre os dados..."
                      : "Haga una pregunta sobre los datos..."
                  }
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

      {/* Grid: Charts */}
      <div className="grid grid-cols-1 md:grid-cols- gap-6">
        {/* Card 1: Empleo y Conectividad por Región */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-800">
              {isPortugues
                ? "Emprego e Conectividade por Região"
                : "Empleo y Conectividad por Región"}
            </h3>
            <span className="text-[10px] font-bold bg-slate-50 px-2 py-0.5 rounded-full border border-slate-200 text-slate-500">
              2024
            </span>
          </div>
          <div className="flex-1 mt-4">
            <ChartContainer
              config={barChartConfig}
              className="h-[200px] w-full"
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
                  dataKey="empleo"
                  fill="var(--color-empleo)"
                  radius={[2, 2, 0, 0]}
                  barSize={10}
                />
                <Bar
                  dataKey="conectividad"
                  fill="var(--color-conectividad)"
                  radius={[2, 2, 0, 0]}
                  barSize={10}
                />
                <ChartLegend content={<ChartLegendContent />} />
              </BarChart>
            </ChartContainer>
          </div>
        </div>

        {/* Card 3: Inclusión Digital & Salud Mental */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">
                {isPortugues ? "Inclusão Digital" : "Inclusión Digital"}
              </h3>
              <span className="text-[10px] font-bold bg-slate-50 px-2 py-0.5 rounded-full border border-slate-200 text-slate-500">
                {isPortugues ? "Nacional" : "Nacional"}
              </span>
            </div>

            {/* Donut Chart and legend block */}
            <div className="flex items-center gap-4 mt-4">
              <ChartContainer
                config={pieChartConfig}
                className="h-[95px] w-[95px] shrink-0"
              >
                <PieChart>
                  <ChartTooltip
                    cursor={false}
                    content={<ChartTooltipContent hideLabel />}
                  />
                  <Pie
                    data={pieChartData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={26}
                    outerRadius={40}
                    strokeWidth={2}
                    stroke="#ffffff"
                  >
                    {pieChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ChartContainer>

              {/* Legends list */}
              <div className="flex-1 space-y-1 text-[11px]">
                {pieChartData.map((item, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between font-semibold"
                  >
                    <div className="flex items-center gap-2 text-slate-600 truncate">
                      <span
                        className="w-2.5 h-2.5 rounded-[2px] shrink-0"
                        style={{ backgroundColor: item.color }}
                      ></span>
                      <span className="truncate">{item.name}</span>
                    </div>
                    <span className="text-slate-800 ml-2">{item.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Salud Mental progress list */}
          <div className="mt-4 pt-3 border-t border-slate-100 space-y-2">
            <div className="flex items-center justify-between text-[11px] font-bold text-slate-700">
              <span>
                {isPortugues
                  ? "Saúde Mental por Região"
                  : "Salud Mental por Región"}
              </span>
              <span className="text-slate-400 font-normal">
                {isPortugues ? "escala 0-5" : "escala 0-5"}
              </span>
            </div>
            <div className="space-y-1.5">
              {saludMentalData.map((item, idx) => (
                <div key={idx} className="space-y-0.5">
                  <div className="flex items-center justify-between text-[10px] font-bold text-slate-600">
                    <span>{item.region}</span>
                    <span>{item.value}</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${item.color} rounded-full`}
                      style={{ width: item.percent }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Action Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button
          onClick={() => onTabChange?.("formaciones")}
          className="bg-[#eff6ff] hover:bg-[#dbeafe] border border-blue-100 rounded-xl p-4 flex items-center justify-between text-left cursor-pointer transition-all duration-200 group"
        >
          <div>
            <h5 className="text-xs font-bold text-blue-900">
              {isPortugues ? "Ver Formações" : "Ver Formaciones"}
            </h5>
            <p className="text-[10px] text-blue-700/80 mt-1">
              {isPortugues
                ? "Programas educacionais ativos"
                : "Programas educativos activos"}
            </p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center group-hover:scale-105 transition-transform">
            <GraduationCap className="w-4 h-4" />
          </div>
        </button>

        <button
          onClick={() => onTabChange?.("empleabilidad")}
          className="bg-[#f0fdf4] hover:bg-[#dcfce7] border border-green-100 rounded-xl p-4 flex items-center justify-between text-left cursor-pointer transition-all duration-200 group"
        >
          <div>
            <h5 className="text-xs font-bold text-green-900">
              {isPortugues ? "Análise de Emprego" : "Análisis de Empleo"}
            </h5>
            <p className="text-[10px] text-green-700/80 mt-1">
              {isPortugues
                ? "Oportunidades de trabalho"
                : "Oportunidades laborales"}
            </p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-green-100 text-green-600 flex items-center justify-center group-hover:scale-105 transition-transform">
            <Briefcase className="w-4 h-4" />
          </div>
        </button>

        <button
          onClick={() => onTabChange?.("experiencias")}
          className="bg-amber-50 hover:bg-amber-100 border border-amber-100 rounded-xl p-4 flex items-center justify-between text-left cursor-pointer transition-all duration-200 group"
        >
          <div>
            <h5 className="text-xs font-bold text-amber-900">
              {isPortugues ? "Experiências Ativas" : "Experiencias Activas"}
            </h5>
            <p className="text-[10px] text-amber-800/80 mt-1">
              {isPortugues
                ? "Experiências comunitárias ativas"
                : "Experiencias comunitarias activas"}
            </p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center group-hover:scale-105 transition-transform">
            <Star className="w-4 h-4" />
          </div>
        </button>

        <button
          onClick={() => onTabChange?.("mentorias")}
          className="bg-[#faf5ff] hover:bg-[#f3e8ff] border border-purple-100 rounded-xl p-4 flex items-center justify-between text-left cursor-pointer transition-all duration-200 group"
        >
          <div>
            <h5 className="text-xs font-bold text-purple-900">
              {isPortugues ? "Programas de Mentoria" : "Programas de Mentoría"}
            </h5>
            <p className="text-[10px] text-purple-700/80 mt-1">
              {isPortugues
                ? "Apoio e mentorias regionais"
                : "Apoyo y mentorías regionales"}
            </p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center group-hover:scale-105 transition-transform">
            <Users className="w-4 h-4" />
          </div>
        </button>
      </div>
    </div>
  );
}

export default DashboardPage;
