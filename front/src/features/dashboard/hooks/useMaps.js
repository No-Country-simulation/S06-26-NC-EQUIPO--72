import { useQuery } from "@tanstack/react-query";
import MapsService from "../services/maps.service";

export function useMapsIndicators(category, indicator = null) {
  return useQuery({
    queryKey: ["maps-indicators", category, indicator],
    queryFn: () => MapsService.getMapsIndicators(category, indicator),
    enabled: !!category,
  });
}

export function useRegions() {
  return useQuery({
    queryKey: ["regions"],
    queryFn: () => MapsService.getRegions(),
  });
}

export function useMapData(params = {}) {
  return useQuery({
    queryKey: ["map-data", params],
    queryFn: () => MapsService.getMapData(params),
  });
}

export function usePrograms(params = {}) {
  return useQuery({
    queryKey: ["programs", params],
    queryFn: () => MapsService.getPrograms(params),
  });
}
