import { Skeleton } from "@/components/ui/skeleton";

export const BarChartDataSkeleton = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col">
        {/* Header */}
        <div className="border-b border-slate-100 pb-3">
          <Skeleton className="h-5 w-48" />
        </div>

        {/* Chart */}
        <div className="flex-1 mt-4 flex items-end justify-between h-[240px] px-2">
          <Skeleton className="h-28 w-6 rounded-sm" />
          <Skeleton className="h-40 w-6 rounded-sm" />
          <Skeleton className="h-20 w-6 rounded-sm" />
          <Skeleton className="h-52 w-6 rounded-sm" />
          <Skeleton className="h-36 w-6 rounded-sm" />
          <Skeleton className="h-44 w-6 rounded-sm" />
          <Skeleton className="h-30 w-6 rounded-sm" />
        </div>

        {/* Labels */}
        <div className="mt-3 flex justify-between px-2">
          <Skeleton className="h-3 w-8" />
          <Skeleton className="h-3 w-8" />
          <Skeleton className="h-3 w-8" />
          <Skeleton className="h-3 w-8" />
          <Skeleton className="h-3 w-8" />
          <Skeleton className="h-3 w-8" />
          <Skeleton className="h-3 w-8" />
        </div>
      </div>
    </div>
  );
};

export const ListMentorsSkeleton = () => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 border-b border-slate-100 p-4">
        <Skeleton className="h-5 w-56" />
      </div>
      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs table-auto">
          <tbody>
            {Array.from({ length: 5 }).map((_, index) => (
              <tr key={index}>
                {/* Left */}
                <td className="w-full py-4 pl-4">
                  <section className="flex items-center gap-3">
                    <Skeleton className="w-10 h-10 rounded-xl shrink-0" />

                    <div className="flex flex-col gap-2 w-full">
                      <Skeleton className="h-4 w-44" />

                      <div className="flex items-center gap-4">
                        <Skeleton className="h-3 w-20" />
                        <Skeleton className="h-3 w-28" />
                      </div>
                    </div>
                  </section>
                </td>

                {/* Right */}
                <td className="whitespace-nowrap py-4 pr-4">
                  <section className="flex items-center justify-end gap-3">
                    <Skeleton className="h-6 w-14 rounded-full" />

                    <div className="flex flex-col items-center gap-1">
                      <Skeleton className="h-4 w-10" />
                      <Skeleton className="h-3 w-16" />
                    </div>

                    <Skeleton className="w-7 h-7 rounded-md" />
                  </section>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
