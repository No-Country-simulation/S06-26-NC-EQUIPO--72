import { useState } from "react";
import MainLayout from "./app/layouts/MainLayout";
import DashboardPage from "./features/dashboard/pages/DashboardPage";
import ClusterDetailPage from "./features/dashboard/pages/ClusterDetailPage";
import FormacionesPage from "./features/formaciones/pages/FormacionesPage";
import ExperienciasPage from "./features/experiencias/pages/ExperienciasPage";
import SaludMentalPage from "./features/salud-mental/pages/SaludMentalPage";
import MentoriasPage from "./features/mentorias/pages/MentoriasPage";
import EmpleabilidadPage from "./features/empleabilidad/pages/EmpleabilidadPage";
import ReportesPage from "./features/reportes/pages/ReportesPage";
import AlertasPage from "./features/alertas/pages/AlertasPage";
import ConfiguracionPage from "./features/configuracion/pages/ConfiguracionPage";

function App() {
  const [currentTab, setCurrentTab] = useState("inicio");
  const [selectedCluster, setSelectedCluster] = useState(null);
  const [activeMapTab, setActiveMapTab] = useState("EMPLEO");

  const handleClusterSelect = (clusterName) => {
    setSelectedCluster(clusterName);
    setCurrentTab("cluster-detail");
  };

  return (
    <MainLayout currentTab={currentTab} onTabChange={setCurrentTab}>
      {currentTab === "inicio" ? (
        <DashboardPage 
          onTabChange={setCurrentTab} 
          onClusterSelect={handleClusterSelect}
          activeMapTab={activeMapTab}
          onActiveMapTabChange={setActiveMapTab}
        />
      ) : currentTab === "cluster-detail" ? (
        <ClusterDetailPage 
          clusterName={selectedCluster} 
          onBack={() => {
            setCurrentTab("inicio");
            setSelectedCluster(null);
          }}
          activeTab={activeMapTab}
        />
      ) : currentTab === "formaciones" ? (
        <FormacionesPage />
      ) : currentTab === "experiencias" ? (
        <ExperienciasPage />
      ) : currentTab === "empleabilidad" ? (
        <EmpleabilidadPage />
      ) : currentTab === "salud-mental" ? (
        <SaludMentalPage />
      ) : currentTab === "mentorias" ? (
        <MentoriasPage />
      ) : currentTab === "reportes" ? (
        <ReportesPage />
      ) : currentTab === "alertas" ? (
        <AlertasPage />
      ) : currentTab === "configuracion" ? (
        <ConfiguracionPage />
      ) : (
        <div className="bg-white border border-slate-200 rounded-xl p-8 text-center text-slate-500">
          <h3 className="text-base font-bold text-slate-700 capitalize">
            {currentTab}
          </h3>
          <p className="text-xs mt-1">
            Esta sección se encuentra en desarrollo.
          </p>
        </div>
      )}
    </MainLayout>
  );
}

export default App;
