import React from "react";

import Newsletter from "../Common/Newsletter";
import BestSeller from "./BestSeller";
import Categories from "./Categories";
import Countdown from "./Countdown";
import Hero from "./Hero";
import NewArrival from "./NewArrivals";
import PromoBanner from "./PromoBanner";
import Testimonials from "./Testimonials";

/**
 * Storefront home page, same section order as the NextMerce demo:
 * hero -> categories -> new arrivals -> promo banners -> best sellers ->
 * countdown -> testimonials -> newsletter.
 * Countdown and testimonials only render when real data is configured
 * (see ./homeContent.ts), so the page never shows invented content.
 */
const Home = () => {
  return (
    <main>
      <Hero />
      <Categories />
      <NewArrival />
      <PromoBanner />
      <BestSeller />
      <Countdown />
      <Testimonials />
      <Newsletter />
    </main>
  );
};

export default Home;
