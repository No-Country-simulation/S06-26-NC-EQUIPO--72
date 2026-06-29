import { Skeleton } from "@/components/ui/skeleton";

export const BlockMapSkeleton = () => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <Skeleton className="w-5 h-5 rounded" />
            <Skeleton className="h-5 w-52" />
          </div>

          <Skeleton className="h-4 w-20" />
        </div>

        {/* Tabs */}
        <div className="flex items-center gap-2 mt-4">
          <Skeleton className="w-5 h-5 rounded" />

          <Skeleton className="h-8 w-28 rounded-lg" />
          <Skeleton className="h-8 w-24 rounded-lg" />
          <Skeleton className="h-8 w-32 rounded-lg" />
        </div>

        {/* Fake Map */}
        <div className="flex justify-center mt-6">
          <div className="relative w-full max-w-2xl h-[420px] animate-pulse">
            <div className="absolute top-10 left-16 w-32 h-24 bg-slate-200 rounded-3xl rotate-6" />

            <div className="absolute top-5 left-52 w-36 h-28 bg-slate-200 rounded-[30px] -rotate-6" />

            <div className="absolute top-28 left-32 w-44 h-32 bg-slate-200 rounded-[35px]" />

            <div className="absolute top-18 right-20 w-36 h-28 bg-slate-200 rounded-[30px] rotate-12" />

            <div className="absolute top-44 right-36 w-32 h-28 bg-slate-200 rounded-[28px]" />

            <div className="absolute bottom-24 left-20 w-44 h-32 bg-slate-200 rounded-[40px] -rotate-3" />

            <div className="absolute bottom-14 left-72 w-36 h-28 bg-slate-200 rounded-[35px] rotate-6" />

            <div className="absolute bottom-12 right-20 w-40 h-36 bg-slate-200 rounded-[40px]" />
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 border-t border-slate-100 pt-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Skeleton className="h-4 w-14" />

          <Skeleton className="h-4 w-16 rounded-full" />
          <Skeleton className="h-4 w-16 rounded-full" />
          <Skeleton className="h-4 w-16 rounded-full" />
          <Skeleton className="h-4 w-16 rounded-full" />
        </div>
      </div>
    </div>
  );
};
