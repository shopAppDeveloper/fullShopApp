"use client";

import React, { FormEvent, useState } from "react";
import { useStore } from "@/app/context/StoreContext";

/** "Have any discount code?" box shared by the cart and the checkout. */
export default function CouponBox() {
  const { basket, applyDiscountCode, removeDiscountCode } = useStore();
  const [code, setCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleApply(event: FormEvent) {
    event.preventDefault();
    if (!code.trim()) return;
    setBusy(true);
    setError(null);
    try {
      await applyDiscountCode(code.trim());
      setCode("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "اعمال کد تخفیف انجام نشد.");
    } finally {
      setBusy(false);
    }
  }

  async function handleRemove(voucher: string) {
    setBusy(true);
    setError(null);
    try {
      await removeDiscountCode(voucher);
    } catch (err) {
      setError(err instanceof Error ? err.message : "حذف کد تخفیف انجام نشد.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="rounded-xl bg-white p-5 shadow-1 sm:p-7.5">
      <h3 className="mb-4 font-medium text-dark">کد تخفیف دارید؟</h3>
      <form onSubmit={handleApply} className="flex gap-3">
        <input
          value={code}
          onChange={(event) => setCode(event.target.value)}
          dir="ltr"
          placeholder="کد تخفیف را وارد کنید"
          className="w-full rounded-md border border-gray-3 bg-gray-1 px-4 py-3 outline-none focus:border-blue"
        />
        <button
          type="submit"
          disabled={busy || !code.trim()}
          className="shrink-0 rounded-md bg-blue px-6 py-3 font-medium text-white hover:bg-blue-dark disabled:opacity-60"
        >
          اعمال
        </button>
      </form>
      {error && <p className="mt-3 text-sm text-red">{error}</p>}
      {basket?.vouchers?.length ? (
        <ul className="mt-4 flex flex-wrap gap-2">
          {basket.vouchers.map((voucher) => (
            <li key={voucher} className="flex items-center gap-2 rounded-full bg-green-light-6 px-3 py-1 text-sm text-green">
              <span dir="ltr">{voucher}</span>
              <button type="button" onClick={() => handleRemove(voucher)} disabled={busy} aria-label="حذف کد تخفیف" className="text-base leading-none">
                ×
              </button>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
