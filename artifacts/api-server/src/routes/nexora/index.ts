/**
 * nexora/index.ts — Express route handlers for NexoraAI web API.
 */

import { Router } from "express";
import type { Request, Response } from "express";
import * as mem from "./memory.js";
import { route } from "./intelligence.js";
import {
  SendMessageBody,
  RememberFactBody,
  GetMemoryQueryParams,
  ClearMemoryQueryParams,
} from "@workspace/api-zod";

const router = Router();

// ── POST /nexora/chat ─────────────────────────────────────────────────────────

router.post("/nexora/chat", async (req: Request, res: Response) => {
  const parsed = SendMessageBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid request body" });
    return;
  }

  const { message, sessionId: clientSessionId } = parsed.data;

  // Use existing session or create a new one
  const sessionId = clientSessionId ?? mem.newSession();

  // Store user turn
  mem.addTurn(sessionId, "user", message);

  // Route through intelligence pipeline
  const result = await route(message, sessionId);

  // Store assistant turn
  mem.addTurn(sessionId, "assistant", result.reply);

  res.json({
    reply: result.reply,
    sessionId,
    source: result.source,
    searchResults: result.searchResults ?? null,
  });
});

// ── GET /nexora/memory ────────────────────────────────────────────────────────

router.get("/nexora/memory", (req: Request, res: Response) => {
  const parsed = GetMemoryQueryParams.safeParse(req.query);
  const sessionId = parsed.success ? (parsed.data.sessionId ?? "") : "";
  const query = parsed.success ? parsed.data.query : undefined;

  if (!sessionId) {
    res.json({ memories: [], sessionId: "" });
    return;
  }

  const memories = mem.recallFacts(sessionId, query);
  res.json({ memories, sessionId });
});

// ── DELETE /nexora/memory ─────────────────────────────────────────────────────

router.delete("/nexora/memory", (req: Request, res: Response) => {
  const parsed = ClearMemoryQueryParams.safeParse(req.query);
  const sessionId = parsed.success ? (parsed.data.sessionId ?? "") : "";

  if (sessionId) mem.clearMemory(sessionId);

  res.json({ success: true, message: "Memory cleared." });
});

// ── POST /nexora/memory/remember ──────────────────────────────────────────────

router.post("/nexora/memory/remember", (req: Request, res: Response) => {
  const parsed = RememberFactBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid request body" });
    return;
  }

  const { fact, sessionId: clientSessionId } = parsed.data;
  const sessionId = clientSessionId ?? mem.newSession();

  const message = mem.rememberFact(sessionId, fact);
  res.json({ success: true, message });
});

// ── GET /nexora/suggestions ───────────────────────────────────────────────────

router.get("/nexora/suggestions", (_req: Request, res: Response) => {
  res.json({
    suggestions: [
      "What is photosynthesis?",
      "Tell me about black holes",
      "What is the capital of Japan?",
      "Calculate 25 * (4 + 6)",
      "10 km in miles",
      "What is the speed of light?",
      "Who invented the telephone?",
      "Element oxygen",
      "100 fahrenheit in celsius",
      "What is artificial intelligence?",
      "Explain the Pythagorean theorem",
      "Search for latest tech news",
    ],
  });
});

export default router;
