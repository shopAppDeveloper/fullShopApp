/**
 * Editable marketing content for the home page.
 * Nothing here is invented: sections with no data are simply not rendered.
 */

export interface PromoBannerContent {
  eyebrow: string;
  title: string;
  text: string;
  cta: string;
  href: string;
  tone: "blue" | "teal" | "orange";
}

export const promoBanners: PromoBannerContent[] = [
  {
    eyebrow: "تازه‌ها",
    title: "جدیدترین محصولات فروشگاه",
    text: "تازه‌ترین کفش‌ها و پوشاک اضافه‌شده به کاتالوگ را ببینید.",
    cta: "مشاهده‌ی محصولات",
    href: "/shop-with-sidebar",
    tone: "blue",
  },
  {
    eyebrow: "ویژه",
    title: "پرفروش‌ترین‌ها",
    text: "محصولاتی که بیشتر از همه انتخاب می‌شوند.",
    cta: "خرید کنید",
    href: "/shop-with-sidebar",
    tone: "teal",
  },
  {
    eyebrow: "دسته‌بندی‌ها",
    title: "همه‌ی دسته‌بندی‌ها",
    text: "بر اساس دسته‌بندی دنبال محصول بگردید.",
    cta: "مرور دسته‌بندی‌ها",
    href: "/shop-with-sidebar",
    tone: "orange",
  },
];

/** Shown only while `NEXT_PUBLIC_PROMO_ENDS_AT` (ISO date, e.g. 2026-12-01T00:00:00+03:30) is in the future. */
export const countdownContent = {
  eyebrow: "پیشنهاد ویژه",
  title: "فرصت محدود برای خرید",
  text: "پیش از پایان زمان پیشنهاد، سفارش خود را ثبت کنید.",
  cta: "مشاهده‌ی محصولات",
  href: "/shop-with-sidebar",
  endsAt: process.env.NEXT_PUBLIC_PROMO_ENDS_AT ?? "",
};

export interface Testimonial {
  name: string;
  role?: string;
  review: string;
}

/** Add only REAL customer reviews here (with permission). While empty, the section is hidden. */
export const testimonials: Testimonial[] = [];
