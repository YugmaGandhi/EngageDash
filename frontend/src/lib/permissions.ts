/**
 * Small helpers for role-based UI (hiding/disabling actions by role).
 * These mirror the backend's RBAC rules so the UI matches what the API allows.
 */

import type { UserRole } from "@/types";

export function hasRole(role: UserRole | undefined, allowed: UserRole[]): boolean {
  return role !== undefined && allowed.includes(role);
}

export function isAdmin(role: UserRole | undefined): boolean {
  return role === "admin";
}

// Admins and managers can see/manage everything; CSMs are limited to their own.
export function canManageAll(role: UserRole | undefined): boolean {
  return role === "admin" || role === "manager";
}

// Only admins and managers may delete customers (matches the backend).
export function canDeleteCustomers(role: UserRole | undefined): boolean {
  return canManageAll(role);
}
