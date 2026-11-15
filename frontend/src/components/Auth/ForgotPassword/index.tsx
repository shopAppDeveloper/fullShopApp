"use client";

import React, { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Breadcrumb from "@/components/Common/Breadcrumb";
import { requestPasswordOtp, resetPassword } from "@/lib/store-api";
import { formatNumber } from "@/lib/format";
import { ErrorBox, Field, InfoBox, buttonClass, errorText, inputClass, useCountdown } from "../shared";

/** Step 1: mobile number -> SMS code. Step 2: code + new password. */
export default function ForgotPassword() {
  const router = useRouter();
  const [step, setStep] = useState<1 | 2>(1);
  const [mobile, setMobile] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const resend = useCountdown(60);

  async function sendCode(event?: FormEvent) {
    event?.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await requestPasswordOtp(mobile.trim());
      setStep(2);
      setInfo("اگر این شماره در فروشگاه ثبت شده باشد، کد تأیید پیامک می‌شود.");
      resend.start();
    } catch (err) {
      setError(errorText(err, "ارسال کد انجام نشد."));
    } finally {
      setSubmitting(false);
    }
  }

  async function handleReset(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    if (password !== confirm) {
      setError("رمزهای عبور مطابقت ندارند.");
      return;
    }
    setSubmitting(true);
    try {
      await resetPassword({ mobile: mobile.trim(), code: code.trim(), password });
      router.push("/signin");
    } catch (err) {
      setError(errorText(err, "تغییر رمز انجام نشد."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <Breadcrumb title="فراموشی رمز عبور" pages={["فراموشی رمز عبور"]} />

      <section className="overflow-hidden bg-gray-2 py-20">
        <div className="mx-auto w-full max-w-[1170px] px-4 sm:px-8 xl:px-0">
          <div className="mx-auto w-full max-w-[570px] rounded-xl bg-white p-4 shadow-1 sm:p-7.5 xl:p-11">
            <div className="mb-11 text-center">
              <h2 className="mb-1.5 text-xl font-semibold text-dark sm:text-2xl">بازیابی رمز عبور</h2>
              <p className="text-gray-5">کد تأیید به شماره موبایل ثبت‌شده‌ی شما پیامک می‌شود.</p>
            </div>

            {step === 1 ? (
              <form onSubmit={sendCode}>
                <Field id="mobile" label="شماره موبایل">
                  <input required id="mobile" type="tel" dir="ltr" inputMode="numeric" autoComplete="tel" value={mobile} onChange={(e) => setMobile(e.target.value)} placeholder="09123456789" className={inputClass} />
                </Field>
                <ErrorBox message={error} />
                <button type="submit" disabled={submitting} className={buttonClass}>
                  {submitting ? "در حال ارسال ..." : "ارسال کد تأیید"}
                </button>
              </form>
            ) : (
              <form onSubmit={handleReset}>
                <InfoBox message={info} />
                <Field id="code" label={`کد تأیید ارسال‌شده به ${formatNumber(mobile)}`}>
                  <input required id="code" dir="ltr" inputMode="numeric" autoComplete="one-time-code" maxLength={6} value={code} onChange={(e) => setCode(e.target.value)} className={inputClass} />
                </Field>
                <div className="-mt-2 mb-5 flex justify-between text-sm">
                  <button type="button" className="text-blue" onClick={() => setStep(1)}>
                    تغییر شماره
                  </button>
                  <button type="button" disabled={resend.left > 0 || submitting} className="text-blue disabled:text-gray-5" onClick={() => sendCode()}>
                    {resend.left > 0 ? `ارسال دوباره (${formatNumber(resend.left)})` : "ارسال دوباره کد"}
                  </button>
                </div>
                <Field id="password" label="رمز عبور جدید">
                  <input required id="password" type="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} className={inputClass} />
                </Field>
                <Field id="confirm" label="تکرار رمز عبور جدید">
                  <input required id="confirm" type="password" autoComplete="new-password" value={confirm} onChange={(e) => setConfirm(e.target.value)} className={inputClass} />
                </Field>
                <ErrorBox message={error} />
                <button type="submit" disabled={submitting} className={buttonClass}>
                  {submitting ? "در حال ثبت ..." : "تغییر رمز عبور"}
                </button>
              </form>
            )}

            <p className="mt-6 text-center">
              <Link href="/signin" className="text-dark duration-200 ease-out hover:text-blue">
                بازگشت به ورود
              </Link>
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
