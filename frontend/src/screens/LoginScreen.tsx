/**
 * WORKED EXAMPLE — fully implemented, read this one closely.
 *
 * WHY this screen only calls one function (`login`) from api/auth.ts and
 * contains no HTTP/axios code itself: exactly the same layering
 * principle as the backend (a route calls a service, never touches the
 * database directly) — a screen calls a typed api/*.ts function, never
 * calls `fetch`/`axios` directly. If the backend's auth flow changes,
 * only api/auth.ts needs to change, not every screen that logs a user in.
 *
 * WHY errors are caught and turned into a plain message state instead of
 * letting them propagate: a screen's job is to show *something* useful
 * when a request fails, not to crash. `err?.response?.data?.detail` is
 * where FastAPI puts the message for an HTTPException (see
 * backend/src/bds_backend/api/v1/auth.py — every `raise HTTPException(...,
 * detail=str(exc))` ends up here on the frontend).
 */

import React, { useState } from 'react';
import { ActivityIndicator, Button, Text, TextInput, View } from 'react-native';

import { login } from '../api/auth';

export default function LoginScreen({ onLoggedIn }: { onLoggedIn: () => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async () => {
    setError(null);
    setLoading(true);
    try {
      await login(email.trim(), password);
      onLoggedIn();
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Unable to log in.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ padding: 24, gap: 12 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold' }}>Log in</Text>
      <TextInput
        placeholder="Email"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
        style={{ borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 12 }}
      />
      <TextInput
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        style={{ borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 12 }}
      />
      {error && <Text style={{ color: 'red' }}>{error}</Text>}
      {loading ? <ActivityIndicator /> : <Button title="Log in" onPress={onSubmit} />}
    </View>
  );
}
