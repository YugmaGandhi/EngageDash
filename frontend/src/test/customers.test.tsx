import { screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import CustomersPage from "@/app/(app)/customers/page";
import type { AuthState } from "@/store/slices/authSlice";
import type { CustomerListItem, UserRole } from "@/types";

import { renderWithProviders } from "./renderWithProviders";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
  usePathname: () => "/customers",
}));

vi.mock("@/lib/api/customers", () => ({
  listCustomers: vi.fn(),
  getCustomer: vi.fn(),
  createCustomer: vi.fn(),
  updateCustomer: vi.fn(),
  deleteCustomer: vi.fn(),
}));
import * as customersApi from "@/lib/api/customers";

const sampleCustomer: CustomerListItem = {
  id: 1,
  name: "Acme",
  company: "Acme Inc",
  status: "active",
  health_score: 80,
  assigned_csm_id: 1,
};

function authWith(role: UserRole): AuthState {
  return {
    user: { id: 1, name: "A", email: "a@x.com", role, is_active: true, created_at: "2026-01-01" },
    status: "authenticated",
    error: null,
  };
}

describe("CustomersPage RBAC", () => {
  it("shows the delete action for admins", async () => {
    vi.mocked(customersApi.listCustomers).mockResolvedValue([sampleCustomer]);
    renderWithProviders(<CustomersPage />, { auth: authWith("admin") });

    expect(await screen.findByText("Acme")).toBeInTheDocument();
    expect(screen.getByLabelText("Delete customer")).toBeInTheDocument();
  });

  it("hides the delete action for CSMs", async () => {
    vi.mocked(customersApi.listCustomers).mockResolvedValue([sampleCustomer]);
    renderWithProviders(<CustomersPage />, { auth: authWith("csm") });

    expect(await screen.findByText("Acme")).toBeInTheDocument();
    expect(screen.queryByLabelText("Delete customer")).not.toBeInTheDocument();
  });
});
