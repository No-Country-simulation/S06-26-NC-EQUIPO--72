import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import FormacionesService from "../services/formaciones.service";


export function useFormacionesList(tipo = "FORMACION") {
  return useQuery({

    queryKey: ["formaciones-list", tipo],
    queryFn: () => FormacionesService.getProgramas(tipo),
  });
}

export function useFormacionesBrechas(servicio = "FORMACION") {
  return useQuery({
    queryKey: ["formaciones-brechas", servicio],
    queryFn: () => FormacionesService.getBrechas(servicio),
  });
}

export function useCreateFormacion() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => FormacionesService.createProgram(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["formaciones-list"] });
      queryClient.invalidateQueries({ queryKey: ["formaciones-brechas"] });
    },
  });
}
