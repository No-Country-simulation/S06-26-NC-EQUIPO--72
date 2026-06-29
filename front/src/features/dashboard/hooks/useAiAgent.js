import { useMutation } from "@tanstack/react-query";
import AiService from "../services/ai.service";

export function useAiAgent() {
  return useMutation({
    mutationFn: ({ consulta, idioma }) => AiService.queryAiAgent(consulta, idioma),
  });
}
