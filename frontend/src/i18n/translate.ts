import { DEFAULT_LOCALE, type Locale } from "./config";
import { messages } from "./messages";
import type { TranslateFn, TranslateParams } from "./types";

function interpolate(template: string, params?: TranslateParams): string {
  if (!params) return template;

  return template.replace(/\{(\w+)\}/g, (match, name: string) =>
    name in params ? String(params[name]) : match,
  );
}

/**
 * Build a translate function for a locale.
 *
 * Lookup order: requested locale -> English -> the key itself.
 * A missing key is logged once per key in development so untranslated text
 * is easy to find.
 */
const warned = new Set<string>();

export function createTranslator(
  locale: Locale,
  dictionary: Record<string, string> = messages[locale],
): TranslateFn {
  return (key, params) => {
    const found = dictionary[key] ?? messages.en[key];

    if (found === undefined) {
      if (locale !== "en" && process.env.NODE_ENV !== "production" && !warned.has(key)) {
        warned.add(key);
        console.warn(`[i18n] Missing translation key: ${key}`);
      }
      return key;
    }

    return interpolate(found, params);
  };
}

/** Display number formatting that follows the active language (Persian digits for fa). */
export function formatNumber(
  value: number | string | null | undefined,
  locale: Locale = DEFAULT_LOCALE,
  options?: Intl.NumberFormatOptions,
): string {
  if (value === null || value === undefined || value === "") return "";

  const numeric = typeof value === "number" ? value : Number(value);
  if (Number.isNaN(numeric)) return String(value);

  return new Intl.NumberFormat(locale === "fa" ? "fa-IR" : "en-US", {
    maximumFractionDigits: 2,
    ...options,
  }).format(numeric);
}

const CURRENCY_LABELS: Record<string, Record<Locale, string>> = {
  IRR: { fa: "ریال", en: "IRR" },
  IRT: { fa: "تومان", en: "Toman" },
  USD: { fa: "دلار", en: "USD" },
  EUR: { fa: "یورو", en: "EUR" },
};

/** Human friendly currency name ("IRR" -> "ریال"). Unknown codes are returned unchanged. */
export function currencyLabel(currency: string | null | undefined, locale: Locale): string {
  if (!currency) return "";
  return CURRENCY_LABELS[currency.toUpperCase()]?.[locale] ?? currency;
}

/** "1200000.00", "ریال"  ->  "۱٬۲۰۰٬۰۰۰ ریال" (fa) / "1,200,000 ریال" (en) */
export function formatPrice(
  amount: number | string | null | undefined,
  currency: string | null | undefined,
  locale: Locale = DEFAULT_LOCALE,
): string {
  const formatted = formatNumber(amount, locale);
  if (!formatted) return "";

  const label = currencyLabel(currency, locale);
  return label ? `${formatted} ${label}` : formatted;
}

export function formatDate(
  value: string | number | Date | null | undefined,
  locale: Locale = DEFAULT_LOCALE,
  options: Intl.DateTimeFormatOptions = { year: "numeric", month: "long", day: "numeric" },
): string {
  if (!value) return "";

  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);

  // Persian users expect the Jalali calendar; the "u-ca-persian" extension
  // is supported by every evergreen browser and by Node.
  return new Intl.DateTimeFormat(
    locale === "fa" ? "fa-IR-u-ca-persian" : "en-US",
    options,
  ).format(date);
}
