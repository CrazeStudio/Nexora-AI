/**
 * search.ts — DuckDuckGo instant-answer search via Node.js built-in fetch.
 *
 * Uses DuckDuckGo's free JSON API (no package required, no API key).
 * Falls back gracefully on network errors.
 */

export interface SearchResult {
  title: string;
  url: string;
  snippet: string;
}

const DDG_URL = "https://api.duckduckgo.com/";
const TIMEOUT_MS = 8000;

export async function duckDuckGoSearch(query: string): Promise<SearchResult[]> {
  const params = new URLSearchParams({
    q: query,
    format: "json",
    no_redirect: "1",
    no_html: "1",
    skip_disambig: "1",
  });

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const resp = await fetch(`${DDG_URL}?${params}`, {
      signal: controller.signal,
      headers: { "User-Agent": "NexoraAI/1.0 (educational assistant)" },
    });

    if (!resp.ok) return [];

    const data = (await resp.json()) as Record<string, unknown>;
    const results: SearchResult[] = [];

    // AbstractText — the main instant answer
    if (typeof data.AbstractText === "string" && data.AbstractText) {
      results.push({
        title: (data.Heading as string) || query,
        url: (data.AbstractURL as string) || "https://duckduckgo.com",
        snippet: data.AbstractText,
      });
    }

    // RelatedTopics
    const topics = data.RelatedTopics as Array<Record<string, unknown>>;
    if (Array.isArray(topics)) {
      for (const topic of topics.slice(0, 4)) {
        if (typeof topic.Text === "string" && topic.Text) {
          const firstUrl = (topic.FirstURL as string) || "https://duckduckgo.com";
          results.push({
            title: topic.Text.split(" - ")[0] ?? query,
            url: firstUrl,
            snippet: topic.Text,
          });
        }
      }
    }

    return results.slice(0, 5);
  } catch {
    return [];
  } finally {
    clearTimeout(timer);
  }
}
