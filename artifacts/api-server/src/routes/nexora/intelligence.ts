/**
 * intelligence.ts — NexoraAI core routing engine.
 *
 * Routes each user message through the layered intelligence pipeline and
 * returns a structured response including the answer and its source.
 */

import {
  searchKnowledge,
  matchExample,
  lookupCapital,
  lookupElement,
  lookupConversion,
  evaluateMath,
} from "./knowledge.js";
import { duckDuckGoSearch, type SearchResult } from "./search.js";
import * as memory from "./memory.js";

export type Source =
  | "greeting"
  | "identity"
  | "social"
  | "command"
  | "math"
  | "dataset"
  | "example"
  | "knowledge"
  | "search"
  | "fallback";

export interface AIResponse {
  reply: string;
  source: Source;
  searchResults?: SearchResult[];
}

// ── Trigger sets ──────────────────────────────────────────────────────────────

const GREETING_TRIGGERS = new Set([
  "hi","hello","hey","howdy","greetings","good morning","good afternoon","good evening","sup","yo",
]);
const HOW_ARE_YOU_TRIGGERS = new Set([
  "how are you","how do you do","how's it going","you ok","are you ok","how are things",
]);
const IDENTITY_TRIGGERS = new Set([
  "who are you","what are you","tell me about yourself","what can you do",
  "your name","introduce yourself","what is nexora","about nexorai","what is nexorai",
]);
const COMPLIMENT_TRIGGERS = new Set([
  "thanks","thank you","great","awesome","amazing","well done","nice","excellent","brilliant","perfect","helpful",
]);
const FAREWELL_TRIGGERS = new Set([
  "bye","goodbye","farewell","see you","take care","cya","later",
]);

const GREETING_REPLIES = [
  "Hello! I'm NexoraAI, your intelligent assistant. How can I help you today?",
  "Hey there! NexoraAI here — ready to assist. What's on your mind?",
  "Hi! Great to see you. I'm NexoraAI. Ask me anything!",
  "Greetings! I'm NexoraAI. What would you like to explore today?",
];
const HOW_ARE_YOU_REPLIES = [
  "I'm doing great, thanks for asking! As an AI I don't experience feelings the way humans do, but I'm fully charged and ready to help. How about you?",
  "All systems running smoothly! I'm NexoraAI and I'm here to assist you. What's on your mind?",
  "Functioning perfectly and eager to help! What can I do for you today?",
];
const COMPLIMENT_REPLIES = [
  "You're very welcome! Happy to help.",
  "Glad I could assist! Let me know if you have more questions.",
  "Thank you for the kind words! I'm here if you need anything else.",
  "Always a pleasure! What else can I help you with?",
];
const FAREWELL_REPLIES = [
  "Goodbye! It was a pleasure chatting with you. Come back anytime!",
  "Take care! NexoraAI is always here when you need me.",
  "Farewell! I hope I was helpful. Have a wonderful day!",
];

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

// ── Trigger matching ──────────────────────────────────────────────────────────

function triggerMatch(text: string, triggers: Set<string>): boolean {
  const words = new Set(text.split(/\s+/));
  for (const trigger of triggers) {
    if (trigger.includes(" ")) {
      if (text.includes(trigger)) return true;
    } else {
      if (words.has(trigger)) return true;
    }
  }
  return false;
}

// ── Search intent detection ───────────────────────────────────────────────────

function extractSearchQuery(lower: string, original: string): string | null {
  const match = lower.match(/^(?:search for|search|look up|google|find)\s+(.+)/);
  if (match) return original.slice(lower.indexOf(match[1]));
  return null;
}

// ── Main router ───────────────────────────────────────────────────────────────

export async function route(
  userMessage: string,
  sessionId: string,
): Promise<AIResponse> {
  const lower = userMessage.toLowerCase().trim();

  // Layer 1 — social / chitchat (check before any other logic)
  if (triggerMatch(lower, GREETING_TRIGGERS)) {
    return { reply: pick(GREETING_REPLIES), source: "greeting" };
  }
  if (triggerMatch(lower, HOW_ARE_YOU_TRIGGERS)) {
    return { reply: pick(HOW_ARE_YOU_REPLIES), source: "social" };
  }
  if (triggerMatch(lower, IDENTITY_TRIGGERS)) {
    return {
      reply:
        "I'm NexoraAI v1.0.0 — a fast, modular AI assistant with built-in knowledge across science, history, technology, mathematics, and more.\n\nWhat I can do:\n• Answer questions from my built-in knowledge base\n• Search the internet via DuckDuckGo when needed\n• Evaluate maths expressions\n• Look up capitals, chemical elements, and unit conversions\n• Remember facts you tell me\n• Hold natural multi-turn conversations",
      source: "identity",
    };
  }
  if (triggerMatch(lower, COMPLIMENT_TRIGGERS)) {
    return { reply: pick(COMPLIMENT_REPLIES), source: "social" };
  }
  if (triggerMatch(lower, FAREWELL_TRIGGERS)) {
    return { reply: pick(FAREWELL_REPLIES), source: "social" };
  }

  // Layer 2 — memory commands
  const rememberMatch = lower.match(/^(?:please )?remember\s+(.+)/);
  if (rememberMatch) {
    const fact = userMessage.slice(lower.indexOf(rememberMatch[1])).trim();
    const reply = memory.rememberFact(sessionId, fact);
    return { reply, source: "command" };
  }

  if (/what did i (?:tell|say|ask) you/.test(lower) || lower === "recall" || lower === "recall all") {
    const facts = memory.recallFacts(sessionId);
    const reply = facts.length > 0
      ? `Here's everything I remember:\n${facts.map(f => `• ${f}`).join("\n")}`
      : "I don't have anything stored in memory yet.";
    return { reply, source: "command" };
  }

  const recallMatch = lower.match(/^recall\s+(.+)/);
  if (recallMatch) {
    const topic = recallMatch[1].trim();
    const facts = memory.recallFacts(sessionId, topic);
    const reply = facts.length > 0
      ? `Matching memories for "${topic}":\n${facts.map(f => `• ${f}`).join("\n")}`
      : `I couldn't find anything related to "${topic}" in memory.`;
    return { reply, source: "command" };
  }

  // Layer 3 — explicit search
  const searchQuery = extractSearchQuery(lower, userMessage);
  if (searchQuery) {
    return doSearch(searchQuery);
  }

  // Layer 4 — math
  const mathResult = evaluateMath(lower);
  if (mathResult) {
    return { reply: `Here you go:\n  ${mathResult}`, source: "math" };
  }

  // Layer 5 — dataset lookups
  const capital = lookupCapital(lower);
  if (capital) return { reply: capital, source: "dataset" };

  const element = lookupElement(lower);
  if (element) return { reply: element, source: "dataset" };

  const conversion = lookupConversion(lower);
  if (conversion) return { reply: conversion, source: "dataset" };

  // Layer 6 — example matching
  const example = matchExample(userMessage);
  if (example) return { reply: example, source: "example" };

  // Layer 7 — knowledge base
  const kb = searchKnowledge(userMessage);
  if (kb) return { reply: kb, source: "knowledge" };

  // Layer 8 — automatic DuckDuckGo fallback
  const autoSearch = await doSearch(userMessage);
  if (autoSearch.searchResults && autoSearch.searchResults.length > 0) {
    return autoSearch;
  }

  return {
    reply:
      "I don't have a confident answer for that locally. Try asking me to 'search <topic>' and I'll look it up online, or rephrase your question.",
    source: "fallback",
  };
}

async function doSearch(query: string): Promise<AIResponse> {
  const results = await duckDuckGoSearch(query);
  if (results.length === 0) {
    return {
      reply: `I searched for "${query}" but couldn't retrieve results. Please check your internet connection and try again.`,
      source: "search",
      searchResults: [],
    };
  }

  const summary = results
    .map((r, i) => `${i + 1}. **${r.title}**\n   ${r.snippet}`)
    .join("\n\n");

  return {
    reply: `Here's what I found for "${query}":\n\n${summary}`,
    source: "search",
    searchResults: results,
  };
}
