import React from "react";
import MailSuccess from "@/components/MailSuccess";

import { Metadata } from "next";
export const metadata: Metadata = {
  title: "Mail Success Page | قالب فروشگاه اینترنتی",
  description: "پیام ارسال شد",
  // other metadata
};

const MailSuccessPage = () => {
  return (
    <main>
      <MailSuccess />
    </main>
  );
};

export default MailSuccessPage;
