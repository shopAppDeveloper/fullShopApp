import React from "react";
import Error from "@/components/Error";

import { Metadata } from "next";
export const metadata: Metadata = {
  title: "Error Page | قالب فروشگاه اینترنتی",
  description: "خطا",
  // other metadata
};

const ErrorPage = () => {
  return (
    <main>
      <Error />
    </main>
  );
};

export default ErrorPage;
