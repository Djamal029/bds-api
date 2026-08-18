/**
 * STUB — not implemented. Copy the pattern from api/auth.ts.
 *
 *   export interface Player {
 *     id: string;
 *     first_name: string;
 *     last_name: string;
 *     team: string | null;
 *   }
 *
 *   export async function becomePlayer(code: string): Promise<Player> {
 *     const { data } = await apiClient.post<Player>('/players/become-player', { code });
 *     return data;
 *   }
 *
 *   export async function getMyPlayerStats(): Promise<Player | null> {
 *     try {
 *       const { data } = await apiClient.get<Player>('/players/me');
 *       return data;
 *     } catch (err: any) {
 *       if (err?.response?.status === 404) return null;   // not a player
 *                                                            yet — not an
 *                                                            error state
 *       throw err;
 *     }
 *   }
 *
 * `getMyPlayerStats` treats a 404 as a legitimate, expected outcome
 * (most accounts aren't linked to a player) rather than an error to
 * surface — check the specific status code before deciding that, since
 * a 401/500 on the same call means something actually went wrong and
 * should still propagate.
 */

export {};
