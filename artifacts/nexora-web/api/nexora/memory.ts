import * as mem from "../_lib/memory.js";

export default function handler(req: any, res: any) {
  const sessionId: string = (req.query?.sessionId as string) ?? "";

  if (req.method === "GET") {
    const query = req.query?.query as string | undefined;
    const memories = sessionId ? mem.recallFacts(sessionId, query) : [];
    res.status(200).json({ memories, sessionId });
    return;
  }

  if (req.method === "DELETE") {
    if (sessionId) mem.clearMemory(sessionId);
    res.status(200).json({ success: true, message: "Memory cleared." });
    return;
  }

  res.status(405).json({ error: "Method not allowed" });
}
