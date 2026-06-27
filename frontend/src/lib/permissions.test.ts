import { describe, expect, it } from "vitest";

import { canDeleteCustomers, canManageAll, hasRole, isAdmin } from "@/lib/permissions";

describe("permissions", () => {
  it("hasRole matches only allowed roles", () => {
    expect(hasRole("admin", ["admin"])).toBe(true);
    expect(hasRole("csm", ["admin", "manager"])).toBe(false);
    expect(hasRole(undefined, ["admin"])).toBe(false);
  });

  it("isAdmin", () => {
    expect(isAdmin("admin")).toBe(true);
    expect(isAdmin("manager")).toBe(false);
  });

  it("canManageAll covers admin and manager", () => {
    expect(canManageAll("admin")).toBe(true);
    expect(canManageAll("manager")).toBe(true);
    expect(canManageAll("csm")).toBe(false);
  });

  it("canDeleteCustomers only for admin/manager", () => {
    expect(canDeleteCustomers("admin")).toBe(true);
    expect(canDeleteCustomers("csm")).toBe(false);
  });
});
