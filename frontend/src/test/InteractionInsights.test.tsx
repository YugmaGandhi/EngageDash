import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { InteractionInsights } from "@/components/insights/InteractionInsights";
import type { Insight } from "@/types";

import { renderWithProviders } from "./renderWithProviders";

vi.mock("@/lib/api/insights", () => ({
  listInsights: vi.fn(),
  generateInsight: vi.fn(),
}));
import * as insightsApi from "@/lib/api/insights";

const successInsight: Insight = {
  id: 1,
  interaction_id: 1,
  summary: "Customer is happy",
  sentiment: "positive",
  action_items: ["follow up on pricing"],
  risks: ["budget concern"],
  status: "success",
  model: "fake-model",
  created_at: "2026-01-01T00:00:00Z",
};

describe("InteractionInsights", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows a generate button when there are no insights", async () => {
    vi.mocked(insightsApi.listInsights).mockResolvedValue([]);
    renderWithProviders(<InteractionInsights interactionId={1} interactionTitle="Quarterly review" />);

    expect(await screen.findByText(/no insights yet/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /generate insight/i })).toBeInTheDocument();
  });

  it("renders a generated insight", async () => {
    vi.mocked(insightsApi.listInsights).mockResolvedValue([]);
    vi.mocked(insightsApi.generateInsight).mockResolvedValue(successInsight);
    const user = userEvent.setup();
    renderWithProviders(<InteractionInsights interactionId={1} interactionTitle="Quarterly review" />);

    await screen.findByText(/no insights yet/i);
    await user.click(screen.getByRole("button", { name: /generate insight/i }));

    expect(await screen.findByText("Customer is happy")).toBeInTheDocument();
    expect(screen.getByText("follow up on pricing")).toBeInTheDocument();
    expect(screen.getByText("budget concern")).toBeInTheDocument();
    expect(screen.getByText("positive")).toBeInTheDocument();
  });

  it("shows a fallback notice for fallback insights", async () => {
    const fallback: Insight = {
      ...successInsight,
      status: "fallback",
      sentiment: "neutral",
      summary: "AI insight could not be generated automatically.",
      action_items: [],
      risks: [],
    };
    vi.mocked(insightsApi.listInsights).mockResolvedValue([fallback]);
    renderWithProviders(<InteractionInsights interactionId={1} interactionTitle="Quarterly review" />);

    expect(await screen.findByText(/AI generation was unavailable/i)).toBeInTheDocument();
  });
});
