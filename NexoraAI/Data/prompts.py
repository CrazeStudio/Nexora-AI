"""
prompts.py — NexoraAI response templates and personality phrases.

All user-facing text lives here so tone and wording can be adjusted without
touching business logic.
"""

from __future__ import annotations

import random
from config import AI_NAME, AI_VERSION, AI_DESCRIPTION

# ── Greetings ─────────────────────────────────────────────────────────────────

GREETING_TRIGGERS: set[str] = {
    "hi", "hello", "hey", "howdy", "greetings", "good morning",
    "good afternoon", "good evening", "what's up", "sup", "yo",
}

GREETING_RESPONSES: list[str] = [
    f"Hello! I'm {AI_NAME}, your intelligent assistant. How can I help you today?",
    f"Hey there! {AI_NAME} here — ready to assist. What's on your mind?",
    f"Hi! Great to see you. I'm {AI_NAME}. Ask me anything!",
    f"Greetings! I'm {AI_NAME}. What would you like to explore today?",
    f"Hello! {AI_NAME} at your service. What can I help you with?",
]

# ── Farewells ─────────────────────────────────────────────────────────────────

FAREWELL_TRIGGERS: set[str] = {
    "bye", "goodbye", "exit", "quit", "farewell", "see you",
    "see ya", "take care", "cya", "later",
}

FAREWELL_RESPONSES: list[str] = [
    f"Goodbye! It was a pleasure chatting with you. Come back anytime!",
    f"Take care! {AI_NAME} is always here when you need me.",
    f"Farewell! I hope I was helpful. Have a wonderful day!",
    f"Bye! Don't hesitate to return if you have more questions.",
]

# ── Compliments / Positive Feedback ───────────────────────────────────────────

COMPLIMENT_TRIGGERS: set[str] = {
    "thanks", "thank you", "thank", "great", "awesome", "amazing",
    "well done", "nice", "excellent", "brilliant", "perfect",
    "good job", "well said", "helpful",
}

COMPLIMENT_RESPONSES: list[str] = [
    "You're very welcome! Happy to help.",
    "Glad I could assist! Let me know if you need anything else.",
    "Thank you for the kind words! I'm here if you have more questions.",
    "Always a pleasure! What else can I help you with?",
    "Wonderful! Feel free to ask me anything.",
]

# ── How-are-you / Feelings ────────────────────────────────────────────────────

HOW_ARE_YOU_TRIGGERS: set[str] = {
    "how are you", "how do you do", "how's it going", "you ok",
    "are you ok", "feeling", "how are things",
}

HOW_ARE_YOU_RESPONSES: list[str] = [
    (
        f"I'm doing great, thanks for asking! As an AI I don't experience "
        f"feelings the way humans do, but I'm fully charged and ready to help. "
        f"How about you?"
    ),
    (
        f"All systems running smoothly! I'm {AI_NAME} and I'm here to assist "
        f"you. What's on your mind?"
    ),
    (
        f"Functioning perfectly and eager to help! What can I do for you today?"
    ),
]

# ── Who / What are you ────────────────────────────────────────────────────────

IDENTITY_TRIGGERS: set[str] = {
    "who are you", "what are you", "tell me about yourself",
    "what can you do", "your name", "introduce yourself",
    "what is nexora", "about nexorai",
}

IDENTITY_RESPONSE: str = (
    f"I'm {AI_NAME} v{AI_VERSION} — {AI_DESCRIPTION}\n\n"
    f"Here's what I can do:\n"
    f"  🔍  Answer questions from my built-in knowledge base\n"
    f"  🌐  Search the internet via DuckDuckGo when needed\n"
    f"  🧮  Evaluate maths expressions\n"
    f"  📖  Look up capitals, chemical elements, and unit conversions\n"
    f"  🧠  Remember facts you tell me (across sessions)\n"
    f"  💬  Hold natural multi-turn conversations\n\n"
    f"Type 'help' for a full list of commands."
)

# ── Help menu ─────────────────────────────────────────────────────────────────

HELP_TEXT: str = f"""
{AI_NAME} — Command Reference
{"─" * 40}

Conversation
  Just type and press Enter to chat.

Special Commands
  help                 Show this help menu
  exit / quit / bye    End the session
  clear memory         Forget all stored facts and history
  remember <text>      Store a fact in persistent memory
  recall               Show everything I've remembered
  recall <topic>       Search memory for a topic
  what did i tell you  Show all stored memories
  history              Show conversation history

Examples
  "What is photosynthesis?"
  "Capital of Japan?"
  "20 km in miles"
  "100 * (3 + 7)"
  "Remember I prefer metric units"
  "Recall units"
  "Search for latest Python news"
{"─" * 40}
"""

# ── Not-understood ────────────────────────────────────────────────────────────

NOT_UNDERSTOOD_RESPONSES: list[str] = [
    (
        "I'm not sure I have a local answer for that. "
        "Would you like me to search the internet? "
        "Just ask 'search for <your query>'."
    ),
    (
        "That's outside my current knowledge base. "
        "Try asking me to 'search for {topic}' and I'll look it up online."
    ),
    (
        "Hmm, I don't have a confident answer for that locally. "
        "You can ask me to search online — try 'search <your question>'."
    ),
    (
        "I don't have enough local information on that. "
        "Want me to search DuckDuckGo? Just say 'search <topic>'."
    ),
]

# ── Thinking / Loading ────────────────────────────────────────────────────────

THINKING_PHRASES: list[str] = [
    "Let me think about that…",
    "Processing…",
    "Looking that up for you…",
    "One moment…",
    "Let me check my knowledge base…",
]

SEARCH_PHRASES: list[str] = [
    "Searching the internet for you…",
    "Let me look that up online…",
    "Fetching results from DuckDuckGo…",
    "Searching online…",
]

# ── Utility ───────────────────────────────────────────────────────────────────

def random_greeting() -> str:
    """Return a random greeting response."""
    return random.choice(GREETING_RESPONSES)


def random_farewell() -> str:
    """Return a random farewell response."""
    return random.choice(FAREWELL_RESPONSES)


def random_compliment_reply() -> str:
    """Return a random reply to a compliment."""
    return random.choice(COMPLIMENT_RESPONSES)


def random_how_are_you() -> str:
    """Return a random 'how are you' response."""
    return random.choice(HOW_ARE_YOU_RESPONSES)


def random_not_understood() -> str:
    """Return a random 'not understood' response."""
    return random.choice(NOT_UNDERSTOOD_RESPONSES)
