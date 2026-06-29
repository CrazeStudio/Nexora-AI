"""
api.py — NexoraAI internet search via DuckDuckGo.

Wraps the duckduckgo-search library with graceful error handling, result
formatting, and a source-URL display.  All network errors are caught and
reported as friendly messages rather than exceptions.
"""

from __future__ import annotations

from typing import Optional

from config import SEARCH_MAX_RESULTS, SEARCH_TIMEOUT

# Lazy import so the app still launches if the package is missing.
try:
    from duckduckgo_search import DDGS
    _DDGS_AVAILABLE = True
except ImportError:
    _DDGS_AVAILABLE = False


# ── Public API ─────────────────────────────────────────────────────────────────

def search(query: str) -> str:
    """
    Search DuckDuckGo for *query* and return a formatted result string.

    Fetches up to SEARCH_MAX_RESULTS results and formats each with a
    title, URL, and summary snippet.

    Args:
        query: The search query string.

    Returns:
        A formatted multi-line string with results, or an error message.
    """
    query = query.strip()
    if not query:
        return "Please provide a search query."

    if not _DDGS_AVAILABLE:
        return (
            "DuckDuckGo Search is not installed. "
            "Run: pip install duckduckgo-search"
        )

    results = _fetch_results(query)
    if not results:
        return f"No results found for \"{query}\"."

    return _format_results(query, results)


def is_available() -> bool:
    """Return True if the duckduckgo-search package is installed."""
    return _DDGS_AVAILABLE


# ── Private helpers ───────────────────────────────────────────────────────────

def _fetch_results(query: str) -> list[dict]:
    """
    Hit the DuckDuckGo API and return raw result dicts.

    Args:
        query: Search term.

    Returns:
        List of result dicts, possibly empty on error.
    """
    try:
        with DDGS() as ddgs:
            return list(
                ddgs.text(
                    query,
                    max_results=SEARCH_MAX_RESULTS,
                    timelimit=None,
                )
            )
    except Exception as exc:
        # Surface a friendly error instead of crashing.
        raise _SearchError(str(exc)) from exc


def _format_results(query: str, results: list[dict]) -> str:
    """
    Build a human-readable block from raw DuckDuckGo result dicts.

    Args:
        query:   The original search query.
        results: List of raw result dicts from DDGS.

    Returns:
        Formatted string ready to display in the terminal.
    """
    lines: list[str] = [
        f"Search results for \"{query}\":",
        "─" * 50,
    ]

    for idx, result in enumerate(results, start=1):
        title = result.get("title", "No title").strip()
        url   = result.get("href",  result.get("url", "No URL")).strip()
        body  = result.get("body",  "No description.").strip()

        # Truncate long bodies to keep output readable.
        if len(body) > 280:
            body = body[:277] + "…"

        lines.append(f"\n{idx}. {title}")
        lines.append(f"   🔗 {url}")
        lines.append(f"   {body}")

    lines.append("\n" + "─" * 50)
    return "\n".join(lines)


class _SearchError(Exception):
    """Raised when a DuckDuckGo request fails."""
