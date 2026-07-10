import { useLanguage } from "../context/useLenguage";

export function LanguageSwitch() {
  const { language, toggleLanguage } = useLanguage();

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-200 transition"
    >
      <span className={language === "es" ? "text-slate-900" : "text-slate-400"}>
        ES
      </span>
      <span className="text-slate-300">/</span>
      <span className={language === "pt" ? "text-slate-900" : "text-slate-400"}>
        PT
      </span>
    </button>
  );
}
