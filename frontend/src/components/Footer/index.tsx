import Image from "next/image";
import Link from "next/link";
import React from "react";

import { siteConfig } from "@/lib/site-config";

const accountLinks = [
  { title: "حساب کاربری من", href: "/my-account" },
  { title: "ورود / ثبت‌نام", href: "/signin" },
  { title: "سبد خرید", href: "/cart" },
  { title: "علاقه‌مندی‌ها", href: "/wishlist" },
  { title: "سفارش‌های من", href: "/my-account" },
];

const quickLinks = [
  { title: "فروشگاه", href: "/shop-with-sidebar" },
  { title: "پرفروش‌ترین‌ها", href: "/shop-with-sidebar" },
  { title: "تماس با ما", href: "/contact" },
  { title: "سبد خرید", href: "/cart" },
];

const socials = [
  { title: "اینستاگرام", href: siteConfig.instagram },
  { title: "تلگرام", href: siteConfig.telegram },
  { title: "توییتر", href: siteConfig.twitter },
  { title: "فیس‌بوک", href: siteConfig.facebook },
].filter((item) => item.href);

const linkClass = "ease-out duration-200 hover:text-blue";
const headingClass = "mb-7.5 text-custom-1 font-medium text-dark";

const Footer = () => {
  // Jalali (Persian calendar) year, e.g. ۱۴۰۵
  const year = new Intl.DateTimeFormat("fa-IR-u-ca-persian", { year: "numeric" }).format(new Date());
  const hasApp = Boolean(siteConfig.appStoreUrl || siteConfig.googlePlayUrl);

  return (
    <footer className="overflow-hidden border-t border-gray-3 bg-white">
      <div className="mx-auto max-w-[1170px] px-4 sm:px-8 xl:px-0">
        <div className="grid gap-10 pb-10 pt-17.5 sm:grid-cols-2 xl:grid-cols-4 xl:gap-12 xl:pb-15 xl:pt-22.5">
          {/* Column 1: brand + contact */}
          <div>
            <Link href="/" className="mb-6 inline-block">
              <Image src="/images/logo/logo.svg" alt={siteConfig.name} width={219} height={36} />
            </Link>
            <ul className="flex flex-col gap-3 text-custom-sm text-dark-2">
              <li>{siteConfig.address || "نشانی فروشگاه توسط مدیر تنظیم می‌شود."}</li>
              <li>
                {siteConfig.phone ? (
                  <a href={`tel:${siteConfig.phone}`} className={linkClass} dir="ltr">
                    {siteConfig.phone}
                  </a>
                ) : (
                  "شماره تلفن فروشگاه توسط مدیر تنظیم می‌شود."
                )}
              </li>
              <li>
                {siteConfig.email ? (
                  <a href={`mailto:${siteConfig.email}`} className={linkClass}>
                    {siteConfig.email}
                  </a>
                ) : (
                  "ایمیل فروشگاه توسط مدیر تنظیم می‌شود."
                )}
              </li>
            </ul>
            {socials.length > 0 && (
              <ul className="mt-6 flex flex-wrap gap-2.5">
                {socials.map((item) => (
                  <li key={item.title}>
                    <a
                      href={item.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="rounded-full border border-gray-3 px-3.5 py-1.5 text-custom-sm text-dark duration-200 hover:border-blue hover:text-blue"
                    >
                      {item.title}
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Column 2: account */}
          <div>
            <h2 className={headingClass}>حساب کاربری</h2>
            <ul className="flex flex-col gap-3.5 text-custom-sm text-dark-2">
              {accountLinks.map((item) => (
                <li key={item.title}>
                  <Link href={item.href} className={linkClass}>
                    {item.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3: quick links */}
          <div>
            <h2 className={headingClass}>دسترسی سریع</h2>
            <ul className="flex flex-col gap-3.5 text-custom-sm text-dark-2">
              {quickLinks.map((item) => (
                <li key={item.title}>
                  <Link href={item.href} className={linkClass}>
                    {item.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 4: app download (only when real store links are configured) or support */}
          <div>
            <h2 className={headingClass}>{hasApp ? "دانلود اپلیکیشن" : "پشتیبانی"}</h2>
            {hasApp ? (
              <div className="flex flex-col gap-3 text-custom-sm">
                {siteConfig.appStoreUrl && (
                  <a href={siteConfig.appStoreUrl} target="_blank" rel="noopener noreferrer"
                    className="rounded-md bg-dark px-5 py-3 text-white duration-200 hover:bg-blue">
                    دانلود از اپ استور
                  </a>
                )}
                {siteConfig.googlePlayUrl && (
                  <a href={siteConfig.googlePlayUrl} target="_blank" rel="noopener noreferrer"
                    className="rounded-md bg-dark px-5 py-3 text-white duration-200 hover:bg-blue">
                    دریافت از گوگل پلی
                  </a>
                )}
              </div>
            ) : (
              <div className="text-custom-sm text-dark-2">
                <p className="mb-4">برای پرسش درباره‌ی سفارش یا محصولات با ما در ارتباط باشید.</p>
                <Link href="/contact" className="inline-flex rounded-md bg-blue px-5 py-3 text-white duration-200 hover:bg-blue-dark">
                  تماس با ما
                </Link>
              </div>
            )}
          </div>
        </div>

        <div className="border-t border-gray-3 py-5 text-center text-custom-sm text-dark-3">
          © {year} {siteConfig.name} - تمامی حقوق محفوظ است.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
