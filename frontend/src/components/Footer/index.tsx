import React from "react";
import Link from "next/link";
import { siteConfig } from "@/lib/site-config";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="mt-4 overflow-hidden border-t border-gray-3 bg-[#F7F8FA]">
      <div className="mx-auto w-full max-w-[1170px] px-4 sm:px-8 xl:px-0">
        <div className="grid grid-cols-1 gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8 lg:py-16">
          <div className="lg:col-span-1">
            <h2 className="mb-5 text-base font-semibold text-dark">راهنما و پشتیبانی</h2>
            <p className="mb-5 max-w-[290px] text-sm leading-7 text-dark-4">
              برای راهنمایی درباره محصولات و پیگیری خرید، از راه‌های ارتباطی فروشگاه استفاده کنید.
            </p>
            <ul className="flex flex-col gap-3 text-sm text-dark-3">
              <li>
                <span className="font-medium text-dark">نشانی: </span>
                {siteConfig.address || "نشانی فروشگاه ثبت نشده است."}
              </li>
              <li>
                <span className="font-medium text-dark">تلفن: </span>
                {siteConfig.phone ? (
                  <a className="hover:text-blue" href={`tel:${siteConfig.phone}`}>{siteConfig.phone}</a>
                ) : "شماره تماس ثبت نشده است."}
              </li>
              <li>
                <span className="font-medium text-dark">ایمیل: </span>
                {siteConfig.email ? (
                  <a className="hover:text-blue" href={`mailto:${siteConfig.email}`}>{siteConfig.email}</a>
                ) : "ایمیل فروشگاه ثبت نشده است."}
              </li>
            </ul>
          </div>

          <div>
            <h2 className="mb-5 text-base font-semibold text-dark">حساب کاربری</h2>
            <ul className="flex flex-col gap-3 text-sm text-dark-3">
              <li><Link className="transition hover:text-blue" href="/my-account">حساب کاربری من</Link></li>
              <li><Link className="transition hover:text-blue" href="/signin">ورود به حساب</Link></li>
              <li><Link className="transition hover:text-blue" href="/signup">ساخت حساب کاربری</Link></li>
              <li><Link className="transition hover:text-blue" href="/cart">سبد خرید</Link></li>
              <li><Link className="transition hover:text-blue" href="/wishlist">علاقه‌مندی‌ها</Link></li>
            </ul>
          </div>

          <div>
            <h2 className="mb-5 text-base font-semibold text-dark">دسترسی سریع</h2>
            <ul className="flex flex-col gap-3 text-sm text-dark-3">
              <li><Link className="transition hover:text-blue" href="/shop-with-sidebar">همه محصولات</Link></li>
              <li><Link className="transition hover:text-blue" href="/shop-without-sidebar">نمایش بدون فیلتر</Link></li>
              <li><Link className="transition hover:text-blue" href="/checkout">تسویه‌حساب</Link></li>
              <li><Link className="transition hover:text-blue" href="/contact">تماس با ما</Link></li>
            </ul>
          </div>

          <div>
            <h2 className="mb-5 text-base font-semibold text-dark">خرید مطمئن</h2>
            <p className="text-sm leading-7 text-dark-4">
              اطلاعات محصولات، قیمت و موجودی از سامانه فروشگاه دریافت می‌شود. پیش از ثبت نهایی سفارش،
              جزئیات سبد خرید و اطلاعات ارسال را بررسی کنید.
            </p>
            <Link
              href="/shop-with-sidebar"
              className="mt-5 inline-flex rounded-md bg-dark px-6 py-3 text-sm font-medium text-white transition hover:bg-blue"
            >
              ورود به فروشگاه
            </Link>
          </div>
        </div>

        <div className="flex flex-col items-center justify-between gap-3 border-t border-gray-3 py-5 text-center text-xs text-dark-4 sm:flex-row sm:text-right">
          <p>© {year} {siteConfig.name || "فروشگاه"}. تمامی حقوق محفوظ است.</p>
          <p>طراحی‌شده با Next.js و متصل به Django Oscar</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
