import { useState } from 'react'
import MainLayout from './app/layouts/MainLayout'
import DashboardPage from './features/dashboard/pages/DashboardPage'

function App() {
  const [currentTab, setCurrentTab] = useState('inicio')

  return (
    <MainLayout currentTab={currentTab} onTabChange={setCurrentTab}>
      {currentTab === 'inicio' ? (
        <DashboardPage />
      ) : (
        <div className="bg-white border border-slate-200 rounded-xl p-8 text-center text-slate-500">
          <h3 className="text-base font-bold text-slate-700 capitalize">{currentTab}</h3>
          <p className="text-xs mt-1">Esta sección se encuentra en desarrollo.</p>
        </div>
      )}
    </MainLayout>
  )
}

export default App
