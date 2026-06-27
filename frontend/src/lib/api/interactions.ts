import { api } from "@/lib/axios";
import type {
  Interaction,
  InteractionCreateInput,
  InteractionListItem,
  InteractionListParams,
  InteractionUpdateInput,
} from "@/types";

export async function listInteractions(
  params?: InteractionListParams,
): Promise<InteractionListItem[]> {
  const { data } = await api.get<InteractionListItem[]>("/interactions", { params });
  return data;
}

export async function getInteraction(id: number): Promise<Interaction> {
  const { data } = await api.get<Interaction>(`/interactions/${id}`);
  return data;
}

export async function createInteraction(input: InteractionCreateInput): Promise<Interaction> {
  const { data } = await api.post<Interaction>("/interactions", input);
  return data;
}

export async function updateInteraction(
  id: number,
  input: InteractionUpdateInput,
): Promise<Interaction> {
  const { data } = await api.patch<Interaction>(`/interactions/${id}`, input);
  return data;
}
