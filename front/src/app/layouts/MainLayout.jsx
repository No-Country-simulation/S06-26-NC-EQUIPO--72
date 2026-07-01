import { 
  SidebarProvider, 
  Sidebar, 
  SidebarContent, 
  SidebarHeader, 
  SidebarFooter, 
  SidebarMenu, 
  SidebarMenuItem, 
  SidebarMenuButton,
  SidebarTrigger,
  SidebarInset
} from "@/components/ui/sidebar"
import { TooltipProvider } from "@/components/ui/tooltip"
import { 
  LayoutDashboard, 
  BookOpen, 
  Briefcase, 
  Star, 
  Users, 
  Heart, 
  BarChart3, 
  Bell, 
  Settings, 
  LogOut, 
  Search, 
  Globe, 
  ChevronDown, 
  Download 
} from 'lucide-react'

function MainLayout({ children, currentTab, onTabChange }) {
  const menuItems = [
    { id: 'inicio', label: 'Inicio', icon: LayoutDashboard },
    { id: 'formaciones', label: 'Formaciones', icon: BookOpen },
    { id: 'empleabilidad', label: 'Empleabilidad', icon: Briefcase },
    { id: 'experiencias', label: 'Experiencias', icon: Star },
    { id: 'mentorias', label: 'Mentorias', icon: Users },
    { id: 'salud-mental', label: 'Salud Mental', icon: Heart },
    { id: 'reportes', label: 'Reportes', icon: BarChart3 },
    { id: 'alertas', label: 'Alertas', icon: Bell },
    { id: 'configuracion', label: 'Configuración', icon: Settings },
  ]

  return (
    <TooltipProvider>
      <SidebarProvider>
        <div className="flex h-screen w-full bg-slate-50 text-[#334155] font-sans overflow-hidden">
          {/* Shadcn Sidebar */}
          <Sidebar collapsible="icon" className="border-r border-sidebar-border bg-sidebar">
            {/* Header / Brand */}
            <SidebarHeader className="px-4 group-data-[collapsible=icon]:px-2 py-5 flex flex-row items-center group-data-[collapsible=icon]:justify-center gap-3 border-b border-sidebar-border h-16 shrink-0">
              <div className="w-9 h-9 rounded-lg bg-[#2563eb] flex items-center justify-center text-white shrink-0">
                <BarChart3 className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0 group-data-[collapsible=icon]:hidden">
                <h1 className="font-bold text-white leading-none tracking-wider text-sm truncate">APP BIT</h1>
                <p className="text-[10px] text-slate-400 mt-1 truncate">Intel. Pública</p>
              </div>
            </SidebarHeader>

            {/* Menu Content */}
            <SidebarContent className="px-3 py-4 flex-1 overflow-y-auto">
              <SidebarMenu className="space-y-1">
                {menuItems.map((item) => {
                  const Icon = item.icon
                  const isActive = currentTab === item.id || (item.id === "inicio" && currentTab === "cluster-detail")
                  return (
                    <SidebarMenuItem key={item.id}>
                      <SidebarMenuButton
                        isActive={isActive}
                        onClick={() => onTabChange(item.id)}
                        tooltip={item.label}
                        className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 cursor-pointer ${
                          isActive 
                            ? 'bg-[#1e293b] text-white font-medium border-l-4 border-[#2563eb]' 
                            : 'hover:bg-slate-800/40 hover:text-slate-100'
                        }`}
                      >
                        <Icon className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-[#3b82f6]' : 'text-slate-400'}`} />
                        <span className="group-data-[collapsible=icon]:hidden truncate">{item.label}</span>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  )
                })}
              </SidebarMenu>
            </SidebarContent>

            {/* Footer / Profile */}
            <SidebarFooter className="border-t border-sidebar-border p-4 group-data-[collapsible=icon]:p-2 bg-sidebar animate-none">
              {/* 
              <div className="flex items-center gap-3 px-2 py-1.5 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0">
                <div className="w-8 h-8 rounded-full bg-[#2563eb] flex items-center justify-center text-white font-bold text-xs shrink-0">
                  AR
                </div>
                <div className="flex-1 min-w-0 group-data-[collapsible=icon]:hidden">
                  <h4 className="text-xs font-semibold text-white truncate">Ana Rodrigues</h4>
                  <p className="text-[9px] text-slate-400 truncate">Analista Senior</p>
                </div>
              </div>
              */}

              {/* 
              <button className="w-full mt-2 flex items-center gap-2 px-2 py-2 text-xs hover:text-white text-slate-400 transition-colors group-data-[collapsible=icon]:justify-center">
                <LogOut className="w-3.5 h-3.5 flex-shrink-0" />
                <span className="group-data-[collapsible=icon]:hidden truncate">Cerrar sesión</span>
              </button>
              */}

              <button 
                onClick={() => onTabChange("landing")}
                className="w-full mt-2 flex items-center gap-2 px-2.5 py-2.5 text-xs hover:text-white hover:bg-slate-800 text-slate-400 rounded-lg transition-all group-data-[collapsible=icon]:justify-center cursor-pointer font-medium"
              >
                <LogOut className="w-4 h-4 flex-shrink-0 text-slate-400 group-hover:text-white" />
                <span className="group-data-[collapsible=icon]:hidden truncate">Volver al Inicio</span>
              </button>
            </SidebarFooter>
          </Sidebar>

          {/* Main Content Pane */}
          <SidebarInset className="flex-1 flex flex-col overflow-hidden bg-slate-50/50">
            {/* Header */}
            <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 flex-shrink-0">
              <div className="flex items-center gap-4">
                <SidebarTrigger className="text-slate-600 hover:bg-slate-100 rounded-md cursor-pointer" />
                {/* Search bar */}
                <div className="relative w-80">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input 
                    type="text" 
                    placeholder="Buscar..." 
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-9 pr-4 py-1.5 text-xs focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              {/* Right Actions */}
              <div className="flex items-center gap-5">
                <button className="flex items-center gap-2 bg-[#2563eb] hover:bg-blue-600 text-white font-medium text-xs px-4 py-2 rounded-lg transition-colors cursor-pointer">
                  <Download className="w-3.5 h-3.5" />
                  <span>Exportar</span>
                </button>

                {/* Language */}
                <div className="flex items-center gap-1.5 text-slate-600 text-xs font-medium cursor-pointer">
                  <Globe className="w-4 h-4" />
                  <span>ES</span>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                </div>

                {/* Bell notifications */}
                <div className="relative cursor-pointer p-1 text-slate-600 hover:text-slate-800">
                  <Bell className="w-4 h-4" />
                  <span className="absolute top-1 right-1 w-1.5 h-1.5 bg-red-500 rounded-full"></span>
                </div>

                {/* Profile dropdown */}
                <div className="flex items-center gap-2 cursor-pointer border-l border-slate-200 pl-4">
                  <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-700 text-xs">
                    AR
                  </div>
                  <span className="text-xs font-medium text-slate-700">Ana R.</span>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                </div>
              </div>
            </header>

            {/* Content view */}
            <main className="flex-1 overflow-y-auto p-8">
              {children}
            </main>
          </SidebarInset>
        </div>
      </SidebarProvider>
    </TooltipProvider>
  )
}

export default MainLayout
