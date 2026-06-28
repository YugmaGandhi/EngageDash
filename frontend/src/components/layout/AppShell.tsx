import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

// The overall app frame: sidebar on the left, topbar across the top, content below.
export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      {/* min-w-0 lets this column shrink below its content width so wide tables
          scroll inside their own container instead of pushing the whole page. */}
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar />
        <main className="flex-1 p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
