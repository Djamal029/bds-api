/**
 * STUB — not implemented. Copy the pattern from api/auth.ts.
 *
 *   export interface Payment {
 *     type: 'jersey' | 'license';
 *     status: 'pending' | 'validated' | 'rejected';
 *   }
 *
 *   export async function getMyPayments(): Promise<Payment[]> {
 *     const { data } = await apiClient.get<Payment[]>('/payments/me');
 *     return data;
 *   }
 *
 *   export async function requestPayment(types: Payment['type'][]): Promise<string> {
 *     const { data } = await apiClient.post<{ otp: string }>('/payments/request', { types });
 *     return data.otp;
 *   }
 *
 * `Payment['type'][]` above is TypeScript's indexed-access type syntax:
 * "the type of `Payment`'s `type` field, as an array" — reuses the
 * union already defined on the interface instead of retyping
 * `('jersey' | 'license')[]` a second time, so the two can't drift apart.
 */

export {};
