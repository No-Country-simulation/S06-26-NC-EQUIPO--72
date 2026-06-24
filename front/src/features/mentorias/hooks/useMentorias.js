import { useQuery } from "@tanstack/react-query";
import MentoriasService from "../services/mentorias.service";

export function useMentoriasBrechas(servicio = "MENTORIA") {
  return useQuery({
    queryKey: ["mentorias-brechas", servicio],
    queryFn: () => MentoriasService.getBrechas(servicio),
  });
}
