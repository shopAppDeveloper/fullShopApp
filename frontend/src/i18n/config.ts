/**
 * Locale configuration shared by server and client code.
 *
 * The storefront supports Persian (default, right-to-left) and English.
 * The chosen language is kept in a cookie so that the server can render
 * <html lang dir> correctly on the very first byte (no flash of the wrong
 * direction) and so that the Next.js API proxy can forward the language to
 * Django (API error messages are translated by Django).
 */

export const LOCALES = ["fa", "en"] as const;

export type Locale = (typeof LOCALES)[number];

export const DEFAULT_LOCALE: Locale = "fa";

export const LOCALE_COOKIE = "NEXT_LOCALE";

export const LOCALE_COOKIE_MAX_AGE = 60 * 60 * 24 * 365; // one year

export function isLocale(value: unknown): value is Locale {
  return typeof value === "string" && (LOCALES as readonly string[]).includes(value);
}

export function resolveLocale(value: unknown): Locale {
  return isLocale(value) ? value : DEFAULT_LOCALE;
}

export function getDirection(locale: Locale): "rtl" | "ltr" {
  return locale === "fa" ? "rtl" : "ltr";
}

export const LOCALE_LABELS: Record<Locale, { native: string; short: string }> = {
  fa: { native: "فارسی", short: "FA" },
  en: { native: "English", short: "EN" },
};
