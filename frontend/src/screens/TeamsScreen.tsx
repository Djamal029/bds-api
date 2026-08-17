/**
 * STUB — not implemented. Copy the pattern from screens/LoginScreen.tsx.
 *
 * You'll want at minimum:
 *
 *   export default function TeamsScreen() {
 *     const [teams, setTeams] = useState<Team[] | null>(null);
 *
 *     useEffect(() => {
 *       getTeams().then(setTeams);   // from a new api/teams.ts you write,
 *                                     // matching api/auth.ts's pattern
 *     }, []);
 *
 *     if (teams === null) return <ActivityIndicator />;
 *     return (
 *       <FlatList
 *         data={teams}
 *         keyExtractor={(t) => t.id}
 *         renderItem={({ item }) => <Text>{item.name}</Text>}
 *       />
 *     );
 *   }
 *
 * Before this compiles you also need:
 *   1. `frontend/src/api/teams.ts` — a `Team` interface matching the
 *      backend's `TeamRead` schema (see backend/.../schemas/teams.py,
 *      also a stub) field for field, and a `getTeams()` function
 *      following api/auth.ts's exact shape.
 *   2. The backend route it calls (backend/.../api/v1/teams.py) actually
 *      implemented — this screen has nothing to call until that exists.
 */

export {};
