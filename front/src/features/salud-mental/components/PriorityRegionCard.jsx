export const PriorityRegionCard = ({
  region,
  status,
  mentalHealthIndex,
  connectivity,
  comments,
}) => {
  let borderColor = "";
  let barActiveColor = "";
  let barColor = "";
  let textColor = "";

  switch (status) {
    case "ALERTA":
      borderColor = "border-yellow-200";
      barActiveColor = "bg-amber-500";
      barColor = "bg-yellow-100";
      textColor = "text-amber-600";
      break;
    case "CRITICO":
      borderColor = "border-red-200";
      barActiveColor = "bg-red-500";
      barColor = "bg-red-100";
      textColor = "text-red-500";
      break;
  }

  return (
    <div className={`rounded-lg border p-3 ${borderColor}`}>
      <div className="flex items-start justify-between">
        <h3 className="text-sm font-semibold">{region}</h3>
        <span
          className={`text-xs px-2 py-0.5 rounded-full ${barColor} font-bold ${textColor}`}
        >
          {status}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-6">
        <div>
          <p className="text-xs text-slate-400">Índice Mental</p>
          <p className={`text-lg font-bold ${textColor}`}>
            {mentalHealthIndex}/5
          </p>

          <div className={`mt-3 h-1.5 w-full rounded-full ${barColor}`}>
            <div
              className={`h-1.5 rounded-full ${barActiveColor}`}
              style={{ width: `${(mentalHealthIndex / 5) * 100}%` }}
            />
          </div>
        </div>
        <div>
          <p className="text-xs text-slate-400">Conectividad</p>
          <p className="text-lg font-bold text-slate-700">{connectivity}%</p>
        </div>
      </div>

      <p className="mt-4 text-xs text-slate-500">{comments}</p>
    </div>
  );
};
