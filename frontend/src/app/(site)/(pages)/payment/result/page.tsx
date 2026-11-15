import PaymentResult from "@/components/PaymentResult";
import React, { Suspense } from "react";

import { Metadata } from "next";
export const metadata: Metadata = {
  title: "نتیجه‌ی پرداخت",
};

const PaymentResultPage = () => {
  return (
    <main>
      <Suspense fallback={null}>
        <PaymentResult />
      </Suspense>
    </main>
  );
};

export default PaymentResultPage;
