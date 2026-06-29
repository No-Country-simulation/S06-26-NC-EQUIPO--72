export const BarChartSkeleton = () => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow">
      <div className="space-y-4 animate-pulse">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="h-5 w-64 bg-slate-200 rounded-md" />
        </div>

        {/* Chart */}
        <div className="h-[280px] w-full flex items-end justify-between gap-5 px-6 pt-4">
          {[
            [45, 65],
            [70, 40],
            [55, 55],
            [35, 80],
            [60, 50],
            [50, 70],
            [40, 60],
          ].map(([formal, informal], index) => (
            <div key={index} className="flex flex-col items-center flex-1">
              {/* Stacked Bar */}
              <div className="flex flex-col justify-end h-[220px] w-5 rounded-t overflow-hidden">
                <div
                  className="bg-slate-300"
                  style={{ height: `${formal}px` }}
                />
                <div
                  className="bg-slate-200"
                  style={{ height: `${informal}px` }}
                />
              </div>

              {/* Label */}
              <div className="mt-3 h-2.5 w-8 bg-slate-200 rounded" />
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="flex justify-center gap-6 pt-2">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-slate-300" />
            <div className="h-3 w-14 bg-slate-200 rounded" />
          </div>

          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-slate-200" />
            <div className="h-3 w-16 bg-slate-200 rounded" />
          </div>
        </div>
      </div>
    </div>
  );
};

export const RankingListSkeleton = () => {
  return (
    <div className="animate-pulse bg-white border border-slate-200 rounded-xl p-5">
      {/* Header */}
      <div className="border-b border-slate-100 pb-3 mb-4">
        <div className="h-5 w-64 bg-slate-200 rounded-md" />
      </div>

      {/* Ranking */}
      <div className="divide-y divide-slate-100">
        {Array.from({ length: 6 }).map((_, index) => (
          <div key={index} className="flex items-center gap-4 py-3">
            {/* Ranking */}
            <div className="w-6 h-6 rounded-full bg-slate-200 shrink-0" />

            {/* Content */}
            <div className="flex-1 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              {/* Región */}
              <div className="flex items-center gap-2 w-40">
                <div className="w-4 h-4 rounded-full bg-slate-200 shrink-0" />
                <div className="h-4 w-28 bg-slate-200 rounded" />
              </div>

              {/* Barra */}
              <div className="flex-1 max-w-md mx-0 sm:mx-8">
                <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-slate-200 rounded-full"
                    style={{
                      width: `${40 + index * 10}%`,
                    }}
                  />
                </div>
              </div>

              {/* Valores */}
              <div className="flex items-center gap-6 shrink-0">
                <div className="h-4 w-10 bg-slate-200 rounded" />
                <div className="h-4 w-16 bg-slate-200 rounded" />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
