import { testimonials } from "../homeContent";

/** Renders only real reviews configured in homeContent.ts - hidden while there are none. */
const Testimonials = () => {
  if (testimonials.length === 0) return null;
  return (
    <section className="overflow-hidden py-20">
      <div className="mx-auto w-full max-w-[1170px] px-4 sm:px-8 xl:px-0">
        <div className="mb-10">
          <span className="mb-1.5 block font-medium text-dark">نظرات مشتریان</span>
          <h2 className="text-xl font-semibold text-dark xl:text-heading-5">مشتریان درباره‌ی ما چه می‌گویند</h2>
        </div>
        <div className="grid gap-7.5 sm:grid-cols-2 lg:grid-cols-3">
          {testimonials.map((item) => (
            <figure key={item.name} className="rounded-xl bg-white p-7.5 shadow-1">
              <blockquote className="mb-5 text-dark">{item.review}</blockquote>
              <figcaption>
                <span className="block font-medium text-dark">{item.name}</span>
                {item.role && <span className="text-custom-sm text-dark-4">{item.role}</span>}
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
