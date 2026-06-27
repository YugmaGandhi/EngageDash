import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

// The overall app frame: sidebar on the left, topbar across the top, content below.
export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex flex-1 flex-col">
        <Topbar />
        <main className="flex-1 p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
