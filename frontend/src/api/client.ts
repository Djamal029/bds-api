/**
 * The shared HTTP client every api/*.ts module uses.
 *
 * WORKED EXAMPLE — fully implemented, read this one closely.
 *
 * WHY one shared axios instance instead of each api/*.ts file creating
 * its own: the auth token attachment (the request interceptor below)
 * and the base URL only need to be configured once. Every other
 * api/*.ts module imports THIS `apiClient`, never creates its own —
 * see api/auth.ts for the pattern.
 *
 * WHY a request interceptor to attach the token, instead of passing
 * `Authorization: Bearer ...` explicitly on every call: it means a
 * typed function like `getTeams()` (once you write api/teams.ts) never
 * needs to know anything about auth at all — it just calls
 * `apiClient.get(...)`, and the token is attached transparently, read
 * fresh from storage on every single request (so a freshly refreshed
 * token is picked up immediately, not just at app startup).
 */

import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const ACCESS_TOKEN_KEY = 'access_token';

// Swap this for a real deployed URL, or a LAN IP for testing on a
// physical device (a browser/emulator on the same machine as the
// backend can reach `localhost`, a physical phone cannot).
const API_URL = 'http://localhost:8000/api/v1';

export const apiClient = axios.create({ baseURL: API_URL });

apiClient.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function storeAccessToken(token: string): Promise<void> {
  await SecureStore.setItemAsync(ACCESS_TOKEN_KEY, token);
}

export async function clearAccessToken(): Promise<void> {
  await SecureStore.deleteItemAsync(ACCESS_TOKEN_KEY);
}
