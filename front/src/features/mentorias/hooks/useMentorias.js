import { useQuery } from "@tanstack/react-query";
import MentoriasService from "../services/mentorias.service";

export function useMentorias(servicio = "MENTORIAS") {
  return useQuery({
    queryKey: ["mentorias", servicio],
    queryFn: () => MentoriasService.getProgramas(servicio),
  });
}
