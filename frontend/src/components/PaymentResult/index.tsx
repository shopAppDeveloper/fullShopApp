"use client";

import React from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import Breadcrumb from "@/components/Common/Breadcrumb";

const COPY = {
  ok: {
    title: "پرداخت موفق بود",
    text: "پرداخت شما تأیید شد و سفارش در حال پردازش است.",
    tone: "text-green",
  },
  failed: {
    title: "پرداخت انجام نشد",
    text: "پرداخت لغو یا ناموفق بود. مبلغی از حساب شما کسر نشده است؛ در صورت کسر، ظرف چند ساعت برگشت می‌خورد. می‌توانید دوباره تلاش کنید.",
    tone: "text-red",
  },
  pending: {
    title: "در انتظار تأیید",
    text: "نتیجه‌ی پرداخت هنوز تأیید نشده است. وضعیت سفارش را در حساب کاربری بررسی کنید.",
    tone: "text-dark",
  },
} as const;

export default function PaymentResult() {
  const params = useSearchParams();
  const raw = params.get("status");
  const state = raw === "ok" || raw === "pending" ? raw : "failed";
  const order = params.get("order");
  const copy = COPY[state];

  return (
    <>
      <Breadcrumb title="نتیجه‌ی پرداخت" pages={["نتیجه‌ی پرداخت"]} />
      <section className="bg-gray-2 py-20">
        <div className="mx-auto max-w-[600px] rounded-xl bg-white p-8 text-center shadow-1">
          <h1 className={`text-2xl font-semibold ${copy.tone}`}>{copy.title}</h1>
          {order && <p className="mt-3 text-dark">شماره‌ی سفارش: {order}</p>}
          <p className="mt-4 text-gray-5">{copy.text}</p>
          <div className="mt-8 flex justify-center gap-3">
            <Link href="/my-account" className="rounded-md bg-blue px-6 py-3 font-medium text-white hover:bg-blue-dark">
              سفارش‌های من
            </Link>
            <Link href="/shop-with-sidebar" className="rounded-md border border-gray-3 px-6 py-3 font-medium text-dark hover:bg-gray-1">
              ادامه خرید
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
