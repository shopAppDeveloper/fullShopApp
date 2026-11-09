import { Menu } from "@/types/Menu";

export const menuData: Menu[] = [
  {
    id: 1,
    title: "محبوب",
    newTab: false,
    path: "/",
  },
  {
    id: 2,
    title: "فروشگاه",
    newTab: false,
    path: "/shop-with-sidebar",
  },
  {
    id: 3,
    title: "تماس با ما",
    newTab: false,
    path: "/contact",
  },
  {
    id: 6,
    title: "صفحات",
    newTab: false,
    path: "/",
    submenu: [
      {
        id: 61,
        title: "فروشگاه با نوار کناری",
        newTab: false,
        path: "/shop-with-sidebar",
      },
      {
        id: 62,
        title: "فروشگاه بدون نوار کناری",
        newTab: false,
        path: "/shop-without-sidebar",
      },
      {
        id: 64,
        title: "تسویه‌حساب",
        newTab: false,
        path: "/checkout",
      },
      {
        id: 65,
        title: "سبد خرید",
        newTab: false,
        path: "/cart",
      },
      {
        id: 66,
        title: "علاقه‌مندی‌ها",
        newTab: false,
        path: "/wishlist",
      },
      {
        id: 67,
        title: "ورود",
        newTab: false,
        path: "/signin",
      },
      {
        id: 68,
        title: "ثبت‌نام",
        newTab: false,
        path: "/signup",
      },
      {
        id: 69,
        title: "حساب کاربری من",
        newTab: false,
        path: "/my-account",
      },
      {
        id: 70,
        title: "تماس با ما",
        newTab: false,
        path: "/contact",
      },
    ],
  },
  {
    id: 7,
    title: "پرفروش‌ترین‌ها",
    newTab: false,
    path: "/shop-with-sidebar",
    badge: "حراج",
  },
];
