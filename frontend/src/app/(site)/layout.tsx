"use client";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

import { ModalProvider } from "../context/QuickViewModalContext";
import { CartModalProvider } from "../context/CartSidebarModalContext";
import { ReduxProvider } from "@/redux/provider";
import { StoreProvider } from "../context/StoreContext";
import QuickViewModal from "@/components/Common/QuickViewModal";
import CartSidebarModal from "@/components/Common/CartSidebarModal";
import { PreviewSliderProvider } from "../context/PreviewSliderContext";
import PreviewSliderModal from "@/components/Common/PreviewSlider";

import ScrollToTop from "@/components/Common/ScrollToTop";
import { Toaster } from "react-hot-toast";
import { useI18n } from "@/i18n/client";

/**
 * Storefront shell (providers + header/footer). <html>/<body> live in the root
 * layout (src/app/layout.tsx) so pages are server-rendered instead of waiting
 * for a client-side preloader.
 */
export default function SiteLayout({ children }: { children: React.ReactNode }) {
  const { isRtl } = useI18n();

  return (
    <StoreProvider>
      <ReduxProvider>
        <CartModalProvider>
          <ModalProvider>
            <PreviewSliderProvider>
              <Header />
              {children}

              <QuickViewModal />
              <CartSidebarModal />
              <PreviewSliderModal />
              <Toaster position={isRtl ? "bottom-left" : "bottom-right"} />
            </PreviewSliderProvider>
          </ModalProvider>
        </CartModalProvider>
      </ReduxProvider>
      <ScrollToTop />
      <Footer />
    </StoreProvider>
  );
}
