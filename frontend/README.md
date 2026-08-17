# Frontend skeleton

See the root `README.md` and `CONTRIBUTING.md` for the full picture.
Quick orientation for this folder specifically:

```
src/
  api/         one typed client module per backend domain
    client.ts    the shared axios instance + auth token attachment (FULL example)
    auth.ts      typed functions for /auth/* routes (FULL example)
  screens/     one file per screen
    LoginScreen.tsx   FULL example — the one working screen
    TeamsScreen.tsx   STUB — copy LoginScreen's pattern once teams exist
  navigation/  empty — a real app needs a navigator (react-navigation is
               what the real BDS project uses) wiring LoginScreen and
               whatever screens you add together; out of scope for this
               skeleton, which only demonstrates one screen at a time
```

## Running

```bash
npm install
npm run typecheck   # tsc --noEmit — the two example files must stay clean
npm start           # expo start, once you've wired up a navigator
```

`api/client.ts` points at `http://localhost:8000` by default, matching
the backend's default `uvicorn` port — update it if you run the backend
elsewhere.
