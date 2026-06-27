import { api } from "@/lib/axios";
import type {
  Customer,
  CustomerCreateInput,
  CustomerListItem,
  CustomerListParams,
  CustomerUpdateInput,
} from "@/types";

export async function listCustomers(params?: CustomerListParams): Promise<CustomerListItem[]> {
  const { data } = await api.get<CustomerListItem[]>("/customers", { params });
  return data;
}

export async function getCustomer(id: number): Promise<Customer> {
  const { data } = await api.get<Customer>(`/customers/${id}`);
  return data;
}

export async function createCustomer(input: CustomerCreateInput): Promise<Customer> {
  const { data } = await api.post<Customer>("/customers", input);
  return data;
}

export async function updateCustomer(id: number, input: CustomerUpdateInput): Promise<Customer> {
  const { data } = await api.patch<Customer>(`/customers/${id}`, input);
  return data;
}

export async function deleteCustomer(id: number): Promise<void> {
  await api.delete(`/customers/${id}`);
}
