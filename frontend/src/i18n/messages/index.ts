import type { Locale } from "../config";
import type { MessageDictionary } from "../types";

import { fa } from "./fa";

/** English is the source language: its dictionary is empty (key === text). */
export const messages: Record<Locale, MessageDictionary> = {
  fa,
  en: {},
};
