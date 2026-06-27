/**
 * Small helper for reading/writing the JWT tokens in localStorage.
 *
 * Kept separate so both the Axios interceptors and the Redux auth slice use the
 * same keys. All functions are safe to call during server-side rendering
 * (they no-op when there is no `window`).
 */

const ACCESS_TOKEN_KEY = "engagedash_access_token";
const REFRESH_TOKEN_KEY = "engagedash_refresh_token";

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setTokens(accessToken: string, refreshToken: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
}

export function clearTokens(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}
