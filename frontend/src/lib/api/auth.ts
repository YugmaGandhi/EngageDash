import { api } from "@/lib/axios";
import type { AuthTokens, LoginInput, RegisterInput, User } from "@/types";

export async function register(input: RegisterInput): Promise<User> {
  const { data } = await api.post<User>("/auth/register", input);
  return data;
}

export async function login(input: LoginInput): Promise<AuthTokens> {
  const { data } = await api.post<AuthTokens>("/auth/login", input);
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await api.get<User>("/auth/me");
  return data;
}

export async function updateMe(input: { name: string }): Promise<User> {
  const { data } = await api.patch<User>("/auth/me", input);
  return data;
}
