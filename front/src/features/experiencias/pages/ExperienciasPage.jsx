import { 
  Star, 
  Users, 
  Copy, 
  Rocket, 
  Lightbulb, 
  Handshake, 
  Monitor, 
  Activity, 
  Plus, 
  MapPin, 
  User 
} from 'lucide-react'

// Mock Data
const indicatorMetrics = [
  { 
    label: 'Experiencias activas', 
    value: '6', 
    icon: Star, 
    iconColor: 'text-amber-500', 
    bgColor: 'bg-amber-50 border-amber-100' 
  },
  { 
    label: 'Beneficiarios totales', 
    value: '66K', 
    icon: Users, 
    iconColor: 'text-slate-600', 
    bgColor: 'bg-slate-50 border-slate-100' 
  },
  { 
    label: 'Replicables', 
    value: '5', 
    icon: Copy, 
    iconColor: 'text-blue-600', 
    bgColor: 'bg-blue-50 border-blue-100' 
  },
  { 
    label: 'Alto Impacto', 
    value: '3', 
    icon: Rocket, 
    iconColor: 'text-purple-600', 
    bgColor: 'bg-purple-50 border-purple-100' 
  }
]

const categoryMetrics = [
  {
    title: 'Innovación Social',
    count: '14',
    icon: Lightbulb,
    iconColor: 'text-amber-500 bg-amber-50 border-amber-100',
    barColor: 'bg-blue-600'
  },
  {
    title: 'Economía Solidaria',
    count: '9',
    icon: Handshake,
    iconColor: 'text-emerald-600 bg-emerald-50 border-emerald-100',
    barColor: 'bg-emerald-500'
  },
  {
    title: 'Digital para Todos',
    count: '11',
    icon: Monitor,
    iconColor: 'text-purple-600 bg-purple-50 border-purple-100',
    barColor: 'bg-purple-500'
  },
  {
    title: 'Salud Comunitaria',
    count: '6',
    icon: Activity,
    iconColor: 'text-pink-600 bg-pink-50 border-pink-100',
    barColor: 'bg-pink-500'
  }
]

const featuredExperiences = [
  {
    id: 1,
    title: 'Laboratorio de Innovación Social',
    impact: 'Alto Impacto',
    impactColor: 'bg-green-50 text-green-700 border-green-200',
    replicable: true,
    region: 'Centro',
    beneficiarios: '24.000 beneficiarios',
    leader: 'Ana Carvalho',
    score: '8.7/10',
    barColor: 'bg-green-500'
  },
  {
    id: 2,
    title: 'Red de Guardianes Digitales',
    impact: 'Alto Impacto',
    impactColor: 'bg-green-50 text-green-700 border-green-200',
    replicable: true,
    region: 'Noreste',
    beneficiarios: '15.600 beneficiarios',
    leader: 'Marco Silva',
    score: '8.7/10',
    barColor: 'bg-green-500'
  },
  {
    id: 3,
    title: 'Mercados Comunitarios Inclusivos',
    impact: 'Impacto medio',
    impactColor: 'bg-amber-50 text-amber-700 border-amber-200',
    replicable: true,
    region: 'Occidente',
    beneficiarios: '8.900 beneficiarios',
    leader: 'Rosa Mendez',
    score: '6.2/10',
    barColor: 'bg-amber-500'
  },
  {
    id: 4,
    title: 'Brigadas de Salud Mental Rural',
    impact: 'Impacto medio',
    impactColor: 'bg-amber-50 text-amber-700 border-amber-200',
    replicable: false,
    region: 'Sur',
    beneficiarios: '4.200 beneficiarios',
    leader: 'Carlos Torres',
    score: '6.2/10',
    barColor: 'bg-amber-500'
  },
  {
    id: 5,
    title: 'Cooperativa Digital Agraria',
    impact: 'Bajo impacto',
    impactColor: 'bg-red-50 text-red-700 border-red-200',
    replicable: true,
    region: 'Noroeste',
    beneficiarios: '1.800 beneficiarios',
    leader: 'Lucia Ferreira',
    score: '4.1/10',
    barColor: 'bg-red-500'
  },
  {
    id: 6,
    title: 'Centro de Empleabilidad Juvenil',
    impact: 'Alto Impacto',
    impactColor: 'bg-green-50 text-green-700 border-green-200',
    replicable: true,
    region: 'Oriente',
    beneficiarios: '11.200 beneficiarios',
    leader: 'Pedro Gomes',
    score: '8.7/10',
    barColor: 'bg-green-500'
  }
]

function ExperienciasPage() {
  return (
    <div className="space-y-6">
      {/* Title & Header Row */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Star className="w-5 h-5 text-amber-500" />
            <span>Experiencias Estructurantes</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">Iniciativas exitosas replicables y proyectos comunitarios de alto impacto</p>
        </div>
        <div>
          <button className="flex items-center gap-1.5 bg-[#2563eb] hover:bg-blue-600 text-white font-medium text-xs px-4 py-2.5 rounded-lg transition-colors cursor-pointer shadow-sm">
            <Plus className="w-4 h-4" />
            <span>Registrar experiencia</span>
          </button>
        </div>
      </div>

      {/* Top Indicators Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {indicatorMetrics.map((item, idx) => {
          const Icon = item.icon
          return (
            <div key={idx} className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center border ${item.bgColor} ${item.iconColor}`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div className="mt-3">
                <h4 className="text-2xl font-bold text-slate-800 tracking-tight">{item.value}</h4>
                <p className="text-xs text-slate-500 mt-1 font-semibold">{item.label}</p>
              </div>
            </div>
          )
        })}
      </div>

      {/* Categories Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {categoryMetrics.map((item, idx) => {
          const Icon = item.icon
          return (
            <div key={idx} className="bg-white border border-slate-200 rounded-xl p-4 pb-5 flex flex-col justify-between relative overflow-hidden hover:shadow-sm transition-shadow">
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center border ${item.iconColor}`}>
                  <Icon className="w-4.5 h-4.5" />
                </div>
                <span className="text-xs font-bold text-slate-700">{item.title}</span>
              </div>
              <div className="mt-4">
                <span className="text-2xl font-bold text-slate-800">{item.count}</span>
                <p className="text-[10px] text-slate-400 font-semibold mt-0.5">Iniciativas activas</p>
              </div>
              {/* Bottom Colored Indicator Line */}
              <div className={`absolute bottom-0 left-0 right-0 h-1 ${item.barColor}`} />
            </div>
          )
        })}
      </div>

      {/* Featured Experiences Grid */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-slate-800">Experiencias Destacadas</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredExperiences.map((experience) => (
            <div key={experience.id} className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
              <div>
                {/* Badges Row */}
                <div className="flex items-center justify-between">
                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${experience.impactColor}`}>
                    {experience.impact}
                  </span>
                  {experience.replicable && (
                    <span className="flex items-center gap-1 text-[10px] text-slate-400 font-semibold bg-slate-50 px-2 py-0.5 rounded border border-slate-150">
                      <Copy className="w-3 h-3" />
                      <span>Replicable</span>
                    </span>
                  )}
                </div>

                {/* Title */}
                <h4 className="text-sm font-bold text-slate-800 mt-3.5 leading-snug">
                  {experience.title}
                </h4>

                {/* Details List */}
                <div className="mt-4 space-y-2">
                  <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    <span>{experience.region}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                    <Users className="w-3.5 h-3.5 text-slate-400" />
                    <span>{experience.beneficiarios}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                    <User className="w-3.5 h-3.5 text-slate-400" />
                    <span>Liderado por {experience.leader}</span>
                  </div>
                </div>
              </div>

              {/* Progress Indicator */}
              <div className="mt-5 pt-3.5 border-t border-slate-100">
                <div className="flex items-center justify-between text-[10px] font-bold text-slate-500 mb-1.5">
                  <span>Índice de impacto</span>
                  <span className="text-slate-800">{experience.score}</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${experience.barColor}`} 
                    style={{ width: `${parseFloat(experience.score) * 10}%` }} 
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Featured Success Case Bottom Banner (Without Star Icon) */}
      <div className="bg-gradient-to-r from-teal-800 to-teal-700 text-white rounded-xl p-6 shadow-sm border border-teal-900/50">
        <span className="text-[10px] font-bold text-teal-200 tracking-wider uppercase">
          Caso de Éxito Destacado
        </span>
        <h4 className="text-base font-bold mt-1.5 text-white">
          Laboratorio de Innovación Social — Centro
        </h4>
        <p className="text-xs text-teal-100/90 leading-relaxed mt-2 max-w-3xl font-medium">
          Iniciativa que conecta a 24.000 ciudadanos con servicios digitales, formación y empleabilidad. Modelo replicado en 4 regiones con tasas de éxito superiores al 80%.
        </p>
        
        {/* Success Metrics */}
        <div className="flex flex-wrap items-center gap-8 mt-5 pt-4 border-t border-teal-600/30">
          <div>
            <h5 className="text-xl font-bold text-white leading-none">24K</h5>
            <span className="text-[10px] text-teal-200/90 font-semibold mt-1 inline-block">Beneficiarios</span>
          </div>
          <div>
            <h5 className="text-xl font-bold text-white leading-none">4</h5>
            <span className="text-[10px] text-teal-200/90 font-semibold mt-1 inline-block">Regiones</span>
          </div>
          <div>
            <h5 className="text-xl font-bold text-white leading-none">80%+</h5>
            <span className="text-[10px] text-teal-200/90 font-semibold mt-1 inline-block">Tasa de éxito</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ExperienciasPage
