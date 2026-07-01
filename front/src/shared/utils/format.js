const CLUSTER_NAME_MAP = {
  // Florianópolis
  "AEROPORTO_HLZ": "Aeroporto HLZ",
  "CAMPECHE": "Campeche",
  "CANASVIEIRAS": "Canasvieiras",
  "CBD_BEIRAMAR": "CBD Beiramar",
  "CENTRO_HISTORICO": "Centro Histórico",
  "COQUEIROS": "Coqueiros",
  "ESTREITO_CAPOEIRAS": "Estreito Capoeiras",
  "INGLESES": "Ingleses",
  "JURERE": "Jurerê",
  "LAGOA_CONCEICAO": "Lagoa da Conceição",
  "NORTE_ILHA": "Norte da Ilha",
  "RESIDENCIAL_NORTE": "Residencial Norte",
  "SC401": "SC-401",
  "SC401_CORREDOR": "SC-401 CORREDOR",
  "TRINDADE": "Trindade",
  "UFSC": "UFSC",
  "VIA_EXPRESSA": "Via Expressa",
  "VIA_EXPRESSA_CORREDOR": "Via Expressa CORREDOR",

  // São José
  "SAO_JOSE_CENTRO": "São José Centro",
  "SAO_JOSE_KOBRASOL": "São José Kobrasol",
  "SAO_JOSE_ROÇADO": "São José Roçado",
  "SAO_JOSE_ROCADO": "São José Roçado", 

  // Palhoça
  "PALHOCA_CENTRO": "Palhoça Centro",
  "PALHOCA_PEDRA_BRANCA": "Palhoça Pedra Branca",
  "SAO_JOSE_BARREIROS": "São José Barreiros",

  // Biguaçu
  "BIGUACU_BR101_NORTE": "Biguaçu BR-101 Norte",
  "BIGUACU_BR101": "Biguaçu BR-101",
};

export const formatClusterName = (name) => {
  if (!name) return "";
  
  const upperName = name.toUpperCase().trim();

  //  buscar por el nombre original completo
  if (CLUSTER_NAME_MAP[upperName]) {
    return CLUSTER_NAME_MAP[upperName];
  }

  // Limpiamos prefijos y sufijos técnicos y buscamos de nuevo
  const cleanName = upperName
    .replace("FLORIANOPOLIS_", "")
    .replace("_CORREDOR", "");

  if (CLUSTER_NAME_MAP[cleanName]) {
    return CLUSTER_NAME_MAP[cleanName];
  }

  // Fallback genérico: Reemplazamos todos los guiones bajos por espacios y convertimos a Title Case
  return cleanName
    .toLowerCase()
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
};
