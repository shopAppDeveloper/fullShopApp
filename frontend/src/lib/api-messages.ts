/** Persian versions of the messages returned by the Django API. Unknown messages are shown as received. */
const API_MESSAGES_FA: Record<string, string> = {
  "Address not found.": "آدرس پیدا نشد.",
  "Address saved.": "آدرس ذخیره شد.",
  "An account with this email already exists.": "حسابی با این ایمیل قبلاً ثبت شده است.",
  "Basket line not found.": "این مورد در سبد خرید پیدا نشد.",
  "Email and password are required.": "ایمیل و رمز عبور الزامی است.",
  "Enter a valid email address.": "یک ایمیل معتبر وارد کنید.",
  "Invalid country. Configure countries in Oscar before checkout.": "کشور نامعتبر است.",
  "Invalid country.": "کشور نامعتبر است.",
  "Invalid email or password.": "ایمیل یا رمز عبور نادرست است.",
  "Logged out successfully.": "با موفقیت خارج شدید.",
  "Order not found.": "سفارش پیدا نشد.",
  "Product not found.": "محصول پیدا نشد.",
  "Quantity must be between 1 and 99.": "تعداد باید بین ۱ تا ۹۹ باشد.",
  "Required shipping fields are missing.": "فیلدهای ضروری آدرس ارسال تکمیل نشده است.",
  "Select a product variant before adding it to the basket.": "پیش از افزودن به سبد، تنوع محصول (سایز/رنگ) را انتخاب کنید.",
  "Subscribed.": "عضویت شما ثبت شد.",
  "The order could not be created.": "ثبت سفارش ممکن نشد.",
  "The product could not be added to the basket.": "محصول به سبد خرید اضافه نشد.",
  "This account is not active.": "این حساب کاربری فعال نیست.",
  "Your basket is empty.": "سبد خرید شما خالی است.",
  "Authentication credentials were not provided.": "برای این کار باید وارد حساب کاربری شوید.",
  "You do not have permission to perform this action.": "شما اجازه‌ی انجام این کار را ندارید.",
  "CSRF Failed: CSRF token missing.": "نشست امنیتی منقضی شده است؛ صفحه را دوباره بارگذاری کنید.",
};

export function translateApiMessage(message: string, status?: number): string {
  if (status === 429) return "تعداد درخواست‌ها زیاد است؛ کمی بعد دوباره تلاش کنید.";
  return API_MESSAGES_FA[message] ?? message;
}
