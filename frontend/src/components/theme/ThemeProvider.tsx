"use client";

import { ThemeProvider as NextThemesProvider } from "next-themes";

// Thin wrapper around next-themes so the root layout stays tidy.
export function ThemeProvider({
  children,
  ...props
}: React.ComponentProps<typeof NextThemesProvider>) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
