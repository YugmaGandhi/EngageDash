/**
 * Configured Axios instance used for all backend calls.
 *
 * - Request interceptor: attaches the access token to every request.
 * - Response interceptor: on a 401, tries the refresh token once to get a new
 *   access token and retries the request; if that fails, it logs the user out.
 */

import axios from "axios";

import { clearTokens, getAccessToken, getRefreshToken, setTokens } from "./tokenStorage";

const baseURL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const api = axios.create({ baseURL });

// Attach the access token to outgoing requests.
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

function redirectToLogin() {
  if (typeof window !== "undefined") {
    window.location.href = "/login";
  }
}

// Handle expired access tokens by refreshing once, then retrying.
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    const isUnauthorized = error.response?.status === 401;
    if (!isUnauthorized || originalRequest._retry) {
      return Promise.reject(error);
    }

    originalRequest._retry = true; // only try to refresh once per request
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      clearTokens();
      redirectToLogin();
      return Promise.reject(error);
    }

    try {
      // Use a plain axios call (not `api`) so we don't loop through this interceptor.
      const { data } = await axios.post(`${baseURL}/auth/refresh`, {
        refresh_token: refreshToken,
      });
      setTokens(data.access_token, data.refresh_token);
      originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
      return api(originalRequest);
    } catch (refreshError) {
      clearTokens();
      redirectToLogin();
      return Promise.reject(refreshError);
    }
  },
);
