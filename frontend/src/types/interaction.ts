export type InteractionType = "meeting" | "call" | "email" | "note";

export interface Interaction {
  id: number;
  customer_id: number;
  created_by_id: number;
  type: InteractionType;
  title: string;
  notes: string;
  occurred_at: string;
  created_at: string;
  updated_at: string;
}

export interface InteractionListItem {
  id: number;
  customer_id: number;
  type: InteractionType;
  title: string;
  occurred_at: string;
}

export interface InteractionCreateInput {
  customer_id: number;
  type?: InteractionType;
  title: string;
  notes: string;
  occurred_at: string;
}

export interface InteractionUpdateInput {
  type?: InteractionType;
  title?: string;
  notes?: string;
  occurred_at?: string;
}

// Query params for the list endpoint.
export interface InteractionListParams {
  customer_id?: number;
  type?: InteractionType;
  date_from?: string;
  date_to?: string;
  skip?: number;
  limit?: number;
}
