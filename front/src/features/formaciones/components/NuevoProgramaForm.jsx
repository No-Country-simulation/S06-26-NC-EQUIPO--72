import { useForm } from "react-hook-form";
import { Loader2 } from "lucide-react";
import { useCreateFormacion } from "../hooks/useFormaciones";
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

export default function NuevoProgramaForm({ onSubmitSuccess, onCancel }) {
  // Obtenemos el disparador de la mutación de React Query
  const { mutateAsync: createProgram } = useCreateFormacion();

  // Inicializamos react-hook-form con valores predeterminados y limpios
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
      impactoEstimado: "MEDIO",
      fechaInicio: new Date().toISOString().split("T")[0], // Ponemos la fecha de hoy por defecto
    },
  });

  // Ejecutado al validar y enviar el formulario de manera correcta
  const onSubmit = async (data) => {
    try {
      // Formamos el payload completo que requiere el backend
      const payload = {
        ...data,
        tipo: "FORMACION", // Tipo de programa fijo para esta sección
        municipio: "Florianópolis", // Municipio fijo en Florianópolis
        activo: true, // Se registra activo por defecto
        replicable: 1, // Marcar replicable
      };

      // Disparamos la petición POST mediante React Query y esperamos su respuesta
      await createProgram(payload);

      // Notificamos éxito para cerrar el modal y actualizar listas
      if (onSubmitSuccess) {
        onSubmitSuccess();
      }
    } catch (error) {
      // Capturamos posibles fallos de red o de validación del backend y los mostramos en el formulario
      setError("root", {
        type: "server",
        message: error.message || "Error inesperado al crear el programa",
      });
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-4 bg-white rounded-xl p-6 w-full max-w-md mx-auto"
    >
      <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
        <h3 className="text-sm font-bold text-slate-800">
          Registrar Nuevo Programa de Formación
        </h3>
      </div>

      {/* Alerta de Error de Servidor */}
      {errors.root && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-[11px] text-red-600 font-semibold leading-relaxed">
          {errors.root.message}
        </div>
      )}

      {/* Input: Nombre del programa (Obligatorio, mínimo 5 caracteres) */}
      <div className="space-y-1">
        <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Nombre del Programa
        </label>
        <input
          type="text"
          className={`w-full bg-slate-50 border rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:bg-white transition-all ${
            errors.nombre
              ? "border-red-500"
              : "border-slate-200 focus:border-blue-500"
          }`}
          placeholder="Ej: Curso intensivo de IoT Aplicado"
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

      {/* Textarea: Descripción (Obligatorio) */}
      <div className="space-y-1">
        <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Descripción del Programa
        </label>
        <textarea
          rows={3}
          className={`w-full bg-slate-50 border rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:bg-white transition-all resize-none ${
            errors.descripcion
              ? "border-red-500"
              : "border-slate-200 focus:border-blue-500"
          }`}
          placeholder="Describa brevemente los objetivos generales del curso..."
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

      {/* Select: Clústeres (Obligatorio) */}
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

      {/* Grid: Organización Responsable + Impacto Estimado */}
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Organización Responsable
          </label>
          <input
            type="text"
            className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
            placeholder="Ej: Prefeitura Floripa"
            {...register("organizacion")}
          />
        </div>

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
      </div>

      {/* Input Date: Fecha de Inicio */}
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

      {/* Botones de Envío / Cancelación */}
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
