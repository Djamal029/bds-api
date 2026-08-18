/**
 * STUB — not implemented. Copy the pattern from api/auth.ts.
 *
 *   export interface Notification {
 *     id: string;
 *     title: string;
 *     body: string;
 *     link: string | null;
 *     is_read: boolean;
 *   }
 *
 *   export async function getNotifications(): Promise<Notification[]> {
 *     const { data } = await apiClient.get<Notification[]>('/notifications');
 *     return data;
 *   }
 *
 *   export async function getUnreadCount(): Promise<number> {
 *     const { data } = await apiClient.get<{ count: number }>('/notifications/unread-count');
 *     return data.count;
 *   }
 *
 *   export async function markNotificationRead(id: string): Promise<void> {
 *     await apiClient.post(`/notifications/${id}/read`);
 *   }
 */

export {};
