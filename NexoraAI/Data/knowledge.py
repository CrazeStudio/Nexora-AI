"""
knowledge.py — NexoraAI built-in knowledge base.

Organised by topic. Each entry maps a set of keywords to a detailed answer.
The search() function scores every entry against a query and returns the
best match above the configured relevance threshold.
"""

from __future__ import annotations

import re
from typing import Optional

from config import MIN_RELEVANCE_SCORE

# ── Knowledge base ────────────────────────────────────────────────────────────
# Structure: { topic_key: { "keywords": [...], "answer": "..." } }
KNOWLEDGE_BASE: dict[str, dict] = {

    # ── Science ──────────────────────────────────────────────────────────────
    "photosynthesis": {
        "keywords": ["photosynthesis", "plants", "sunlight", "chlorophyll",
                     "oxygen", "carbon dioxide", "glucose", "leaves"],
        "answer": (
            "Photosynthesis is the process by which green plants, algae, and "
            "some bacteria convert sunlight, water, and carbon dioxide into "
            "glucose and oxygen.\n\n"
            "  Equation: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n\n"
            "It takes place in the chloroplasts, using chlorophyll to absorb "
            "light energy. Photosynthesis is the foundation of almost all food "
            "chains on Earth."
        ),
    },
    "gravity": {
        "keywords": ["gravity", "gravitational", "newton", "mass", "weight",
                     "acceleration", "free fall", "9.8", "attraction"],
        "answer": (
            "Gravity is the fundamental force of attraction between objects "
            "with mass. Key facts:\n\n"
            "• Newton's law: F = G·m₁·m₂ / r²\n"
            "• Earth's surface gravity ≈ 9.8 m/s²\n"
            "• Einstein's general relativity describes gravity as the "
            "curvature of spacetime caused by mass.\n"
            "• Gravity keeps planets in orbit, holds atmospheres in place, "
            "and governs the large-scale structure of the universe."
        ),
    },
    "dna": {
        "keywords": ["dna", "genetics", "gene", "chromosome", "nucleotide",
                     "adenine", "thymine", "guanine", "cytosine", "rna",
                     "double helix", "watson", "crick"],
        "answer": (
            "DNA (Deoxyribonucleic Acid) is the molecule that carries genetic "
            "information in all living organisms.\n\n"
            "• Structure: double helix of two strands of nucleotides.\n"
            "• Base pairs: Adenine–Thymine (A-T) and Guanine–Cytosine (G-C).\n"
            "• Genes are segments of DNA that encode proteins.\n"
            "• Humans have ~3 billion base pairs across 23 chromosome pairs.\n"
            "• Discovered by Watson and Crick in 1953 using X-ray data from "
            "Rosalind Franklin."
        ),
    },
    "black_hole": {
        "keywords": ["black hole", "singularity", "event horizon",
                     "hawking", "spacetime", "light", "escape velocity"],
        "answer": (
            "A black hole is a region of spacetime where gravity is so strong "
            "that nothing — not even light — can escape once it crosses the "
            "event horizon.\n\n"
            "• Formed by the gravitational collapse of massive stars.\n"
            "• The boundary of no return is called the event horizon.\n"
            "• At the centre lies a singularity — a point of infinite density.\n"
            "• Stephen Hawking predicted black holes slowly emit radiation "
            "(Hawking Radiation) and eventually evaporate.\n"
            "• The first image of a black hole (M87*) was captured in 2019."
        ),
    },
    "evolution": {
        "keywords": ["evolution", "darwin", "natural selection", "species",
                     "adaptation", "mutation", "survival", "ancestor",
                     "charles darwin", "origin of species"],
        "answer": (
            "Evolution is the process by which populations of organisms change "
            "over successive generations through mechanisms including:\n\n"
            "• Natural selection — traits that improve survival/reproduction "
            "become more common.\n"
            "• Mutation — random changes in DNA create variation.\n"
            "• Genetic drift — random changes in allele frequency.\n"
            "• Gene flow — movement of genes between populations.\n\n"
            "Charles Darwin published 'On the Origin of Species' in 1859, "
            "laying the scientific foundation for evolutionary theory."
        ),
    },
    "atom": {
        "keywords": ["atom", "proton", "neutron", "electron", "nucleus",
                     "atomic", "element", "bohr", "quantum"],
        "answer": (
            "An atom is the basic unit of a chemical element.\n\n"
            "• Nucleus: contains protons (positive charge) and neutrons "
            "(no charge).\n"
            "• Electrons: negatively charged particles orbiting the nucleus "
            "in shells/orbitals.\n"
            "• Atomic number = number of protons (defines the element).\n"
            "• Mass number = protons + neutrons.\n"
            "• Atoms are ~99.9999999% empty space.\n"
            "• Quantum mechanics describes electrons as probability clouds, "
            "not fixed orbits."
        ),
    },
    "speed_of_light": {
        "keywords": ["speed of light", "light speed", "299", "c constant",
                     "electromagnetic", "vacuum"],
        "answer": (
            "The speed of light in a vacuum is exactly 299,792,458 m/s "
            "(≈ 3 × 10⁸ m/s), denoted by the symbol 'c'.\n\n"
            "• It is the ultimate speed limit in the universe (special "
            "relativity).\n"
            "• Light takes ~8 minutes 20 seconds to travel from the Sun "
            "to Earth.\n"
            "• One light-year ≈ 9.46 trillion kilometres.\n"
            "• E = mc² shows mass and energy are related through c."
        ),
    },
    "climate_change": {
        "keywords": ["climate change", "global warming", "greenhouse gas",
                     "co2", "carbon dioxide", "fossil fuel", "temperature",
                     "ice cap", "sea level", "emissions"],
        "answer": (
            "Climate change refers to long-term shifts in global temperatures "
            "and weather patterns, primarily driven since the 20th century by "
            "human activities.\n\n"
            "• Main cause: burning fossil fuels releases CO₂ and other "
            "greenhouse gases.\n"
            "• Greenhouse effect: gases trap heat in Earth's atmosphere.\n"
            "• Effects: rising seas, extreme weather, melting ice, species "
            "loss, droughts.\n"
            "• The Paris Agreement (2015) targets limiting warming to 1.5–2 °C "
            "above pre-industrial levels."
        ),
    },

    # ── Mathematics ──────────────────────────────────────────────────────────
    "pythagorean_theorem": {
        "keywords": ["pythagorean", "pythagoras", "right triangle",
                     "hypotenuse", "a squared", "b squared", "c squared"],
        "answer": (
            "The Pythagorean theorem states that in a right-angled triangle:\n\n"
            "  a² + b² = c²\n\n"
            "where c is the hypotenuse (longest side) and a, b are the other "
            "two sides.\n\n"
            "Example: if a = 3, b = 4 → c² = 9 + 16 = 25 → c = 5.\n"
            "This (3-4-5) is called a Pythagorean triple.\n\n"
            "Named after the ancient Greek mathematician Pythagoras (~570–495 BC)."
        ),
    },
    "pi": {
        "keywords": ["pi", "3.14", "circle", "circumference", "radius",
                     "diameter", "area circle", "π"],
        "answer": (
            "Pi (π) is the ratio of a circle's circumference to its diameter.\n\n"
            "• π ≈ 3.14159265358979…  (an irrational, transcendental number)\n"
            "• Circumference = 2πr\n"
            "• Area of circle = πr²\n"
            "• Volume of sphere = (4/3)πr³\n\n"
            "π appears throughout mathematics, physics, and engineering. "
            "It has been calculated to over 100 trillion decimal places."
        ),
    },
    "fibonacci": {
        "keywords": ["fibonacci", "fibonacci sequence", "golden ratio",
                     "fib", "1 1 2 3 5 8"],
        "answer": (
            "The Fibonacci sequence is a series where each number is the sum "
            "of the two preceding ones:\n\n"
            "  0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, …\n\n"
            "• Rule: F(n) = F(n-1) + F(n-2), with F(0)=0, F(1)=1.\n"
            "• The ratio of consecutive terms approaches the Golden Ratio "
            "φ ≈ 1.6180339…\n"
            "• Fibonacci patterns appear in nature: flower petals, pinecones, "
            "shells, and galaxies."
        ),
    },
    "prime_numbers": {
        "keywords": ["prime", "prime number", "divisible", "factor",
                     "sieve", "eratosthenes"],
        "answer": (
            "A prime number is a natural number greater than 1 that has no "
            "positive divisors other than 1 and itself.\n\n"
            "• First primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29…\n"
            "• 2 is the only even prime.\n"
            "• There are infinitely many primes (proved by Euclid).\n"
            "• The Sieve of Eratosthenes is an efficient algorithm to find "
            "all primes up to a given limit.\n"
            "• Primes are fundamental to modern cryptography (RSA encryption)."
        ),
    },

    # ── Technology & Computing ────────────────────────────────────────────────
    "artificial_intelligence": {
        "keywords": ["artificial intelligence", "ai", "machine learning",
                     "deep learning", "neural network", "algorithm",
                     "model", "training", "inference"],
        "answer": (
            "Artificial Intelligence (AI) is the simulation of human "
            "intelligence processes by computer systems.\n\n"
            "• Machine Learning: systems that learn from data.\n"
            "• Deep Learning: ML using multi-layer neural networks.\n"
            "• Natural Language Processing (NLP): understanding human language.\n"
            "• Computer Vision: interpreting images and video.\n"
            "• Reinforcement Learning: learning through reward signals.\n\n"
            "Key milestones: IBM Deep Blue (chess, 1997), AlphaGo (2016), "
            "GPT series (2018–), and image-generation models (2022+)."
        ),
    },
    "internet": {
        "keywords": ["internet", "world wide web", "www", "tcp", "ip",
                     "http", "https", "protocol", "network", "arpanet"],
        "answer": (
            "The Internet is a global network of interconnected computers "
            "communicating via standardised protocols.\n\n"
            "• Originated from ARPANET (1969, US military research).\n"
            "• TCP/IP: the core communication protocol suite.\n"
            "• The World Wide Web (invented by Tim Berners-Lee, 1989) runs "
            "on top of the internet using HTTP/HTTPS.\n"
            "• DNS translates domain names (e.g. google.com) to IP addresses.\n"
            "• Today ~5.3 billion people use the internet."
        ),
    },
    "python_language": {
        "keywords": ["python", "programming language", "guido van rossum",
                     "interpreted", "pep 8", "indentation", "pip"],
        "answer": (
            "Python is a high-level, interpreted, general-purpose programming "
            "language created by Guido van Rossum (first released 1991).\n\n"
            "• Philosophy: readability counts — uses indentation for blocks.\n"
            "• Dynamically typed, garbage-collected.\n"
            "• Huge ecosystem: NumPy, Pandas, Django, Flask, TensorFlow…\n"
            "• Use cases: web development, data science, AI/ML, scripting, "
            "automation, scientific computing.\n"
            "• Package manager: pip.  Style guide: PEP 8."
        ),
    },
    "blockchain": {
        "keywords": ["blockchain", "bitcoin", "cryptocurrency", "ledger",
                     "decentralised", "hash", "mining", "satoshi"],
        "answer": (
            "A blockchain is a distributed ledger of records (blocks) linked "
            "cryptographically in a chain.\n\n"
            "• Decentralised: no single point of control.\n"
            "• Immutable: altering one block invalidates all subsequent blocks.\n"
            "• Consensus mechanisms: Proof of Work (PoW), Proof of Stake (PoS).\n"
            "• Bitcoin (2009, Satoshi Nakamoto) was the first major blockchain.\n"
            "• Ethereum introduced smart contracts — self-executing code on "
            "the blockchain.\n"
            "• Uses: cryptocurrency, supply chain, voting, NFTs, DeFi."
        ),
    },
    "operating_system": {
        "keywords": ["operating system", "os", "kernel", "linux", "windows",
                     "macos", "process", "memory management", "scheduler"],
        "answer": (
            "An Operating System (OS) is software that manages hardware "
            "resources and provides services for application programs.\n\n"
            "• Kernel: core component managing CPU, memory, devices.\n"
            "• Major OSes: Windows, macOS, Linux, Android, iOS.\n"
            "• Key functions: process management, memory management, file "
            "systems, device drivers, security.\n"
            "• Linux is the dominant OS for servers, supercomputers, and "
            "Android devices."
        ),
    },

    # ── History ───────────────────────────────────────────────────────────────
    "world_war_2": {
        "keywords": ["world war 2", "ww2", "second world war", "wwii",
                     "hitler", "nazi", "holocaust", "allied", "axis",
                     "hiroshima", "d-day"],
        "answer": (
            "World War II (1939–1945) was a global conflict involving most of "
            "the world's nations, forming two opposing alliances:\n\n"
            "• Allies: USA, UK, USSR, France, China, and others.\n"
            "• Axis: Nazi Germany, Italy, Japan.\n"
            "• Began: Germany invaded Poland (1 Sep 1939).\n"
            "• Holocaust: systematic genocide of ~6 million Jews and millions "
            "of others by Nazi Germany.\n"
            "• D-Day (6 Jun 1944): Allied invasion of Normandy.\n"
            "• Ended: Germany surrendered May 1945; Japan surrendered after "
            "atomic bombs on Hiroshima and Nagasaki (Aug 1945).\n"
            "• Death toll: ~70–85 million, making it the deadliest conflict "
            "in history."
        ),
    },
    "french_revolution": {
        "keywords": ["french revolution", "france", "revolution", "1789",
                     "louis xvi", "bastille", "liberty", "napoleon",
                     "guillotine", "republic"],
        "answer": (
            "The French Revolution (1789–1799) was a period of radical "
            "political and societal transformation in France.\n\n"
            "• Causes: financial crisis, inequality, Enlightenment ideas.\n"
            "• Key event: Storming of the Bastille (14 July 1789).\n"
            "• King Louis XVI and Marie Antoinette were executed by guillotine.\n"
            "• Resulted in the end of absolute monarchy and rise of the "
            "First French Republic.\n"
            "• The Reign of Terror (1793–94) saw mass executions of perceived "
            "enemies.\n"
            "• Napoleon Bonaparte rose to power, becoming Emperor in 1804."
        ),
    },
    "moon_landing": {
        "keywords": ["moon landing", "apollo", "neil armstrong", "nasa",
                     "apollo 11", "buzz aldrin", "1969", "lunar"],
        "answer": (
            "Apollo 11 was the first crewed mission to land on the Moon.\n\n"
            "• Date: 20 July 1969.\n"
            "• Crew: Neil Armstrong (Commander), Buzz Aldrin (Lunar Module "
            "Pilot), Michael Collins (Command Module Pilot).\n"
            "• Neil Armstrong became the first human to walk on the Moon, "
            "saying: 'That's one small step for man, one giant leap for "
            "mankind.'\n"
            "• Part of NASA's Apollo programme, motivated by the Space Race "
            "with the Soviet Union.\n"
            "• Six Apollo missions landed on the Moon between 1969 and 1972."
        ),
    },

    # ── Geography ─────────────────────────────────────────────────────────────
    "largest_countries": {
        "keywords": ["largest country", "biggest country", "area", "land area",
                     "square kilometres", "russia", "canada"],
        "answer": (
            "The 10 largest countries by land area:\n\n"
            "1.  Russia       — 17,098,242 km²\n"
            "2.  Canada       — 9,984,670 km²\n"
            "3.  United States— 9,833,517 km²\n"
            "4.  China        — 9,596,960 km²\n"
            "5.  Brazil       — 8,515,767 km²\n"
            "6.  Australia    — 7,692,024 km²\n"
            "7.  India        — 3,287,263 km²\n"
            "8.  Argentina    — 2,780,400 km²\n"
            "9.  Kazakhstan   — 2,724,900 km²\n"
            "10. Algeria      — 2,381,741 km²"
        ),
    },
    "highest_mountains": {
        "keywords": ["highest mountain", "tallest mountain", "everest",
                     "k2", "himalayas", "summit", "altitude", "metres"],
        "answer": (
            "The 5 highest mountains on Earth:\n\n"
            "1. Mount Everest   — 8,848.86 m (Nepal/Tibet)\n"
            "2. K2              — 8,611 m (Pakistan/China)\n"
            "3. Kangchenjunga   — 8,586 m (Nepal/India)\n"
            "4. Lhotse          — 8,516 m (Nepal/Tibet)\n"
            "5. Makalu          — 8,485 m (Nepal/Tibet)\n\n"
            "All top 14 'eight-thousanders' are in the Himalayas or "
            "Karakoram range. Everest was first summited by Edmund Hillary "
            "and Tenzing Norgay on 29 May 1953."
        ),
    },
    "oceans": {
        "keywords": ["ocean", "sea", "pacific", "atlantic", "indian",
                     "arctic", "southern", "deepest", "mariana"],
        "answer": (
            "Earth's five oceans:\n\n"
            "1. Pacific Ocean   — largest (165 million km²)\n"
            "2. Atlantic Ocean  — 106 million km²\n"
            "3. Indian Ocean    — 70 million km²\n"
            "4. Southern Ocean  — surrounds Antarctica\n"
            "5. Arctic Ocean    — smallest, mostly frozen\n\n"
            "Deepest point: Mariana Trench (Pacific), ~11,034 m below sea "
            "level. Oceans cover ~71% of Earth's surface and hold 97% of "
            "Earth's water."
        ),
    },

    # ── Space ─────────────────────────────────────────────────────────────────
    "solar_system": {
        "keywords": ["solar system", "planet", "sun", "mercury", "venus",
                     "earth", "mars", "jupiter", "saturn", "uranus",
                     "neptune", "orbit"],
        "answer": (
            "Our solar system consists of the Sun and everything bound to it "
            "by gravity:\n\n"
            "Planets (in order from the Sun):\n"
            "1. Mercury — smallest, closest to Sun\n"
            "2. Venus   — hottest (462 °C average)\n"
            "3. Earth   — only known planet with life\n"
            "4. Mars    — the Red Planet\n"
            "5. Jupiter — largest planet\n"
            "6. Saturn  — famous ring system\n"
            "7. Uranus  — rotates on its side\n"
            "8. Neptune — farthest, strongest winds\n\n"
            "Also contains: dwarf planets, asteroid belt, Kuiper belt, "
            "Oort cloud, and hundreds of moons."
        ),
    },
    "big_bang": {
        "keywords": ["big bang", "universe origin", "universe created",
                     "cosmology", "13.8 billion", "expansion", "inflation"],
        "answer": (
            "The Big Bang theory describes the origin and evolution of the "
            "universe.\n\n"
            "• ~13.8 billion years ago, the universe began as an "
            "extraordinarily hot, dense singularity.\n"
            "• It rapidly expanded (inflation) and cooled over time.\n"
            "• First atoms formed ~380,000 years after the Big Bang.\n"
            "• First stars appeared ~200 million years later.\n"
            "• Evidence: cosmic microwave background radiation, expansion "
            "of the universe (Hubble's law), abundance of light elements.\n"
            "• The universe continues to expand — and the expansion is "
            "accelerating due to dark energy."
        ),
    },

    # ── Health & Biology ─────────────────────────────────────────────────────
    "human_body": {
        "keywords": ["human body", "organ", "heart", "brain", "lung",
                     "blood", "bones", "cells", "anatomy"],
        "answer": (
            "Key facts about the human body:\n\n"
            "• 37 trillion cells make up the human body.\n"
            "• 206 bones in the adult skeleton.\n"
            "• The heart beats ~100,000 times per day, pumping ~7,500 litres "
            "of blood.\n"
            "• The brain has ~86 billion neurons.\n"
            "• Lungs contain ~300 million alveoli for gas exchange.\n"
            "• The liver performs over 500 functions.\n"
            "• Skin is the largest organ (~2 m²).\n"
            "• DNA in one cell, uncoiled, would stretch ~2 metres."
        ),
    },
    "covid19": {
        "keywords": ["covid", "covid-19", "coronavirus", "pandemic",
                     "sars-cov-2", "vaccine", "virus"],
        "answer": (
            "COVID-19 is an infectious disease caused by the SARS-CoV-2 "
            "coronavirus, first identified in Wuhan, China in late 2019.\n\n"
            "• Declared a pandemic by WHO on 11 March 2020.\n"
            "• Spreads primarily through respiratory droplets.\n"
            "• Symptoms: fever, cough, fatigue, loss of taste/smell.\n"
            "• Vaccines developed in record time (< 1 year) using mRNA "
            "technology (Pfizer-BioNTech, Moderna) and viral vector "
            "technology (AstraZeneca, Johnson & Johnson).\n"
            "• Resulted in >7 million confirmed deaths worldwide."
        ),
    },

    # ── Philosophy & Society ─────────────────────────────────────────────────
    "democracy": {
        "keywords": ["democracy", "democratic", "vote", "election",
                     "government", "representation", "parliament",
                     "republic", "athens", "ancient greece"],
        "answer": (
            "Democracy is a system of government where citizens exercise "
            "power by voting.\n\n"
            "• Direct democracy: citizens vote on legislation directly "
            "(ancient Athens).\n"
            "• Representative democracy: elected representatives vote on "
            "behalf of citizens (most modern states).\n"
            "• Core principles: free elections, rule of law, civil liberties, "
            "separation of powers.\n"
            "• ~57% of the world's countries are classified as democracies "
            "(2023 Democracy Index)."
        ),
    },

    # ── Language & Literature ────────────────────────────────────────────────
    "shakespeare": {
        "keywords": ["shakespeare", "william shakespeare", "hamlet",
                     "romeo juliet", "macbeth", "othello", "sonnets",
                     "elizabethan", "bard"],
        "answer": (
            "William Shakespeare (1564–1616) is widely regarded as the "
            "greatest writer in the English language.\n\n"
            "• Born: Stratford-upon-Avon, England.\n"
            "• Wrote 37 plays, 154 sonnets, and several longer poems.\n"
            "• Famous tragedies: Hamlet, Macbeth, Othello, King Lear.\n"
            "• Famous comedies: A Midsummer Night's Dream, Much Ado About "
            "Nothing, Twelfth Night.\n"
            "• Famous histories: Henry V, Richard III.\n"
            "• Coined over 1,700 words still used in English today."
        ),
    },
}


_STOP_WORDS: frozenset[str] = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "what", "who", "where", "when", "how", "why", "which",
    "do", "does", "did", "can", "could", "tell", "me", "about",
    "explain", "describe", "give", "show", "define", "definition",
    "in", "of", "to", "for", "and", "or", "it", "its", "i",
    "my", "your", "some", "any", "all", "just", "more", "please",
})


def _tokenise(text: str) -> list[str]:
    """Return lowercase words from *text*, stripping punctuation."""
    return re.findall(r"[a-z0-9]+", text.lower())


def _query_tokens(text: str) -> set[str]:
    """
    Return significant tokens from a user query.

    Removes stop words and also adds de-pluralised variants (strips trailing
    's') so that 'holes' matches 'hole', 'stars' matches 'star', etc.
    """
    raw = set(_tokenise(text)) - _STOP_WORDS
    expanded: set[str] = set()
    for token in raw:
        expanded.add(token)
        if len(token) > 3 and token.endswith("s"):
            expanded.add(token[:-1])  # simple de-plural
    return expanded


def search(query: str) -> Optional[str]:
    """
    Find the best matching knowledge-base entry for *query*.

    Scores each entry by the fraction of its keywords that appear in the
    query tokens. Returns the answer of the top-scoring entry if its score
    meets MIN_RELEVANCE_SCORE, otherwise returns None.

    Args:
        query: The user's input string.

    Returns:
        A formatted answer string, or None if no good match found.
    """
    tokens = _query_tokens(query)
    if not tokens:
        return None

    best_score = 0.0
    best_key: Optional[str] = None

    for key, entry in KNOWLEDGE_BASE.items():
        keywords = entry["keywords"]
        # Count how many query tokens match any keyword (or keyword part).
        # Scoring against len(tokens) means a single strong keyword hit in a
        # short query (e.g. "what is photosynthesis") ranks highly.
        hits = sum(
            1
            for token in tokens
            if any(token in _tokenise(kw) or token == kw for kw in keywords)
        )
        score = hits / len(tokens) if tokens else 0.0
        if score > best_score:
            best_score = score
            best_key = key

    if best_key and best_score >= MIN_RELEVANCE_SCORE:
        return KNOWLEDGE_BASE[best_key]["answer"]
    return None


def list_topics() -> list[str]:
    """Return a sorted list of all topic keys in the knowledge base."""
    return sorted(KNOWLEDGE_BASE.keys())
