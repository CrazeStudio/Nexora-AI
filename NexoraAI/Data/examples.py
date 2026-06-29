"""
examples.py — NexoraAI example-based response system.

Each example maps a canonical question to a short, direct answer.
The match() function finds the closest example using token overlap scoring
and returns its answer if the similarity is high enough.
"""

from __future__ import annotations

import re
from typing import Optional


# ── Example Q&A pairs ─────────────────────────────────────────────────────────

EXAMPLES: list[dict[str, str]] = [
    # General knowledge
    {"q": "who invented the telephone",
     "a": "The telephone was invented by Alexander Graham Bell, who received "
          "the first patent in 1876."},
    {"q": "who invented the light bulb",
     "a": "Thomas Edison is credited with developing the first practical "
          "incandescent light bulb in 1879, though earlier inventors made "
          "important contributions."},
    {"q": "who wrote hamlet",
     "a": "Hamlet was written by William Shakespeare, believed to be between "
          "1599 and 1601."},
    {"q": "what is the boiling point of water",
     "a": "Water boils at 100 °C (212 °F) at standard atmospheric pressure "
          "(1 atm). At higher altitudes, where pressure is lower, it boils "
          "at lower temperatures."},
    {"q": "what is the freezing point of water",
     "a": "Water freezes at 0 °C (32 °F) at standard atmospheric pressure."},
    {"q": "how many continents are there",
     "a": "There are 7 continents: Africa, Antarctica, Asia, Australia "
          "(Oceania), Europe, North America, and South America."},
    {"q": "how many countries in the world",
     "a": "There are 195 countries in the world — 193 United Nations member "
          "states plus Vatican City and Palestine as observer states."},
    {"q": "what is the largest ocean",
     "a": "The Pacific Ocean is the largest and deepest ocean, covering "
          "about 165 million km² — more than all land combined."},
    {"q": "what is the smallest country in the world",
     "a": "Vatican City is the world's smallest country, covering only "
          "about 44 hectares (0.44 km²) within Rome, Italy."},
    {"q": "how far is the moon from earth",
     "a": "The average distance from Earth to the Moon is about 384,400 km "
          "(238,855 miles). It varies because the Moon's orbit is elliptical."},
    {"q": "how far is the sun from earth",
     "a": "The average distance from Earth to the Sun is about 149.6 million km "
          "(93 million miles), defined as 1 Astronomical Unit (AU)."},
    {"q": "how old is the earth",
     "a": "Earth is approximately 4.54 billion years old, based on radiometric "
          "dating of meteorites and Earth's oldest rocks."},
    {"q": "how old is the universe",
     "a": "The universe is approximately 13.8 billion years old, based on "
          "measurements of the cosmic microwave background radiation."},
    # Programming
    {"q": "what does html stand for",
     "a": "HTML stands for HyperText Markup Language. It is the standard "
          "language for creating web pages."},
    {"q": "what does css stand for",
     "a": "CSS stands for Cascading Style Sheets. It is used to style and "
          "layout web pages written in HTML."},
    {"q": "what is a variable in programming",
     "a": "A variable is a named storage location in memory that holds a "
          "value which can be read or modified during program execution."},
    {"q": "what is an algorithm",
     "a": "An algorithm is a finite, step-by-step set of instructions designed "
          "to solve a problem or accomplish a task."},
    {"q": "what is recursion",
     "a": "Recursion is a programming technique where a function calls itself "
          "to solve smaller instances of the same problem. Every recursive "
          "function needs a base case to stop infinite recursion."},
    {"q": "what is object oriented programming",
     "a": "Object-Oriented Programming (OOP) is a paradigm that organises "
          "code around objects — bundles of data (attributes) and behaviour "
          "(methods). Core principles: Encapsulation, Inheritance, "
          "Polymorphism, and Abstraction."},
    # Maths shortcuts
    {"q": "what is the square root of 144",
     "a": "The square root of 144 is 12, because 12 × 12 = 144."},
    {"q": "what is 2 to the power of 10",
     "a": "2 to the power of 10 is 1,024."},
    # Science shortcuts
    {"q": "what is the chemical formula for water",
     "a": "The chemical formula for water is H₂O — two hydrogen atoms bonded "
          "to one oxygen atom."},
    {"q": "what is the chemical formula for salt",
     "a": "Table salt is sodium chloride, with the chemical formula NaCl."},
    {"q": "what is the chemical formula for carbon dioxide",
     "a": "Carbon dioxide has the formula CO₂ — one carbon atom and two "
          "oxygen atoms."},
    {"q": "how many bones in the human body",
     "a": "An adult human body has 206 bones. Babies are born with around "
          "270–300 bones, many of which fuse together during childhood."},
    {"q": "how many chambers does the heart have",
     "a": "The human heart has 4 chambers: the right atrium, right ventricle, "
          "left atrium, and left ventricle."},
    # History
    {"q": "when did world war 1 start",
     "a": "World War I started on 28 July 1914 when Austria-Hungary declared "
          "war on Serbia, following the assassination of Archduke Franz "
          "Ferdinand."},
    {"q": "when did world war 2 end",
     "a": "World War II ended in 1945: Germany surrendered on 8 May "
          "(V-E Day) and Japan surrendered on 2 September (V-J Day) after "
          "the atomic bombings of Hiroshima and Nagasaki."},
    {"q": "who was the first president of the united states",
     "a": "George Washington was the first President of the United States, "
          "serving from 1789 to 1797."},
]


# ── Similarity scoring ────────────────────────────────────────────────────────

_STOP_WORDS: set[str] = {
    "a", "an", "the", "is", "are", "was", "were", "what", "who",
    "where", "when", "how", "why", "which", "do", "does", "did",
    "in", "of", "to", "for", "and", "or", "it", "its", "i",
}

_MIN_EXAMPLE_SCORE: float = 0.45  # minimum fraction of query tokens that must match


def _clean_tokens(text: str) -> set[str]:
    """Return significant lowercase tokens from *text*, minus stop words."""
    raw = set(re.findall(r"[a-z0-9]+", text.lower()))
    return raw - _STOP_WORDS


def match(query: str) -> Optional[str]:
    """
    Find the closest example to *query* using token Jaccard similarity.

    Args:
        query: The user's input string.

    Returns:
        The example answer if similarity meets the threshold, else None.
    """
    q_tokens = _clean_tokens(query)
    if not q_tokens:
        return None

    best_score = 0.0
    best_answer: Optional[str] = None

    for example in EXAMPLES:
        e_tokens = _clean_tokens(example["q"])
        if not e_tokens:
            continue

        # Jaccard-like: intersection / union
        intersection = q_tokens & e_tokens
        union = q_tokens | e_tokens
        score = len(intersection) / len(union) if union else 0.0

        if score > best_score:
            best_score = score
            best_answer = example["a"]

    if best_score >= _MIN_EXAMPLE_SCORE:
        return best_answer
    return None
