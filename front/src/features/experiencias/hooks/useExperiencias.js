import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import ExperienciasService from "../services/experiencias.service";

/**
 * Hook para obtener la lista de experiencias desde el backend.
 * Utiliza React Query para almacenar en caché la respuesta y administrar los estados de carga.
 * 
 * @returns {Object} Consulta de React Query con los datos y estados
 */
export function useExperienciasList() {
  return useQuery({
    // La queryKey identifica la petición de manera única en el caché global
    queryKey: ["experiencias-list"],
    // Llamamos a nuestro servicio para obtener experiencias filtrando por tipo "EXPERIENCIA"
    queryFn: () => ExperienciasService.getProgramas("EXPERIENCIA"),
  });
}

/**
 * Hook para obtener las brechas territoriales y de cobertura de servicios
 * asociados a las experiencias.
 * 
 * @returns {Object} Consulta de React Query con los datos de brechas
 */
export function useExperienciasBrechas() {
  return useQuery({
    // La queryKey identifica las brechas de experiencias en la caché
    queryKey: ["experiencias-brechas"],
    queryFn: () => ExperienciasService.getBrechas("EXPERIENCIA"),
  });
}

/**
 * Hook de mutación para registrar una nueva experiencia en la base de datos.
 * Al completarse con éxito, invalida las consultas de la caché de React Query
 * para provocar una actualización y re-renderizado automático e inmediato en la interfaz.
 * 
 * @returns {Object} Mutación de React Query para disparar el guardado
 */
export function useCreateExperiencia() {
  const queryClient = useQueryClient();
  
  return useMutation({
    // Definimos la función de mutación que enviará los datos del formulario al servicio
    mutationFn: (payload) => ExperienciasService.createProgram(payload),
    // onSuccess se ejecuta al recibir una respuesta exitosa (HTTP 200/201) del backend
    onSuccess: () => {
      // Invalidamos las queries de la caché asociadas a las experiencias.
      // Esto fuerza a React Query a re-ejecutar las llamadas fetch y traer los datos frescos.
      queryClient.invalidateQueries({ queryKey: ["experiencias-list"] });
      queryClient.invalidateQueries({ queryKey: ["experiencias-brechas"] });
    },
  });
}
