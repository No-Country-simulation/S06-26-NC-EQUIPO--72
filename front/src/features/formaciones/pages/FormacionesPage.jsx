import { useState, useMemo, useRef, useEffect } from "react";
import {
  BookOpen,
  Users,
  Activity,
  AlertTriangle,
  Plus,
  Search,
  ChevronDown,
  MapPin,
  ChevronRight,
  CheckCircle,
  AlertCircle,
  XCircle,
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

// Importamos los hooks de React Query creados para conectarnos al backend
import {
  useFormacionesList,
  useFormacionesBrechas,
} from "../hooks/useFormaciones";

// Importamos el formulario de creación de nuevo programa
import NuevoProgramaForm from "../components/NuevoProgramaForm";
import { formatClusterName } from "@/shared/utils/format";
import {
  BarChartSkeleton,
  ProgramListSkeleton,
} from "../skeletons/FormacionesPageSkeleton";

// Lista de clústeres oficiales para el municipio de Florianópolis
const FLORI_CLUSTERS = [
  "AEROPORTO_HLZ",
  "CAMPECHE",
  "CANASVIEIRAS",
  "CBD_BEIRAMAR",
  "CENTRO_HISTORICO",
  "COQUEIROS",
  "ESTREITO_CAPOEIRAS",
  "INGLESES",
  "JURERE",
  "LAGOA_CONCEICAO",
  "NORTE_ILHA",
  "RESIDENCIAL_NORTE",
  "SC401_CORREDOR",
  "TRINDADE",
  "UFSC",
  "VIA_EXPRESSA_CORREDOR",
];

// Configuración de colores y etiquetas para el gráfico de barras
const barChartConfig = {
  programas: {
    label: "Programas",
    color: "#2563eb",
  },
  cobertura: {
    label: "Cobertura %",
    color: "#0d9488",
  },
};

// Configuración de colores y etiquetas para el gráfico de torta (Categorías)
const pieChartConfig = {
  digital: {
    label: "Formación Digital",
    color: "#2563eb",
  },
  tecnica: {
    label: "Formación Técnica",
    color: "#0d9488",
  },
  emprendimiento: {
    label: "Emprendimiento",
    color: "#a855f7",
  },
  idiomas: {
    label: "Idiomas",
    color: "#f97316",
  },
  otros: {
    label: "Otros",
    color: "#64748b",
  },
};

/**
 * Función de utilidad determinista para generar datos de clúster territoriales.
 * Si el clúster existe en la respuesta del backend (`/brechas`), usará sus datos.
 * Si no está sembrado, generará valores estables y coherentes basados en un hash
 * del nombre del clúster para que la interfaz se muestre siempre completa y estética.
 *
 * @param {string} clusterName - Nombre del clúster territorial
 * @param {Array} brechasList - Listado de brechas devuelto por el backend
 */
const getClusterData = (clusterName, brechasList) => {
  // Buscamos si el clúster existe en los datos reales del backend
  const realMatch = brechasList?.find(
    (b) => b.cluster.toUpperCase() === clusterName.toUpperCase(),
  );

  if (realMatch) {
    const coverageVal = realMatch.indicador_social?.valor
      ? parseFloat(realMatch.indicador_social.valor)
      : 0;
    const pct = coverageVal < 2 ? coverageVal * 100 : coverageVal;

    return {
      nUsuarios: realMatch.n_usuarios || 0,
      cobertura: Math.round(pct),
      programasActivos: realMatch.programas_activos || 0,
      severidad: realMatch.severidad_brecha || null,
    };
  }

  return {
    nUsuarios: null,
    cobertura: null,
    programasActivos: 0,
    severidad: null,
  };
};

function FormacionesPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("Todos");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Estado para controlar la visibilidad del modal para crear un programa
  const [isFormOpen, setIsFormOpen] = useState(false);

  // 1. Petición al endpoint /programas?size=100&tipo=FORMACION
  const {
    data: rawProgramas,
    isLoading: loadingPrograms,
    error: errorPrograms,
  } = useFormacionesList();

  // 2. Petición al endpoint /brechas?servicio=FORMACION
  const {
    data: rawBrechas,
    isLoading: loadingBrechas,
    error: errorBrechas,
  } = useFormacionesBrechas();

  // Cerrar el dropdown del filtro de estados cuando se hace clic afuera
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // 3. Procesamiento y mapeo de la lista de programas
  const programList = useMemo(() => {
    if (!rawProgramas) return [];

    return rawProgramas.map((prog) => {
      // Para cada programa del backend, consultamos los datos del territorio (clúster)
      const territorial = getClusterData(prog.cluster, rawBrechas?.brechas);

      const isActivo = prog.activo !== undefined ? prog.activo : true;

      let estado = "Activo";
      if (!isActivo) {
        estado = "Crítico"; // Inactivo/crítico
      } else if (territorial.cobertura !== null && territorial.cobertura !== undefined) {
        if (territorial.cobertura < 40) {
          estado = "Crítico"; // Cobertura muy baja
        } else if (territorial.cobertura < 70) {
          estado = "Alerta"; // Cobertura intermedia
        }
      }

      return {
        id: prog.id,
        nombre: prog.nombre,
        region: prog.cluster,
        beneficiarios: territorial.nUsuarios !== null && territorial.nUsuarios !== undefined
          ? territorial.nUsuarios.toLocaleString("es-ES")
          : "-",
        beneficiariosRaw: territorial.nUsuarios,
        cobertura: territorial.cobertura,
        estado: estado,
        activo: isActivo,
      };
    });
  }, [rawProgramas, rawBrechas]);

  // 4. Filtrado en memoria de programas por término de búsqueda y estado
  const filteredPrograms = useMemo(() => {
    return programList.filter((program) => {
      const matchesSearch =
        program.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        program.region.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesStatus =
        statusFilter === "Todos" ||
        program.estado.toLowerCase() === statusFilter.toLowerCase();

      return matchesSearch && matchesStatus;
    });
  }, [programList, searchTerm, statusFilter]);

  // 5. Cálculo dinámico de indicadores superiores (KPIs)
  const kpis = useMemo(() => {
    const totalProgramas = programList.length;
    const activos = programList.filter((p) => p.activo).length;

    const beneficiariosTotales = rawBrechas?.brechas?.reduce((sum, b) => {
      return sum + (b.n_usuarios || 0);
    }, 0) || 0;

    // Formateamos los beneficiarios (ej: 145000 -> 145K)
    const beneficiariosFormateados =
      beneficiariosTotales >= 1000
        ? Math.round(beneficiariosTotales / 1000) + "K"
        : beneficiariosTotales;

    const brechasValidas = rawBrechas?.brechas?.filter((b) => b.indicador_social?.valor !== undefined) || [];
    const totalCobertura = brechasValidas.reduce((sum, b) => {
      const val = parseFloat(b.indicador_social.valor);
      const pct = val < 2 ? val * 100 : val;
      return sum + pct;
    }, 0);
    const coberturaMedia = brechasValidas.length
      ? Math.round(totalCobertura / brechasValidas.length)
      : 0;

    const regionesConBrecha = brechasValidas.filter((b) => {
      const val = parseFloat(b.indicador_social.valor);
      const pct = val < 2 ? val * 100 : val;
      return pct < 50;
    }).length;

    return {
      activosText: `${activos} de ${totalProgramas} totales`,
      activosCount: activos,
      beneficiarios: beneficiariosFormateados,
      cobertura: `${coberturaMedia}%`,
      regionesBrechaText: `${regionesConBrecha} de ${rawBrechas?.brechas?.length || 0} registradas`,
      regionesBrechaCount: regionesConBrecha,
    };
  }, [programList, rawBrechas]);

  const barChartData = useMemo(() => {
    return FLORI_CLUSTERS.map((c) => {
      const count = programList.filter(
        (p) => p.region.toUpperCase() === c.toUpperCase(),
      ).length;

      const clusterInfo = getClusterData(c, rawBrechas?.brechas);

      return {
        region: formatClusterName(c),
        programas: count,
        cobertura: clusterInfo.cobertura,
      };
    }).filter(
      (d) => d.programas > 0 || (d.cobertura !== null && d.cobertura !== undefined)
    );
  }, [programList, rawBrechas]);

  // 7. Categorización del gráfico de torta en base a palabras clave de los programas activos
  const pieChartData = useMemo(() => {
    let digital = 0;
    let tecnica = 0;
    let emprendimiento = 0;
    let idiomas = 0;
    let otros = 0;

    programList.forEach((p) => {
      const name = p.nombre.toLowerCase();
      // Clasificación semántica por nombre del programa
      if (
        name.includes("digital") ||
        name.includes("programacion") ||
        name.includes("python") ||
        name.includes("web") ||
        name.includes("ux/ui") ||
        name.includes("tecnologias")
      ) {
        digital++;
      } else if (
        name.includes("tecnica") ||
        name.includes("iot") ||
        name.includes("agroindustrial")
      ) {
        tecnica++;
      } else if (
        name.includes("emprendedor") ||
        name.includes("innovacion") ||
        name.includes("negocios") ||
        name.includes("marketing")
      ) {
        emprendimiento++;
      } else if (name.includes("ingles") || name.includes("idiomas")) {
        idiomas++;
      } else {
        otros++;
      }
    });

    const total = digital + tecnica + emprendimiento + idiomas + otros || 1;

    return [
      {
        name: "Formación Digital",
        value: Math.round((digital / total) * 100),
        color: "#2563eb",
      },
      {
        name: "Formación Técnica",
        value: Math.round((tecnica / total) * 100),
        color: "#0d9488",
      },
      {
        name: "Emprendimiento",
        value: Math.round((emprendimiento / total) * 100),
        color: "#a855f7",
      },
      {
        name: "Idiomas",
        value: Math.round((idiomas / total) * 100),
        color: "#f97316",
      },
      {
        name: "Otros",
        value: Math.round((otros / total) * 100),
        color: "#64748b",
      },
    ];
  }, [programList]);

  // Selección de colores para las barras de progreso del listado
  const getCoverageColors = (val) => {
    if (val === null || val === undefined) return { text: "text-slate-400", bar: "bg-slate-200" };
    if (val >= 70) return { text: "text-green-600", bar: "bg-green-500" };
    if (val >= 40) return { text: "text-amber-600", bar: "bg-amber-500" };
    return { text: "text-red-600", bar: "bg-red-500" };
  };

  // Selector de etiquetas de estado
  const getStatusBadge = (estado) => {
    switch (estado) {
      case "Activo":
        return (
          <span className="inline-flex items-center gap-1 bg-green-50 text-green-700 border border-green-200 px-2.5 py-0.5 rounded-full text-xs font-semibold">
            <CheckCircle className="w-3.5 h-3.5 text-green-600" />
            <span>Activo</span>
          </span>
        );
      case "Alerta":
        return (
          <span className="inline-flex items-center gap-1 bg-amber-50 text-amber-700 border border-amber-200 px-2.5 py-0.5 rounded-full text-xs font-semibold">
            <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
            <span>Alerta</span>
          </span>
        );
      case "Crítico":
        return (
          <span className="inline-flex items-center gap-1 bg-red-50 text-red-700 border border-red-200 px-2.5 py-0.5 rounded-full text-xs font-semibold">
            <XCircle className="w-3.5 h-3.5 text-red-600" />
            <span>Crítico</span>
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Cabecera de la página */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-600" />
            <span>Programas de Formación</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Cobertura de formación y capacitación por clústeres en Florianópolis
          </p>
        </div>
        <div>
          <button
            onClick={() => setIsFormOpen(true)}
            className="flex items-center gap-1.5 bg-[#2563eb] hover:bg-blue-600 text-white font-medium text-xs px-4 py-2.5 rounded-lg transition-colors cursor-pointer shadow-sm"
          >
            <Plus className="w-4 h-4" />
            <span>Nuevo programa</span>
          </button>
        </div>
      </div>

      {/* Fila de Tarjetas de Indicadores Superiores (KPIs) */}
      {loadingPrograms || loadingBrechas ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
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
      ) : errorPrograms || errorBrechas ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span>
            Error al sincronizar indicadores del panel de formaciones con el
            servidor
          </span>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Tarjeta 1: Programas Activos */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div className="flex items-center justify-between">
              <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center border border-emerald-100 text-emerald-600">
                <BookOpen className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="flex items-baseline gap-1.5">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {kpis.activosCount}
                </span>
                <span className="text-[10px] text-slate-400 font-bold uppercase">
                  {kpis.activosText}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1 font-semibold">
                Programas Activos
              </p>
            </div>
          </div>

          {/* Tarjeta 2: Beneficiarios Totales */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div className="flex items-center justify-between">
              <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center border border-blue-100 text-blue-600">
                <Users className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="flex items-baseline gap-1.5">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {kpis.beneficiarios}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1 font-semibold">
                Beneficiarios Totales
              </p>
            </div>
          </div>

          {/* Tarjeta 3: Cobertura Media */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div className="flex items-center justify-between">
              <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center border border-teal-100 text-teal-600">
                <Activity className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="flex items-baseline gap-1.5">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {kpis.cobertura}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1 font-semibold">
                Cobertura Media
              </p>
            </div>
          </div>

          {/* Tarjeta 4: Regiones con Brecha */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div className="flex items-center justify-between">
              <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center border border-amber-100 text-amber-600">
                <AlertTriangle className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="flex items-baseline gap-1.5">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {kpis.regionesBrechaCount}
                </span>
                <span className="text-[10px] text-slate-400 font-bold uppercase">
                  {kpis.regionesBrechaText}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1 font-semibold">
                Regiones con Brecha
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Grid de Visualizaciones y Gráficos */}
      {loadingPrograms || loadingBrechas ? (
        <BarChartSkeleton />
      ) : errorPrograms || errorBrechas ? (
        <></>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Gráfico de Barras: Cobertura y Programas por Clúster */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">
                Programas y Cobertura por Región (Clúster)
              </h3>
            </div>
            <div className="flex-1 mt-4">
              <ChartContainer
                config={barChartConfig}
                className="h-[240px] w-full"
              >
                <BarChart
                  data={barChartData}
                  margin={{ top: 10, right: -10, left: -20, bottom: 0 }}
                >
                  <CartesianGrid vertical={false} strokeDasharray="3 3" />
                  <XAxis
                    dataKey="region"
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    interval={0}
                    tick={{
                      fontSize: 7,
                      fill: "#64748b",
                      angle: -35,
                      textAnchor: "end",
                    }}
                    height={50}
                  />
                  <YAxis
                    yAxisId="left"
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    tick={{ fontSize: 9, fill: "#64748b" }}
                    domain={[0, 100]}
                    unit="%"
                  />
                  <YAxis
                    yAxisId="right"
                    orientation="right"
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    tick={{ fontSize: 9, fill: "#64748b" }}
                    domain={[0, 'auto']}
                    allowDecimals={false}
                  />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <Bar
                    yAxisId="right"
                    dataKey="programas"
                    fill="var(--color-programas)"
                    radius={[2, 2, 0, 0]}
                    barSize={8}
                  />
                  <Bar
                    yAxisId="left"
                    dataKey="cobertura"
                    fill="var(--color-cobertura)"
                    radius={[2, 2, 0, 0]}
                    barSize={8}
                  />
                  <ChartLegend content={<ChartLegendContent />} />
                </BarChart>
              </ChartContainer>
            </div>
          </div>

          {/* Gráfico de Donut: Distribución de Categorías */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
            <div>
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <h3 className="text-sm font-bold text-slate-800">
                  Por Categoría
                </h3>
              </div>

              <div className="flex flex-col items-center gap-6 mt-6">
                <ChartContainer
                  config={pieChartConfig}
                  className="h-[125px] w-[125px] shrink-0"
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
                      innerRadius={32}
                      outerRadius={48}
                      strokeWidth={2}
                      stroke="#ffffff"
                    >
                      {pieChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                  </PieChart>
                </ChartContainer>

                <div className="w-full space-y-2 text-xs">
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
          </div>
        </div>
      )}

      {/* Listado Principal de Programas (Tabla) */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
        {/* Barra superior de la tabla */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <h3 className="text-sm font-bold text-slate-800">
            Listado de Programas
          </h3>
          <div className="flex items-center gap-3">
            {/* Input de Búsqueda */}
            <div className="relative w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
              <input
                type="text"
                placeholder="Buscar programa..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-9 pr-3 py-1.5 text-xs focus:outline-none focus:border-blue-500 focus:bg-white transition-all text-slate-700"
              />
            </div>

            {/* Dropdown de Filtrado por Estado */}
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="flex items-center justify-between gap-1.5 bg-white border border-slate-200 text-xs font-semibold text-slate-700 px-3.5 py-1.5 rounded-lg hover:bg-slate-50 cursor-pointer min-w-[100px] select-none text-left"
              >
                <span>{statusFilter}</span>
                <ChevronDown
                  className={`w-3.5 h-3.5 text-slate-400 transition-transform duration-150 ${isDropdownOpen ? "rotate-180" : ""}`}
                />
              </button>

              {isDropdownOpen && (
                <div className="absolute right-0 top-full mt-1.5 w-32 bg-white border border-slate-200 rounded-lg shadow-md py-1 z-50 animate-in fade-in slide-in-from-top-1 duration-100">
                  {["Todos", "Activo", "Crítico", "Alerta"].map((opt) => (
                    <button
                      key={opt}
                      onClick={() => {
                        setStatusFilter(opt);
                        setIsDropdownOpen(false);
                      }}
                      className={`w-full text-left px-3 py-1.5 text-xs hover:bg-slate-50 cursor-pointer flex items-center justify-between ${statusFilter === opt ? "bg-blue-50/50 text-blue-600 font-bold" : "text-slate-700"}`}
                    >
                      <span>{opt}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Estructura de Tabla */}
        {loadingPrograms ? (
          <ProgramListSkeleton />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-slate-100 text-slate-400 font-semibold h-10">
                    <th className="py-2 pr-4 pl-1">Programa</th>
                    <th className="py-2 px-4">Región (Clúster)</th>
                    <th className="py-2 px-4">Beneficiarios</th>
                    <th className="py-2 px-4">Cobertura</th>
                    <th className="py-2 px-4">Estado</th>
                    <th className="py-2 pl-4 pr-1 text-right"></th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPrograms.length > 0 ? (
                    filteredPrograms.map((program) => {
                      const colors = getCoverageColors(program.cobertura);
                      return (
                        <tr
                          key={program.id}
                          className="border-b border-slate-100 hover:bg-slate-50/40 transition-colors h-14"
                        >
                          {/* Nombre del Programa */}
                          <td className="py-3 pr-4 pl-1 font-bold text-slate-800 max-w-xs md:max-w-sm lg:max-w-md truncate">
                            {program.nombre}
                          </td>

                          {/* Región (Clúster) */}
                          <td className="py-3 px-4 text-slate-600 font-medium">
                            <span className="flex items-center gap-1.5">
                              <MapPin className="w-3.5 h-3.5 text-slate-400 animate-pulse" />
                              <span>{formatClusterName(program.region)}</span>
                            </span>
                          </td>

                          {/* Beneficiarios */}
                          <td className="py-3 px-4 text-slate-600 font-medium">
                            <span className="flex items-center gap-1.5">
                              <Users className="w-3.5 h-3.5 text-slate-400" />
                              <span>{program.beneficiarios}</span>
                            </span>
                          </td>

                          {/* Cobertura */}
                          <td className="py-3 px-4">
                            <div className="flex flex-col gap-1">
                              <span className={`font-bold ${colors.text}`}>
                                {program.cobertura !== null && program.cobertura !== undefined
                                  ? `${program.cobertura}%`
                                  : "Sin datos"}
                              </span>
                              {program.cobertura !== null && program.cobertura !== undefined && (
                                <div className="w-24 bg-slate-100 rounded-full h-1 overflow-hidden">
                                  <div
                                    className={`h-full rounded-full ${colors.bar} transition-all duration-500`}
                                    style={{ width: `${program.cobertura}%` }}
                                  ></div>
                                </div>
                              )}
                            </div>
                          </td>

                          {/* Estado */}
                          <td className="py-3 px-4">
                            {getStatusBadge(program.estado)}
                          </td>

                          {/* Botón de detalle */}
                          <td className="py-3 pl-4 pr-1 text-right">
                            <button className="p-1 hover:bg-slate-100 rounded text-slate-400 hover:text-slate-600 transition-colors cursor-pointer">
                              <ChevronRight className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td
                        colSpan="6"
                        className="py-8 text-center text-slate-400 font-medium"
                      >
                        No se encontraron programas con los filtros
                        seleccionados.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Footer del Listado */}
            <div className="flex justify-between items-center pt-2 text-[11px] text-slate-400 font-semibold select-none">
              <span>
                Mostrando {filteredPrograms.length} de {programList.length}{" "}
                programas de formación activos
              </span>
            </div>
          </>
        )}
      </div>

      {/* Modal del Formulario de Creación */}
      {isFormOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
          <div className="bg-white rounded-xl shadow-lg border border-slate-200/80 overflow-hidden w-full max-w-md animate-in zoom-in-95 duration-200">
            <NuevoProgramaForm
              onSubmitSuccess={() => setIsFormOpen(false)}
              onCancel={() => setIsFormOpen(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default FormacionesPage;
