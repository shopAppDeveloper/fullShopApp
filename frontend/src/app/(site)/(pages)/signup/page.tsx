import Signup from "@/components/Auth/Signup";
import React from "react";

import { Metadata } from "next";
export const metadata: Metadata = {
  title: "Signup Page | قالب فروشگاه اینترنتی",
  description: "ثبت‌نام در فروشگاه",
  // other metadata
};

const SignupPage = () => {
  return (
    <main>
      <Signup />
    </main>
  );
};

export default SignupPage;
