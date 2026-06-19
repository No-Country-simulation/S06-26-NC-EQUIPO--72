import { useState } from "react";
import { Settings, User, Bell, Globe, Check, Loader2 } from "lucide-react";

export default function ConfiguracionPage() {
  // Card 1: User Profile State
  const [profile, setProfile] = useState({
    nombreCompleto: "Ana Rodrigues",
    cargo: "Analista Senior de Política Pública",
    institucion: "Ministerio de Desarrollo Social",
    correoElectronico: "ana.rodrigues@governo.gob.br",
  });

  // Card 2: Notifications State
  const [notifications, setNotifications] = useState({
    alertasCriticas: true,
    resumenSemanal: true,
    tiempoReal: false,
    informesAuto: true,
  });

  // Card 3: Language & Region State
  const [locale, setLocale] = useState({
    idioma: "Español",
    zonaHoraria: "America/Sao_Paulo (UTC-3)",
    formatoFecha: "DD/MM/AAAA",
  });

  // Saving states feedback
  const [saveStatus, setSaveStatus] = useState({
    profile: "idle", // 'idle' | 'saving' | 'saved'
    notifications: "idle",
    locale: "idle",
  });

  // Profile inputs handler
  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  };

  // Locale inputs handler
  const handleLocaleChange = (e) => {
    const { name, value } = e.target;
    setLocale((prev) => ({ ...prev, [name]: value }));
  };

  // Switch toggle handler
  const toggleNotification = (key) => {
    setNotifications((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  // Form submit handler with micro-animations
  const triggerSave = (section) => {
    setSaveStatus((prev) => ({ ...prev, [section]: "saving" }));
    setTimeout(() => {
      setSaveStatus((prev) => ({ ...prev, [section]: "saved" }));
      // Reset back to idle after 1.5s
      setTimeout(() => {
        setSaveStatus((prev) => ({ ...prev, [section]: "idle" }));
      }, 1500);
    }, 600);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
          <Settings className="w-5 h-5 text-slate-600 animate-spin-slow" />
          <span>Configuración</span>
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          Gestione su cuenta, notificaciones y preferencias de la plataforma
        </p>
      </div>

      {/* Configuration Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Card 1: Perfil de Usuario */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 hover:shadow-xs transition-shadow flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            {/* Card Title Header */}
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 shrink-0">
                <User className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-slate-800">
                  Perfil de Usuario
                </h3>
                <p className="text-[10px] text-slate-400 mt-0.5 leading-normal">
                  Nombre, cargo, institución y datos de contacto
                </p>
              </div>
            </div>

            {/* Inputs Block */}
            <div className="space-y-3 pt-2">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Nombre completo
                </label>
                <input
                  type="text"
                  name="nombreCompleto"
                  value={profile.nombreCompleto}
                  onChange={handleProfileChange}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Cargo
                </label>
                <input
                  type="text"
                  name="cargo"
                  value={profile.cargo}
                  onChange={handleProfileChange}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Institución
                </label>
                <input
                  type="text"
                  name="institucion"
                  value={profile.institucion}
                  onChange={handleProfileChange}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Correo electrónico
                </label>
                <input
                  type="email"
                  name="correoElectronico"
                  value={profile.correoElectronico}
                  onChange={handleProfileChange}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>
            </div>
          </div>

          {/* Action Button */}
          <button
            onClick={() => triggerSave("profile")}
            disabled={saveStatus.profile !== "idle"}
            className="w-full flex items-center justify-center gap-1.5 bg-blue-50 hover:bg-blue-100/80 text-blue-600 border border-blue-100/50 font-semibold text-xs py-2.5 rounded-lg transition-all duration-200 cursor-pointer disabled:opacity-80 disabled:pointer-events-none"
          >
            {saveStatus.profile === "saving" && (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Guardando...</span>
              </>
            )}
            {saveStatus.profile === "saved" && (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600 stroke-[3]" />
                <span className="text-emerald-600">¡Guardado con éxito!</span>
              </>
            )}
            {saveStatus.profile === "idle" && <span>Guardar cambios</span>}
          </button>
        </div>

        {/* Card 2: Notificaciones */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 hover:shadow-xs transition-shadow flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            {/* Card Title Header */}
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-orange-50 border border-orange-100 flex items-center justify-center text-orange-600 shrink-0">
                <Bell className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-slate-800">
                  Notificaciones
                </h3>
                <p className="text-[10px] text-slate-400 mt-0.5 leading-normal">
                  Configure alertas, frecuencia y canales de notificación
                </p>
              </div>
            </div>

            {/* Custom Toggle Switch rows */}
            <div className="space-y-4 pt-4">
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-600 font-semibold">
                  Alertas críticas por email
                </span>
                <button
                  type="button"
                  onClick={() => toggleNotification("alertasCriticas")}
                  className={`relative inline-flex h-5.5 w-10 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500/25 ${
                    notifications.alertasCriticas
                      ? "bg-blue-600"
                      : "bg-slate-200"
                  }`}
                >
                  <span
                    className={`pointer-events-none inline-block h-4.5 w-4.5 transform rounded-full bg-white shadow-xs ring-0 transition duration-200 ease-in-out ${
                      notifications.alertasCriticas
                        ? "translate-x-4.5"
                        : "translate-x-0"
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-600 font-semibold">
                  Resumen semanal
                </span>
                <button
                  type="button"
                  onClick={() => toggleNotification("resumenSemanal")}
                  className={`relative inline-flex h-5.5 w-10 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500/25 ${
                    notifications.resumenSemanal
                      ? "bg-blue-600"
                      : "bg-slate-200"
                  }`}
                >
                  <span
                    className={`pointer-events-none inline-block h-4.5 w-4.5 transform rounded-full bg-white shadow-xs ring-0 transition duration-200 ease-in-out ${
                      notifications.resumenSemanal
                        ? "translate-x-4.5"
                        : "translate-x-0"
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-600 font-semibold">
                  Notificaciones en tiempo real
                </span>
                <button
                  type="button"
                  onClick={() => toggleNotification("tiempoReal")}
                  className={`relative inline-flex h-5.5 w-10 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500/25 ${
                    notifications.tiempoReal ? "bg-blue-600" : "bg-slate-200"
                  }`}
                >
                  <span
                    className={`pointer-events-none inline-block h-4.5 w-4.5 transform rounded-full bg-white shadow-xs ring-0 transition duration-200 ease-in-out ${
                      notifications.tiempoReal
                        ? "translate-x-4.5"
                        : "translate-x-0"
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-600 font-semibold">
                  Informes automáticos
                </span>
                <button
                  type="button"
                  onClick={() => toggleNotification("informesAuto")}
                  className={`relative inline-flex h-5.5 w-10 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500/25 ${
                    notifications.informesAuto ? "bg-blue-600" : "bg-slate-200"
                  }`}
                >
                  <span
                    className={`pointer-events-none inline-block h-4.5 w-4.5 transform rounded-full bg-white shadow-xs ring-0 transition duration-200 ease-in-out ${
                      notifications.informesAuto
                        ? "translate-x-4.5"
                        : "translate-x-0"
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>

          {/* Action Button */}
          <button
            onClick={() => triggerSave("notifications")}
            disabled={saveStatus.notifications !== "idle"}
            className="w-full flex items-center justify-center gap-1.5 bg-orange-50/70 hover:bg-orange-100/80 text-orange-700 border border-orange-100/50 font-semibold text-xs py-2.5 rounded-lg transition-all duration-200 cursor-pointer disabled:opacity-80 disabled:pointer-events-none"
          >
            {saveStatus.notifications === "saving" && (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Guardando...</span>
              </>
            )}
            {saveStatus.notifications === "saved" && (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600 stroke-[3]" />
                <span className="text-emerald-600">¡Guardado con éxito!</span>
              </>
            )}
            {saveStatus.notifications === "idle" && (
              <span>Guardar cambios</span>
            )}
          </button>
        </div>

        {/* Card 3: Idioma y Región */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 hover:shadow-xs transition-shadow flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            {/* Card Title Header */}
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 shrink-0">
                <Globe className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-slate-800">
                  Idioma y Región
                </h3>
                <p className="text-[10px] text-slate-400 mt-0.5 leading-normal">
                  Idioma de la interfaz y configuración regional
                </p>
              </div>
            </div>

            {/* Inputs Block */}
            <div className="space-y-3 pt-2">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Idioma
                </label>
                <input
                  type="text"
                  name="idioma"
                  value={locale.idioma}
                  onChange={handleLocaleChange}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Zona horaria
                </label>
                <input
                  type="text"
                  name="zonaHoraria"
                  value={locale.zonaHoraria}
                  onChange={handleLocaleChange}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Formato de fecha
                </label>
                <input
                  type="text"
                  name="formatoFecha"
                  value={locale.formatoFecha}
                  onChange={handleLocaleChange}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>
            </div>
          </div>

          {/* Action Button */}
          <button
            onClick={() => triggerSave("locale")}
            disabled={saveStatus.locale !== "idle"}
            className="w-full flex items-center justify-center gap-1.5 bg-emerald-50 hover:bg-emerald-100/80 text-emerald-700 border border-emerald-100/50 font-semibold text-xs py-2.5 rounded-lg transition-all duration-200 cursor-pointer disabled:opacity-80 disabled:pointer-events-none"
          >
            {saveStatus.locale === "saving" && (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Guardando...</span>
              </>
            )}
            {saveStatus.locale === "saved" && (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600 stroke-[3]" />
                <span className="text-emerald-600">¡Guardado con éxito!</span>
              </>
            )}
            {saveStatus.locale === "idle" && <span>Guardar cambios</span>}
          </button>
        </div>
      </div>

      {/* System Information Panel */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-xs transition-shadow">
        <h3 className="text-xs font-bold text-slate-800 mb-4">
          Información del Sistema
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8">
          <div>
            <p className="text-[10px] text-slate-400 font-semibold">
              Versión APP BIT
            </p>
            <p className="text-xs font-bold text-slate-700 mt-1">v2.4.1</p>
          </div>

          <div>
            <p className="text-[10px] text-slate-400 font-semibold">
              Última actualización
            </p>
            <p className="text-xs font-bold text-slate-700 mt-1">10 dic 2024</p>
          </div>

          <div>
            <p className="text-[10px] text-slate-400 font-semibold">
              Base de datos
            </p>
            <p className="text-xs font-bold text-slate-700 mt-1">Q4 2024</p>
          </div>

          <div>
            <p className="text-[10px] text-slate-400 font-semibold">Acceso</p>
            <p className="text-xs font-bold text-slate-700 mt-1">
              Administrador
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
