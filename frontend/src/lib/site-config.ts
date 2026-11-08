/** Public storefront configuration. */
export const siteConfig = {
  name: process.env.NEXT_PUBLIC_STORE_NAME || "فروشگاه من",
  email: process.env.NEXT_PUBLIC_STORE_EMAIL || "",
  phone: process.env.NEXT_PUBLIC_STORE_PHONE || "",
  address: process.env.NEXT_PUBLIC_STORE_ADDRESS || "",
  facebook: process.env.NEXT_PUBLIC_STORE_FACEBOOK || "",
  instagram: process.env.NEXT_PUBLIC_STORE_INSTAGRAM || "",
  twitter: process.env.NEXT_PUBLIC_STORE_TWITTER || "",
  telegram: process.env.NEXT_PUBLIC_STORE_TELEGRAM || "",
  appStoreUrl: process.env.NEXT_PUBLIC_APP_STORE_URL || "",
  googlePlayUrl: process.env.NEXT_PUBLIC_GOOGLE_PLAY_URL || "",
};
