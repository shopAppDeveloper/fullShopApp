/** Persian number/price formatting shared by all storefront components. */
const nf = new Intl.NumberFormat("fa-IR", { maximumFractionDigits: 2 });

const CURRENCY_FA: Record<string, string> = { IRR: "ریال", IRT: "تومان", USD: "دلار", EUR: "یورو" };

export function formatNumber(value: number | string | null | undefined): string {
  if (value === null || value === undefined || value === "") return "";
  const n = typeof value === "number" ? value : Number(value);
  return Number.isNaN(n) ? String(value) : nf.format(n);
}

/** "1200000.00" + "ریال" -> "۱٬۲۰۰٬۰۰۰ ریال". Money values arrive from Django as strings. */
export function formatMoney(
  amount: number | string | null | undefined,
  currency?: string | null,
): string {
  const num = formatNumber(amount);
  if (!num) return "";
  const label = currency ? (CURRENCY_FA[currency.toUpperCase()] ?? currency) : "";
  return label ? `${num} ${label}` : num;
}
