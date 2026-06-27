// Adds the jest-dom matchers (e.g. toBeInTheDocument) to Vitest's expect.
import "@testing-library/jest-dom/vitest";

import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// Unmount and clear the DOM after each test so tests don't leak into each other.
afterEach(() => {
  cleanup();
});
