import { useQuery } from "@tanstack/react-query";
import SaludMentalService from "../services/saludMental.service";

export function useSaludMental(service = "SALUD_MENTAL") {
  return useQuery({
    queryKey: ["saludMental"],
    queryFn: () => SaludMentalService.getSaludMental(service),
  });
}
