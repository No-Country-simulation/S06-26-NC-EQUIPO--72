import { Skeleton } from "@/components/ui/skeleton";

export const IndicatorsSkeleton = () => {
  return (
    <>
      {/* KPI Skeletons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.from({ length: 4 }).map((_, idx) => (
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

      {/* Category Skeletons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
        {Array.from({ length: 4 }).map((_, idx) => (
          <div
            key={idx}
            className="relative overflow-hidden bg-white border border-slate-200 rounded-xl p-4 pb-5 flex flex-col justify-between"
          >
            <div className="flex items-center gap-3">
              <Skeleton className="w-8 h-8 rounded-lg" />
              <Skeleton className="h-4 w-28" />
            </div>

            <div className="mt-4 space-y-2">
              <Skeleton className="h-8 w-16" />
              <Skeleton className="h-3 w-24" />
            </div>

            {/* Línea inferior */}
            <Skeleton className="absolute bottom-0 left-0 right-0 h-1 rounded-none" />
          </div>
        ))}
      </div>
    </>
  );
};

export const ExperienciasSkeletons = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: 6 }).map((_, index) => (
        <div
          key={index}
          className="animate-pulse bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between"
        >
          <div>
            {/* Badges */}
            <div className="flex items-center justify-between">
              <div className="h-5 w-20 bg-slate-200 rounded-full" />
              <div className="h-5 w-24 bg-slate-200 rounded-full" />
            </div>

            {/* Title */}
            <div className="mt-4 space-y-2">
              <div className="h-4 w-4/5 bg-slate-200 rounded" />
              <div className="h-4 w-3/5 bg-slate-200 rounded" />
            </div>

            {/* Description */}
            <div className="mt-3 space-y-2">
              <div className="h-3 w-full bg-slate-200 rounded" />
              <div className="h-3 w-5/6 bg-slate-200 rounded" />
            </div>

            {/* Details */}
            <div className="mt-5 space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded-full bg-slate-200" />
                  <div className="h-3 w-32 bg-slate-200 rounded" />
                </div>
              ))}
            </div>
          </div>

          {/* Progress */}
          <div className="mt-5 pt-3.5 border-t border-slate-100">
            <div className="flex items-center justify-between mb-2">
              <div className="h-3 w-24 bg-slate-200 rounded" />
              <div className="h-3 w-8 bg-slate-200 rounded" />
            </div>

            <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-slate-200 rounded-full"
                style={{ width: "70%" }}
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
