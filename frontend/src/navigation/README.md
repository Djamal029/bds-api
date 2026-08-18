# Navigation — intentionally empty

The real project uses `@react-navigation/native` (a stack navigator for
auth vs. main app, a bottom tab navigator for the main app's top-level
screens, nested stacks for admin/reporter/treasurer sub-screens). Wiring
that up is a one-time setup task, not something worth re-deriving as a
stub here — install `@react-navigation/native` and
`@react-navigation/native-stack`, follow their own setup docs, and wire
in the screens from `../screens/` once you have more than one working.

Until then, `App.tsx` (not present in this skeleton — you'd create it)
can simply render `<LoginScreen onLoggedIn={...} />` directly, exactly
as the frontend `README.md` describes running things.
