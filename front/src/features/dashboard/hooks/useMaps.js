import { useQuery } from "@tanstack/react-query";
import MapsService from "../services/maps.service";

export function useMapsIndicators(category) {
  return useQuery({
    queryKey: ["maps-indicators", category],
    queryFn: () => MapsService.getMapsIndicators(category),
    enabled: !!category,
  });
}
