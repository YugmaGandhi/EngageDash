import { screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import DashboardPage from "@/app/(app)/dashboard/page";
import type { DashboardData } from "@/types";

import { renderWithProviders } from "./renderWithProviders";

vi.mock("@/lib/api/dashboard", () => ({ getDashboard: vi.fn() }));
import * as dashboardApi from "@/lib/api/dashboard";

const data: DashboardData = {
  total_customers: 3,
  customers_by_status: { prospect: 1, active: 1, at_risk: 1, churned: 0 },
  at_risk_customers: 1,
  total_interactions: 2,
  interactions_last_7_days: 1,
  sentiment_breakdown: { positive: 1, neutral: 0, negative: 1 },
  recent_interactions: [
    {
      id: 1,
      customer_id: 1,
      type: "meeting",
      title: "QBR call",
      occurred_at: "2026-01-01T10:00:00Z",
    },
  ],
};

const emptyData: DashboardData = {
  total_customers: 0,
  customers_by_status: { prospect: 0, active: 0, at_risk: 0, churned: 0 },
  at_risk_customers: 0,
  total_interactions: 0,
  interactions_last_7_days: 0,
  sentiment_breakdown: { positive: 0, neutral: 0, negative: 0 },
  recent_interactions: [],
};

describe("DashboardPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders KPIs and recent activity with data", async () => {
    vi.mocked(dashboardApi.getDashboard).mockResolvedValue(data);
    renderWithProviders(<DashboardPage />);

    // Recent interaction appears once data loads.
    expect(await screen.findByText("QBR call")).toBeInTheDocument();
    // Section titles (unique) render.
    expect(screen.getByText("Customers by status")).toBeInTheDocument();
    expect(screen.getByText("Sentiment breakdown")).toBeInTheDocument();
    // A KPI label renders.
    expect(screen.getByText("Customers")).toBeInTheDocument();
    // A sentiment breakdown row label renders.
    expect(screen.getByText("Positive")).toBeInTheDocument();
  });

  it("renders an empty state without data", async () => {
    vi.mocked(dashboardApi.getDashboard).mockResolvedValue(emptyData);
    renderWithProviders(<DashboardPage />);

    expect(await screen.findByText(/no recent interactions/i)).toBeInTheDocument();
  });
});
