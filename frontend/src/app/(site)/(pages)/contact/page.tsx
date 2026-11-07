import Contact from "@/components/Contact";

import { Metadata } from "next";
export const metadata: Metadata = {
  title: "Contact Page | قالب فروشگاه اینترنتی",
  description: "تماس با ما",
  // other metadata
};

const ContactPage = () => {
  return (
    <main>
      <Contact />
    </main>
  );
};

export default ContactPage;
