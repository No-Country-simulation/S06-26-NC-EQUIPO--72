import { Skeleton } from "@/components/ui/skeleton";

export const BarChartDataSkeleton = () => {
  return (
    <div className="grid grid-cols-1 gap-6">
      <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <Skeleton className="h-5 w-72" />
          <Skeleton className="h-7 w-32 rounded-lg" />
        </div>

        {/* Chart */}
        <div className="flex-1 mt-4 flex items-end justify-between h-[240px] px-3">
          {[
            [110, 85],
            [170, 120],
            [140, 95],
            [200, 155],
            [125, 80],
            [180, 135],
          ].map(([left, right], index) => (
            <div key={index} className="flex flex-col items-center gap-2">
              <div className="flex items-end gap-1 h-[200px]">
                <Skeleton
                  className="w-5 rounded-sm"
                  style={{ height: `${left}px` }}
                />
                <Skeleton
                  className="w-5 rounded-sm"
                  style={{ height: `${right}px` }}
                />
              </div>

              <Skeleton className="h-3 w-10" />
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="mt-4 flex justify-center gap-6">
          <div className="flex items-center gap-2">
            <Skeleton className="w-3 h-3 rounded-sm" />
            <Skeleton className="h-3 w-20" />
          </div>

          <div className="flex items-center gap-2">
            <Skeleton className="w-3 h-3 rounded-sm" />
            <Skeleton className="h-3 w-16" />
          </div>
        </div>
      </div>
    </div>
  );
};

export const HealthIndicatorsCardSkeleton = () => {
  return (
    <div className="grid grid-cols-1">
      {/* Título */}
      <Skeleton className="h-6 w-64 mb-3" />

      <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} className="rounded-lg border border-slate-200 p-3">
            {/* Header */}
            <div className="flex items-start justify-between">
              <Skeleton className="h-5 w-24" />
              <Skeleton className="h-6 w-14 rounded-full" />
            </div>

            {/* Contenido */}
            <div className="mt-4">
              <Skeleton className="h-3 w-20 mb-2" />
              <Skeleton className="h-7 w-16 mb-3" />

              <Skeleton className="h-1.5 w-full rounded-full" />
            </div>

            {/* Mensaje */}
            <div className="mt-4 space-y-2">
              <Skeleton className="h-3 w-full" />
              <Skeleton className="h-3 w-5/6" />
            </div>
          </div>
        ))}
      </section>
    </div>
  );
};
