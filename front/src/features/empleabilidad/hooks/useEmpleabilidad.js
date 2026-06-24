import { useQuery } from "@tanstack/react-query";
import EmpleabilidadService from "../services/empleabilidad.service";

export function useEmpleabilidad(service = "EMPLEO") {
  return useQuery({
    queryKey: ["empleabilidad"],
    queryFn: () => EmpleabilidadService.getEmpleabilidad(service),
  });
}
