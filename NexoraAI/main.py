"""
main.py — NexoraAI entry point and conversation engine.

Runs an interactive command-line loop, routing each user turn through a
layered intelligence pipeline:

  1. Command detection   (built-in commands: help, exit, remember…)
  2. Social/chitchat     (greetings, farewells, "how are you", identity)
  3. Math evaluation     (expressions like "12 * (3 + 7)")
  4. Dataset lookup      (capitals, elements, unit conversions)
  5. Example matching    (curated Q&A pairs)
  6. Knowledge base      (topic-indexed knowledge with keyword scoring)
  7. DuckDuckGo search   (fallback — triggered explicitly or automatically)

No external AI API is required.  All intelligence is built-in.
"""

from __future__ import annotations

import re
import sys
import os

# ── Make sure sibling packages are on sys.path when running from any CWD ─────
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from config import AI_NAME, AI_SYMBOL, PROMPT_SYMBOL, SEPARATOR

from Data import memory, knowledge, datasets, examples, prompts
from Api import api

# Optional colour support (degrades gracefully without colorama)
try:
    from colorama import Fore, Style, init as _colorama_init
    _colorama_init(autoreset=True)
    _HAS_COLOR = True
except ImportError:
    _HAS_COLOR = False


# ── Colour helpers ─────────────────────────────────────────────────────────────

def _color(text: str, color_code: str) -> str:
    """Wrap *text* in ANSI colour if colorama is available."""
    if _HAS_COLOR:
        return f"{color_code}{text}{Style.RESET_ALL}"
    return text


def _ai(text: str) -> str:
    return _color(f"{AI_SYMBOL}: ", Fore.CYAN) + text if _HAS_COLOR else f"{AI_SYMBOL}: {text}"


def _user_prompt() -> str:
    return _color(f"{PROMPT_SYMBOL}: ", Fore.GREEN) if _HAS_COLOR else f"{PROMPT_SYMBOL}: "


def _dim(text: str) -> str:
    return _color(text, Style.DIM) if _HAS_COLOR else text


# ── Trigger matching ──────────────────────────────────────────────────────────

def _trigger_match(text: str, triggers: set[str]) -> bool:
    """
    Return True if any trigger phrase appears in *text* with word boundaries.

    Single-word triggers must match whole words (prevents "yo" matching "you").
    Multi-word triggers use substring matching (they already span words).

    Args:
        text:     Lowercased user input.
        triggers: Set of trigger strings to check.

    Returns:
        True if at least one trigger matches.
    """
    words = set(text.split())
    for trigger in triggers:
        if " " in trigger:
            # Multi-word: substring match is fine
            if trigger in text:
                return True
        else:
            # Single-word: require exact whole-word match
            if trigger in words:
                return True
    return False


# ── NexoraAI class ─────────────────────────────────────────────────────────────

class NexoraAI:
    """
    Core AI assistant engine.

    Attributes:
        name: The assistant's display name.
    """

    def __init__(self) -> None:
        self.name: str = AI_NAME

    # ── Public interface ───────────────────────────────────────────────────────

    def respond(self, user_input: str) -> str:
        """
        Generate a response for *user_input*.

        Routes the input through the intelligence pipeline and returns
        a response string.  Never raises — all errors are caught and
        surfaced as friendly messages.

        Args:
            user_input: Raw text entered by the user.

        Returns:
            The assistant's response as a string.
        """
        text = user_input.strip()
        if not text:
            return "I didn't catch that — could you rephrase?"

        # Store the user's turn in session memory.
        memory.add_turn("user", text)

        response = self._route(text)

        # Store the assistant's response in session memory.
        memory.add_turn("assistant", response)
        return response

    # ── Pipeline ───────────────────────────────────────────────────────────────

    def _route(self, text: str) -> str:
        """
        Run *text* through the multi-layer intelligence pipeline.

        Each layer returns a string response or None to fall through to
        the next layer.

        Args:
            text: Cleaned user input.

        Returns:
            The first non-None response from the pipeline.
        """
        lower = text.lower().strip()

        # Layer 1 — built-in commands
        cmd = self._handle_command(lower, text)
        if cmd is not None:
            return cmd

        # Layer 2 — social / chitchat
        social = self._handle_social(lower)
        if social is not None:
            return social

        # Layer 3 — explicit internet search request
        search_trigger = self._extract_search_query(lower, text)
        if search_trigger is not None:
            return self._do_search(search_trigger)

        # Layer 4 — math expression
        math_result = datasets.evaluate_math(lower)
        if math_result is not None:
            return f"Here you go:\n  {math_result}"

        # Layer 5 — structured dataset lookups
        dataset_result = self._dataset_lookup(lower)
        if dataset_result is not None:
            return dataset_result

        # Layer 6 — example-based answers
        example_result = examples.match(text)
        if example_result is not None:
            return example_result

        # Layer 7 — knowledge base
        kb_result = knowledge.search(text)
        if kb_result is not None:
            return kb_result

        # Layer 8 — automatic online fallback
        return prompts.random_not_understood()

    # ── Layer handlers ─────────────────────────────────────────────────────────

    def _handle_command(self, lower: str, original: str) -> str | None:
        """
        Detect and execute built-in commands.

        Args:
            lower:    Lowercased user input.
            original: Original casing (used for 'remember').

        Returns:
            Response string if a command matched, else None.
        """
        # Exit commands
        if lower in {"exit", "quit", "bye", "goodbye", "farewell"}:
            return _SENTINEL_EXIT  # handled by the REPL loop

        # Help
        if lower in {"help", "?", "commands"}:
            return prompts.HELP_TEXT

        # Clear memory
        if lower in {"clear memory", "forget everything", "reset memory",
                     "clear", "wipe memory"}:
            return memory.clear_memory()

        # Conversation history
        if lower in {"history", "show history", "conversation history"}:
            h = memory.history_summary()
            return h

        # What did I tell you / recall all
        if re.search(r"what did i (?:tell|say|ask) you", lower) or \
                lower in {"recall", "recall all", "what do you remember",
                          "show memories", "memories"}:
            return memory.list_memories()

        # Remember <fact>
        remember_match = re.match(
            r"(?:please )?remember\s+(.+)", lower, re.IGNORECASE
        )
        if remember_match:
            fact = original[remember_match.start(1):].strip()
            return memory.remember(fact)

        # Recall <topic>
        recall_match = re.match(r"recall\s+(.+)", lower, re.IGNORECASE)
        if recall_match:
            topic = recall_match.group(1).strip()
            return memory.recall(topic)

        return None

    def _handle_social(self, lower: str) -> str | None:
        """
        Handle greetings, farewells, compliments, and identity questions.

        Args:
            lower: Lowercased user input.

        Returns:
            Response string if recognised, else None.
        """
        # Greetings
        if _trigger_match(lower, prompts.GREETING_TRIGGERS):
            return prompts.random_greeting()

        # How are you
        if _trigger_match(lower, prompts.HOW_ARE_YOU_TRIGGERS):
            return prompts.random_how_are_you()

        # Identity
        if _trigger_match(lower, prompts.IDENTITY_TRIGGERS):
            return prompts.IDENTITY_RESPONSE

        # Compliments / thanks
        if _trigger_match(lower, prompts.COMPLIMENT_TRIGGERS):
            return prompts.random_compliment_reply()

        return None

    def _extract_search_query(self, lower: str, original: str) -> str | None:
        """
        Detect explicit search requests and extract the query.

        Patterns matched:
          - "search for <query>"
          - "search <query>"
          - "look up <query>"
          - "google <query>"  / "find <query> online"

        Args:
            lower:    Lowercased input.
            original: Original casing.

        Returns:
            The search query string if a pattern matched, else None.
        """
        patterns = [
            r"(?:search for|search|look up|google|find online|find)\s+(.+)",
        ]
        for pat in patterns:
            m = re.match(pat, lower)
            if m:
                # Use original casing for the query
                start = m.start(1)
                return original[start:].strip()
        return None

    def _dataset_lookup(self, lower: str) -> str | None:
        """
        Run all structured dataset lookups in priority order.

        Args:
            lower: Lowercased user input.

        Returns:
            Lookup result string or None.
        """
        # Capital cities
        result = datasets.lookup_capital(lower)
        if result:
            return result

        # Chemical elements
        result = datasets.lookup_element(lower)
        if result:
            return result

        # Unit conversions
        result = datasets.lookup_conversion(lower)
        if result:
            return result

        return None

    def _do_search(self, query: str) -> str:
        """
        Execute a DuckDuckGo search and return formatted results.

        Args:
            query: The search query.

        Returns:
            Formatted search results or an error message.
        """
        try:
            return api.search(query)
        except Exception as exc:
            return (
                f"Sorry, I couldn't complete the search right now "
                f"({exc}). Please check your internet connection and try again."
            )


# ── Sentinel ───────────────────────────────────────────────────────────────────
_SENTINEL_EXIT = "__EXIT__"


# ── REPL loop ──────────────────────────────────────────────────────────────────

def run() -> None:
    """Start the interactive NexoraAI session."""
    _print_banner()
    ai = NexoraAI()

    while True:
        try:
            user_input = input(_user_prompt()).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print(_ai(prompts.random_farewell()))
            break

        if not user_input:
            continue

        # Check for exit before calling respond() so we can print goodbye.
        if user_input.lower() in {"exit", "quit", "bye", "goodbye", "farewell"}:
            print(_ai(prompts.random_farewell()))
            break

        response = ai.respond(user_input)

        # Sentinel check (belt-and-suspenders if routed through respond())
        if response == _SENTINEL_EXIT:
            print(_ai(prompts.random_farewell()))
            break

        print(_ai(response))
        print()  # breathing room between turns


# ── Banner ─────────────────────────────────────────────────────────────────────

def _print_banner() -> None:
    """Print the NexoraAI startup banner."""
    from config import AI_VERSION, AI_DESCRIPTION

    banner_lines = [
        SEPARATOR,
        _color(f"  {AI_NAME}  v{AI_VERSION}", Fore.CYAN if _HAS_COLOR else ""),
        _dim(f"  {AI_DESCRIPTION}"),
        "",
        _dim("  Type 'help' for commands.  Type 'exit' to quit."),
        SEPARATOR,
        "",
    ]
    print("\n".join(banner_lines))


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run()
