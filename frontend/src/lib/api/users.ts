import { api } from "@/lib/axios";
import type { User, UserRole } from "@/types";

// Admin-only endpoints.
export async function listUsers(): Promise<User[]> {
  const { data } = await api.get<User[]>("/users");
  return data;
}

export async function updateUser(
  id: number,
  input: { role?: UserRole; is_active?: boolean },
): Promise<User> {
  const { data } = await api.patch<User>(`/users/${id}`, input);
  return data;
}
