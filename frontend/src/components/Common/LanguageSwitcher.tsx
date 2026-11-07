"use client";

import { LOCALES, LOCALE_LABELS } from "@/i18n/config";
import { useI18n } from "@/i18n/client";

/** Small FA / EN toggle. The choice is stored in a cookie and applied on the server. */
const LanguageSwitcher = ({ className = "" }: { className?: string }) => {
  const { locale, setLocale, t } = useI18n();

  return (
    <div className={`inline-flex items-center gap-1 ${className}`} role="group" aria-label={t("Language")}>
      {LOCALES.map((code) => (
        <button
          key={code}
          type="button"
          onClick={() => setLocale(code)}
          aria-pressed={locale === code}
          className={`px-2 py-0.5 rounded text-custom-xs font-medium duration-200 ${
            locale === code ? "bg-blue text-white" : "text-dark-4 hover:text-blue"
          }`}
        >
          {LOCALE_LABELS[code].short}
        </button>
      ))}
    </div>
  );
};

export default LanguageSwitcher;
