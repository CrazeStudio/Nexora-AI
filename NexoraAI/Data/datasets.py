"""
datasets.py — NexoraAI structured lookup datasets.

Each dataset is a plain Python dictionary with a dedicated lookup function.
All functions return a string ready to display to the user or None when no
match is found.
"""

from __future__ import annotations

import re
from typing import Optional


# ── Countries & Capitals ─────────────────────────────────────────────────────

CAPITALS: dict[str, str] = {
    "afghanistan": "Kabul",
    "albania": "Tirana",
    "algeria": "Algiers",
    "argentina": "Buenos Aires",
    "australia": "Canberra",
    "austria": "Vienna",
    "bangladesh": "Dhaka",
    "belgium": "Brussels",
    "bolivia": "Sucre",
    "brazil": "Brasília",
    "canada": "Ottawa",
    "chile": "Santiago",
    "china": "Beijing",
    "colombia": "Bogotá",
    "croatia": "Zagreb",
    "cuba": "Havana",
    "czechia": "Prague",
    "denmark": "Copenhagen",
    "egypt": "Cairo",
    "ethiopia": "Addis Ababa",
    "finland": "Helsinki",
    "france": "Paris",
    "germany": "Berlin",
    "ghana": "Accra",
    "greece": "Athens",
    "hungary": "Budapest",
    "india": "New Delhi",
    "indonesia": "Jakarta",
    "iran": "Tehran",
    "iraq": "Baghdad",
    "ireland": "Dublin",
    "israel": "Jerusalem",
    "italy": "Rome",
    "japan": "Tokyo",
    "jordan": "Amman",
    "kenya": "Nairobi",
    "malaysia": "Kuala Lumpur",
    "mexico": "Mexico City",
    "morocco": "Rabat",
    "netherlands": "Amsterdam",
    "new zealand": "Wellington",
    "nigeria": "Abuja",
    "north korea": "Pyongyang",
    "norway": "Oslo",
    "pakistan": "Islamabad",
    "peru": "Lima",
    "philippines": "Manila",
    "poland": "Warsaw",
    "portugal": "Lisbon",
    "romania": "Bucharest",
    "russia": "Moscow",
    "saudi arabia": "Riyadh",
    "south africa": "Pretoria",
    "south korea": "Seoul",
    "spain": "Madrid",
    "sweden": "Stockholm",
    "switzerland": "Bern",
    "syria": "Damascus",
    "thailand": "Bangkok",
    "turkey": "Ankara",
    "ukraine": "Kyiv",
    "united arab emirates": "Abu Dhabi",
    "united kingdom": "London",
    "united states": "Washington, D.C.",
    "usa": "Washington, D.C.",
    "uk": "London",
    "venezuela": "Caracas",
    "vietnam": "Hanoi",
    "zimbabwe": "Harare",
}


def lookup_capital(query: str) -> Optional[str]:
    """
    Return the capital city of the country mentioned in *query*, or None.

    Args:
        query: User query string.

    Returns:
        Formatted answer string or None.
    """
    q = query.lower()
    for country, capital in CAPITALS.items():
        if country in q:
            return f"The capital of {country.title()} is {capital}."
    return None


# ── Periodic Table ────────────────────────────────────────────────────────────

ELEMENTS: dict[str, dict] = {
    "hydrogen":   {"symbol": "H",  "number": 1,   "mass": 1.008},
    "helium":     {"symbol": "He", "number": 2,   "mass": 4.003},
    "lithium":    {"symbol": "Li", "number": 3,   "mass": 6.941},
    "carbon":     {"symbol": "C",  "number": 6,   "mass": 12.011},
    "nitrogen":   {"symbol": "N",  "number": 7,   "mass": 14.007},
    "oxygen":     {"symbol": "O",  "number": 8,   "mass": 15.999},
    "fluorine":   {"symbol": "F",  "number": 9,   "mass": 18.998},
    "neon":       {"symbol": "Ne", "number": 10,  "mass": 20.180},
    "sodium":     {"symbol": "Na", "number": 11,  "mass": 22.990},
    "magnesium":  {"symbol": "Mg", "number": 12,  "mass": 24.305},
    "aluminium":  {"symbol": "Al", "number": 13,  "mass": 26.982},
    "silicon":    {"symbol": "Si", "number": 14,  "mass": 28.086},
    "phosphorus": {"symbol": "P",  "number": 15,  "mass": 30.974},
    "sulfur":     {"symbol": "S",  "number": 16,  "mass": 32.06},
    "chlorine":   {"symbol": "Cl", "number": 17,  "mass": 35.45},
    "argon":      {"symbol": "Ar", "number": 18,  "mass": 39.948},
    "potassium":  {"symbol": "K",  "number": 19,  "mass": 39.098},
    "calcium":    {"symbol": "Ca", "number": 20,  "mass": 40.078},
    "iron":       {"symbol": "Fe", "number": 26,  "mass": 55.845},
    "copper":     {"symbol": "Cu", "number": 29,  "mass": 63.546},
    "zinc":       {"symbol": "Zn", "number": 30,  "mass": 65.38},
    "silver":     {"symbol": "Ag", "number": 47,  "mass": 107.868},
    "gold":       {"symbol": "Au", "number": 79,  "mass": 196.967},
    "mercury":    {"symbol": "Hg", "number": 80,  "mass": 200.592},
    "lead":       {"symbol": "Pb", "number": 82,  "mass": 207.2},
    "uranium":    {"symbol": "U",  "number": 92,  "mass": 238.029},
}

# Symbol → name reverse map
_SYMBOL_TO_ELEMENT = {v["symbol"].lower(): k for k, v in ELEMENTS.items()}


def lookup_element(query: str) -> Optional[str]:
    """
    Return element info if a known element name or symbol appears in *query*.

    Args:
        query: User query string.

    Returns:
        Formatted answer string or None.
    """
    tokens = set(re.findall(r"[a-z]+", query.lower()))

    for token in tokens:
        # Check by full name
        if token in ELEMENTS:
            el = ELEMENTS[token]
            return (
                f"Element: {token.capitalize()} ({el['symbol']})\n"
                f"  Atomic number : {el['number']}\n"
                f"  Atomic mass   : {el['mass']} u"
            )
        # Check by symbol
        if token in _SYMBOL_TO_ELEMENT:
            name = _SYMBOL_TO_ELEMENT[token]
            el = ELEMENTS[name]
            return (
                f"Element: {name.capitalize()} ({el['symbol']})\n"
                f"  Atomic number : {el['number']}\n"
                f"  Atomic mass   : {el['mass']} u"
            )
    return None


# ── Unit Conversions ──────────────────────────────────────────────────────────

# Conversion rules: { "from_to": factor }
_CONVERSIONS: dict[str, tuple[float, str]] = {
    # Length
    "km_miles":      (0.621371, "miles"),
    "miles_km":      (1.60934,  "km"),
    "m_ft":          (3.28084,  "ft"),
    "ft_m":          (0.3048,   "m"),
    "cm_inches":     (0.393701, "inches"),
    "inches_cm":     (2.54,     "cm"),
    # Mass
    "kg_lbs":        (2.20462,  "lbs"),
    "lbs_kg":        (0.453592, "kg"),
    "g_oz":          (0.035274, "oz"),
    "oz_g":          (28.3495,  "g"),
    # Temperature handled separately
}


def lookup_conversion(query: str) -> Optional[str]:
    """
    Detect and evaluate simple unit conversion requests in *query*.

    Supports patterns like "10 km in miles", "convert 5 kg to lbs",
    "72 fahrenheit in celsius".

    Args:
        query: User query string.

    Returns:
        Formatted conversion result or None.
    """
    q = query.lower()

    # Temperature conversions
    temp_match = re.search(
        r"(-?\d+(?:\.\d+)?)\s*°?\s*(celsius|fahrenheit|kelvin|c|f|k)"
        r"(?:\s+(?:in|to|into))?\s+(celsius|fahrenheit|kelvin|c|f|k)",
        q,
    )
    if temp_match:
        value = float(temp_match.group(1))
        from_unit = temp_match.group(2)[0]
        to_unit = temp_match.group(3)[0]
        result = _convert_temp(value, from_unit, to_unit)
        if result is not None:
            return f"{value} {_temp_name(from_unit)} = {result:.2f} {_temp_name(to_unit)}"

    # General conversions
    num_match = re.search(r"(-?\d+(?:\.\d+)?)", q)
    if not num_match:
        return None
    value = float(num_match.group(1))

    for key, (factor, to_label) in _CONVERSIONS.items():
        from_unit, to_unit = key.split("_")
        if from_unit in q and to_unit in q:
            result = value * factor
            return f"{value} {from_unit} = {result:.4f} {to_label}"

    return None


def _convert_temp(value: float, from_unit: str, to_unit: str) -> Optional[float]:
    """Convert temperature between C, F, K."""
    if from_unit == to_unit:
        return value
    # To Celsius first
    if from_unit == "f":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "k":
        celsius = value - 273.15
    else:
        celsius = value
    # From Celsius to target
    if to_unit == "f":
        return celsius * 9 / 5 + 32
    elif to_unit == "k":
        return celsius + 273.15
    else:
        return celsius


def _temp_name(abbr: str) -> str:
    return {"c": "Celsius", "f": "Fahrenheit", "k": "Kelvin"}.get(abbr, abbr)


# ── Math Evaluator ────────────────────────────────────────────────────────────

_SAFE_NAMES: dict[str, object] = {
    "abs": abs, "round": round, "max": max, "min": min,
    "pow": pow, "sum": sum,
}


def evaluate_math(query: str) -> Optional[str]:
    """
    Attempt to evaluate a mathematical expression found in *query*.

    Uses Python's eval() with a restricted namespace — no builtins, no
    imports.  Only processes queries that contain digits and arithmetic
    operators to avoid misfire.

    Args:
        query: User query string.

    Returns:
        Formatted result string or None.
    """
    # Extract a likely expression.  Strip leading question words.
    expr_match = re.search(
        r"(?:what(?:'s| is)?|calculate|compute|eval(?:uate)?|solve)?\s*"
        r"([-+]?\d[\d\s\+\-\*\/\.\(\)\^%]*)",
        query.lower(),
    )
    if not expr_match:
        return None

    raw = expr_match.group(1).strip()
    # Replace ^ with ** for exponentiation
    raw = raw.replace("^", "**")

    if not re.search(r"[\+\-\*\/\^]", raw):
        return None  # No operator — not a math expression

    try:
        result = eval(raw, {"__builtins__": {}}, _SAFE_NAMES)  # noqa: S307
        if isinstance(result, float) and result == int(result):
            result = int(result)
        return f"{raw} = {result}"
    except Exception:
        return None
