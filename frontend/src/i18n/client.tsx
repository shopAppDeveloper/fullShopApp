"use client";

import React, { createContext, useCallback, useContext, useMemo } from "react";
import { useRouter } from "next/navigation";

import {
  LOCALE_COOKIE,
  LOCALE_COOKIE_MAX_AGE,
  getDirection,
  type Locale,
} from "./config";
import { createTranslator, formatDate, formatNumber, formatPrice } from "./translate";
import type { TranslateFn } from "./types";

interface I18nContextValue {
  locale: Locale;
  dir: "rtl" | "ltr";
  isRtl: boolean;
  t: TranslateFn;
  setLocale: (locale: Locale) => void;
  /** Number formatted for the active language (Persian digits in fa). */
  n: (value: number | string | null | undefined) => string;
  /** Amount + currency name, e.g. "۱٬۲۰۰٬۰۰۰ ریال". */
  price: (amount: number | string | null | undefined, currency?: string | null) => string;
  /** Date formatted with the Jalali calendar in fa. */
  date: (value: string | number | Date | null | undefined, options?: Intl.DateTimeFormatOptions) => string;
}

const I18nContext = createContext<I18nContextValue | null>(null);

export function I18nProvider({
  locale,
  children,
}: {
  locale: Locale;
  children: React.ReactNode;
}) {
  const router = useRouter();

  const setLocale = useCallback(
    (next: Locale) => {
      if (next === locale) return;

      document.cookie = `${LOCALE_COOKIE}=${next}; path=/; max-age=${LOCALE_COOKIE_MAX_AGE}; samesite=lax`;
      document.documentElement.lang = next;
      document.documentElement.dir = getDirection(next);

      // Re-render the server layout (it reads the cookie) and refresh data.
      router.refresh();
    },
    [locale, router],
  );

  const value = useMemo<I18nContextValue>(
    () => ({
      locale,
      dir: getDirection(locale),
      isRtl: getDirection(locale) === "rtl",
      t: createTranslator(locale),
      setLocale,
      n: (amount) => formatNumber(amount, locale),
      price: (amount, currency) => formatPrice(amount, currency, locale),
      date: (input, options) => formatDate(input, locale, options),
    }),
    [locale, setLocale],
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

/** Full i18n helpers: `const { t, locale, isRtl, n, price, date } = useI18n();` */
export function useI18n() {
  const context = useContext(I18nContext);

  if (!context) {
    throw new Error("useI18n must be used inside <I18nProvider>.");
  }

  return context;
}

/** Shortcut when only the translate function is needed: `const t = useT();` */
export function useT(): TranslateFn {
  return useI18n().t;
}
