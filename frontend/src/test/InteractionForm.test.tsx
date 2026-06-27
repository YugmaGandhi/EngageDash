import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { InteractionForm } from "@/components/interactions/InteractionForm";
import type { CustomerListItem } from "@/types";

const customers: CustomerListItem[] = [
  { id: 1, name: "Acme", company: null, status: "active", health_score: 80, assigned_csm_id: 1 },
];

describe("InteractionForm validation", () => {
  it("requires title and notes", async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    // fixedCustomerId avoids interacting with the customer dropdown.
    render(
      <InteractionForm
        customers={customers}
        fixedCustomerId={1}
        submitting={false}
        submitLabel="Save"
        onSubmit={onSubmit}
      />,
    );

    await user.click(screen.getByRole("button", { name: /save/i }));
    expect(await screen.findByText(/title and notes are required/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("submits with the fixed customer", async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(
      <InteractionForm
        customers={customers}
        fixedCustomerId={1}
        submitting={false}
        submitLabel="Save"
        onSubmit={onSubmit}
      />,
    );

    await user.type(screen.getByLabelText(/title/i), "Kickoff call");
    await user.type(screen.getByLabelText(/notes/i), "Discussed onboarding.");
    await user.click(screen.getByRole("button", { name: /save/i }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        customer_id: 1,
        title: "Kickoff call",
        notes: "Discussed onboarding.",
        type: "note",
      }),
    );
  });
});
