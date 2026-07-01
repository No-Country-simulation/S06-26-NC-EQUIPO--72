import { useState, useMemo } from "react";
import { 
  BarChart3, 
  Map, 
  Bot, 
  Wifi, 
  ArrowRight, 
  ShieldCheck, 
  Lock, 
  FileText,
  MapPin,
  TrendingUp,
  Brain,
  Check,
  Globe
} from "lucide-react";
import { useMapsIndicators } from "../hooks/useMaps";
import { generarMapaOrganico } from "../utils/organicMap";
import { formatClusterName } from "@/shared/utils/format";

// Datos estáticos para recrear el mapa 
const MOCK_MAP_REGIONS = [
  { cluster: "CENTRO_HISTORICO", congestionamento_medio: 0.72, n_usuarios: 58000 },
  { cluster: "NORTE_ILHA", congestionamento_medio: 0.42, n_usuarios: 62000 },
  { cluster: "ESTREITO_CAPOEIRAS", congestionamento_medio: 0.25, n_usuarios: 65000 },
  { cluster: "AEROPORTO_HLZ", congestionamento_medio: 0.52, n_usuarios: 58000 },
  { cluster: "CBD_BEIRAMAR", congestionamento_medio: 0.78, n_usuarios: 82000 },
  { cluster: "SC401_CORREDOR", congestionamento_medio: 0.65, n_usuarios: 74000 },
  { cluster: "TRINDADE", congestionamento_medio: 0.98, n_usuarios: 54000 },
  { cluster: "Canasvieiras", congestionamento_medio: 0.54, n_usuarios: 54000 },
  { cluster: "Rio Tavares", congestionamento_medio: 0.80, n_usuarios: 54000 },

];

const fillColors = {
  critico: "#f87171", 
  alerta: "#fcd34d",    
  bueno: "#86efac",     
  optimo: "#93c5fd",    
};

const getStatusFromCongestion = (value) => {
  if (value >= 0.75) return fillColors.optimo;
  if (value >= 0.55) return fillColors.bueno;
  if (value >= 0.35) return fillColors.alerta;
  return fillColors.critico;
};

export default function LandingPage({ onEnterDemo }) {
  const regionesQuery = useMapsIndicators("EMPLEO");
  const totalRegiones = regionesQuery.data?.regiones?.length || 16;
  const regionesCompletas = useMemo(() => {
    return generarMapaOrganico(MOCK_MAP_REGIONS);
  }, []);

  const regionTextCenter = useMemo(() => {
    return regionesCompletas.map((region) => {
      const coords = region.points
        .split(" ")
        .map((p) => p.split(",").map(Number));
      const centerPositionX =
        coords.reduce((sum, [x]) => sum + x, 0) / coords.length;
      const centerPositionY =
        coords.reduce((sum, [, y]) => sum + y, 0) / coords.length;
      return { ...region, centerPositionX, centerPositionY };
    });
  }, [regionesCompletas]);

  return (
    <div className="min-h-screen bg-slate-50 text-[#334155] font-sans flex flex-col justify-between selection:bg-blue-150 overflow-x-hidden">
      
      {/* 1. Header / Navbar */}
      <header className="w-full bg-white border-b border-slate-200 h-16 px-6 lg:px-16 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-[#2563eb] flex items-center justify-center text-white shrink-0 shadow-md shadow-blue-500/10">
            <BarChart3 className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-slate-800 leading-none tracking-wider text-sm">APP BIT</h1>
            <p className="text-[10px] text-slate-400 mt-0.5 font-medium">Inteligencia Pública</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <span className="hidden sm:flex items-center gap-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold px-2.5 py-1 rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            Demo disponible
          </span>
        </div>
      </header>

      {/* 2. Hero Section */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 lg:px-16 py-8 lg:py-14 flex flex-col lg:flex-row items-center justify-between gap-12">
        
        {/* Lado Izquierdo */}
        <div className="w-full lg:w-1/2 flex flex-col gap-6 lg:gap-8">
          <div className="space-y-4">
            <h2 className="text-3xl lg:text-5xl font-extrabold text-slate-800 tracking-tight leading-tight">
              Panel de Datos <br />
              <span className="bg-gradient-to-r from-blue-600 to-emerald-500 bg-clip-text text-transparent">Públicos</span>
            </h2>
            <p className="text-slate-500 text-sm lg:text-base leading-relaxed max-w-lg">
              Una plataforma inteligente para visualizar indicadores públicos, analizar información territorial y apoyar la toma de decisiones basada en datos.
            </p>
            <p className="text-slate-400 text-xs leading-relaxed max-w-md">
              Explore mapas interactivos, indicadores sociales y consultas asistidas por IA en una experiencia diseñada para gestores públicos y analistas.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
            <button 
              onClick={onEnterDemo}
              className="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 hover:shadow-lg hover:shadow-blue-500/20 text-white font-bold text-sm px-6 py-3 rounded-xl shadow-md transition-all cursor-pointer group"
            >
              <span>Acceder a la Demo</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </button>
            <span className="text-slate-400 text-[10px] font-semibold sm:ml-2">
              No requiere inicio de sesión.
            </span>
          </div>

          {/* Estadísticas */}
          <div className="grid grid-cols-3 gap-6 pt-6 border-t border-slate-200 max-w-md w-full">
            <div>
              <p className="text-2xl lg:text-3xl font-extrabold text-slate-800 tracking-tight">{totalRegiones}</p>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mt-1">Regiones analizadas</p>
            </div>
            <div>
              <p className="text-2xl lg:text-3xl font-extrabold text-slate-800 tracking-tight">12+</p>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mt-1">Indicadores públicos</p>
            </div>
            <div>
              <p className="text-2xl lg:text-3xl font-extrabold text-slate-800 tracking-tight">100%</p>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mt-1">Datos abiertos</p>
            </div>
          </div>
        </div>

        {/* Lado Derecho */}
        <div className="w-full lg:w-1/2 flex justify-center lg:justify-end">
          <div className="relative w-full max-w-[500px] aspect-[4/3] bg-white border border-slate-200/80 shadow-2xl rounded-2xl p-4 flex flex-col justify-between overflow-hidden select-none hover:shadow-blue-500/5 transition-all duration-500">
            
            {/* Header del panel simulado */}
            <div className="flex items-center justify-between border-b border-slate-100 pb-2.5 shrink-0 z-10">
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-xs font-bold text-slate-700">Mapa de Inclusión Social</span>
              </div>
              <div className="flex gap-1">
                <span className="text-[9px] bg-blue-600 text-white font-bold px-2 py-0.5 rounded-md shadow-sm">Empleo</span>
                <span className="text-[9px] bg-slate-50 text-slate-500 border border-slate-200 font-semibold px-2 py-0.5 rounded-md">Conectividad</span>
                <span className="text-[9px] bg-slate-50 text-slate-500 border border-slate-200 font-semibold px-2 py-0.5 rounded-md">Salud</span>
              </div>
            </div>

            {/* Simulación del mapa estático (SVG con los mismos polígonos) */}
            <div className="flex-1 w-full relative flex items-center justify-center p-2 min-h-0">
              <svg 
                viewBox="0 0 700 450" 
                className="w-full h-full object-contain filter drop-shadow-sm opacity-90 scale-105"
              >
                {regionTextCenter.map((region) => {
                  const fillColor = getStatusFromCongestion(region.congestionamento_medio);
                  return (
                    <g key={region.cluster}>
                      <polygon
                        points={region.points}
                        fill={fillColor}
                        stroke="#fff"
                        strokeWidth="3.5"
                      />
                      <text
                        x={region.centerPositionX}
                        y={region.centerPositionY - 5}
                        textAnchor="middle"
                        fontSize="9"
                        fontWeight="800"
                        fill="#0f172a"
                      >
                        {formatClusterName(region.cluster)}
                      </text>
                      <text
                        x={region.centerPositionX}
                        y={region.centerPositionY + 10}
                        textAnchor="middle"
                        fontSize="11"
                        fontWeight="900"
                        fill="#0f172a"
                      >
                        {`${Math.round(region.congestionamento_medio * 100)}%`}
                      </text>
                    </g>
                  );
                })}
              </svg>

              {/* OVERLAY 1: Tasa Empleo (Flotante arriba derecha) */}
              <div className="hidden sm:flex absolute top-4 right-4 bg-white/95 backdrop-blur-xs border border-slate-100 rounded-xl p-2.5 shadow-lg flex-col gap-0.5 pointer-events-none scale-90 sm:scale-100 origin-top-right z-20">
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wide">Tasa Empleo</span>
                <span className="text-base font-extrabold text-slate-800 tracking-tight">68.4%</span>
                <span className="text-[9px] text-emerald-600 font-bold flex items-center gap-0.5">
                  <TrendingUp className="w-2.5 h-2.5" />  2.3% <span className="text-slate-400 font-normal">vs mes ant.</span>
                </span>
              </div>

              {/* OVERLAY 2: Lista de Indicadores (Flotante izquierda) */}
              <div className="hidden sm:flex absolute top-8 left-4 bg-white/95 backdrop-blur-xs border border-slate-100 rounded-xl p-2.5 shadow-lg flex-col gap-1.5 pointer-events-none scale-90 sm:scale-100 origin-top-left z-20 w-28">
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wide">Indicadores</span>
                <div className="space-y-1 text-[9px] font-bold">
                  <div className="flex justify-between text-blue-600">
                    <span>Empleo</span>
                    <span>68%</span>
                  </div>
                  <div className="flex justify-between text-indigo-500">
                    <span>Digital</span>
                    <span>49%</span>
                  </div>
                  <div className="flex justify-between text-rose-500">
                    <span>Salud M.</span>
                    <span>62%</span>
                  </div>
                </div>
              </div>

              {/* OVERLAY 3: Conectividad (Flotante abajo izquierda) */}
              <div className="hidden sm:flex absolute bottom-4 left-4 bg-white/95 backdrop-blur-xs border border-slate-100 rounded-xl p-2.5 shadow-lg flex-col gap-1 pointer-events-none scale-90 sm:scale-100 origin-bottom-left z-20 w-32">
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wide">Conectividad</span>
                <span className="text-sm font-extrabold text-slate-800">54.2%</span>
                <div className="w-full bg-slate-100 h-1 rounded-full overflow-hidden">
                  <div className="bg-emerald-500 h-full rounded-full" style={{ width: "54.2%" }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* 3. Bottom Features Grid */}
      <section className="bg-slate-50/50 border-t border-slate-200 py-8 lg:py-12 shrink-0">
        <div className="max-w-7xl mx-auto px-6 lg:px-16 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          
          {/* Card 1 */}
          <div className="flex flex-col gap-2.5 p-5 rounded-2xl bg-white border border-slate-200 hover:border-slate-300 hover:shadow-sm transition-all duration-300">
            <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center shrink-0">
              <Map className="w-4 h-4" />
            </div>
            <h4 className="text-xs font-bold text-slate-800">Mapas interactivos</h4>
            <p className="text-[10px] text-slate-400 font-medium leading-relaxed">
              Visualice indicadores territoriales con capas de datos geolocalizados por región.
            </p>
          </div>

          {/* Card 2 */}
          <div className="flex flex-col gap-2.5 p-5 rounded-2xl bg-white border border-slate-200 hover:border-slate-300 hover:shadow-sm transition-all duration-300">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 border border-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
              <BarChart3 className="w-4 h-4" />
            </div>
            <h4 className="text-xs font-bold text-slate-800">Analítica avanzada</h4>
            <p className="text-[10px] text-slate-400 font-medium leading-relaxed">
              Gráficos y comparativas regionales en tiempo real diseñados para decisores públicos.
            </p>
          </div>

          {/* Card 3 */}
          <div className="flex flex-col gap-2.5 p-5 rounded-2xl bg-white border border-slate-200 hover:border-slate-300 hover:shadow-sm transition-all duration-300">
            <div className="w-8 h-8 rounded-lg bg-indigo-50 border border-indigo-100 text-indigo-600 flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <h4 className="text-xs font-bold text-slate-800">Asistente con IA</h4>
            <p className="text-[10px] text-slate-400 font-medium leading-relaxed">
              Consultas y reportes en lenguaje natural impulsados por inteligencia artificial integrada.
            </p>
          </div>

          {/* Card 4 */}
          <div className="flex flex-col gap-2.5 p-5 rounded-2xl bg-white border border-slate-200 hover:border-slate-300 hover:shadow-sm transition-all duration-300">
            <div className="w-8 h-8 rounded-lg bg-rose-50 border border-rose-100 text-rose-600 flex items-center justify-center shrink-0">
              <Wifi className="w-4 h-4" />
            </div>
            <h4 className="text-xs font-bold text-slate-800">Conectividad digital</h4>
            <p className="text-[10px] text-slate-400 font-medium leading-relaxed">
              Brechas de infraestructura, cobertura celular y estrategias de inclusión social.
            </p>
          </div>
        </div>
      </section>

      {/* 4. Footer */}
      <footer className="w-full bg-slate-900 text-slate-400 py-6 px-6 lg:px-16 border-t border-slate-800 shrink-0">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-[10px]">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center text-white shrink-0">
              <BarChart3 className="w-4 h-4" />
            </div>
            <div>
              <p className="font-bold text-slate-100 uppercase tracking-wider">APP BIT</p>
              <p className="text-[9px] text-slate-500 font-medium mt-0.5">Plataforma de Inteligencia Pública</p>
            </div>
          </div>

          <div className="text-slate-500 font-semibold select-none">
            © 2026 APP BIT — v1.4.1
          </div>
        </div>
      </footer>

    </div>
  );
}
