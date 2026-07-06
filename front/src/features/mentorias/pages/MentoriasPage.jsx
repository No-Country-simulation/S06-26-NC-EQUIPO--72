import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import {
  AlertCircle,
  // ArrowRight,
  ChevronRight,
  // GraduationCap,
  MapPin,
  SquareCheckBig,
  Star,
  User,
  Users,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  // PolarAngleAxis,
  // PolarGrid,
  // Radar,
  // RadarChart,
  XAxis,
  YAxis,
} from "recharts";
import { useMentoriasBrechas } from "../hooks/useMentorias";
import { formatClusterName } from "@/shared/utils/format";
import { Skeleton } from "@/components/ui/skeleton";
import {
  BarChartDataSkeleton,
  ListMentorsSkeleton,
} from "../skeletons/MentoriasPageSkeleton";

// data del backend
// {
//   "brechas": [
//     {
//       "cluster": "SAO_JOSE_BARREIROS",
//       "municipio": "São José",
//       "n_usuarios": 9400,
//       "congestionamento_medio": 0.31,
//       "rat_type_predominante": "LTE",
//       "indicador_social": {
//         "categoria": "EMPLEO",
//         "indicador": "taxa_desemprego_municipal",
//         "valor": 8.3,
//         "unidad": "porcentaje"
//       },
//       "programas_activos": 1,
//       "severidad_brecha": "MEDIA"
//     }
//   ],
//   "criterio": {
//     "servicio": "MENTORIA",
//     "logica": "congestionamento_medio > 0.6 AND programas_activos = 0",
//     "umbral_congestionamento": 0.6
//   }
// }

export default function MentoriasPage() {
  const { data, isLoading, isError } = useMentoriasBrechas();

  const allPerson = data?.brechas?.reduce(
    (acc, item) => acc + item.n_usuarios,
    0,
  );

  const programsActive = data?.brechas?.reduce(
    (acc, item) => acc + item.programas_activos,
    0,
  );

  const barChartConfig = {
    mentorizados: {
      label: "Mentores",
      color: "#7f22fe ",
    },
  };

  const barChartData = data?.brechas?.map((brecha) => ({
    region: formatClusterName(brecha.cluster),
    mentorizados: brecha.indicador_social?.valor,
  }));

  // const barChartData = [
  //   { region: "Noroeste", mentorizados: 8 },
  //   { region: "Norte", mentorizados: 14 },
  //   { region: "Noreste", mentorizados: 22 },
  //   { region: "Occidente", mentorizados: 11 },
  //   { region: "Centro", mentorizados: 48 },
  //   { region: "Oriente", mentorizados: 24 },
  //   { region: "Suroeste", mentorizados: 4 },
  //   { region: "Sur", mentorizados: 7 },
  //   { region: "Sureste", mentorizados: 11 },
  // ];

  // const chartConfig = {
  //   evaluation: {
  //     label: "Evaluation",
  //     color: "#7f22fe",
  //   },
  // };

  // const chartData = [
  //   { indicators: "Cobertura", evaluation: 72 },
  //   { indicators: "Diversidad", evaluation: 62 },
  //   { indicators: "Impacto", evaluation: 76 },
  //   { indicators: "Satisfacción", evaluation: 88 },
  //   { indicators: "Retención", evaluation: 68 },
  //   { indicators: "Efectividad", evaluation: 84 },
  // ];

  const programs = data?.brechas?.map((brecha) => ({
    name: formatClusterName(brecha.cluster),
    region: brecha.municipio,
    mentees: brecha.programas_activos,
    status: brecha.severidad_brecha,
    effectiveness: brecha.indicador_social?.valor,
  }));

  // const programs = [
  //   {
  //     name: "Red de Líderes Comunitarios",
  //     region: "Centro",
  //     mentors: 145,
  //     mentees: 890,
  //     status: "Activo",
  //     effectiveness: 4.6,
  //   },
  //   {
  //     name: "Mentoría Empresarial Juvenil",
  //     region: "Noreste",
  //     mentors: 78,
  //     mentees: 412,
  //     status: "Activo",
  //     effectiveness: 4.2,
  //   },
  //   {
  //     name: "Programa Mujeres Emprendedoras",
  //     region: "Oriente",
  //     mentors: 62,
  //     mentees: 348,
  //     status: "Activo",
  //     effectiveness: 4.4,
  //   },
  //   {
  //     name: "Mentoría Tecnológica Rural",
  //     region: "Sureste",
  //     mentors: 18,
  //     mentees: 94,
  //     status: "Crítico",
  //     effectiveness: 3.1,
  //   },
  //   {
  //     name: "Red de Mentores Académicos",
  //     region: "Norte",
  //     mentors: 54,
  //     mentees: 287,
  //     status: "Alerta",
  //     effectiveness: 3.8,
  //   },
  //   {
  //     name: "Desarrollo de Capacidades Locales",
  //     region: "Sur",
  //     mentors: 23,
  //     mentees: 118,
  //     status: "Alerta",
  //     effectiveness: 3.3,
  //   },
  // ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Users className="w-5 h-5 text-violet-600" />
            <span>Programas de Mentoría</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Programas activos, cobertura y efectividad de las mentorías
            regionales
          </p>
        </div>
      </div>
      {/*  */}
      {isLoading ? (
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
      ) : isError ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center flex items-center justify-center gap-2 text-xs text-red-600 font-semibold shadow-xs">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span>Error al sincronizar datos de mentorias con el servidor</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
          <div className="flex items-center gap-4">
            <GraduationCap className="w-8 h-8 text-gray-600" />
            <div className="flex flex-col items-baseline gap-1">
              <span className="text-2xl font-bold text-slate-800 tracking-tight">
                380
              </span>
            </div>
          </div>
          <p className="text-xs text-slate-500 font-medium">Mentores Activos</p>
        </div> */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-4">
              <User className="w-8 h-8 text-gray-600" />
              <div className="flex flex-col items-baseline gap-1">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {allPerson}
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">
              Acceso a servicios
            </p>
          </div>
          {/* <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
          <div className="flex items-center gap-4">
            <Star className="w-8 h-8 text-yellow-400" />
            <div className="flex flex-col items-baseline gap-1">
              <span className="text-2xl font-bold text-slate-800 tracking-tight">
                3.9/5
              </span>
            </div>
          </div>
          <p className="text-xs text-slate-500 font-medium">
            Efectividad Media
          </p>
        </div> */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-4">
              <SquareCheckBig className="w-8 h-8 text-green-600" />
              <div className="flex flex-col items-baseline gap-1">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {programsActive}
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">
              Programas Activos
            </p>
          </div>
        </div>
      )}

      {isLoading ? (
        <BarChartDataSkeleton />
      ) : isError ? (
        <></>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col hover:shadow-sm transition-shadow">
            <div className="border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">
                Mentorizados por Región
              </h3>
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
                    domain={[0, 10]}
                  />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <Bar
                    dataKey="mentorizados"
                    fill="var(--color-mentores)"
                    radius={[2, 2, 0, 0]}
                    barSize={25}
                  />
                </BarChart>
              </ChartContainer>
            </div>
          </div>
          {/* <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col hover:shadow-sm transition-shadow">
          <div className="border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-800">
              Evaluación de Desempeño Nacional
            </h3>
          </div>
          <div className="flex-1 mt-4">
            <ChartContainer config={chartConfig} className="h-[240px] w-full">
              <RadarChart data={chartData}>
                <ChartTooltip
                  cursor={false}
                  content={<ChartTooltipContent />}
                />
                <PolarAngleAxis dataKey="indicators" />
                <PolarGrid />
                <Radar
                  dataKey="evaluation"
                  fill="var(--color-evaluation)"
                  fillOpacity={0.2}
                  stroke="var(--color-evaluation)"
                  strokeWidth={2}
                />
              </RadarChart>
            </ChartContainer>
          </div>
        </div> */}
        </div>
      )}

      {isLoading ? (
        <ListMentorsSkeleton />
      ) : isError ? (
        <></>
      ) : (
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm">
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 border-b border-slate-100 p-4">
            <h3 className="text-sm font-bold text-slate-800">
              Programas de Mentoría Activos
            </h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs table-auto">
              <tbody>
                {programs?.map((program) => (
                  <tr
                    key={program.name}
                    className="border-b border-slate-200 hover:bg-slate-50 transition-colors"
                  >
                    <td className="w-full py-4 pl-4">
                      <section className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-violet-100 flex items-center justify-center">
                          <Users className="w-5 h-5 text-violet-600" />
                        </div>
                        <div className="flex flex-col gap-1">
                          <span className="font-semibold text-slate-800">
                            {program.name}
                          </span>

                          <div className="flex items-center gap-3 text-slate-500 text-xs">
                            <span className="flex items-center gap-1">
                              <MapPin className="w-3 h-3" />
                              {program.region}
                            </span>

                            <span className="flex items-center gap-1">
                              <Users className="w-3 h-3" />
                              {program.mentees} mentorizados
                            </span>
                          </div>
                        </div>
                      </section>
                    </td>
                    <td className="whitespace-nowrap py-4 pr-4 text-center">
                      <section className="flex items-center gap-3">
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${
                            program.status === "ALTA"
                              ? "bg-green-100 text-green-700"
                              : program.status === "MEDIA"
                                ? "bg-amber-100 text-amber-700"
                                : "bg-red-100 text-red-700"
                          }`}
                        >
                          {program.status}
                        </span>
                        <div className="flex flex-col items-center">
                          <span className="font-bold text-slate-800 flex items-center gap-1">
                            <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                            {program.effectiveness}
                          </span>

                          <span className="text-xs text-slate-400">
                            efectividad
                          </span>
                        </div>
                        <button className="p-1 rounded hover:bg-slate-100">
                          <ChevronRight className="w-4 h-4 text-slate-400" />
                        </button>
                      </section>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      {/*  */}
      {/* <div className="bg-white border border-red-100 rounded-2xl p-5">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-xl bg-red-100 flex items-center justify-center shrink-0">
            <AlertCircle className="w-5 h-5 text-red-500" />
          </div>
          <div className="flex-1">
            <h3 className="text-sm font-bold text-slate-900">
              Atención requerida — Región Suroeste
            </h3>
            <p className="mt-1 text-sm text-slate-600 leading-relaxed max-w-3xl">
              La región Suroeste cuenta con apenas 18 mentores activos para 94
              mentorizados — ratio de 1:5.2, muy por debajo del objetivo de 1:3.
              Se recomienda reclutamiento urgente.
            </p>
            <button className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-red-200 text-red-600 font-medium text-sm bg-red-100 cursor-pointer">
              Ver plan de intervención
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div> */}
    </div>
  );
}
