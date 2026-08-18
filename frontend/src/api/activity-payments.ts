/**
 * STUB — not implemented. Copy the pattern from api/auth.ts.
 *
 *   export interface ActivityPaymentDue {
 *     id: string;
 *     activity_name: string;
 *     status: 'pending' | 'validated' | 'rejected';
 *   }
 *
 *   export async function getActivityPaymentDues(): Promise<ActivityPaymentDue[]> {
 *     const { data } = await apiClient.get<ActivityPaymentDue[]>('/activity-payments');
 *     return data;
 *   }
 *
 *   export async function validateActivityPaymentDue(dueId: string): Promise<void> {
 *     await apiClient.post(`/activity-payments/${dueId}/validate`);
 *   }
 *
 * File named with a hyphen (`activity-payments.ts`), matching the
 * backend route's URL segment (`/activity-payments`) rather than the
 * usual one-word-per-domain naming — the frontend api/ folder generally
 * favors matching the URL over strict naming uniformity, since that's
 * what makes "which file handles this endpoint" easiest to guess.
 */

export {};
