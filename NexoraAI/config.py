"""
config.py — NexoraAI global configuration.

All tuneable constants live here so nothing is buried in business logic.
"""

# ── Identity ────────────────────────────────────────────────────────────────
AI_NAME: str = "NexoraAI"
AI_VERSION: str = "1.0.0"
AI_AUTHOR: str = "NexoraAI Team"
AI_DESCRIPTION: str = (
    "A fast, modular AI assistant that works offline with a built-in "
    "knowledge base and online via DuckDuckGo search."
)

# ── Personality ──────────────────────────────────────────────────────────────
PERSONALITY_TRAITS: list[str] = [
    "curious", "helpful", "friendly", "precise", "creative",
]
PERSONALITY_TONE: str = "professional yet warm"

# ── Memory ───────────────────────────────────────────────────────────────────
MEMORY_FILE: str = "nexora_memory.json"      # persistent key-value facts
MAX_HISTORY: int = 50                        # max conversation turns kept

# ── Search ────────────────────────────────────────────────────────────────────
SEARCH_MAX_RESULTS: int = 5                  # DuckDuckGo results to fetch
SEARCH_TIMEOUT: int = 8                      # seconds before giving up

# ── Knowledge ────────────────────────────────────────────────────────────────
MIN_RELEVANCE_SCORE: float = 0.25           # keyword match threshold (0-1)

# ── Display ──────────────────────────────────────────────────────────────────
PROMPT_SYMBOL: str = "You"
AI_SYMBOL: str = AI_NAME
SEPARATOR: str = "─" * 60
