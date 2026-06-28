import { NavLinks } from "./NavLinks";

// Desktop sidebar. Hidden on small screens, where MobileNav takes over.
export function Sidebar() {
  return (
    <aside className="bg-sidebar hidden w-60 shrink-0 border-r md:block">
      <div className="flex h-14 items-center px-6 text-lg font-bold">EngageDash</div>
      <NavLinks />
    </aside>
  );
}
