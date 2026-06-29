import { route } from "../_lib/intelligence.js";
import * as mem from "../_lib/memory.js";

export default async function handler(req: any, res: any) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const { message, sessionId: clientSessionId } = req.body ?? {};

  if (!message || typeof message !== "string" || !message.trim()) {
    res.status(400).json({ error: "message is required" });
    return;
  }

  const sessionId: string = clientSessionId ?? mem.newSession();

  mem.addTurn(sessionId, "user", message);
  const result = await route(message, sessionId);
  mem.addTurn(sessionId, "assistant", result.reply);

  res.status(200).json({
    reply: result.reply,
    sessionId,
    source: result.source,
    searchResults: result.searchResults ?? null,
  });
}
