import type { Metadata, Viewport } from "next";

import { getDirection } from "@/i18n/config";
import { getLocale } from "@/i18n/server";
import { I18nProvider } from "@/i18n/client";

import "./css/euclid-circular-a-font.css";
import "./css/vazirmatn-font.css";
import "./css/style.css";

export const metadata: Metadata = {
  title: { default: "فروشگاه من", template: "%s | فروشگاه من" },
  description: "فروشگاه آنلاین کفش و پوشاک",
};

export const viewport: Viewport = { width: "device-width", initialScale: 1 };

/**
 * Root layout (server component): reads the language cookie so the first HTML
 * already has the end `lang` and `dir` - no flash, and the page is fully
 * server-rendered (good for SEO).
 */
export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const locale = await getLocale();

  return (
    <html lang={locale} dir={getDirection(locale)} suppressHydrationWarning>
      <body>
        <I18nProvider locale={locale}>{children}</I18nProvider>
      </body>
    </html>
  );
}
