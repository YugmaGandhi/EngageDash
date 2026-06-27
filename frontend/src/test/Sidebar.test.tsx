import { screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { Sidebar } from "@/components/layout/Sidebar";
import type { AuthState } from "@/store/slices/authSlice";
import type { UserRole } from "@/types";

import { renderWithProviders } from "./renderWithProviders";

// Sidebar uses usePathname for the active link; mock it.
vi.mock("next/navigation", () => ({ usePathname: () => "/dashboard" }));

function authWith(role: UserRole): AuthState {
  return {
    user: { id: 1, name: "A", email: "a@x.com", role, is_active: true, created_at: "2026-01-01" },
    status: "authenticated",
    error: null,
  };
}

describe("Sidebar role-gating", () => {
  it("shows the Users link for admins", () => {
    renderWithProviders(<Sidebar />, { auth: authWith("admin") });
    expect(screen.getByText("Users")).toBeInTheDocument();
  });

  it("hides the Users link for CSMs", () => {
    renderWithProviders(<Sidebar />, { auth: authWith("csm") });
    expect(screen.queryByText("Users")).not.toBeInTheDocument();
  });
});
