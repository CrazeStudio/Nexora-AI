"""
memory.py — NexoraAI memory system.

Two layers:
  1. Session memory  — conversation history for the current run (in-RAM list).
  2. Persistent memory — user-defined facts stored in a JSON file on disk so
                         they survive across sessions.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Optional

from config import MAX_HISTORY, MEMORY_FILE


# ── Type aliases ─────────────────────────────────────────────────────────────
Turn = dict[str, str]          # {"role": "user"|"assistant", "text": "..."}
FactStore = dict[str, str]     # {"key": "value"}


# ── Session memory ────────────────────────────────────────────────────────────

_conversation_history: list[Turn] = []


def add_turn(role: str, text: str) -> None:
    """
    Append a turn to the in-session conversation history.

    Args:
        role: Either "user" or "assistant".
        text: The message content.
    """
    _conversation_history.append(
        {"role": role, "text": text, "time": _now()}
    )
    # Trim to keep only the most recent MAX_HISTORY turns.
    if len(_conversation_history) > MAX_HISTORY:
        del _conversation_history[: len(_conversation_history) - MAX_HISTORY]


def get_history() -> list[Turn]:
    """Return a copy of the current conversation history."""
    return list(_conversation_history)


def clear_history() -> None:
    """Wipe all in-session conversation history."""
    _conversation_history.clear()


def history_summary() -> str:
    """Return a human-readable summary of the conversation history."""
    if not _conversation_history:
        return "No conversation history yet."
    lines = []
    for turn in _conversation_history:
        label = "You" if turn["role"] == "user" else "NexoraAI"
        lines.append(f"[{turn.get('time', '')}] {label}: {turn['text']}")
    return "\n".join(lines)


# ── Persistent memory ─────────────────────────────────────────────────────────

def _load_facts() -> FactStore:
    """Load persistent facts from the JSON file on disk."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_facts(facts: FactStore) -> None:
    """Persist facts to the JSON file on disk."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as fh:
            json.dump(facts, fh, indent=2, ensure_ascii=False)
    except OSError as exc:
        print(f"[Memory] Warning: could not save facts — {exc}")


def remember(text: str) -> str:
    """
    Store *text* in persistent memory, keyed by a simple slug.

    The entire sentence is stored.  A short key is derived from the first
    few words so the user can recall it.

    Args:
        text: The fact/statement to remember.

    Returns:
        A confirmation message.
    """
    text = text.strip()
    if not text:
        return "There is nothing to remember — please provide some text."

    facts = _load_facts()
    # Derive a key from the first 4 words (lowercase, underscored).
    words = text.split()[:4]
    key = "_".join(w.lower() for w in words)
    key = key[:40]  # cap key length

    facts[key] = text
    _save_facts(facts)
    return f"Got it! I've remembered: \"{text}\""


def recall(query: str = "") -> str:
    """
    Retrieve facts from persistent memory.

    If *query* is provided, return the facts whose key or value contains
    the query string.  If *query* is empty, return all stored facts.

    Args:
        query: An optional search string.

    Returns:
        A formatted string listing matching facts, or a 'nothing found' note.
    """
    facts = _load_facts()
    if not facts:
        return "I don't have anything stored in memory yet."

    q = query.strip().lower()
    if q:
        matches = {
            k: v for k, v in facts.items()
            if q in k.lower() or q in v.lower()
        }
    else:
        matches = facts

    if not matches:
        return f"I couldn't find anything related to \"{query}\" in memory."

    lines = [f"• {v}" for v in matches.values()]
    header = "Here's everything I remember:" if not q else f"Matching memories for \"{query}\":"
    return f"{header}\n" + "\n".join(lines)


def clear_memory() -> str:
    """
    Delete all persistent facts from memory.

    Returns:
        A confirmation message.
    """
    if os.path.exists(MEMORY_FILE):
        try:
            os.remove(MEMORY_FILE)
        except OSError:
            pass
    clear_history()
    return "Memory cleared. I've forgotten everything stored so far."


def list_memories() -> str:
    """
    Return all stored facts as a readable list.

    Returns:
        Formatted string of facts or a 'nothing stored' message.
    """
    return recall()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _now() -> str:
    """Return the current time as a short HH:MM string."""
    return datetime.now().strftime("%H:%M")
