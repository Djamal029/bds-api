/**
 * STUB — not implemented. Copy the pattern from api/auth.ts.
 *
 *   export interface Fixture {
 *     id: string;
 *     sport: string;
 *     home_team: string;
 *     away_team: string;
 *     date_time: string;    // ISO string over the wire — parse with
 *                            // `new Date(...)` only where you need to
 *                            // actually manipulate it, keep it a string
 *                            // in the type otherwise
 *     status: 'scheduled' | 'in_progress' | 'finished' | 'cancelled' | 'postponed';
 *     home_score: number | null;
 *     away_score: number | null;
 *   }
 *
 *   export async function getUpcomingFixtures(): Promise<Fixture[]> {
 *     const { data } = await apiClient.get<Fixture[]>('/fixtures/upcoming');
 *     return data;
 *   }
 *
 * The `status` union type is typed out by hand here to match
 * backend/.../models/enums.py's (stub) `FixtureStatusEnum` values
 * exactly, string for string — TypeScript has no way to import a Python
 * enum, so keeping these two lists in sync is a manual contract, the
 * same as every other field name in this file.
 */

export {};
