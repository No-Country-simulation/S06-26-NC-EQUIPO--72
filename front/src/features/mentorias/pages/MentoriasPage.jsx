import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import {
  AlertCircle,
  ChevronRight,
  MapPin,
  SquareCheckBig,
  User,
  Users,
} from "lucide-react";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import { useMentorias } from "../hooks/useMentorias";
import { Skeleton } from "@/components/ui/skeleton";
import {
  BarChartDataSkeleton,
  ListMentorsSkeleton,
} from "../skeletons/MentoriasPageSkeleton";
import { useLanguage } from "@/context/useLenguage";

export default function MentoriasPage() {
  const { lenguage } = useLanguage();
  const isPortugues = lenguage === "pt";

  const { data, isLoading, isError } = useMentorias();

  const barChartConfig = {
    mentorias: {
      label: isPortugues ? "mentorias" : "mentorias",
      color: "#7f22fe ",
    },
  };

  const barChartData = data?.map((r) => ({
    region: r.municipio,
    mentorias: 3,
  }));

  const programs = data?.map((r) => ({
    name: r.nombre,
    region: r.municipio,
    status: r.impactoEstimado,
    effectiveness: r.indicador_social?.valor,
  }));

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Users className="w-5 h-5 text-violet-600" />
            <span>
              {isPortugues ? "Programas de Mentoria" : "Programas de Mentoría"}
            </span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            {isPortugues
              ? "Programas ativos, cobertura e eficácia das mentorias regionais"
              : "Programas activos, cobertura y efectividad de las mentorías regionales"}
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
          <span>
            {isPortugues
              ? "Erro ao sincronizar dados de mentorias com o servidor"
              : "Error al sincronizar datos de mentorias con el servidor"}
          </span>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-4">
              <User className="w-8 h-8 text-gray-600" />
              <div className="flex flex-col items-baseline gap-1">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  42
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">
              {isPortugues ? "Acesso a serviços" : "Acceso a servicios"}
            </p>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-4">
              <SquareCheckBig className="w-8 h-8 text-green-600" />
              <div className="flex flex-col items-baseline gap-1">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {data?.length || 0}
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">
              {isPortugues ? "Programas Ativos" : "Programas Activos"}
            </p>
          </div>
        </div>
      )}

      {isLoading ? (
        <BarChartDataSkeleton />
      ) : isError ? (
        <></>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col hover:shadow-sm transition-shadow">
            <div className="border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">
                {isPortugues ? "Programas por Região" : "Programas por Región"}
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
                    dataKey="mentorias"
                    fill="var(--color-mentorias)"
                    radius={[2, 2, 0, 0]}
                    barSize={25}
                  />
                </BarChart>
              </ChartContainer>
            </div>
          </div>
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
              {isPortugues
                ? "Programas de Mentoria Ativos"
                : "Programas de Mentoría Activos"}
            </h3>
          </div>
          <div className="overflow-x-auto max-h-[400px] overflow-y-auto">
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
                          </div>
                        </div>
                      </section>
                    </td>
                    <td className="whitespace-nowrap py-4 pr-4 text-center">
                      <section className="flex items-center gap-3">
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${
                            program.status === "ALTO"
                              ? "bg-green-100 text-green-700"
                              : program.status === "MEDIO"
                                ? "bg-amber-100 text-amber-700"
                                : "bg-red-100 text-red-700"
                          }`}
                        >
                          {program.status}
                        </span>
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
    </div>
  );
}
