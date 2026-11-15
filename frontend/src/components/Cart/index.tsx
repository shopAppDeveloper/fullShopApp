"use client";
import { formatMoney, formatNumber } from "@/lib/format";

import React from "react";
import Image from "next/image";
import Link from "next/link";
import Breadcrumb from "../Common/Breadcrumb";
import CouponBox from "../Common/CouponBox";
import { useStore } from "@/app/context/StoreContext";

export default function Cart() {
  const { basket, refreshingBasket, updateBasketQuantity, removeFromBasket, emptyBasket } =
    useStore();

  const currency = basket?.currency ?? "";

  return (
    <>
      <Breadcrumb title="سبد خرید" pages={["سبد خرید"]} />

      <section className="overflow-hidden py-20 bg-gray-2">
        <div className="max-w-[1170px] w-full mx-auto px-4 sm:px-8 xl:px-0">
          {!basket?.lines.length ? (
            <div className="rounded-xl bg-white p-12 text-center shadow-1">
              <h2 className="text-2xl font-medium text-dark">سبد خرید شما خالی است</h2>
              <p className="mt-3 text-gray-5">برای ادامه، محصولی به سبد خرید اضافه کنید.</p>
              <Link
                href="/shop-with-sidebar"
                className="mt-7 inline-flex rounded-md bg-dark px-8 py-3 font-medium text-white hover:bg-blue"
              >
                ادامه خرید
              </Link>
            </div>
          ) : (
            <>
              <div className="mb-7.5 flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-medium text-dark">سبد خرید شما</h2>
                  {refreshingBasket && (
                    <p className="mt-1 text-sm text-gray-5">در حال به‌روزرسانی…</p>
                  )}
                </div>
                <button onClick={emptyBasket} className="text-blue hover:text-blue-dark">
                  خالی کردن سبد خرید
                </button>
              </div>

              <div className="overflow-hidden rounded-[10px] bg-white shadow-1">
                <div className="overflow-x-auto">
                  <div className="min-w-[900px]">
                    <div className="grid grid-cols-[3fr_1fr_1.4fr_1.2fr_50px] gap-5 border-b border-gray-3 px-7.5 py-5">
                      <span className="text-dark">محصول</span>
                      <span className="text-dark">قیمت</span>
                      <span className="text-dark">تعداد</span>
                      <span className="text-dark">جمع جزء</span>
                      <span />
                    </div>

                    {basket.lines.map((line) => (
                      <div
                        key={line.id}
                        className="grid grid-cols-[3fr_1fr_1.4fr_1.2fr_50px] items-center gap-5 border-b border-gray-3 px-7.5 py-6"
                      >
                        <Link
                          href={`/products/${encodeURIComponent(line.slug)}`}
                          className="flex items-center gap-5 min-w-0"
                        >
                          <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-lg bg-gray-2 overflow-hidden">
                            {line.image ? (
                              <Image
                                src={line.image}
                                alt={line.title}
                                width={80}
                                height={80}
                                className="h-full w-full object-contain"
                              />
                            ) : (
                              <span className="text-xs text-gray-4">بدون تصویر</span>
                            )}
                          </div>
                          <div className="min-w-0">
                            <h3 className="truncate font-medium text-dark hover:text-blue">
                              {line.title}
                            </h3>
                            <p className="mt-1 text-sm text-gray-5">کد کالا: {line.sku ?? "—"}</p>
                          </div>
                        </Link>

                        <span className="font-medium text-dark">
                          {formatMoney(line.unit_price, line.currency ?? currency)}
                        </span>

                        <div className="inline-flex w-fit items-center overflow-hidden rounded-md border border-gray-3">
                          <button
                            onClick={() =>
                              updateBasketQuantity(line.id, Math.max(1, line.quantity - 1))
                            }
                            className="px-3 py-2 text-lg hover:bg-gray-1"
                            aria-label={`کم کردن تعداد ${line.title}`}
                          >
                            −
                          </button>
                          <span className="min-w-10 px-3 py-2 text-center text-sm">
                            {line.quantity}
                          </span>
                          <button
                            onClick={() => updateBasketQuantity(line.id, line.quantity + 1)}
                            className="px-3 py-2 text-lg hover:bg-gray-1"
                            aria-label={`افزایش تعداد ${line.title}`}
                          >
                            +
                          </button>
                        </div>

                        <span className="font-medium text-dark">
                          {formatMoney(line.line_total, line.currency ?? currency)}
                        </span>

                        <button
                          onClick={() => removeFromBasket(line.id)}
                          className="text-xl text-gray-5 hover:text-red"
                          aria-label={`حذف ${line.title}`}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-8 flex flex-col gap-7.5 lg:flex-row lg:items-start lg:justify-between">
                <div className="w-full lg:max-w-[480px]">
                  <CouponBox />
                </div>
                <div className="w-full max-w-[420px] rounded-xl bg-white p-7.5 shadow-1">
                  <h3 className="mb-4 font-medium text-dark">خلاصه‌ی سفارش</h3>
                  {basket.lines.map((line) => (
                    <div key={line.id} className="flex justify-between gap-4 pb-2 text-sm">
                      <span className="truncate text-gray-5">{line.title} × {formatNumber(line.quantity)}</span>
                      <span className="shrink-0 text-dark">{formatMoney(line.line_total, line.currency ?? currency)}</span>
                    </div>
                  ))}
                  <div className="mt-3 flex items-center justify-between border-t border-gray-3 pt-4 text-sm">
                    <span className="text-gray-5">جمع جزء</span>
                    <span className="text-dark">{formatMoney(basket.subtotal ?? basket.total, currency)}</span>
                  </div>
                  {Number(basket.discount) > 0 && (
                    <div className="flex items-center justify-between pt-2 text-sm text-green">
                      <span>تخفیف</span>
                      <span>−{formatMoney(basket.discount, currency)}</span>
                    </div>
                  )}
                  <div className="mt-4 flex items-center justify-between border-t border-gray-3 pb-5 pt-4 text-sm">
                    <span className="text-dark">تعداد اقلام</span>
                    <span className="font-medium text-dark">{formatNumber(basket.num_items)}</span>
                  </div>
                  <div className="flex items-center justify-between py-5">
                    <span className="text-lg font-medium text-dark">مجموع</span>
                    <span className="text-lg font-semibold text-dark">
                      {formatMoney(basket.total, currency)}
                    </span>
                  </div>
                  <Link
                    href="/checkout"
                    className="flex w-full justify-center rounded-md bg-blue py-3.5 font-medium text-white hover:bg-blue-dark"
                  >
                    ادامه به تسویه‌حساب
                  </Link>
                </div>
              </div>
            </>
          )}
        </div>
      </section>
    </>
  );
}
