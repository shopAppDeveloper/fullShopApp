/** A flat dictionary: "group.key" -> translated text. {name} placeholders are interpolated. */
export type MessageDictionary = Record<string, string>;

export type TranslateParams = Record<string, string | number>;

export type TranslateFn = (key: string, params?: TranslateParams) => string;
