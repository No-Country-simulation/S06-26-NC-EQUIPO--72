import { useState, useMemo, useRef, useEffect } from 'react'
import { 
  BookOpen, 
  Users, 
  Activity, 
  AlertTriangle, 
  Plus, 
  Search, 
  ChevronDown, 
  MapPin, 
  ChevronRight,
  CheckCircle,
  AlertCircle,
  XCircle
} from 'lucide-react'
import {
  BarChart,
  Bar,
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

// Mock Data
const barChartData = [
  { region: 'Noroeste', programas: 20, cobertura: 38 },
  { region: 'Norte', programas: 22, cobertura: 45 },
  { region: 'Noreste', programas: 27, cobertura: 68 },
  { region: 'Occidente', programas: 21, cobertura: 52 },
  { region: 'Centro', programas: 65, cobertura: 90 },
  { region: 'Oriente', programas: 28, cobertura: 72 },
  { region: 'Suroeste', programas: 18, cobertura: 26 },
  { region: 'Sur', programas: 20, cobertura: 32 },
  { region: 'Sureste', programas: 21, cobertura: 44 }
]

const barChartConfig = {
  programas: {
    label: 'Programas',
    color: '#2563eb',
  },
  cobertura: {
    label: 'Cobertura %',
    color: '#0d9488',
  }
}

const pieChartData = [
  { name: 'Formación Digital', value: 35, color: '#2563eb' },
  { name: 'Formación Técnica', value: 28, color: '#0d9488' },
  { name: 'Emprendimiento', value: 20, color: '#a855f7' },
  { name: 'Idiomas', value: 10, color: '#f97316' },
  { name: 'Otros', value: 7, color: '#64748b' }
]

const pieChartConfig = {
  digital: {
    label: 'Formación Digital',
    color: '#2563eb',
  },
  tecnica: {
    label: 'Formación Técnica',
    color: '#0d9488',
  },
  emprendimiento: {
    label: 'Emprendimiento',
    color: '#a855f7',
  },
  idiomas: {
    label: 'Idiomas',
    color: '#f97316',
  },
  otros: {
    label: 'Otros',
    color: '#64748b',
  }
}

const programList = [
  {
    id: 1,
    nombre: 'Programa Nacional de Capacitación Digital',
    region: 'Centro',
    beneficiarios: '12.450',
    cobertura: 89,
    estado: 'Activo'
  },
  {
    id: 2,
    nombre: 'Formación Técnica para Jóvenes',
    region: 'Noreste',
    beneficiarios: '8.230',
    cobertura: 72,
    estado: 'Activo'
  },
  {
    id: 3,
    nombre: 'Alfabetización Digital Rural',
    region: 'Suroeste',
    beneficiarios: '3.120',
    cobertura: 28,
    estado: 'Crítico'
  },
  {
    id: 4,
    nombre: 'Emprendimiento e Innovación Social',
    region: 'Oriente',
    beneficiarios: '5.670',
    cobertura: 84,
    estado: 'Activo'
  },
  {
    id: 5,
    nombre: 'Habilidades para el Trabajo 4.0',
    region: 'Norte',
    beneficiarios: '4.890',
    cobertura: 45,
    estado: 'Alerta'
  },
  {
    id: 6,
    nombre: 'Formación Agroindustrial',
    region: 'Sur',
    beneficiarios: '2.340',
    cobertura: 33,
    estado: 'Alerta'
  },
  {
    id: 7,
    nombre: 'Tecnología Aplicada a Servicios',
    region: 'Occidente',
    beneficiarios: '4.100',
    cobertura: 52,
    estado: 'Activo'
  },
  {
    id: 8,
    nombre: 'Idiomas para la Empleabilidad',
    region: 'Noroeste',
    beneficiarios: '1.870',
    cobertura: 31,
    estado: 'Crítico'
  }
]

function FormacionesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('Todos')
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)
  const dropdownRef = useRef(null)

  // Handle outside click to close status filter dropdown
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Filtered Programs
  const filteredPrograms = useMemo(() => {
    return programList.filter(program => {
      const matchesSearch = program.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            program.region.toLowerCase().includes(searchTerm.toLowerCase())
      
      const matchesStatus = statusFilter === 'Todos' || 
                            program.estado.toLowerCase() === statusFilter.toLowerCase()

      return matchesSearch && matchesStatus
    })
  }, [searchTerm, statusFilter])

  // Get coverage progress bar colors
  const getCoverageColors = (val) => {
    if (val >= 70) return { text: 'text-green-600', bar: 'bg-green-500' }
    if (val >= 40) return { text: 'text-amber-600', bar: 'bg-amber-500' }
    return { text: 'text-red-600', bar: 'bg-red-500' }
  }

  // Get status badge styles
  const getStatusBadge = (estado) => {
    switch (estado) {
      case 'Activo':
        return (
          <span className="inline-flex items-center gap-1 bg-green-50 text-green-700 border border-green-200 px-2.5 py-0.5 rounded-full text-xs font-semibold">
            <CheckCircle className="w-3.5 h-3.5 text-green-600" />
            <span>Activo</span>
          </span>
        )
      case 'Alerta':
        return (
          <span className="inline-flex items-center gap-1 bg-amber-50 text-amber-700 border border-amber-200 px-2.5 py-0.5 rounded-full text-xs font-semibold">
            <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
            <span>Alerta</span>
          </span>
        )
      case 'Crítico':
        return (
          <span className="inline-flex items-center gap-1 bg-red-50 text-red-700 border border-red-200 px-2.5 py-0.5 rounded-full text-xs font-semibold">
            <XCircle className="w-3.5 h-3.5 text-red-600" />
            <span>Crítico</span>
          </span>
        )
      default:
        return null
    }
  }

  return (
    <div className="space-y-6">
      {/* Title & Header Row */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-600" />
            <span>Programas de Formación</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">Cobertura de formación y capacitación por región</p>
        </div>
        <div>
          <button className="flex items-center gap-1.5 bg-[#2563eb] hover:bg-blue-600 text-white font-medium text-xs px-4 py-2.5 rounded-lg transition-colors cursor-pointer shadow-sm">
            <Plus className="w-4 h-4" />
            <span>Nuevo programa</span>
          </button>
        </div>
      </div>

      {/* Metrics Indicators Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Programas Activos */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center border border-emerald-100 text-emerald-600">
              <BookOpen className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-slate-800 tracking-tight">4</span>
              <span className="text-xs text-slate-400 font-medium">de 8 totales</span>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-semibold">Programas Activos</p>
          </div>
        </div>

        {/* Card 2: Beneficiarios Totales */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center border border-blue-100 text-blue-600">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-slate-800 tracking-tight">43K</span>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-semibold">Beneficiarios Totales</p>
          </div>
        </div>

        {/* Card 3: Cobertura Media */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center border border-teal-100 text-teal-600">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-slate-800 tracking-tight">52%</span>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-semibold">Cobertura Media</p>
          </div>
        </div>

        {/* Card 4: Regiones con brecha */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between">
            <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center border border-amber-100 text-amber-600">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-slate-800 tracking-tight">4</span>
              <span className="text-xs text-slate-400 font-medium">de 9 totales</span>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-semibold">Regiones con brecha</p>
          </div>
        </div>
      </div>

      {/* Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Card: Programas y Beneficiarios por Región */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 lg:col-span-2 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-800">Programas y Beneficiarios por Región</h3>
          </div>
          <div className="flex-1 mt-4">
            <ChartContainer config={barChartConfig} className="h-[240px] w-full">
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
                <Bar dataKey="programas" fill="var(--color-programas)" radius={[2, 2, 0, 0]} barSize={10} />
                <Bar dataKey="cobertura" fill="var(--color-cobertura)" radius={[2, 2, 0, 0]} barSize={10} />
                <ChartLegend content={<ChartLegendContent />} />
              </BarChart>
            </ChartContainer>
          </div>
        </div>

        {/* Right Card: Por Categoría Donut Chart */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:shadow-sm transition-shadow">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800">Por Categoría</h3>
            </div>
            
            <div className="flex items-center gap-4 mt-8">
              <ChartContainer config={pieChartConfig} className="h-[120px] w-[120px] shrink-0">
                <PieChart>
                  <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
                  <Pie 
                    data={pieChartData} 
                    dataKey="value" 
                    nameKey="name" 
                    innerRadius={32} 
                    outerRadius={48} 
                    strokeWidth={2}
                    stroke="#ffffff"
                  >
                    {pieChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ChartContainer>
              
              <div className="flex-1 space-y-2 text-xs">
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
        </div>
      </div>

      {/* Programs List Table Section */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
        {/* Table Top Bar */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <h3 className="text-sm font-bold text-slate-800">Listado de Programas</h3>
          <div className="flex items-center gap-3">
            {/* Search Input */}
            <div className="relative w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
              <input 
                type="text" 
                placeholder="Buscar programa..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-9 pr-3 py-1.5 text-xs focus:outline-none focus:border-blue-500 focus:bg-white transition-all text-slate-700"
              />
            </div>

            {/* Dropdown Select Status Filter */}
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="flex items-center justify-between gap-1.5 bg-white border border-slate-200 text-xs font-semibold text-slate-700 px-3.5 py-1.5 rounded-lg hover:bg-slate-50 cursor-pointer min-w-[100px] select-none text-left"
              >
                <span>{statusFilter}</span>
                <ChevronDown className={`w-3.5 h-3.5 text-slate-400 transition-transform duration-150 ${isDropdownOpen ? 'rotate-180' : ''}`} />
              </button>

              {isDropdownOpen && (
                <div className="absolute right-0 top-full mt-1.5 w-32 bg-white border border-slate-200 rounded-lg shadow-md py-1 z-50 animate-in fade-in slide-in-from-top-1 duration-100">
                  {['Todos', 'Activo', 'Crítico', 'Alerta'].map((opt) => (
                    <button
                      key={opt}
                      onClick={() => {
                        setStatusFilter(opt)
                        setIsDropdownOpen(false)
                      }}
                      className={`w-full text-left px-3 py-1.5 text-xs hover:bg-slate-50 cursor-pointer flex items-center justify-between ${statusFilter === opt ? 'bg-blue-50/50 text-blue-600 font-bold' : 'text-slate-700'}`}
                    >
                      <span>{opt}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Table Content */}
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-100 text-slate-400 font-semibold h-10">
                <th className="py-2 pr-4 pl-1">Programa</th>
                <th className="py-2 px-4">Región</th>
                <th className="py-2 px-4">Beneficiarios</th>
                <th className="py-2 px-4">Cobertura</th>
                <th className="py-2 px-4">Estado</th>
                <th className="py-2 pl-4 pr-1 text-right"></th>
              </tr>
            </thead>
            <tbody>
              {filteredPrograms.length > 0 ? (
                filteredPrograms.map((program) => {
                  const colors = getCoverageColors(program.cobertura)
                  return (
                    <tr key={program.id} className="border-b border-slate-100 hover:bg-slate-50/40 transition-colors h-14">
                      {/* Name */}
                      <td className="py-3 pr-4 pl-1 font-bold text-slate-800 max-w-xs md:max-w-sm lg:max-w-md truncate">
                        {program.nombre}
                      </td>

                      {/* Region */}
                      <td className="py-3 px-4 text-slate-600 font-medium">
                        <span className="flex items-center gap-1.5">
                          <MapPin className="w-3.5 h-3.5 text-slate-400" />
                          <span>{program.region}</span>
                        </span>
                      </td>

                      {/* Beneficiarios */}
                      <td className="py-3 px-4 text-slate-600 font-medium">
                        <span className="flex items-center gap-1.5">
                          <Users className="w-3.5 h-3.5 text-slate-400" />
                          <span>{program.beneficiarios}</span>
                        </span>
                      </td>

                      {/* Cobertura */}
                      <td className="py-3 px-4">
                        <div className="flex flex-col gap-1">
                          <span className={`font-bold ${colors.text}`}>{program.cobertura}%</span>
                          <div className="w-24 bg-slate-100 rounded-full h-1 overflow-hidden">
                            <div className={`h-full rounded-full ${colors.bar}`} style={{ width: `${program.cobertura}%` }}></div>
                          </div>
                        </div>
                      </td>

                      {/* Estado */}
                      <td className="py-3 px-4">
                        {getStatusBadge(program.estado)}
                      </td>

                      {/* Detail Icon */}
                      <td className="py-3 pl-4 pr-1 text-right">
                        <button className="p-1 hover:bg-slate-100 rounded text-slate-400 hover:text-slate-600 transition-colors cursor-pointer">
                          <ChevronRight className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  )
                })
              ) : (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 font-medium">
                    No se encontraron programas con los filtros seleccionados.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Table Footer / Info */}
        <div className="flex justify-between items-center pt-2 text-[11px] text-slate-400 font-semibold select-none">
          <span>Mostrando {filteredPrograms.length} de {programList.length} programas</span>
        </div>
      </div>
    </div>
  )
}

export default FormacionesPage
