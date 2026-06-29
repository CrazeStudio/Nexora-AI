import { useState } from "react";

const SESSION_KEY = "nexora_session_id";

export function useSession() {
  const [sessionId, setSessionId] = useState<string | null>(() => {
    return localStorage.getItem(SESSION_KEY);
  });

  const ensureSession = () => {
    if (!sessionId) {
      const newId = crypto.randomUUID();
      localStorage.setItem(SESSION_KEY, newId);
      setSessionId(newId);
      return newId;
    }
    return sessionId;
  };

  const saveSession = (id: string) => {
    localStorage.setItem(SESSION_KEY, id);
    setSessionId(id);
  };

  return { sessionId, ensureSession, saveSession };
}
