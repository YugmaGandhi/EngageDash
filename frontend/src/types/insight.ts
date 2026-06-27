export type Sentiment = "positive" | "neutral" | "negative";
export type InsightStatus = "success" | "fallback";

export interface Insight {
  id: number;
  interaction_id: number;
  summary: string;
  sentiment: Sentiment;
  action_items: string[];
  risks: string[];
  status: InsightStatus;
  model: string | null;
  created_at: string;
}
