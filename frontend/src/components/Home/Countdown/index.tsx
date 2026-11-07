"use client";

import React, { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { adaptOscarProduct, getProducts } from "@/lib/store-api";
import type { Product } from "@/types/product";

/**
 * NextMerce-style wide feature panel, populated from the live Oscar catalogue.
 * We avoid showing an expired timer or an unconfigured discount.
 */
export default function Countdown() {
  const [product, setProduct] = useState<Product | null>(null);

  useEffect(() => {
    let active = true;
    getProducts({ sort: "priority", page: 1 })
      .then((response) => {
        if (!active) return;
        const featured = response.results[0];
        setProduct(featured ? adaptOscarProduct(featured) : null);
      })
      .catch(() => {
        if (active) setProduct(null);
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <section className="overflow-hidden pb-16 lg:pb-20">
      <div className="mx-auto w-full max-w-[1170px] px-4 sm:px-8 xl:px-0">
        <div className="relative isolate overflow-hidden rounded-xl bg-[#DCECF4] px-6 py-10 sm:px-10 lg:min-h-[310px] lg:px-14 lg:py-14">
          <div aria-hidden="true" className="absolute -bottom-28 -left-16 -z-10 h-80 w-80 rounded-full bg-white/40" />
          <div className="relative z-10 max-w-[510px]">
            <span className="mb-2 block text-sm font-medium text-blue">پیشنهاد فروشگاه</span>
            <h2 className="mb-3 text-2xl font-bold text-dark sm:text-3xl">انتخاب بعدی شما اینجاست</h2>
            <p className="max-w-[440px] leading-7 text-dark-4">
              محصولات فروشگاه را ببینید، جزئیات و موجودی را بررسی کنید و با خیال راحت انتخاب کنید.
            </p>
            <Link
              href={product?.slug ? `/products/${encodeURIComponent(product.slug)}` : "/shop-with-sidebar"}
              className="mt-6 inline-flex rounded-md bg-blue px-8 py-3 text-sm font-medium text-white transition hover:bg-blue-dark"
            >
              {product ? "مشاهده محصول منتخب" : "مشاهده فروشگاه"}
            </Link>
          </div>

          {product?.imgs?.previews?.[0] ? (
            <div className="relative mt-8 flex h-52 items-center justify-center sm:h-64 lg:absolute lg:bottom-0 lg:left-12 lg:mt-0 lg:h-[285px] lg:w-[360px]">
              <Image
                src={product.imgs.previews[0]}
                alt={product.title}
                fill
                sizes="(min-width: 1024px) 360px, 80vw"
                className="object-contain"
              />
            </div>
          ) : (
            <div aria-hidden="true" className="absolute -bottom-16 left-10 hidden h-64 w-64 rounded-full border-[28px] border-white/30 lg:block" />
          )}
        </div>
      </div>
    </section>
  );
}
