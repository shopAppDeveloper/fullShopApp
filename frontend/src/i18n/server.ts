import { cookies } from "next/headers";

import { LOCALE_COOKIE, resolveLocale, type Locale } from "./config";
import { createTranslator } from "./translate";

/** Active locale for the current request (server components, route handlers). */
export async function getLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  return resolveLocale(cookieStore.get(LOCALE_COOKIE)?.value);
}

/** Translator for the current request: `const t = await getT();` */
export async function getT() {
  return createTranslator(await getLocale());
}
