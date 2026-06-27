import { api } from "@/lib/axios";
import type { Insight } from "@/types";

export async function generateInsight(interactionId: number): Promise<Insight> {
  const { data } = await api.post<Insight>(`/interactions/${interactionId}/insights`);
  return data;
}

export async function listInsights(interactionId: number): Promise<Insight[]> {
  const { data } = await api.get<Insight[]>(`/interactions/${interactionId}/insights`);
  return data;
}
