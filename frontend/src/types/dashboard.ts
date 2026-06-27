import type { InteractionType } from "./interaction";

export interface CustomersByStatus {
  prospect: number;
  active: number;
  at_risk: number;
  churned: number;
}

export interface SentimentBreakdown {
  positive: number;
  neutral: number;
  negative: number;
}

export interface RecentInteraction {
  id: number;
  customer_id: number;
  type: InteractionType;
  title: string;
  occurred_at: string;
}

export interface DashboardData {
  total_customers: number;
  customers_by_status: CustomersByStatus;
  at_risk_customers: number;
  total_interactions: number;
  interactions_last_7_days: number;
  sentiment_breakdown: SentimentBreakdown;
  recent_interactions: RecentInteraction[];
}
