import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import LoginPage from "@/app/(auth)/login/page";
import type { User } from "@/types";

import { renderWithProviders } from "./renderWithProviders";

// Mock the router so the redirect-on-success can be asserted.
const replace = vi.fn();
vi.mock("next/navigation", () => ({ useRouter: () => ({ replace }) }));

// Mock the auth API module so no real network calls happen.
vi.mock("@/lib/api/auth", () => ({
  login: vi.fn(),
  getMe: vi.fn(),
  register: vi.fn(),
  updateMe: vi.fn(),
}));
import * as authApi from "@/lib/api/auth";

const fakeUser: User = {
  id: 1,
  name: "Asha",
  email: "asha@example.com",
  role: "csm",
  is_active: true,
  created_at: "2026-01-01",
};

describe("LoginPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows a validation error when fields are empty", async () => {
    const user = userEvent.setup();
    renderWithProviders(<LoginPage />);
    await user.click(screen.getByRole("button", { name: /sign in/i }));
    expect(await screen.findByText(/enter your email and password/i)).toBeInTheDocument();
    expect(authApi.login).not.toHaveBeenCalled();
  });

  it("shows an error message when login fails", async () => {
    vi.mocked(authApi.login).mockRejectedValue(new Error("bad creds"));
    const user = userEvent.setup();
    renderWithProviders(<LoginPage />);
    await user.type(screen.getByLabelText(/email/i), "asha@example.com");
    await user.type(screen.getByLabelText(/password/i), "supersecret123");
    await user.click(screen.getByRole("button", { name: /sign in/i }));
    expect(await screen.findByText(/invalid email or password/i)).toBeInTheDocument();
  });

  it("logs in and redirects to the dashboard on success", async () => {
    vi.mocked(authApi.login).mockResolvedValue({
      access_token: "a",
      refresh_token: "r",
      token_type: "bearer",
    });
    vi.mocked(authApi.getMe).mockResolvedValue(fakeUser);
    const user = userEvent.setup();
    renderWithProviders(<LoginPage />);
    await user.type(screen.getByLabelText(/email/i), "asha@example.com");
    await user.type(screen.getByLabelText(/password/i), "supersecret123");
    await user.click(screen.getByRole("button", { name: /sign in/i }));
    await vi.waitFor(() => expect(replace).toHaveBeenCalledWith("/dashboard"));
  });
});
