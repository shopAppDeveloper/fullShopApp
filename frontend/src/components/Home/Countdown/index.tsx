"use client";

import Link from "next/link";
import React, { useEffect, useState } from "react";

import { formatNumber } from "@/lib/format";

import { countdownContent } from "../homeContent";

const UNITS: [string, number][] = [
  ["روز", 86_400_000],
  ["ساعت", 3_600_000],
  ["دقیقه", 60_000],
  ["ثانیه", 1_000],
];

const Countdown = () => {
  const end = Date.parse(countdownContent.endsAt);
  const [now, setNow] = useState<number | null>(null);

  useEffect(() => {
    setNow(Date.now());
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Hidden until an end date is configured and still in the future.
  if (Number.isNaN(end) || now === null || end <= now) return null;

  let remaining = end - now;
  const parts = UNITS.map(([label, ms]) => {
    const value = Math.floor(remaining / ms);
    remaining -= value * ms;
    return { label, value };
  });

  return (
    <section className="overflow-hidden py-10">
      <div className="mx-auto w-full max-w-[1170px] px-4 sm:px-8 xl:px-0">
        <div className="rounded-lg bg-gradient-to-br from-dark to-dark-2 px-6 py-12 text-white sm:px-12 lg:flex lg:items-center lg:justify-between">
          <div className="mb-8 lg:mb-0 lg:max-w-[420px]">
            <span className="mb-2 block font-medium text-teal">{countdownContent.eyebrow}</span>
            <h2 className="mb-3 text-heading-4 font-bold">{countdownContent.title}</h2>
            <p className="mb-6 opacity-80">{countdownContent.text}</p>
            <Link
              href={countdownContent.href}
              className="inline-flex rounded-md bg-blue px-7 py-3 font-medium duration-200 hover:bg-blue-dark"
            >
              {countdownContent.cta}
            </Link>
          </div>
          <div className="flex gap-4" dir="ltr" aria-live="off">
            {parts.map((part) => (
              <div key={part.label} className="min-w-[72px] rounded-md bg-white/10 px-3 py-4 text-center">
                <span className="block text-2xl font-semibold">{formatNumber(part.value)}</span>
                <span className="text-custom-sm opacity-80">{part.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Countdown;
