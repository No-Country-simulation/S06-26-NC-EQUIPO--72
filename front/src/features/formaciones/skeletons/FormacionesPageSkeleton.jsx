import { Skeleton } from "@/components/ui/skeleton";

export const BarChartSkeleton = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      {/* Skeleton Bar Chart */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="h-5 w-60 bg-slate-200 rounded-md" />
        </div>

        <div className="flex-1 mt-6">
          <div className="h-[240px] flex items-end justify-between gap-3 px-4">
            {[
              [80, 55],
              [120, 90],
              [70, 110],
              [150, 80],
              [90, 130],
              [110, 60],
              [140, 100],
            ].map(([a, b], index) => (
              <div key={index} className="flex items-end gap-1 flex-1">
                <div
                  className="w-3 bg-slate-200 rounded-t"
                  style={{ height: `${a}px` }}
                />
                <div
                  className="w-3 bg-slate-300 rounded-t"
                  style={{ height: `${b}px` }}
                />
              </div>
            ))}
          </div>

          {/* Labels */}
          <div className="flex justify-between mt-4 px-4">
            {Array.from({ length: 7 }).map((_, i) => (
              <div key={i} className="h-2 w-8 bg-slate-200 rounded" />
            ))}
          </div>
        </div>
      </div>

      {/* Skeleton Pie Chart */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col">
        <div className="border-b border-slate-100 pb-3">
          <div className="h-5 w-32 bg-slate-200 rounded-md" />
        </div>

        <div className="flex flex-col items-center gap-6 mt-6">
          {/* Donut */}
          <div className="relative w-[125px] h-[125px]">
            <div className="absolute inset-0 rounded-full border-[18px] border-slate-200" />
            <div className="absolute inset-[36px] rounded-full bg-white" />
          </div>

          {/* Legend */}
          <div className="w-full space-y-3">
            {Array.from({ length: 5 }).map((_, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded bg-slate-200" />
                  <div className="h-3 w-24 bg-slate-200 rounded" />
                </div>

                <div className="h-3 w-8 bg-slate-200 rounded" />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export const ProgramListSkeleton = () => {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-xs">
        <thead>
          <tr className="border-b border-slate-100 h-10">
            <th className="py-2 pr-4 pl-1 text-left">
              <Skeleton className="h-3 w-20" />
            </th>
            <th className="py-2 px-4 text-left">
              <Skeleton className="h-3 w-24" />
            </th>
            <th className="py-2 px-4 text-left">
              <Skeleton className="h-3 w-24" />
            </th>
            <th className="py-2 px-4 text-left">
              <Skeleton className="h-3 w-20" />
            </th>
            <th className="py-2 px-4 text-left">
              <Skeleton className="h-3 w-16" />
            </th>
            <th className="py-2 pl-4 pr-1"></th>
          </tr>
        </thead>

        <tbody>
          {Array.from({ length: 6 }).map((_, index) => (
            <tr key={index} className="border-b border-slate-100 h-14">
              {/* Programa */}
              <td className="py-3 pr-4 pl-1">
                <Skeleton className="h-4 w-52" />
              </td>

              {/* Región */}
              <td className="py-3 px-4">
                <div className="flex items-center gap-2">
                  <Skeleton className="w-4 h-4 rounded-full" />
                  <Skeleton className="h-4 w-24" />
                </div>
              </td>

              {/* Beneficiarios */}
              <td className="py-3 px-4">
                <div className="flex items-center gap-2">
                  <Skeleton className="w-4 h-4 rounded-full" />
                  <Skeleton className="h-4 w-16" />
                </div>
              </td>

              {/* Cobertura */}
              <td className="py-3 px-4">
                <div className="flex flex-col gap-2">
                  <Skeleton className="h-4 w-10" />
                  <Skeleton className="h-1.5 w-24 rounded-full" />
                </div>
              </td>

              {/* Estado */}
              <td className="py-3 px-4">
                <Skeleton className="h-6 w-20 rounded-full" />
              </td>

              {/* Acción */}
              <td className="py-3 pl-4 pr-1 text-right">
                <Skeleton className="h-8 w-8 rounded-md ml-auto" />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
