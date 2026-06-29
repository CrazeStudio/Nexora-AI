import * as mem from "../../_lib/memory.js";

export default function handler(req: any, res: any) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const { fact, sessionId: clientSessionId } = req.body ?? {};

  if (!fact || typeof fact !== "string" || !fact.trim()) {
    res.status(400).json({ error: "fact is required" });
    return;
  }

  const sessionId: string = clientSessionId ?? mem.newSession();
  const message = mem.rememberFact(sessionId, fact);
  res.status(200).json({ success: true, message });
}
