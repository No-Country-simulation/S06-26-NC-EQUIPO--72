import { useMemo } from "react";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import {
  AlertCircle,
  MapPin,
  SquareCheckBig,
  Star,
  User,
  Users,
} from "lucide-react";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import { useMentorias, useMentoriasBrechas } from "../hooks/useMentorias";
import { Skeleton } from "@/components/ui/skeleton";
import {
  BarChartDataSkeleton,
  ListMentorsSkeleton,
} from "../skeletons/MentoriasPageSkeleton";
import { useLanguage } from "@/context/useLenguage";
import { formatClusterName } from "@/shared/utils/format";

export default function MentoriasPage() {
  const { lenguage } = useLanguage();
  const isPortugues = lenguage === "pt";

  const { data, isLoading: loadingProgramas, isError: errorProgramas } = useMentorias();
  const { data: brechasData, isLoading: loadingBrechas, isError: errorBrechas } = useMentoriasBrechas();

  const isLoading = loadingProgramas || loadingBrechas;
  const isError = errorProgramas || errorBrechas;

  const allPerson = useMemo(() => {
    if (!brechasData?.brechas) return 0;
    return brechasData.brechas.reduce((sum, item) => sum + (item.n_usuarios || 0), 0);
  }, [brechasData]);

  const allPersonFormatted = useMemo(() => {
    if (allPerson >= 1000) {
      return Math.round(allPerson / 1000) + "K";
    }
    return allPerson.toString();
  }, [allPerson]);

  const avgEffectiveness = useMemo(() => {
    if (!data || data.length === 0) return "0.0";
    const totalEffectiveness = data.reduce((sum, r) => sum + (r.efectividad || 0), 0);
    return (totalEffectiveness / data.length).toFixed(1);
  }, [data]);

  const barChartConfig = {
    mentorias: {
      label: isPortugues ? "mentorias" : "mentorias",
      color: "#7f22fe ",
    },
  };

  const barChartData = useMemo(() => {
    if (!data) return [];
    const counts = {};
    data.forEach((r) => {
      const name = formatClusterName(r.cluster) || r.cluster || "Sin definir";
      counts[name] = (counts[name] || 0) + 1;
    });
    return Object.entries(counts).map(([region, count]) => ({
      region,
      mentorias: count,
    }));
  }, [data]);

  const programs = useMemo(() => {
    if (!data) return [];
    return data.map((r) => ({
      name: r.nombre,
      region: formatClusterName(r.cluster) || r.cluster || "Sin definir",
      status: r.impactoEstimado || "MEDIO",
      effectiveness: r.efectividad,
    }));
  }, [data]);

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
                  {allPersonFormatted}
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
          <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-3 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-4">
              <Star className="w-8 h-8 text-yellow-400 fill-yellow-400" />
              <div className="flex flex-col items-baseline gap-1">
                <span className="text-2xl font-bold text-slate-800 tracking-tight">
                  {avgEffectiveness}/5
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">
              {isPortugues ? "Eficácia Média" : "Efectividad Media"}
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
                    allowDecimals={false}
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
                      <section className="flex items-center gap-4 justify-end">
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

                        <div className="flex flex-col items-center min-w-[50px]">
                          <span className="font-bold text-slate-800 flex items-center gap-0.5 text-xs">
                            <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                            {program.effectiveness !== undefined && program.effectiveness !== null
                              ? parseFloat(program.effectiveness).toFixed(1)
                              : "0.0"}
                          </span>
                          <span className="text-[10px] text-slate-400 capitalize">
                            {isPortugues ? "eficácia" : "efectividad"}
                          </span>
                        </div>
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
