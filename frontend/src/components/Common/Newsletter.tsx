"use client";

import Image from "next/image";
import React, { FormEvent, useState } from "react";

import { subscribeNewsletter } from "@/lib/store-api";

const Newsletter = () => {
  const [email, setEmail] = useState("");
  const [state, setState] = useState<"idle" | "loading" | "done" | "error">("idle");
  const [message, setMessage] = useState("");

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setState("loading");
    try {
      const result = await subscribeNewsletter(email.trim());
      setMessage(result.detail);
      setState("done");
      setEmail("");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "ثبت عضویت ممکن نشد.");
      setState("error");
    }
  };

  return (
    <section className="overflow-hidden py-20">
      <div className="max-w-[1170px] mx-auto px-4 sm:px-8 xl:px-0">
        <div className="relative z-1 overflow-hidden rounded-xl">
          <Image
            src="/images/shapes/newsletter-bg.jpg"
            alt=""
            aria-hidden="true"
            className="absolute -z-1 w-full h-full start-0 top-0 rounded-xl"
            width={1170}
            height={200}
          />
          <div className="flex flex-wrap xl:flex-nowrap gap-10 items-center justify-between px-4 py-7.5 sm:px-11 lg:px-14 xl:px-19 sm:py-11 bg-dark/70">
            <div className="max-w-[491px] w-full">
              <h2 className="max-w-[399px] text-white font-bold text-lg sm:text-xl xl:text-heading-4 mb-3">
                جدیدترین ترندها و تخفیف‌ها را از دست ندهید
              </h2>
              <p className="text-white">
                برای دریافت اخبار جدیدترین پیشنهادها و کدهای تخفیف ثبت‌نام کنید
              </p>
            </div>

            <div className="max-w-[477px] w-full">
              <form onSubmit={onSubmit}>
                <div className="flex flex-col sm:flex-row gap-4">
                  <input
                    type="email"
                    name="email"
                    required
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="ایمیل خود را وارد کنید"
                    aria-label="ایمیل"
                    className="w-full rounded-md border border-gray-3 bg-gray-1 text-dark placeholder:text-dark-4 py-3 px-5 outline-none"
                  />
                  <button
                    type="submit"
                    disabled={state === "loading"}
                    className="inline-flex justify-center rounded-md bg-blue py-3 px-7 text-white ease-out duration-200 hover:bg-blue-dark disabled:opacity-60"
                  >
                    {state === "loading" ? "در حال ثبت..." : "عضویت"}
                  </button>
                </div>
              </form>
              {state !== "idle" && state !== "loading" && (
                <p
                  role="status"
                  className={`mt-3 text-custom-sm ${state === "done" ? "text-green-light-4" : "text-red-light-2"}`}
                >
                  {message}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Newsletter;
