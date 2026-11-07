import React from "react";
import Image from "next/image";

const featureData = [
  {
    img: "/images/icons/icon-01.svg",
    title: "موجودی به‌روز",
    description: "اطلاعات موجودی از سیستم فروشگاه",
  },
  {
    img: "/images/icons/icon-02.svg",
    title: "تنوع سایز و رنگ",
    description: "انتخاب از میان ویژگی‌های واقعی کالا",
  },
  {
    img: "/images/icons/icon-03.svg",
    title: "خرید امن",
    description: "مدیریت نشست و امنیت توسط سرور فروشگاه",
  },
  {
    img: "/images/icons/icon-04.svg",
    title: "میزبانی مستقل",
    description: "کنترل کامل زیرساخت و اطلاعات فروشگاه",
  },
];

const HeroFeature = () => {
  return (
    <div className="mx-auto w-full max-w-[1060px] px-4 sm:px-8 xl:px-0">
      <div className="mt-10 flex flex-wrap items-center justify-between gap-7.5 xl:gap-8">
        {featureData.map((item) => (
          <div className="flex items-center gap-4" key={item.title}>
            <Image src={item.img} alt="" aria-hidden="true" width={40} height={41} />
            <div>
              <h3 className="text-lg font-medium text-dark">{item.title}</h3>
              <p className="text-sm text-dark-4">{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HeroFeature;
