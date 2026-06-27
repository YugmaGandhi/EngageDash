import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Produce a minimal, self-contained server bundle at `.next/standalone`
  // for a lean production Docker image.
  output: "standalone",
};

export default nextConfig;
