import ForgotPassword from "@/components/Auth/ForgotPassword";
import React from "react";

import { Metadata } from "next";
export const metadata: Metadata = {
  title: "فراموشی رمز عبور",
  description: "بازیابی رمز عبور با پیامک",
};

const ForgotPasswordPage = () => {
  return (
    <main>
      <ForgotPassword />
    </main>
  );
};

export default ForgotPasswordPage;
