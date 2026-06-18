import { AlertCircle, AlertTriangle, Info, X } from "lucide-react";

export const AlertCard = ({ alert }) => {
  const config = {
    critical: {
      icon: AlertCircle,
      border: "border-red-200",
      borderl: "border-l-red-500",
      label: "Crítica",
      action: "bg-red-50 text-red-500",
    },
    warning: {
      icon: AlertTriangle,
      border: "border-amber-200",
      borderl: "border-l-amber-500",
      label: "Alerta",
      action: "bg-amber-100 text-amber-500",
    },
    info: {
      icon: Info,
      border: "border-blue-200",
      borderl: "border-l-blue-500",
      label: "Aviso",
      action: "bg-blue-50 text-blue-500",
    },
  };

  const current = config[alert.type];
  const Icon = current.icon;

  return (
    <div
      className={`border-l-4 ${current.border} ${current.borderl} border rounded-lg p-4`}
    >
      <div className="flex justify-between gap-4">
        <div className="flex gap-3 flex-1">
          <div
            className={`p-2 rounded-lg ${current.border} ${current.action} h-fit`}
          >
            <Icon className="w-4 h-4" />
          </div>

          <div className="flex-1">
            <h3 className="font-semibold text-slate-800">{alert.title}</h3>

            <p className="text-sm text-slate-500 mt-1">{alert.description}</p>

            <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 mt-3">
              <span>{alert.region}</span>
              <span>{alert.date}</span>
            </div>

            <div className="flex flex-wrap gap-2 mt-4">
              <button
                className={`px-3 py-1 rounded-md text-xs border ${current.border} ${current.action}`}
              >
                → {alert.action}
              </button>

              <button className="px-3 py-1 rounded-md border text-xs text-slate-600 hover:bg-slate-50">
                Marcar resuelto
              </button>
            </div>
          </div>
        </div>

        <div className="flex flex-col justify-between items-end">
          <span
            className={`px-2 py-1 rounded-full text-xs font-medium ${current.action}`}
          >
            {current.label}
          </span>

          <button>
            <X className="w-4 h-4 text-slate-400" />
          </button>
        </div>
      </div>
    </div>
  );
};
