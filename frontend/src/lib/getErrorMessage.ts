import axios from "axios";

/**
 * Pull a human-friendly message out of an error.
 * Our backend returns errors as { error: { code, message, details } }, so we
 * read that message when it's available; otherwise we use a fallback.
 */
export function getErrorMessage(error: unknown, fallback = "Something went wrong."): string {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.error?.message;
    if (typeof message === "string") return message;
  }
  return fallback;
}
