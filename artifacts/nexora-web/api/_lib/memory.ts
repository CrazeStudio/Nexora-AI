/**
 * memory.ts — NexoraAI session + persistent memory for the web server.
 *
 * Session memory is stored in a Map keyed by sessionId (in-process, cleared
 * on restart).  Persistent facts are stored per-session in the same Map so
 * each browser tab gets its own private memory space.
 */

import { randomUUID } from "crypto";

export interface Turn {
  role: "user" | "assistant";
  text: string;
  time: string;
}

export interface SessionData {
  history: Turn[];
  facts: string[];
}

const MAX_HISTORY = 50;
const sessions = new Map<string, SessionData>();

function getOrCreate(sessionId: string): SessionData {
  if (!sessions.has(sessionId)) {
    sessions.set(sessionId, { history: [], facts: [] });
  }
  return sessions.get(sessionId)!;
}

export function newSession(): string {
  const id = randomUUID();
  sessions.set(id, { history: [], facts: [] });
  return id;
}

export function addTurn(sessionId: string, role: "user" | "assistant", text: string): void {
  const session = getOrCreate(sessionId);
  session.history.push({ role, text, time: new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }) });
  if (session.history.length > MAX_HISTORY) {
    session.history.splice(0, session.history.length - MAX_HISTORY);
  }
}

export function rememberFact(sessionId: string, fact: string): string {
  const trimmed = fact.trim();
  if (!trimmed) return "There is nothing to remember — please provide some text.";
  const session = getOrCreate(sessionId);
  session.facts.push(trimmed);
  return `Got it! I've remembered: "${trimmed}"`;
}

export function recallFacts(sessionId: string, query?: string): string[] {
  const session = getOrCreate(sessionId);
  if (!query) return session.facts;
  const q = query.toLowerCase();
  return session.facts.filter(f => f.toLowerCase().includes(q));
}

export function clearMemory(sessionId: string): void {
  sessions.set(sessionId, { history: [], facts: [] });
}

export function getHistory(sessionId: string): Turn[] {
  return getOrCreate(sessionId).history;
}
