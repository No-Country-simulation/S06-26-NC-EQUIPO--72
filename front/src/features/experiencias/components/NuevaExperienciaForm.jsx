import { useForm } from "react-hook-form";
import { Loader2 } from "lucide-react";
import { useCreateExperiencia } from "../hooks/useExperiencias";
import { formatClusterName } from "@/shared/utils/format";

// Lista oficial de clústeres para Florianópolis
const FLORI_CLUSTERS = [
  "AEROPORTO_HLZ",
  "CAMPECHE",
  "CANASVIEIRAS",
  "CBD_BEIRAMAR",
  "CENTRO_HISTORICO",
  "COQUEIROS",
  "ESTREITO_CAPOEIRAS",
  "INGLESES",
  "JURERE",
  "LAGOA_CONCEICAO",
  "NORTE_ILHA",
  "RESIDENCIAL_NORTE",
  "SC401_CORREDOR",
  "TRINDADE",
  "UFSC",
  "VIA_EXPRESSA_CORREDOR",
];

/**
 * Componente del formulario interactivo para registrar una nueva experiencia estructurante.
 * Emplea react-hook-form para controlar el estado del formulario y validar las entradas.
 * 
 * @param {Function} onSubmitSuccess - Callback invocado al completar con éxito el registro
 * @param {Function} onCancel - Callback para cerrar el modal o cancelar el registro
 */
export default function NuevaExperienciaForm({ onSubmitSuccess, onCancel }) {
  // Obtenemos la función de mutación del hook personalizado de React Query
  const { mutateAsync: createExperiencia } = useCreateExperiencia();

  // Configuramos react-hook-form con los valores iniciales y vacíos
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      nombre: "",
      descripcion: "",
      cluster: "",
      organizacion: "",
      liderReferente: "",
      impactoEstimado: "MEDIO",
      replicable: true, // Habilitado por defecto para coincidir con la mayoría de mocks
      fechaInicio: new Date().toISOString().split("T")[0], // Fecha por defecto el día de hoy
    },
  });

  // Invocado tras pasar las validaciones locales del cliente
  const onSubmit = async (data) => {
    try {
      // Estructuramos el payload que el backend de Spring Boot espera.
      // Convertimos el booleano 'replicable' a un entero (1 o 0) para la columna de la DB.
      const payload = {
        nombre: data.nombre,
        descripcion: data.descripcion,
        cluster: data.cluster,
        organizacion: data.organizacion,
        liderReferente: data.liderReferente,
        impactoEstimado: data.impactoEstimado,
        replicable: data.replicable ? 1 : 0,
        fechaInicio: data.fechaInicio,
        tipo: "EXPERIENCIA", // Forzamos tipo a EXPERIENCIA
        municipio: "Florianópolis", // Forzamos municipio a Florianópolis
        activo: true, // Registramos activo por defecto
      };

      // Ejecutamos la mutación asíncrona
      await createExperiencia(payload);

      // Notificamos de forma exitosa al componente padre para que actualice la interfaz
      if (onSubmitSuccess) {
        onSubmitSuccess();
      }
    } catch (error) {
      // Capturamos el error devuelto por la API y lo mostramos en el mensaje global del formulario
      setError("root", {
        type: "server",
        message: error.message || "Error inesperado al crear la experiencia",
      });
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-4 bg-white rounded-xl p-6 w-full max-w-md mx-auto"
    >
      {/* Cabecera del formulario */}
      <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
        <h3 className="text-sm font-bold text-slate-800">
          Registrar Nueva Experiencia Estructurante
        </h3>
      </div>

      {/* Alerta de Error de Servidor/API */}
      {errors.root && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-[11px] text-red-600 font-semibold leading-relaxed">
          {errors.root.message}
        </div>
      )}

      {/* Campo: Nombre de la Experiencia */}
      <div className="space-y-1">
        <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Nombre de la Experiencia
        </label>
        <input
          type="text"
          className={`w-full bg-slate-50 border rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:bg-white transition-all ${
            errors.nombre
              ? "border-red-500"
              : "border-slate-200 focus:border-blue-500"
          }`}
          placeholder="Ej: Laboratorio de Innovación Social y Solidaria"
          {...register("nombre", {
            required: "El nombre es obligatorio",
            minLength: {
              value: 5,
              message: "El nombre debe contener al menos 5 letras",
            },
          })}
        />
        {errors.nombre && (
          <p className="text-[10px] text-red-500 font-semibold mt-0.5">
            {errors.nombre.message}
          </p>
        )}
      </div>

      {/* Campo: Descripción detallada */}
      <div className="space-y-1">
        <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Descripción de la Iniciativa
        </label>
        <textarea
          rows={3}
          className={`w-full bg-slate-50 border rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:bg-white transition-all resize-none ${
            errors.descripcion
              ? "border-red-500"
              : "border-slate-200 focus:border-blue-500"
          }`}
          placeholder="Describa brevemente la iniciativa y sus metas principales..."
          {...register("descripcion", {
            required: "La descripción es requerida para el registro",
          })}
        />
        {errors.descripcion && (
          <p className="text-[10px] text-red-500 font-semibold mt-0.5">
            {errors.descripcion.message}
          </p>
        )}
      </div>

      {/* Selector: Clúster Territorial */}
      <div className="space-y-1">
        <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Clúster Territorial (Región)
        </label>
        <select
          className={`w-full bg-slate-50 border rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:bg-white transition-all cursor-pointer ${
            errors.cluster
              ? "border-red-500"
              : "border-slate-200 focus:border-blue-500"
          }`}
          {...register("cluster", {
            required: "Debe seleccionar un clúster de aplicación",
          })}
        >
          <option value="">Seleccione una región territorial...</option>
          {FLORI_CLUSTERS.map((c) => (
            <option key={c} value={c}>
              {formatClusterName(c)}
            </option>
          ))}
        </select>
        {errors.cluster && (
          <p className="text-[10px] text-red-500 font-semibold mt-0.5">
            {errors.cluster.message}
          </p>
        )}
      </div>

      {/* Fila: Organización Responsable + Líder Referente */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Organización Responsable
          </label>
          <input
            type="text"
            className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
            placeholder="Ej: ONG Verde Vida"
            {...register("organizacion")}
          />
        </div>

        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Líder Referente
          </label>
          <input
            type="text"
            className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
            placeholder="Ej: Ana Carvalho"
            {...register("liderReferente")}
          />
        </div>
      </div>

      {/* Fila: Impacto Estimado + Fecha de Inicio */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Impacto Estimado
          </label>
          <select
            className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all cursor-pointer"
            {...register("impactoEstimado")}
          >
            <option value="BAJO">BAJO</option>
            <option value="MEDIO">MEDIO</option>
            <option value="ALTO">ALTO</option>
          </select>
        </div>

        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Fecha de Inicio
          </label>
          <input
            type="date"
            className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all cursor-pointer"
            {...register("fechaInicio", {
              required: "La fecha de inicio es requerida",
            })}
          />
          {errors.fechaInicio && (
            <p className="text-[10px] text-red-500 font-semibold mt-0.5">
              {errors.fechaInicio.message}
            </p>
          )}
        </div>
      </div>

      {/* Checkbox: Replicabilidad */}
      <div className="flex items-center gap-2 py-1 select-none">
        <input
          type="checkbox"
          id="replicable"
          className="w-3.5 h-3.5 border border-slate-200 rounded text-blue-600 focus:ring-blue-500/20 cursor-pointer"
          {...register("replicable")}
        />
        <label htmlFor="replicable" className="text-xs text-slate-600 font-semibold cursor-pointer">
          Esta experiencia es replicable
        </label>
      </div>

      {/* Acciones del formulario */}
      <div className="flex items-center justify-end gap-2 pt-4 border-t border-slate-100 mt-2">
        <button
          type="button"
          onClick={onCancel}
          className="px-3.5 py-2 border border-slate-200 rounded-lg text-xs font-semibold text-slate-500 hover:bg-slate-50 cursor-pointer select-none transition-colors"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="flex items-center justify-center gap-1.5 bg-[#2563eb] hover:bg-blue-600 disabled:bg-blue-400 text-white px-4 py-2 rounded-lg text-xs font-semibold cursor-pointer select-none transition-all shadow-sm"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              <span>Guardando...</span>
            </>
          ) : (
            <span>Registrar</span>
          )}
        </button>
      </div>
    </form>
  );
}
