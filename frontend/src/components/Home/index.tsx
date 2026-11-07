import React from "react";
import Hero from "./Hero";
import Categories from "./Categories";
import NewArrival from "./NewArrivals";
import PromoBanner from "./PromoBanner";
import BestSeller from "./BestSeller";
import Countdown from "./Countdown";

/**
 * Storefront homepage follows the NextMerce demo section rhythm while
 * keeping all catalogue and price information connected to Django Oscar.
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
    </main>
  );
};

export default Home;
