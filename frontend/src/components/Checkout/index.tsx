"use client";
import { formatMoney } from "@/lib/format";

import { orderStatusLabel } from "@/lib/labels";
import React, { FormEvent, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import Breadcrumb from "../Common/Breadcrumb";
import CouponBox from "../Common/CouponBox";
import {
  createAddress,
  createOrder,
  startPayment,
  getAddresses,
  getCountries,
  getPaymentMethods,
  getShippingMethods,
  type StorePaymentMethod,
  type StoreAddress,
  type StoreCountry,
  type StoreOrder,
} from "@/lib/store-api";
import { useStore } from "@/app/context/StoreContext";

interface FormState {
  first_name: string;
  last_name: string;
  line1: string;
  line2: string;
  city: string;
  state: string;
  postcode: string;
  country: string;
  phone_number: string;
  notes: string;
  save_address: boolean;
}

const initialForm: FormState = {
  first_name: "",
  last_name: "",
  line1: "",
  line2: "",
  city: "",
  state: "",
  postcode: "",
  country: "",
  phone_number: "",
  notes: "",
  save_address: false,
};

export default function Checkout() {
  const { basket, user, loading: storeLoading } = useStore();

  const [countries, setCountries] = useState<StoreCountry[]>([]);
  const [addresses, setAddresses] = useState<StoreAddress[]>([]);
  const [shippingMethods, setShippingMethods] = useState<Awaited<ReturnType<typeof getShippingMethods>>>([]);
  const [shippingCode, setShippingCode] = useState("");
  const [paymentMethods, setPaymentMethods] = useState<StorePaymentMethod[]>([]);
  const [paymentCode, setPaymentCode] = useState("");
  const [form, setForm] = useState<FormState>(initialForm);
  const [loadingData, setLoadingData] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [order, setOrder] = useState<StoreOrder | null>(null);
  const [paying, setPaying] = useState(false);
  const [payError, setPayError] = useState<string | null>(null);

  const shipping = shippingMethods.find((m) => m.code === shippingCode) ?? shippingMethods[0];
  const shippingPrice = shipping?.price ?? "0";
  const shippingCurrency = shipping?.currency ?? "";

  async function handlePay() {
    if (!order) return;
    setPayError(null);
    setPaying(true);
    try {
      const { redirect_url } = await startPayment(order.number, paymentCode || undefined);
      window.location.href = redirect_url;
    } catch (err) {
      setPayError(err instanceof Error ? err.message : "اتصال به درگاه پرداخت انجام نشد.");
      setPaying(false);
    }
  }

  useEffect(() => {
    if (!user) {
      setLoadingData(false);
      return;
    }

    let active = true;

    (async () => {
      try {
        const [countryResult, addressResult, shippingResult, paymentResult] = await Promise.all([
          getCountries(),
          getAddresses(),
          getShippingMethods(),
          getPaymentMethods(),
        ]);

        if (!active) return;

        setCountries(countryResult);
        setAddresses(addressResult);

        setShippingMethods(shippingResult);
        setShippingCode(shippingResult[0]?.code ?? "");
        setPaymentMethods(paymentResult);
        setPaymentCode(paymentResult[0]?.code ?? "");

        const preferred =
          addressResult.find((item) => item.is_default_for_shipping) ?? addressResult[0];

        if (preferred) {
          setForm({
            first_name: preferred.first_name,
            last_name: preferred.last_name,
            line1: preferred.line1,
            line2: preferred.line2,
            city: preferred.line4,
            state: preferred.state,
            postcode: preferred.postcode,
            country: preferred.country,
            phone_number: preferred.phone_number,
            notes: "",
            save_address: false,
          });
        } else if (countryResult.length === 1) {
          setForm((current) => ({
            ...current,
            country: countryResult[0].code,
          }));
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "آماده‌سازی تسویه‌حساب ممکن نشد.");
      } finally {
        if (active) setLoadingData(false);
      }
    })();

    return () => {
      active = false;
    };
  }, [user]);

  const subtotal = basket?.total ?? "0";
  const total = useMemo(() => {
    const subtotalNumber = Number(subtotal);
    const shippingNumber = Number(shippingPrice);
    return Number.isFinite(subtotalNumber + shippingNumber)
      ? (subtotalNumber + shippingNumber).toFixed(0)
      : subtotal;
  }, [subtotal, shippingPrice]);

  function updateField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!user) {
      setError("لطفاً پیش از ثبت سفارش وارد حساب کاربری شوید.");
      return;
    }

    if (!basket || basket.is_empty) {
      setError("سبد خرید شما خالی است.");
      return;
    }

    setError(null);
    setSubmitting(true);

    try {
      if (form.save_address) {
        await createAddress({
          first_name: form.first_name,
          last_name: form.last_name,
          line1: form.line1,
          line2: form.line2,
          line4: form.city,
          state: form.state,
          postcode: form.postcode,
          country: form.country,
          phone_number: form.phone_number,
          is_default_for_shipping: true,
        });
      }

      /**
       * The backend creates a pending order only while the development
       * flag CHECKOUT_ALLOW_PENDING_ORDERS is enabled.
       *
       * A real production payment provider must be connected before
       * treating this flow as a paid checkout.
       */
      if (!paymentCode) {
        setError("هیچ روش پرداختی فعال نیست.");
        setSubmitting(false);
        return;
      }

      const result = await createOrder({
        shipping_method: shippingCode || undefined,
        first_name: form.first_name,
        last_name: form.last_name,
        line1: form.line1,
        line2: form.line2,
        city: form.city,
        state: form.state,
        postcode: form.postcode,
        country: form.country,
        phone_number: form.phone_number,
        notes: form.notes,
      });

      setOrder(result.order);

      // Go straight to the payment gateway; if that fails the confirmation page offers a retry.
      try {
        const { redirect_url } = await startPayment(result.order.number, paymentCode);
        window.location.href = redirect_url;
        return;
      } catch (payErr) {
        setPayError(payErr instanceof Error ? payErr.message : "اتصال به درگاه پرداخت انجام نشد.");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "ثبت سفارش ممکن نشد.");
    } finally {
      setSubmitting(false);
    }
  }

  if (storeLoading || loadingData) {
    return (
      <>
        <Breadcrumb title="تسویه‌حساب" pages={["تسویه‌حساب"]} />
        <section className="bg-gray-2 py-20">
          <div className="mx-auto max-w-[1170px] px-4 text-center">در حال بارگذاری تسویه‌حساب...</div>
        </section>
      </>
    );
  }

  if (!user) {
    return (
      <>
        <Breadcrumb title="تسویه‌حساب" pages={["تسویه‌حساب"]} />
        <section className="bg-gray-2 py-20">
          <div className="mx-auto max-w-[570px] rounded-xl bg-white p-8 text-center shadow-1">
            <h1 className="text-2xl font-semibold text-dark">برای تسویه‌حساب وارد شوید</h1>
            <p className="mt-3 text-gray-5">
              می‌توانید پیش از ورود سبد خرید بسازید، اما برای تسویه‌حساب باید وارد حساب کاربری شوید.
            </p>
            <Link
              href="/signin"
              className="mt-6 inline-flex rounded-md bg-blue px-7 py-3 font-medium text-white hover:bg-blue-dark"
            >
              ورود
            </Link>
          </div>
        </section>
      </>
    );
  }

  if (order) {
    return (
      <>
        <Breadcrumb title="سفارش دریافت شد" pages={["تسویه‌حساب", "/", "تکمیل سفارش"]} />
        <section className="bg-gray-2 py-20">
          <div className="mx-auto max-w-[700px] rounded-xl bg-white p-8 shadow-1">
            <p className="text-sm font-medium text-blue">سفارش ثبت شد</p>
            <h1 className="mt-2 text-3xl font-semibold text-dark">سفارش شماره‌ی {order.number}</h1>
            <p className="mt-4 text-gray-5">
              وضعیت سفارش شما: <strong>{orderStatusLabel(order.status)}</strong>. برای نهایی شدن سفارش، پرداخت را انجام دهید.
            </p>

            <div className="mt-8 border-y border-gray-3 py-5">
              {order.lines.map((line) => (
                <div
                  key={line.id}
                  className="flex items-center justify-between gap-4 border-b border-gray-3 py-3 last:border-b-0"
                >
                  <span>
                    {line.title} × {line.quantity}
                  </span>
                  <span>
                    {formatMoney(line.line_total, order.currency)}
                  </span>
                </div>
              ))}
            </div>

            {payError && (
              <p className="mt-6 rounded-md bg-red-light-6 px-4 py-3 text-sm text-red">{payError}</p>
            )}

            <button
              type="button"
              onClick={handlePay}
              disabled={paying}
              className="mt-6 flex w-full items-center justify-center rounded-md bg-dark px-6 py-3 font-medium text-white hover:bg-blue disabled:opacity-60"
            >
              {paying ? "در حال انتقال به درگاه ..." : `پرداخت ${formatMoney(order.total_incl_tax, order.currency)}`}
            </button>

            <div className="mt-6 flex gap-3">
              <Link
                href="/my-account"
                className="rounded-md bg-blue px-6 py-3 font-medium text-white hover:bg-blue-dark"
              >
                مشاهده‌ی حساب کاربری
              </Link>
              <Link
                href="/shop-with-sidebar"
                className="rounded-md border border-gray-3 px-6 py-3 font-medium text-dark hover:bg-gray-1"
              >
                ادامه خرید
              </Link>
            </div>
          </div>
        </section>
      </>
    );
  }

  return (
    <>
      <Breadcrumb title="تسویه‌حساب" pages={["تسویه‌حساب"]} />

      <section className="bg-gray-2 py-20">
        <div className="mx-auto w-full max-w-[1170px] px-4 sm:px-8 xl:px-0">
          <form onSubmit={handleSubmit}>
            <div className="grid gap-7.5 lg:grid-cols-[1fr_420px]">
              <div className="rounded-xl bg-white p-5 shadow-1 sm:p-8">
                <div>
                  <h2 className="text-xl font-semibold text-dark">اطلاعات ارسال</h2>
                  <p className="mt-1 text-sm text-gray-5">
                    آدرس زیر برای سفارش شما ثبت می‌شود.
                  </p>
                </div>

                {error && (
                  <div className="mt-6 rounded-md bg-red-light-6 px-4 py-3 text-sm text-red">
                    {error}
                  </div>
                )}

                <div className="mt-7 grid gap-5 sm:grid-cols-2">
                  <Field
                    label="نام"
                    value={form.first_name}
                    onChange={(value) => updateField("first_name", value)}
                    required
                  />
                  <Field
                    label="نام خانوادگی"
                    value={form.last_name}
                    onChange={(value) => updateField("last_name", value)}
                    required
                  />
                </div>

                <div className="mt-5">
                  <Field
                    label="نشانی"
                    value={form.line1}
                    onChange={(value) => updateField("line1", value)}
                    required
                  />
                </div>

                <div className="mt-5">
                  <Field
                    label="Apartment / unit (optional)"
                    value={form.line2}
                    onChange={(value) => updateField("line2", value)}
                  />
                </div>

                <div className="mt-5 grid gap-5 sm:grid-cols-2">
                  <Field
                    label="شهر"
                    value={form.city}
                    onChange={(value) => updateField("city", value)}
                    required
                  />
                  <Field
                    label="استان"
                    value={form.state}
                    onChange={(value) => updateField("state", value)}
                  />
                </div>

                <div className="mt-5 grid gap-5 sm:grid-cols-2">
                  <Field
                    label="کد پستی"
                    value={form.postcode}
                    onChange={(value) => updateField("postcode", value)}
                    required
                  />

                  <label className="block">
                    <span className="mb-2.5 block">کشور</span>
                    <select
                      required
                      value={form.country}
                      onChange={(event) => updateField("country", event.target.value)}
                      className="w-full rounded-lg border border-gray-3 bg-gray-1 px-5 py-3 outline-none focus:ring-2 focus:ring-blue/20"
                    >
                      <option value="">انتخاب کشور</option>
                      {countries.map((country) => (
                        <option key={country.code} value={country.code}>
                          {country.name}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>

                <div className="mt-5">
                  <Field
                    label="Phone (optional)"
                    value={form.phone_number}
                    onChange={(value) => updateField("phone_number", value)}
                  />
                </div>

                <div className="mt-5">
                  <label className="block">
                    <span className="mb-2.5 block">توضیحات (اختیاری)</span>
                    <textarea
                      value={form.notes}
                      onChange={(event) => updateField("notes", event.target.value)}
                      rows={4}
                      className="w-full rounded-lg border border-gray-3 bg-gray-1 px-5 py-3 outline-none focus:ring-2 focus:ring-blue/20"
                    />
                  </label>
                </div>

                {addresses.length > 0 && (
                  <div className="mt-6 rounded-lg bg-gray-1 p-4">
                    <p className="font-medium text-dark">نشانی‌های ذخیره‌شده</p>
                    <p className="mt-1 text-sm text-gray-5">
                      آدرس پیش‌فرض شما به‌صورت خودکار بارگذاری شد. پیش از ثبت سفارش می‌توانید فیلدهای بالا را ویرایش کنید.
                    </p>
                  </div>
                )}

                <label className="mt-6 flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={form.save_address}
                    onChange={(event) => updateField("save_address", event.target.checked)}
                  />
                  <span className="text-sm text-gray-5">این آدرس در حساب کاربری من ذخیره شود.</span>
                </label>
              </div>

              <div className="flex h-fit flex-col gap-5">
              <CouponBox />
              <div className="h-fit rounded-xl bg-white p-5 shadow-1 sm:p-8">
                <h2 className="text-xl font-semibold text-dark">سفارش شما</h2>

                <div className="mt-5 border-y border-gray-3">
                  {basket?.lines.map((line) => (
                    <div
                      key={line.id}
                      className="flex justify-between gap-4 border-b border-gray-3 py-4 last:border-b-0"
                    >
                      <div className="text-sm">
                        <p className="font-medium text-dark">{line.title}</p>
                        <p className="mt-1 text-gray-5">تعداد: {line.quantity}</p>
                      </div>
                      <p className="text-sm font-medium text-dark">
                        {formatMoney(line.line_total, line.currency ?? basket.currency ?? "")}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="mt-5 space-y-3">
                  <SummaryRow
                    label="جمع جزء"
                    value={formatMoney(basket?.subtotal ?? subtotal, basket?.currency ?? shippingCurrency)}
                  />
                  {Number(basket?.discount) > 0 && (
                    <SummaryRow
                      label="تخفیف"
                      value={`−${formatMoney(basket?.discount, basket?.currency)}`}
                    />
                  )}
                  <SummaryRow
                    label="ارسال"
                    value={formatMoney(shippingPrice, shippingCurrency || basket?.currency)}
                  />
                  <div className="flex justify-between border-t border-gray-3 pt-4 font-semibold text-dark">
                    <span>مجموع</span>
                    <span>
                      {formatMoney(total, basket?.currency ?? shippingCurrency)}
                    </span>
                  </div>
                </div>

                <h3 className="mt-8 font-medium text-dark">روش ارسال</h3>
                <div className="mt-3 space-y-3">
                  {shippingMethods.map((m) => (
                    <OptionRadio
                      key={m.code}
                      name="shipping"
                      checked={(shipping?.code ?? "") === m.code}
                      onChange={() => setShippingCode(m.code)}
                      title={m.name}
                      hint={m.description}
                      side={Number(m.price) > 0 ? formatMoney(m.price, m.currency) : "رایگان"}
                    />
                  ))}
                </div>

                <h3 className="mt-8 font-medium text-dark">روش پرداخت</h3>
                <div className="mt-3 space-y-3">
                  {paymentMethods.length === 0 && (
                    <p className="rounded-lg bg-yellow-light-4 p-4 text-sm text-dark">
                      در حال حاضر هیچ روش پرداختی فعال نیست. لطفاً بعداً تلاش کنید.
                    </p>
                  )}
                  {paymentMethods.map((m) => (
                    <OptionRadio
                      key={m.code}
                      name="payment"
                      checked={paymentCode === m.code}
                      onChange={() => setPaymentCode(m.code)}
                      title={m.name}
                      hint={m.description}
                    />
                  ))}
                </div>

                <button
                  type="submit"
                  disabled={submitting || !basket || basket.is_empty || !paymentCode}
                  className="mt-6 w-full rounded-md bg-blue px-6 py-3 font-medium text-white hover:bg-blue-dark disabled:cursor-not-allowed disabled:bg-gray-4"
                >
                  {submitting ? "در حال ثبت سفارش..." : "ثبت سفارش و پرداخت"}
                </button>
              </div>
              </div>
            </div>
          </form>
        </div>
      </section>
    </>
  );
}

function Field({
  label,
  value,
  onChange,
  required = false,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
}) {
  return (
    <label className="block">
      <span className="mb-2.5 block">
        {label}
        {required && <span className="ps-1 text-red">*</span>}
      </span>
      <input
        required={required}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-lg border border-gray-3 bg-gray-1 px-5 py-3 outline-none focus:ring-2 focus:ring-blue/20"
      />
    </label>
  );
}

function SummaryRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between gap-4 text-sm">
      <span className="text-gray-5">{label}</span>
      <span className="font-medium text-dark">{value}</span>
    </div>
  );
}

function OptionRadio({
  name,
  checked,
  onChange,
  title,
  hint,
  side,
}: {
  name: string;
  checked: boolean;
  onChange: () => void;
  title: string;
  hint?: string;
  side?: string;
}) {
  return (
    <label
      className={`flex cursor-pointer items-center justify-between gap-4 rounded-lg border p-4 ${checked ? "border-blue bg-blue-light-5/40" : "border-gray-3"}`}
    >
      <span className="flex items-center gap-3">
        <input type="radio" name={name} checked={checked} onChange={onChange} className="accent-blue" />
        <span>
          <span className="block text-sm font-medium text-dark">{title}</span>
          {hint && <span className="block text-xs text-gray-5">{hint}</span>}
        </span>
      </span>
      {side && <span className="shrink-0 text-sm text-dark">{side}</span>}
    </label>
  );
}
