import { useState, useEffect } from "react";
import { LanguageContext, STORAGE_KEY } from "./LanguageContext";

export function LanguageProvider({ children, defaultLanguage = "es" }) {
  const [language, setLanguage] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved === "es" || saved === "pt" ? saved : defaultLanguage;
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, language);
  }, [language]);

  const toggleLanguage = () => {
    setLanguage((prev) => (prev === "es" ? "pt" : "es"));
  };

  const value = {
    language,
    setLanguage,
    toggleLanguage,
    isEs: language === "es",
    isPt: language === "pt",
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}
