import { 
  Calendar, 
  Filter, 
  ArrowUpRight, 
  Send, 
  Briefcase, 
  Bell, 
  FileText, 
  GraduationCap, 
  Activity, 
  Wifi, 
  Users, 
  Heart, 
  Briefcase as JobIcon,
  Bot
} from 'lucide-react'
import { useState } from 'react'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts'
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent
} from '@/components/ui/chart'

function DashboardPage() {
  const [activeMapTab, setActiveMapTab] = useState('empleo')

  const barChartData = [
    { region: 'Noroeste', empleo: 58, conectividad: 38 },
    { region: 'Norte', empleo: 62, conectividad: 45 },
    { region: 'Noreste', empleo: 71, conectividad: 68 },
    { region: 'Occidente', empleo: 65, conectividad: 52 },
    { region: 'Centro', empleo: 82, conectividad: 90 },
    { region: 'Oriente', empleo: 74, conectividad: 72 },
    { region: 'Suroeste', empleo: 49, conectividad: 28 },
    { region: 'Sur', empleo: 54, conectividad: 34 },
    { region: 'Sureste', empleo: 61, conectividad: 44 }
  ]

  const barChartConfig = {
    empleo: {
      label: 'Empleo',
      color: '#2563eb',
    },
    conectividad: {
      label: 'Conectividad',
      color: '#0d9488',
    }
  }

  const lineChartData = [
    { mes: 'Ene', empleo: 64, conectividad: 49, inclusion: 44 },
    { mes: 'Feb', empleo: 65, conectividad: 50, inclusion: 45 },
    { mes: 'Mar', empleo: 66, conectividad: 51, inclusion: 46 },
    { mes: 'Abr', empleo: 65, conectividad: 52, inclusion: 47 },
    { mes: 'May', empleo: 67, conectividad: 53, inclusion: 48 },
    { mes: 'Jun', empleo: 68, conectividad: 54, inclusion: 48 },
    { mes: 'Jul', empleo: 67, conectividad: 54, inclusion: 49 },
    { mes: 'Ago', empleo: 69, conectividad: 55, inclusion: 49 },
    { mes: 'Sep', empleo: 70, conectividad: 55, inclusion: 50 },
    { mes: 'Oct', empleo: 69, conectividad: 54, inclusion: 50 },
    { mes: 'Nov', empleo: 70, conectividad: 55, inclusion: 51 },
    { mes: 'Dic', empleo: 71, conectividad: 56, inclusion: 51 }
  ]

  const lineChartConfig = {
    empleo: {
      label: 'Empleo',
      color: '#2563eb',
    },
    conectividad: {
      label: 'Conectividad',
      color: '#0d9488',
    },
    inclusion: {
      label: 'Inclusión',
      color: '#a855f7',
    }
  }

  const pieChartData = [
    { name: 'Con acceso digital', value: 49, color: '#2563eb' },
    { name: 'Brecha urbana-rural', value: 28, color: '#f97316' },
    { name: 'Sin conectividad', value: 23, color: '#ef4444' }
  ]

  const pieChartConfig = {
    acceso: {
      label: 'Con acceso digital',
      color: '#2563eb',
    },
    brecha: {
      label: 'Brecha urbana-rural',
      color: '#f97316',
    },
    sinConectividad: {
      label: 'Sin conectividad',
      color: '#ef4444',
    }
  }

  const saludMentalData = [
    { region: 'Noroeste', value: '2.9/5', percent: '58%', color: 'bg-amber-500' },
    { region: 'Norte', value: '3.2/5', percent: '64%', color: 'bg-amber-500' },
    { region: 'Noreste', value: '3.8/5', percent: '76%', color: 'bg-green-500' },
    { region: 'Occidente', value: '3.5/5', percent: '70%', color: 'bg-amber-500' }
  ]

  const metrics = [
    {
      title: 'Tasa de Empleo',
      value: '68.4%',
      change: '+2.3% vs. mes anterior',
      badge: 'Normal',
      badgeClass: 'bg-green-50 text-green-700 border-green-200',
      icon: JobIcon,
      color: '#3b82f6',
      linePoints: '0,10 20,8 40,12 60,7 80,11 100,5'
    },
    {
      title: 'Cobertura de Conectividad',
      value: '54.2%',
      change: '+5.1% vs. mes anterior',
      badge: 'En crecimiento',
      badgeClass: 'bg-teal-50 text-teal-700 border-teal-200',
      icon: Wifi,
      color: '#10b981',
      linePoints: '0,12 20,10 40,8 60,9 80,6 100,4'
    },
    {
      title: 'Inclusión Digital',
      value: '48.7%',
      change: '+1.8% vs. mes anterior',
      badge: 'Moderado',
      badgeClass: 'bg-purple-50 text-purple-700 border-purple-200',
      icon: Activity,
      color: '#a855f7',
      linePoints: '0,12 20,11 40,13 60,10 80,9 100,7'
    },
    {
      title: 'Acceso a Salud Mental',
      value: '3.4/5',
      change: '+0.2 índice promedio',
      badge: 'Alerta',
      badgeClass: 'bg-amber-50 text-amber-700 border-amber-200',
      icon: Heart,
      color: '#ec4899',
      linePoints: '0,11 20,10 40,12 60,9 80,10 100,8'
    },
    {
      title: 'Concentración Poblacional',
      value: '12.4M',
      change: '+0.8% 9 regiones activas',
      badge: 'Estable',
      badgeClass: 'bg-slate-100 text-slate-700 border-slate-200',
      icon: Users,
      color: '#f97316',
      linePoints: '0,12 20,11 40,11 60,10 80,9 100,9'
    }
  ]

  const mapRegions = [
    { name: 'Noroeste', value: '58%', status: 'alerta', color: 'bg-[#fed7aa] text-amber-900 border-amber-300' },
    { name: 'Norte', value: '62%', status: 'bueno', color: 'bg-[#bbf7d0] text-green-900 border-green-300' },
    { name: 'Noreste', value: '71%', status: 'bueno', color: 'bg-[#bbf7d0] text-green-900 border-green-300' },
    { name: 'Centroeste', value: '65%', status: 'bueno', color: 'bg-[#bbf7d0] text-green-900 border-green-300' },
    { name: 'Centro', value: '82%', status: 'optimo', color: 'bg-[#bfdbfe] text-blue-900 border-blue-300' },
    { name: 'Oriente', value: '74%', status: 'bueno', color: 'bg-[#bbf7d0] text-green-900 border-green-300' },
    { name: 'Suroeste', value: '49%', status: 'critico', color: 'bg-[#fecaca] text-red-900 border-red-300' },
    { name: 'Sur', value: '84%', status: 'optimo', color: 'bg-[#bfdbfe] text-blue-900 border-blue-300' },
    { name: 'Sureste', value: '61%', status: 'bueno', color: 'bg-[#bbf7d0] text-green-900 border-green-300' },
  ]

  return (
    <div className="space-y-6">
      {/* Title & Filters Row */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 leading-tight">Panel Principal</h2>
          <p className="text-xs text-slate-500">Actualizado: 10 dic 2024, 09:42 - 9 regiones analizadas</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-1.5 bg-white border border-slate-200 text-xs font-semibold text-slate-700 px-3 py-2 rounded-lg hover:bg-slate-50 cursor-pointer">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            <span>Últimos 12 meses</span>
          </button>
          <button className="flex items-center gap-1.5 bg-white border border-slate-200 text-xs font-semibold text-slate-700 px-3 py-2 rounded-lg hover:bg-slate-50 cursor-pointer">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span>Filtros</span>
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {metrics.map((metric, idx) => {
          const Icon = metric.icon
          return (
            <div key={idx} className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
              <div className="flex items-start justify-between">
                <div className="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center border border-slate-100">
                  <Icon className="w-4 h-4 text-slate-500" />
                </div>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${metric.badgeClass}`}>
                  {metric.badge}
                </span>
              </div>
              <div className="mt-3">
                <h4 className="text-2xl font-bold text-slate-800 tracking-tight">{metric.value}</h4>
                <p className="text-[11px] text-slate-500 mt-1 font-semibold">{metric.title}</p>
                <div className="flex items-center gap-1 text-[10px] text-green-600 font-semibold mt-1">
                  <ArrowUpRight className="w-3 h-3 flex-shrink-0" />
                  <span>{metric.change}</span>
                </div>
              </div>
              {/* Sparkline Curve */}
              <div className="h-6 mt-3">
                <svg className="w-full h-full" viewBox="0 0 100 15" preserveAspectRatio="none">
                  <polyline
                    fill="none"
                    stroke={metric.color}
                    strokeWidth="1.5"
                    points={metric.linePoints}
                  />
                </svg>
              </div>
            </div>
          )
        })}
      </div>

      {/* Map and AI Assistant Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Card: Mapa de Inclusión Social */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">Mapa de Inclusión Social</h3>
              <button className="text-xs text-blue-600 hover:text-blue-700 font-semibold">
                Ver detalle →
              </button>
            </div>
            
            {/* Map Tabs */}
            <div className="flex flex-wrap gap-1 mt-4">
              <button 
                onClick={() => setActiveMapTab('empleo')}
                className={`text-[11px] px-3 py-1.5 rounded-lg font-semibold border cursor-pointer ${
                  activeMapTab === 'empleo' 
                    ? 'bg-blue-600 border-blue-600 text-white' 
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                Tasa de Empleo
              </button>
              <button 
                onClick={() => setActiveMapTab('conectividad')}
                className={`text-[11px] px-3 py-1.5 rounded-lg font-semibold border cursor-pointer ${
                  activeMapTab === 'conectividad' 
                    ? 'bg-blue-600 border-blue-600 text-white' 
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                Conectividad
              </button>
              <button 
                onClick={() => setActiveMapTab('salud')}
                className={`text-[11px] px-3 py-1.5 rounded-lg font-semibold border cursor-pointer ${
                  activeMapTab === 'salud' 
                    ? 'bg-blue-600 border-blue-600 text-white' 
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                Salud Mental
              </button>
              <button 
                onClick={() => setActiveMapTab('digital')}
                className={`text-[11px] px-3 py-1.5 rounded-lg font-semibold border cursor-pointer ${
                  activeMapTab === 'digital' 
                    ? 'bg-blue-600 border-blue-600 text-white' 
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                Inclusión Digital
              </button>
            </div>

            {/* Grid Map Representation */}
            <div className="grid grid-cols-3 gap-2 mt-6 max-w-xl mx-auto">
              {mapRegions.map((region, idx) => (
                <div key={idx} className={`p-4 rounded-xl border flex flex-col items-center justify-center ${region.color}`}>
                  <span className="text-[10px] uppercase font-bold tracking-wider opacity-70">{region.name}</span>
                  <span className="text-lg font-bold mt-1">{region.value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Map Legend */}
          <div className="mt-6 border-t border-slate-100 pt-4 flex items-center justify-between text-[11px] text-slate-500 font-semibold">
            <div className="flex items-center gap-1.5">
              <span>Escala:</span>
              <div className="flex items-center gap-3 ml-2">
                <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 bg-red-400 border border-red-500 rounded-full inline-block"></span> Crítico</span>
                <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 bg-amber-300 border border-amber-400 rounded-full inline-block"></span> Alerta</span>
                <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 bg-green-200 border border-green-300 rounded-full inline-block"></span> Bueno</span>
                <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 bg-blue-200 border border-blue-300 rounded-full inline-block"></span> Óptimo</span>
              </div>
            </div>
            <span>Tasa de Empleo</span>
          </div>
        </div>

        {/* Right Card: Asistente IA */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded bg-[#2563eb] text-white flex items-center justify-center">
                  <Bot className="w-3.5 h-3.5" />
                </div>
                <h3 className="text-sm font-bold text-slate-800">Asistente IA</h3>
              </div>
              <span className="flex items-center gap-1.5 text-[10px] text-green-600 font-bold bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                <span>En línea</span>
              </span>
            </div>

            {/* AI Welcome Message */}
            <div className="mt-4 flex gap-3 items-start bg-slate-50 rounded-xl p-3 border border-slate-100">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold flex-shrink-0 text-sm">
                AI
              </div>
              <p className="text-xs text-slate-700 leading-relaxed">
                Hola, soy el asistente de IA del APP BIT. Puedo ayudarle a analizar datos sociales, identificar brechas regionales y generar recomendaciones basadas en evidencia. ¿Qué le gustaría explorar hoy?
              </p>
            </div>

            {/* Suggestions Prompts */}
            <div className="mt-4 space-y-2">
              <button className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer leading-tight">
                ¿Qué regiones tienen alto desempleo y baja conectividad?
              </button>
              <button className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer leading-tight">
                ¿Dónde faltan programas de formación?
              </button>
              <button className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer leading-tight">
                ¿Qué zonas son prioridad para inversión social?
              </button>
              <button className="w-full text-left text-[11px] text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 p-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer leading-tight">
                ¿Cómo impacta la conectividad en la salud mental?
              </button>
            </div>
          </div>

          {/* AI Chat Input */}
          <div className="mt-6 relative">
            <input 
              type="text" 
              placeholder="Haga una pregunta sobre los datos..."
              className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-3 pr-10 py-2.5 text-xs focus:outline-none focus:border-blue-500"
            />
            <button className="absolute right-2 top-1/2 -translate-y-1/2 w-7 h-7 bg-blue-100 hover:bg-blue-200 text-blue-600 flex items-center justify-center rounded-md cursor-pointer transition-colors">
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Grid: Charts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Card 1: Empleo y Conectividad por Región */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-800">Empleo y Conectividad por Región</h3>
            <span className="text-[10px] font-bold bg-slate-50 px-2 py-0.5 rounded-full border border-slate-200 text-slate-500">2024</span>
          </div>
          <div className="flex-1 mt-4">
            <ChartContainer config={barChartConfig} className="h-[200px] w-full">
              <BarChart data={barChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid vertical={false} strokeDasharray="3 3" />
                <XAxis 
                  dataKey="region" 
                  tickLine={false} 
                  axisLine={false} 
                  tickMargin={8} 
                  tick={{ fontSize: 9, fill: '#64748b' }}
                />
                <YAxis 
                  tickLine={false} 
                  axisLine={false} 
                  tickMargin={8} 
                  tick={{ fontSize: 9, fill: '#64748b' }}
                  domain={[0, 100]}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Bar dataKey="empleo" fill="var(--color-empleo)" radius={[2, 2, 0, 0]} barSize={10} />
                <Bar dataKey="conectividad" fill="var(--color-conectividad)" radius={[2, 2, 0, 0]} barSize={10} />
                <ChartLegend content={<ChartLegendContent />} />
              </BarChart>
            </ChartContainer>
          </div>
        </div>

        {/* Card 2: Evolución de Indicadores */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-800">Evolución de Indicadores</h3>
            <span className="text-[10px] font-bold bg-slate-50 px-2 py-0.5 rounded-full border border-slate-200 text-slate-500">12 meses</span>
          </div>
          <div className="flex-1 mt-4">
            <ChartContainer config={lineChartConfig} className="h-[200px] w-full">
              <LineChart data={lineChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid vertical={false} strokeDasharray="3 3" />
                <XAxis 
                  dataKey="mes" 
                  tickLine={false} 
                  axisLine={false} 
                  tickMargin={8} 
                  tick={{ fontSize: 9, fill: '#64748b' }}
                />
                <YAxis 
                  tickLine={false} 
                  axisLine={false} 
                  tickMargin={8} 
                  tick={{ fontSize: 9, fill: '#64748b' }}
                  domain={[40, 85]}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Line type="monotone" dataKey="empleo" stroke="var(--color-empleo)" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="conectividad" stroke="var(--color-conectividad)" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="inclusion" stroke="var(--color-inclusion)" strokeWidth={2} dot={false} />
                <ChartLegend content={<ChartLegendContent />} />
              </LineChart>
            </ChartContainer>
          </div>
        </div>

        {/* Card 3: Inclusión Digital & Salud Mental */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">Inclusión Digital</h3>
              <span className="text-[10px] font-bold bg-slate-50 px-2 py-0.5 rounded-full border border-slate-200 text-slate-500">Nacional</span>
            </div>
            
            {/* Donut Chart and legend block */}
            <div className="flex items-center gap-4 mt-4">
              <ChartContainer config={pieChartConfig} className="h-[95px] w-[95px] shrink-0">
                <PieChart>
                  <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
                  <Pie 
                    data={pieChartData} 
                    dataKey="value" 
                    nameKey="name" 
                    innerRadius={26} 
                    outerRadius={40} 
                    strokeWidth={2}
                    stroke="#ffffff"
                  >
                    {pieChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ChartContainer>
              
              {/* Legends list */}
              <div className="flex-1 space-y-1 text-[11px]">
                {pieChartData.map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between font-semibold">
                    <div className="flex items-center gap-2 text-slate-600 truncate">
                      <span className="w-2.5 h-2.5 rounded-[2px] shrink-0" style={{ backgroundColor: item.color }}></span>
                      <span className="truncate">{item.name}</span>
                    </div>
                    <span className="text-slate-800 ml-2">{item.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Salud Mental progress list */}
          <div className="mt-4 pt-3 border-t border-slate-100 space-y-2">
            <div className="flex items-center justify-between text-[11px] font-bold text-slate-700">
              <span>Salud Mental por Región</span>
              <span className="text-slate-400 font-normal">escala 0-5</span>
            </div>
            <div className="space-y-1.5">
              {saludMentalData.map((item, idx) => (
                <div key={idx} className="space-y-0.5">
                  <div className="flex items-center justify-between text-[10px] font-bold text-slate-600">
                    <span>{item.region}</span>
                    <span>{item.value}</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div className={`h-full ${item.color} rounded-full`} style={{ width: item.percent }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Action Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button className="bg-[#eff6ff] hover:bg-[#dbeafe] border border-blue-100 rounded-xl p-4 flex items-center justify-between text-left cursor-pointer transition-all duration-200 group">
          <div>
            <h5 className="text-xs font-bold text-blue-900">Ver Formaciones</h5>
            <p className="text-[10px] text-blue-700/80 mt-1">Programas educativos activos</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center group-hover:scale-105 transition-transform">
            <GraduationCap className="w-4 h-4" />
          </div>
        </button>

        <button className="bg-[#f0fdf4] hover:bg-[#dcfce7] border border-green-100 rounded-xl p-4 flex items-center justify-between text-left cursor-pointer transition-all duration-200 group">
          <div>
            <h5 className="text-xs font-bold text-green-900">Análisis de Empleo</h5>
            <p className="text-[10px] text-green-700/80 mt-1">Oportunidades laborales</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-green-100 text-green-600 flex items-center justify-center group-hover:scale-105 transition-transform">
            <Briefcase className="w-4 h-4" />
          </div>
        </button>

        <button className="bg-[#fef2f2] hover:bg-[#fee2e2] border border-red-100 rounded-xl p-4 flex items-center justify-between text-left cursor-pointer transition-all duration-200 group">
          <div>
            <h5 className="text-xs font-bold text-red-900">Alertas Activas</h5>
            <p className="text-[10px] text-red-700/80 mt-1">Alertas críticas del portal</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-red-100 text-red-600 flex items-center justify-center group-hover:scale-105 transition-transform">
            <Bell className="w-4 h-4" />
          </div>
        </button>

        <button className="bg-[#faf5ff] hover:bg-[#f3e8ff] border border-purple-100 rounded-xl p-4 flex items-center justify-between text-left cursor-pointer transition-all duration-200 group">
          <div>
            <h5 className="text-xs font-bold text-purple-900">Generar Reporte</h5>
            <p className="text-[10px] text-purple-700/80 mt-1">Exportar informe analítico</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-purple-100 text-purple-600 flex items-center justify-center group-hover:scale-105 transition-transform">
            <FileText className="w-4 h-4" />
          </div>
        </button>
      </div>
    </div>
  )
}

export default DashboardPage
