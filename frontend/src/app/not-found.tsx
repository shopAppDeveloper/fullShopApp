import Error from "@/components/Error";

import SiteLayout from "./(site)/layout";

const notFound = () => {
  return (
    <SiteLayout>
      <Error />
    </SiteLayout>
  );
};

export default notFound;
