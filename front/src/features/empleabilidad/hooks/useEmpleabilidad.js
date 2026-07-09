import { useQuery } from "@tanstack/react-query";
import EmpleabilidadService from "../services/empleabilidad.service";

export function useEmpleabilidad(categoria = "EMPLEO") {
  return useQuery({
    queryKey: ["empleabilidad", categoria],
    queryFn: () => EmpleabilidadService.getEmpleabilidad(categoria),
  });
}

export function useIndicadoresEvolucion(categoria = "EMPLEO", indicador = "taxa_emprego_formal", municipio = null) {
  return useQuery({
    queryKey: ["indicadoresEvolucion", categoria, indicador, municipio],
    queryFn: () => EmpleabilidadService.getIndicadoresEvolucion(categoria, indicador, municipio),
  });
}
