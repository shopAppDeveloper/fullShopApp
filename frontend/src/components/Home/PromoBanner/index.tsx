import React from "react";
import Link from "next/link";

const campaigns = [
  {
    eyebrow: "انتخاب روزمره",
    title: "قدم‌های راحت‌تر",
    description: "مدل‌های متنوع کفش را ببینید و گزینه مناسب استفاده روزانه‌تان را پیدا کنید.",
    href: "/shop-with-sidebar",
    action: "مشاهده کفش‌ها",
    tone: "bg-[#E7F0FA]",
    accent: "bg-[#D4E5F7]",
    mark: "01",
  },
  {
    eyebrow: "استایل شخصی",
    title: "برای هر سلیقه‌ای",
    description: "محصولات فروشگاه را بررسی کنید و ترکیب مورد علاقه‌تان را بسازید.",
    href: "/shop-with-sidebar",
    action: "رفتن به فروشگاه",
    tone: "bg-[#E7F4F1]",
    accent: "bg-[#CFE9E2]",
    mark: "02",
  },
  {
    eyebrow: "تازه‌های فروشگاه",
    title: "انتخاب‌های تازه",
    description: "جدیدترین محصولات اضافه‌شده به فروشگاه را از نزدیک ببینید.",
    href: "/shop-with-sidebar?sort=latest",
    action: "دیدن تازه‌رسیده‌ها",
    tone: "bg-[#FFF0E8]",
    accent: "bg-[#F9DCCB]",
    mark: "03",
  },
];

export default function PromoBanner() {
  return (
    <section className="overflow-hidden py-16 lg:py-20">
      <div className="mx-auto grid w-full max-w-[1170px] grid-cols-1 gap-5 px-4 sm:px-8 lg:grid-cols-3 xl:px-0">
        {campaigns.map((campaign) => (
          <article
            key={campaign.mark}
            className={`relative isolate min-h-[245px] overflow-hidden rounded-xl ${campaign.tone} p-7 sm:p-8`}
          >
            <span
              aria-hidden="true"
              className={`absolute -left-12 -top-12 -z-10 h-44 w-44 rounded-full ${campaign.accent}`}
            />
            <span
              aria-hidden="true"
              className="absolute bottom-5 left-7 -z-10 text-7xl font-bold tracking-tight text-black/[0.045]"
            >
              {campaign.mark}
            </span>
            <div className="max-w-[270px]">
              <span className="mb-2 block text-sm font-medium text-blue">{campaign.eyebrow}</span>
              <h2 className="mb-3 text-2xl font-semibold text-dark">{campaign.title}</h2>
              <p className="min-h-[52px] text-sm leading-7 text-dark-4">{campaign.description}</p>
              <Link
                href={campaign.href}
                className="mt-6 inline-flex items-center rounded-md bg-dark px-6 py-3 text-sm font-medium text-white transition hover:bg-blue"
              >
                {campaign.action}
              </Link>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
