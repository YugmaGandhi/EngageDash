import { AppShell } from "@/components/layout/AppShell";

// Wraps all the main app pages (dashboard, customers, interactions) with the
// sidebar + topbar shell. Route protection is added in the next stage.
export default function AppLayout({ children }: { children: React.ReactNode }) {
  return <AppShell>{children}</AppShell>;
}
