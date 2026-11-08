import Link from "next/link";

import { promoBanners, type PromoBannerContent } from "../homeContent";

const TONES: Record<PromoBannerContent["tone"], string> = {
  blue: "from-blue to-blue-dark",
  teal: "from-teal to-teal-dark",
  orange: "from-orange to-orange-dark",
};

const Card = ({ banner, large = false }: { banner: PromoBannerContent; large?: boolean }) => (
  <div
    className={`relative overflow-hidden rounded-lg bg-gradient-to-br ${TONES[banner.tone]} text-white ${
      large ? "px-6 py-10 sm:px-10 lg:row-span-2 lg:py-16" : "px-6 py-8 sm:px-8"
    }`}
  >
    <span className="mb-2.5 block text-custom-sm font-medium opacity-90">{banner.eyebrow}</span>
    <h3 className={`font-semibold ${large ? "mb-3 text-heading-4" : "mb-2 text-heading-6"}`}>{banner.title}</h3>
    <p className={`mb-6 max-w-[360px] ${large ? "text-custom-lg" : "text-custom-sm"} opacity-90`}>{banner.text}</p>
    <Link
      href={banner.href}
      className="inline-flex rounded-md bg-white px-6 py-2.5 text-custom-sm font-medium text-dark duration-200 hover:bg-dark hover:text-white"
    >
      {banner.cta}
    </Link>
  </div>
);

const PromoBanner = () => {
  const [main, ...rest] = promoBanners;
  if (!main) return null;
  return (
    <section className="overflow-hidden py-20">
      <div className="mx-auto w-full max-w-[1170px] px-4 sm:px-8 xl:px-0">
        <div className="grid gap-7.5 lg:grid-cols-2">
          <Card banner={main} large />
          {rest.slice(0, 2).map((banner) => (
            <Card key={banner.title} banner={banner} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default PromoBanner;
