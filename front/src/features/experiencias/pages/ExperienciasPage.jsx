import { useState, useMemo } from "react";
import {
  Star,
  Users,
  Copy,
  Rocket,
  Lightbulb,
  Handshake,
  Monitor,
  Activity,
  Plus,
  MapPin,
  User,
  AlertCircle,
} from "lucide-react";

// Importamos los hooks de React Query desarrollados para la API de experiencias
import {
  useExperienciasList,
  useExperienciasBrechas,
} from "../hooks/useExperiencias";

// Importamos el formulario interactivo para registrar experiencias
import NuevaExperienciaForm from "../components/NuevaExperienciaForm";
import {
  ExperienciasSkeletons,
  IndicatorsSkeleton,
} from "../skeletons/ExperienciasPageSkeletons";
import { formatClusterName } from "@/shared/utils/format";
import { useLanguage } from "@/context/useLenguage";

// Lista oficial de clústeres para Florianópolis (coincide con la sección de Formaciones)
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

/**
 * Función de utilidad determinista para generar y procesar datos territoriales.
 * Si el clúster existe en los datos reales devueltos por el backend, los mapea.
 * Si no está sembrado, calcula una estimación consistente y fija basada en el hash de su nombre
 * para que no aparezcan datos vacíos o inconsistentes en la interfaz.
 */
const getClusterData = (clusterName, brechasList) => {
  if (!clusterName)
    return { nUsuarios: null, cobertura: null, severidad: null };

  // Buscamos si existe una brecha registrada para este clúster
  const realMatch = brechasList?.find(
    (b) => b.cluster.toUpperCase() === clusterName.toUpperCase(),
  );

  if (realMatch) {
    const coverageVal = realMatch.indicador_social?.valor
      ? parseFloat(realMatch.indicador_social.valor)
      : 0;
    // Si viene como fracción (< 2), la multiplicamos por 100
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

function ExperienciasPage() {
  const { language } = useLanguage();
  const isPortugues = language === "pt";

  // Estado local para el filtrado de las tarjetas por impacto
  const [impactFilter, setImpactFilter] = useState("Todos");

  // Estado para controlar la visibilidad del modal de registro
  const [isFormOpen, setIsFormOpen] = useState(false);

  // 1. Petición GET al endpoint /programas?size=100&tipo=EXPERIENCIA
  const {
    data: rawExperiencias,
    isLoading: loadingExperiencias,
    error: errorExperiencias,
  } = useExperienciasList();

  // 2. Petición GET al endpoint /brechas?servicio=EXPERIENCIA
  const {
    data: rawBrechas,
    isLoading: loadingBrechas,
    error: errorBrechas,
  } = useExperienciasBrechas();

  // 3. Mapeo y procesamiento de los registros del backend a la estructura visual de las tarjetas
  const experienceList = useMemo(() => {
    if (!rawExperiencias) return [];

    return rawExperiencias.map((exp) => {
      // Cruzamos con la respuesta de brechas/territorio
      const territorial = getClusterData(exp.cluster, rawBrechas?.brechas);

      // Mapeamos el impacto y colores dinámicos
      let impactText = isPortugues ? "Impacto médio" : "Impacto medio";
      let impactColor = "bg-amber-50 text-amber-700 border-amber-200";

      if (exp.impactoEstimado === "ALTO") {
        impactText = isPortugues ? "Alto Impacto" : "Alto Impacto";
        impactColor = "bg-green-50 text-green-700 border-green-200";
      } else if (exp.impactoEstimado === "BAJO") {
        impactText = isPortugues ? "Baixo impacto" : "Bajo impacto";
        impactColor = "bg-red-50 text-red-700 border-red-200";
      }

      return {
        id: exp.id,
        title: exp.nombre,
        description: exp.descripcion || "",
        impact: impactText,
        impactColor: impactColor,
        replicable: exp.replicable === 1,
        region:
          formatClusterName(exp.cluster) ||
          (isPortugues ? "Não definido" : "Sin definir"),
        beneficiarios:
          territorial.nUsuarios !== null && territorial.nUsuarios !== undefined
            ? `${territorial.nUsuarios.toLocaleString("es-ES")} ${isPortugues ? "beneficiários" : "beneficiarios"}`
            : "Sin datos de beneficiarios",
        beneficiariosRaw: territorial.nUsuarios,
        leader:
          exp.liderReferente || (isPortugues ? "Não atribuído" : "No asignado"),
      };
    });
  }, [rawExperiencias, rawBrechas]);

  // 4. Filtrado en tiempo real en base al nivel de impacto seleccionado
  const filteredExperiences = useMemo(() => {
    return experienceList.filter((exp) => {
      const matchesImpact =
        impactFilter === "Todos" ||
        exp.impact.toLowerCase() === impactFilter.toLowerCase();

      return matchesImpact;
    });
  }, [experienceList, impactFilter]);

  // 5. Cálculo dinámico de los 4 indicadores superiores (KPIs)
  const kpis = useMemo(() => {
    const totalActivas = experienceList.length;

    // Calculamos beneficiarios sumando los usuarios reales que vienen del backend
    const beneficiariosTotales =
      rawBrechas?.brechas?.reduce((sum, b) => {
        return sum + (b.n_usuarios || 0);
      }, 0) || 0;

    const beneficiariosFormateados =
      beneficiariosTotales >= 1000
        ? Math.round(beneficiariosTotales / 1000) + "K"
        : beneficiariosTotales;

    const replicables = experienceList.filter((e) => e.replicable).length;
    const altoImpacto = experienceList.filter(
      (e) => e.impact === "Alto Impacto",
    ).length;

    return [
      {
        label: isPortugues ? "Experiências ativas" : "Experiencias activas",
        value: totalActivas.toString(),
        icon: Star,
        iconColor: "text-amber-500",
        bgColor: "bg-amber-50 border-amber-100",
      },
      {
        label: isPortugues ? "Beneficiários totais" : "Beneficiarios totales",
        value: beneficiariosFormateados.toString(),
        icon: Users,
        iconColor: "text-slate-600",
        bgColor: "bg-slate-50 border-slate-100",
      },
      {
        label: isPortugues ? "Replicáveis" : "Replicables",
        value: replicables.toString(),
        icon: Copy,
        iconColor: "text-blue-600",
        bgColor: "bg-blue-50 border-blue-100",
      },
      {
        label: isPortugues ? "Alto Impacto" : "Alto Impacto",
        value: altoImpacto.toString(),
        icon: Rocket,
        iconColor: "text-purple-600",
        bgColor: "bg-purple-50 border-purple-100",
      },
    ];
  }, [experienceList, rawBrechas]);

  // 6. Clasificación semántica de las categorías en base a palabras clave de títulos/descripciones
  const categoryMetrics = useMemo(() => {
    let innovacion = 0;
    let economia = 0;
    let digital = 0;
    let salud = 0;

    experienceList.forEach((exp) => {
      const text = `${exp.title.toLowerCase()} ${exp.description.toLowerCase()}`;

      if (
        text.includes("innovacion") ||
        text.includes("social") ||
        text.includes("comunidad") ||
        text.includes("laboratorio")
      ) {
        innovacion++;
      } else if (
        text.includes("economia") ||
        text.includes("solidaria") ||
        text.includes("mercados") ||
        text.includes("cooperativa") ||
        text.includes("inclusivo")
      ) {
        economia++;
      } else if (
        text.includes("digital") ||
        text.includes("tecnologias") ||
        text.includes("red") ||
        text.includes("guardianes") ||
        text.includes("computacion")
      ) {
        digital++;
      } else if (
        text.includes("salud") ||
        text.includes("comunitaria") ||
        text.includes("mental") ||
        text.includes("brigadas") ||
        text.includes("bienestar") ||
        text.includes("cocina")
      ) {
        salud++;
      } else {
        // Asignación por defecto en caso de no coincidencia clara
        innovacion++;
      }
    });

    return [
      {
        title: isPortugues ? "Inovação Social" : "Innovación Social",
        count: innovacion.toString(),
        icon: Lightbulb,
        iconColor: "text-amber-500 bg-amber-50 border-amber-100",
        barColor: "bg-blue-600",
      },
      {
        title: isPortugues ? "Economia Solidária" : "Economía Solidaria",
        count: economia.toString(),
        icon: Handshake,
        iconColor: "text-emerald-600 bg-emerald-50 border-emerald-100",
        barColor: "bg-emerald-500",
      },
      {
        title: isPortugues ? "Digital para Todos" : "Digital para Todos",
        count: digital.toString(),
        icon: Monitor,
        iconColor: "text-purple-600 bg-purple-50 border-purple-100",
        barColor: "bg-purple-500",
      },
      {
        title: isPortugues ? "Saúde Comunitária" : "Salud Comunitaria",
        count: salud.toString(),
        icon: Activity,
        iconColor: "text-pink-600 bg-pink-50 border-pink-100",
        barColor: "bg-pink-500",
      },
    ];
  }, [experienceList]);

  return (
    <div className="space-y-6">
      {/* Title & Header Row */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Star className="w-5 h-5 text-amber-500 animate-pulse" />
            <span>
              {isPortugues
                ? "Experiências Estruturantes"
                : "Experiencias Estructurantes"}
            </span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            {isPortugues
              ? "Iniciativas de sucesso replicáveis e projetos comunitários de alto impacto em Florianópolis"
              : "Iniciativas exitosas replicables y proyectos comunitarios de alto impacto en Florianópolis"}
          </p>
        </div>
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto">
          <div className="flex items-center gap-2 bg-white border border-slate-200 px-3.5 py-2 rounded-lg shadow-xs w-full sm:w-auto justify-between sm:justify-start">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider whitespace-nowrap">
              {isPortugues ? "Impacto:" : "Impacto:"}
            </span>
            <select
              value={impactFilter}
              onChange={(e) => setImpactFilter(e.target.value)}
              className="bg-transparent text-xs font-bold text-slate-700 cursor-pointer focus:outline-none select-none"
            >
              <option value="Todos">Todos</option>
              <option value={isPortugues ? "Alto Impacto" : "Alto Impacto"}>
                {isPortugues ? "Alto Impacto" : "Alto Impacto"}
              </option>
              <option value={isPortugues ? "Impacto médio" : "Impacto medio"}>
                {isPortugues ? "Impacto médio" : "Impacto medio"}
              </option>
              <option value={isPortugues ? "Baixo impacto" : "Bajo impacto"}>
                {isPortugues ? "Baixo impacto" : "Bajo impacto"}
              </option>
            </select>
          </div>
          <button
            onClick={() => setIsFormOpen(true)}
            className="flex items-center justify-center gap-1.5 bg-[#2563eb] hover:bg-blue-600 text-white font-medium text-xs px-4 py-2.5 rounded-lg transition-all active:scale-[0.98] cursor-pointer shadow-sm w-full sm:w-auto"
          >
            <Plus className="w-4 h-4" />
            <span>
              {isPortugues ? "Registrar experiência" : "Registrar experiencia"}
            </span>
          </button>
        </div>
      </div>

      {loadingExperiencias || loadingBrechas ? (
        <IndicatorsSkeleton />
      ) : errorExperiencias || errorBrechas ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span>
            {isPortugues
              ? "Erro ao sincronizar dados de experiências com o servidor"
              : "Error al sincronizar datos de experiencias con el servidor"}
          </span>
        </div>
      ) : (
        <>
          {/* Top Indicators Row (KPIs) */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {kpis.map((item, idx) => {
              const Icon = item.icon;
              return (
                <div
                  key={idx}
                  className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-xs transition-shadow"
                >
                  <div className="flex items-center justify-between">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center border ${item.bgColor} ${item.iconColor}`}
                    >
                      <Icon className="w-4 h-4" />
                    </div>
                  </div>
                  <div className="mt-3">
                    <h4 className="text-2xl font-bold text-slate-800 tracking-tight">
                      {item.value}
                    </h4>
                    <p className="text-xs text-slate-500 mt-1 font-semibold">
                      {item.label}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Categories Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {categoryMetrics.map((item, idx) => {
              const Icon = item.icon;
              return (
                <div
                  key={idx}
                  className="bg-white border border-slate-200 rounded-xl p-4 pb-5 flex flex-col justify-between relative overflow-hidden hover:shadow-xs transition-shadow"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center border ${item.iconColor}`}
                    >
                      <Icon className="w-4.5 h-4.5" />
                    </div>
                    <span className="text-xs font-bold text-slate-700">
                      {item.title}
                    </span>
                  </div>
                  <div className="mt-4">
                    <span className="text-2xl font-bold text-slate-800">
                      {item.count}
                    </span>
                    <p className="text-[10px] text-slate-400 font-semibold mt-0.5">
                      {isPortugues
                        ? "Iniciativas ativas"
                        : "Iniciativas activas"}
                    </p>
                  </div>
                  {/* Bottom Colored Indicator Line */}
                  <div
                    className={`absolute bottom-0 left-0 right-0 h-1 ${item.barColor}`}
                  />
                </div>
              );
            })}
          </div>
        </>
      )}

      {/* Filtro reposicionado en la cabecera */}

      {/* Featured Experiences Grid */}
      {!errorExperiencias && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-800">
              {isPortugues
                ? "Experiências Destacadas"
                : "Experiencias Destacadas"}
            </h3>
            <span className="text-[10px] text-slate-400 font-bold uppercase">
              {isPortugues
                ? `Mostrando ${filteredExperiences.length} de ${experienceList.length} experiências`
                : `Mostrando ${filteredExperiences.length} de ${experienceList.length} experiencias`}
            </span>
          </div>

          {loadingExperiencias ? (
            <ExperienciasSkeletons />
          ) : filteredExperiences.length > 0 ? (
            <div className="max-h-[500px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-slate-200">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredExperiences.map((experience) => (
                  <div
                    key={experience.id}
                    className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-xs transition-shadow"
                  >
                    <div>
                      {/* Badges Row */}
                      <div className="flex items-center justify-between">
                        <span
                          className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${experience.impactColor}`}
                        >
                          {experience.impact}
                        </span>
                        {experience.replicable && (
                          <span className="flex items-center gap-1 text-[10px] text-slate-400 font-semibold bg-slate-50 px-2 py-0.5 rounded border border-slate-150">
                            <Copy className="w-3 h-3" />
                            <span>
                              {isPortugues ? "Replicável" : "Replicable"}
                            </span>
                          </span>
                        )}
                      </div>

                      {/* Title */}
                      <h4 className="text-sm font-bold text-slate-800 mt-3.5 leading-snug">
                        {experience.title}
                      </h4>

                      {/* Description */}
                      <p className="text-[11px] text-slate-500 font-medium mt-2 line-clamp-2 leading-relaxed">
                        {experience.description}
                      </p>

                      {/* Details List */}
                      <div className="mt-4 space-y-2">
                        <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                          <MapPin className="w-3.5 h-3.5 text-slate-400" />
                          <span className="capitalize">{experience.region}</span>
                        </div>
                        <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                          <Users className="w-3.5 h-3.5 text-slate-400" />
                          <span>{experience.beneficiarios}</span>
                        </div>
                        <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                          <User className="w-3.5 h-3.5 text-slate-400" />
                          <span>
                            {isPortugues
                              ? `Liderado por ${experience.leader}`
                              : `Liderado por ${experience.leader}`}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-8 text-center text-slate-400 font-medium">
              {isPortugues
                ? "Nenhuma experiência registrada foi encontrada que corresponda à pesquisa ou filtro."
                : "No se encontraron experiencias registradas que coincidan con la búsqueda o filtro."}
            </div>
          )}
        </div>
      )}

      {/* Modal Overlay para el formulario NuevaExperienciaForm */}
      {isFormOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-in fade-in duration-200">
          <div className="bg-white rounded-xl shadow-lg w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-200">
            <NuevaExperienciaForm
              onSubmitSuccess={() => {
                setIsFormOpen(false);
              }}
              onCancel={() => setIsFormOpen(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default ExperienciasPage;
