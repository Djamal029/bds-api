/**
 * STUB — not implemented. Copy the pattern from api/auth.ts.
 *
 *   export interface Activity {
 *     id: string;
 *     name: string;
 *     date_time: string;
 *     location: string | null;
 *     spots_remaining: number | null;
 *     is_registered: boolean;
 *   }
 *
 *   export async function getUpcomingActivities(): Promise<Activity[]> {
 *     const { data } = await apiClient.get<Activity[]>('/activities');
 *     return data;
 *   }
 *
 *   export async function registerForActivity(activityId: string): Promise<void> {
 *     await apiClient.post(`/activities/${activityId}/registration`);
 *   }
 *
 * A 204 No Content response (see backend/.../api/v1/activities.py's stub
 * for `register`) means `registerForActivity` above has nothing useful
 * in `data` — don't destructure it, just await the call and treat a
 * thrown error (axios throws on a non-2xx status by default) as the
 * failure signal.
 */

export {};
