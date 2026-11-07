import MyAccount from "@/components/MyAccount";
import React from "react";

import { Metadata } from "next";
export const metadata: Metadata = {
  title: "My Account | قالب فروشگاه اینترنتی",
  description: "حساب کاربری من",
  // other metadata
};

const MyAccountPage = () => {
  return (
    <main>
      <MyAccount />
    </main>
  );
};

export default MyAccountPage;
