import { useQuery } from "@tanstack/react-query";
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
