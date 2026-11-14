/** Persian number/price formatting shared by all storefront components. */
const nf = new Intl.NumberFormat("fa-IR", { maximumFractionDigits: 2 });

const nfMoney = new Intl.NumberFormat("fa-IR", { maximumFractionDigits: 0 });
const TOMAN = "تومان";

/** The store sells in Toman only (whole numbers); any legacy/unknown label is shown as Toman. */
export function currencyLabel(_currency?: string | null): string {
  return TOMAN;
}

export function formatNumber(value: number | string | null | undefined): string {
  if (value === null || value === undefined || value === "") return "";
  const n = typeof value === "number" ? value : Number(value);
  return Number.isNaN(n) ? String(value) : nf.format(n);
}

/** "1200000" -> "۱٬۲۰۰٬۰۰۰ تومان". Money values arrive from Django as strings. */
export function formatMoney(
  amount: number | string | null | undefined,
  _currency?: string | null,
): string {
  if (amount === null || amount === undefined || amount === "") return "";
  const n = Number(amount);
  if (Number.isNaN(n)) return String(amount);
  return `${nfMoney.format(n)} ${TOMAN}`;
}
