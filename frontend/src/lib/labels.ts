/** Persian labels for backend (Oscar) status values. Unknown values are shown as-is. */
const ORDER_STATUS_FA: Record<string, string> = {
  Pending: "در انتظار پرداخت",
  "Being processed": "در حال پردازش",
  Processed: "پردازش‌شده",
  Shipped: "ارسال‌شده",
  Delivered: "تحویل‌شده",
  Cancelled: "لغوشده",
};

export function orderStatusLabel(status: string | null | undefined): string {
  if (!status) return "";
  return ORDER_STATUS_FA[status] ?? status;
}
