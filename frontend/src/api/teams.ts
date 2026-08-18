/**
 * STUB — not implemented. Copy the pattern from api/auth.ts.
 *
 *   export interface Sport {
 *     id: string;
 *     name: string;
 *   }
 *
 *   export interface Team {
 *     id: string;
 *     name: string;
 *     sport: string;       // matches backend schemas/teams.py's TeamRead —
 *                           // the sport's NAME, already joined server-side
 *     season: string;
 *   }
 *
 *   export async function getSports(): Promise<Sport[]> {
 *     const { data } = await apiClient.get<Sport[]>('/sports');
 *     return data;
 *   }
 *
 *   export async function getTeams(sportId?: string): Promise<Team[]> {
 *     const { data } = await apiClient.get<Team[]>('/teams', {
 *       params: { sport_id: sportId },
 *     });
 *     return data;
 *   }
 *
 * Every field name here must match the backend's Pydantic schema
 * exactly (see backend/.../schemas/teams.py's stub) — this file IS the
 * frontend's copy of that contract, kept in sync by hand.
 */

export {};
