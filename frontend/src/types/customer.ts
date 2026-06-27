export type CustomerStatus = "prospect" | "active" | "at_risk" | "churned";

export interface Customer {
  id: number;
  name: string;
  company: string | null;
  email: string | null;
  phone: string | null;
  status: CustomerStatus;
  health_score: number;
  assigned_csm_id: number;
  created_by_id: number;
  created_at: string;
  updated_at: string;
}

export interface CustomerListItem {
  id: number;
  name: string;
  company: string | null;
  status: CustomerStatus;
  health_score: number;
  assigned_csm_id: number;
}

export interface CustomerCreateInput {
  name: string;
  company?: string | null;
  email?: string | null;
  phone?: string | null;
  status?: CustomerStatus;
  health_score?: number;
  assigned_csm_id?: number | null;
}

// Same fields as create, all optional (only send what changed).
export type CustomerUpdateInput = Partial<CustomerCreateInput>;

// Query params for the list endpoint.
export interface CustomerListParams {
  status?: CustomerStatus;
  search?: string;
  assigned_csm_id?: number;
  skip?: number;
  limit?: number;
}
