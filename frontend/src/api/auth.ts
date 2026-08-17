/**
 * Typed client functions for the auth domain — one function per backend
 * route, matching backend/src/bds_backend/api/v1/auth.py exactly.
 *
 * WORKED EXAMPLE — fully implemented, read this one closely.
 *
 * WHY a TypeScript `interface` mirrors each backend Pydantic schema by
 * field name: this is the contract between the two languages. If the
 * backend's `UserRead.username` is renamed, this file (and every screen
 * using it) breaks at compile time via a type error, instead of the app
 * silently reading `undefined` at runtime from a field that no longer
 * exists — catching a backend/frontend mismatch as early as possible.
 *
 * WHY every function returns just the `data`, not the full axios
 * response: a screen calling `login(...)` cares about the token pair,
 * not axios's `status`/`headers`/`config` wrapper around it — unwrapping
 * here once means every call site stays simple.
 */

import { apiClient, clearAccessToken, storeAccessToken } from './client';

export type Role = 'member' | 'administrator';

export interface User {
  id: string;
  email: string;
  username: string | null;
  role: Role;
  is_active: boolean;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export async function register(email: string, password: string): Promise<User> {
  const { data } = await apiClient.post<User>('/auth/register', { email, password });
  return data;
}

export async function login(email: string, password: string): Promise<User> {
  const { data } = await apiClient.post<TokenPair>('/auth/login', { email, password });
  await storeAccessToken(data.access_token);
  return getMe();
}

export async function logout(): Promise<void> {
  await clearAccessToken();
}

export async function getMe(): Promise<User> {
  const { data } = await apiClient.get<User>('/auth/me');
  return data;
}

export async function updateProfile(fields: {
  username?: string;
  first_name?: string;
  last_name?: string;
}): Promise<User> {
  const { data } = await apiClient.patch<User>('/auth/me', fields);
  return data;
}
