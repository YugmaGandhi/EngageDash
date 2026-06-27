import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { CustomerForm } from "@/components/customers/CustomerForm";

describe("CustomerForm validation", () => {
  it("requires a name", async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(<CustomerForm submitting={false} submitLabel="Create" onSubmit={onSubmit} />);

    await user.click(screen.getByRole("button", { name: /create/i }));
    expect(await screen.findByText(/name is required/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("rejects an invalid email", async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(<CustomerForm submitting={false} submitLabel="Create" onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/name/i), "Acme");
    await user.type(screen.getByLabelText(/email/i), "not-an-email");
    await user.click(screen.getByRole("button", { name: /create/i }));

    expect(await screen.findByText(/valid email/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("rejects an out-of-range health score", async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(<CustomerForm submitting={false} submitLabel="Create" onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/name/i), "Acme");
    const score = screen.getByLabelText(/health score/i);
    await user.clear(score);
    await user.type(score, "150");
    await user.click(screen.getByRole("button", { name: /create/i }));

    expect(await screen.findByText(/between 0 and 100/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("submits valid values", async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(<CustomerForm submitting={false} submitLabel="Create" onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/name/i), "Acme");
    await user.click(screen.getByRole("button", { name: /create/i }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ name: "Acme", status: "prospect", health_score: 50 }),
    );
  });
});
