/**
 * knowledge.ts — NexoraAI built-in knowledge base (TypeScript port).
 */

export interface KnowledgeEntry {
  keywords: string[];
  answer: string;
}

export const KNOWLEDGE_BASE: Record<string, KnowledgeEntry> = {
  photosynthesis: {
    keywords: ["photosynthesis", "plants", "sunlight", "chlorophyll", "oxygen", "carbon dioxide", "glucose", "leaves"],
    answer: "Photosynthesis is the process by which green plants, algae, and some bacteria convert sunlight, water, and carbon dioxide into glucose and oxygen.\n\nEquation: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n\nIt takes place in the chloroplasts, using chlorophyll to absorb light energy. Photosynthesis is the foundation of almost all food chains on Earth.",
  },
  gravity: {
    keywords: ["gravity", "gravitational", "newton", "mass", "weight", "acceleration", "free fall", "9.8", "attraction"],
    answer: "Gravity is the fundamental force of attraction between objects with mass.\n\n• Newton's law: F = G·m₁·m₂ / r²\n• Earth's surface gravity ≈ 9.8 m/s²\n• Einstein's general relativity describes gravity as the curvature of spacetime caused by mass.\n• Gravity keeps planets in orbit, holds atmospheres in place, and governs the large-scale structure of the universe.",
  },
  dna: {
    keywords: ["dna", "genetics", "gene", "chromosome", "nucleotide", "adenine", "thymine", "guanine", "cytosine", "double helix", "watson", "crick"],
    answer: "DNA (Deoxyribonucleic Acid) is the molecule that carries genetic information in all living organisms.\n\n• Structure: double helix of two strands of nucleotides.\n• Base pairs: Adenine–Thymine (A-T) and Guanine–Cytosine (G-C).\n• Genes are segments of DNA that encode proteins.\n• Humans have ~3 billion base pairs across 23 chromosome pairs.\n• Discovered by Watson and Crick in 1953.",
  },
  black_hole: {
    keywords: ["black hole", "singularity", "event horizon", "hawking", "spacetime", "escape velocity"],
    answer: "A black hole is a region of spacetime where gravity is so strong that nothing — not even light — can escape once it crosses the event horizon.\n\n• Formed by the gravitational collapse of massive stars.\n• The boundary of no return is called the event horizon.\n• At the centre lies a singularity — a point of infinite density.\n• Stephen Hawking predicted black holes slowly emit radiation (Hawking Radiation).\n• The first image of a black hole (M87*) was captured in 2019.",
  },
  evolution: {
    keywords: ["evolution", "darwin", "natural selection", "species", "adaptation", "mutation", "survival", "ancestor", "charles darwin", "origin of species"],
    answer: "Evolution is the process by which populations of organisms change over successive generations through mechanisms including:\n\n• Natural selection — traits that improve survival/reproduction become more common.\n• Mutation — random changes in DNA create variation.\n• Genetic drift — random changes in allele frequency.\n• Gene flow — movement of genes between populations.\n\nCharles Darwin published 'On the Origin of Species' in 1859.",
  },
  atom: {
    keywords: ["atom", "proton", "neutron", "electron", "nucleus", "atomic", "element", "bohr", "quantum"],
    answer: "An atom is the basic unit of a chemical element.\n\n• Nucleus: contains protons (positive charge) and neutrons (no charge).\n• Electrons: negatively charged particles orbiting the nucleus in shells/orbitals.\n• Atomic number = number of protons (defines the element).\n• Mass number = protons + neutrons.\n• Atoms are ~99.9999999% empty space.",
  },
  speed_of_light: {
    keywords: ["speed of light", "light speed", "299", "c constant", "electromagnetic", "vacuum"],
    answer: "The speed of light in a vacuum is exactly 299,792,458 m/s (≈ 3 × 10⁸ m/s), denoted by the symbol 'c'.\n\n• It is the ultimate speed limit in the universe (special relativity).\n• Light takes ~8 minutes 20 seconds to travel from the Sun to Earth.\n• One light-year ≈ 9.46 trillion kilometres.\n• E = mc² shows mass and energy are related through c.",
  },
  climate_change: {
    keywords: ["climate change", "global warming", "greenhouse gas", "co2", "carbon dioxide", "fossil fuel", "temperature", "ice cap", "sea level", "emissions"],
    answer: "Climate change refers to long-term shifts in global temperatures and weather patterns, primarily driven since the 20th century by human activities.\n\n• Main cause: burning fossil fuels releases CO₂ and other greenhouse gases.\n• Greenhouse effect: gases trap heat in Earth's atmosphere.\n• Effects: rising seas, extreme weather, melting ice, species loss, droughts.\n• The Paris Agreement (2015) targets limiting warming to 1.5–2 °C above pre-industrial levels.",
  },
  pythagorean_theorem: {
    keywords: ["pythagorean", "pythagoras", "right triangle", "hypotenuse", "a squared", "b squared", "c squared"],
    answer: "The Pythagorean theorem states that in a right-angled triangle:\n\n  a² + b² = c²\n\nwhere c is the hypotenuse (longest side) and a, b are the other two sides.\n\nExample: if a = 3, b = 4 → c² = 9 + 16 = 25 → c = 5. This (3-4-5) is called a Pythagorean triple.\n\nNamed after the ancient Greek mathematician Pythagoras (~570–495 BC).",
  },
  pi: {
    keywords: ["pi", "3.14", "circle", "circumference", "radius", "diameter", "area circle", "π"],
    answer: "Pi (π) is the ratio of a circle's circumference to its diameter.\n\n• π ≈ 3.14159265358979… (an irrational, transcendental number)\n• Circumference = 2πr\n• Area of circle = πr²\n• Volume of sphere = (4/3)πr³\n\nπ appears throughout mathematics, physics, and engineering. It has been calculated to over 100 trillion decimal places.",
  },
  fibonacci: {
    keywords: ["fibonacci", "fibonacci sequence", "golden ratio", "fib"],
    answer: "The Fibonacci sequence is a series where each number is the sum of the two preceding ones:\n\n  0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, …\n\n• Rule: F(n) = F(n-1) + F(n-2), with F(0)=0, F(1)=1.\n• The ratio of consecutive terms approaches the Golden Ratio φ ≈ 1.6180339…\n• Fibonacci patterns appear in nature: flower petals, pinecones, shells, and galaxies.",
  },
  prime_numbers: {
    keywords: ["prime", "prime number", "divisible", "factor", "sieve", "eratosthenes"],
    answer: "A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.\n\n• First primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29…\n• 2 is the only even prime.\n• There are infinitely many primes (proved by Euclid).\n• The Sieve of Eratosthenes is an efficient algorithm to find all primes up to a given limit.\n• Primes are fundamental to modern cryptography (RSA encryption).",
  },
  artificial_intelligence: {
    keywords: ["artificial intelligence", "ai", "machine learning", "deep learning", "neural network", "algorithm", "model", "training", "inference"],
    answer: "Artificial Intelligence (AI) is the simulation of human intelligence processes by computer systems.\n\n• Machine Learning: systems that learn from data.\n• Deep Learning: ML using multi-layer neural networks.\n• Natural Language Processing (NLP): understanding human language.\n• Computer Vision: interpreting images and video.\n• Reinforcement Learning: learning through reward signals.\n\nKey milestones: IBM Deep Blue (chess, 1997), AlphaGo (2016), GPT series (2018–), and image-generation models (2022+).",
  },
  internet: {
    keywords: ["internet", "world wide web", "www", "tcp", "ip", "http", "https", "protocol", "network", "arpanet"],
    answer: "The Internet is a global network of interconnected computers communicating via standardised protocols.\n\n• Originated from ARPANET (1969, US military research).\n• TCP/IP: the core communication protocol suite.\n• The World Wide Web (invented by Tim Berners-Lee, 1989) runs on top of the internet using HTTP/HTTPS.\n• DNS translates domain names to IP addresses.\n• Today ~5.3 billion people use the internet.",
  },
  python_language: {
    keywords: ["python", "programming language", "guido van rossum", "interpreted", "pep 8", "indentation", "pip"],
    answer: "Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum (first released 1991).\n\n• Philosophy: readability counts — uses indentation for blocks.\n• Dynamically typed, garbage-collected.\n• Huge ecosystem: NumPy, Pandas, Django, Flask, TensorFlow…\n• Use cases: web development, data science, AI/ML, scripting, automation, scientific computing.\n• Package manager: pip. Style guide: PEP 8.",
  },
  blockchain: {
    keywords: ["blockchain", "bitcoin", "cryptocurrency", "ledger", "decentralised", "hash", "mining", "satoshi"],
    answer: "A blockchain is a distributed ledger of records (blocks) linked cryptographically in a chain.\n\n• Decentralised: no single point of control.\n• Immutable: altering one block invalidates all subsequent blocks.\n• Consensus mechanisms: Proof of Work (PoW), Proof of Stake (PoS).\n• Bitcoin (2009, Satoshi Nakamoto) was the first major blockchain.\n• Ethereum introduced smart contracts — self-executing code on the blockchain.\n• Uses: cryptocurrency, supply chain, voting, NFTs, DeFi.",
  },
  solar_system: {
    keywords: ["solar system", "planet", "sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "orbit"],
    answer: "Our solar system consists of the Sun and everything bound to it by gravity.\n\nPlanets (in order from the Sun):\n1. Mercury — smallest, closest to Sun\n2. Venus — hottest (462 °C average)\n3. Earth — only known planet with life\n4. Mars — the Red Planet\n5. Jupiter — largest planet\n6. Saturn — famous ring system\n7. Uranus — rotates on its side\n8. Neptune — farthest, strongest winds\n\nAlso contains: dwarf planets, asteroid belt, Kuiper belt, Oort cloud, and hundreds of moons.",
  },
  big_bang: {
    keywords: ["big bang", "universe origin", "universe created", "cosmology", "13.8 billion", "expansion", "inflation"],
    answer: "The Big Bang theory describes the origin and evolution of the universe.\n\n• ~13.8 billion years ago, the universe began as an extraordinarily hot, dense singularity.\n• It rapidly expanded (inflation) and cooled over time.\n• First atoms formed ~380,000 years after the Big Bang.\n• Evidence: cosmic microwave background radiation, expansion of the universe (Hubble's law), abundance of light elements.\n• The universe continues to expand — and the expansion is accelerating due to dark energy.",
  },
  world_war_2: {
    keywords: ["world war 2", "ww2", "second world war", "wwii", "hitler", "nazi", "holocaust", "allied", "axis", "hiroshima", "d-day"],
    answer: "World War II (1939–1945) was a global conflict involving most of the world's nations.\n\n• Allies: USA, UK, USSR, France, China, and others.\n• Axis: Nazi Germany, Italy, Japan.\n• Began: Germany invaded Poland (1 Sep 1939).\n• Holocaust: systematic genocide of ~6 million Jews and millions of others.\n• D-Day (6 Jun 1944): Allied invasion of Normandy.\n• Ended: Germany surrendered May 1945; Japan surrendered August 1945.\n• Death toll: ~70–85 million, making it the deadliest conflict in history.",
  },
  moon_landing: {
    keywords: ["moon landing", "apollo", "neil armstrong", "nasa", "apollo 11", "buzz aldrin", "1969", "lunar"],
    answer: "Apollo 11 was the first crewed mission to land on the Moon.\n\n• Date: 20 July 1969.\n• Crew: Neil Armstrong (Commander), Buzz Aldrin (Lunar Module Pilot), Michael Collins (Command Module Pilot).\n• Neil Armstrong became the first human to walk on the Moon, saying: 'That's one small step for man, one giant leap for mankind.'\n• Part of NASA's Apollo programme during the Space Race.\n• Six Apollo missions landed on the Moon between 1969 and 1972.",
  },
  human_body: {
    keywords: ["human body", "organ", "heart", "brain", "lung", "blood", "bones", "cells", "anatomy"],
    answer: "Key facts about the human body:\n\n• 37 trillion cells make up the human body.\n• 206 bones in the adult skeleton.\n• The heart beats ~100,000 times per day, pumping ~7,500 litres of blood.\n• The brain has ~86 billion neurons.\n• Lungs contain ~300 million alveoli for gas exchange.\n• The liver performs over 500 functions.\n• Skin is the largest organ (~2 m²).\n• DNA in one cell, uncoiled, would stretch ~2 metres.",
  },
};

const STOP_WORDS = new Set([
  "a","an","the","is","are","was","were","be","been","what","who","where",
  "when","how","why","which","do","does","did","can","could","tell","me",
  "about","explain","describe","give","show","define","in","of","to","for",
  "and","or","it","its","i","my","your","some","any","all","just","more","please",
]);

function tokenise(text: string): string[] {
  return text.toLowerCase().match(/[a-z0-9]+/g) ?? [];
}

function queryTokens(text: string): Set<string> {
  const raw = new Set(tokenise(text).filter(t => !STOP_WORDS.has(t)));
  const expanded = new Set<string>(raw);
  for (const token of raw) {
    if (token.length > 3 && token.endsWith("s")) {
      expanded.add(token.slice(0, -1)); // simple de-plural
    }
  }
  return expanded;
}

export function searchKnowledge(query: string): string | null {
  const tokens = queryTokens(query);
  if (tokens.size === 0) return null;

  let bestScore = 0;
  let bestKey: string | null = null;

  for (const [key, entry] of Object.entries(KNOWLEDGE_BASE)) {
    const keywordTokens = entry.keywords.flatMap(kw => tokenise(kw));
    let hits = 0;
    for (const token of tokens) {
      if (keywordTokens.includes(token)) hits++;
    }
    const score = hits / tokens.size;
    if (score > bestScore) {
      bestScore = score;
      bestKey = key;
    }
  }

  const MIN_SCORE = 0.25;
  if (bestKey && bestScore >= MIN_SCORE) {
    return KNOWLEDGE_BASE[bestKey].answer;
  }
  return null;
}

// ── Examples ──────────────────────────────────────────────────────────────────

interface Example { q: string; a: string }

export const EXAMPLES: Example[] = [
  { q: "who invented the telephone", a: "The telephone was invented by Alexander Graham Bell, who received the first patent in 1876." },
  { q: "who invented the light bulb", a: "Thomas Edison is credited with developing the first practical incandescent light bulb in 1879, though earlier inventors made important contributions." },
  { q: "what is the boiling point of water", a: "Water boils at 100 °C (212 °F) at standard atmospheric pressure (1 atm). At higher altitudes it boils at lower temperatures." },
  { q: "what is the freezing point of water", a: "Water freezes at 0 °C (32 °F) at standard atmospheric pressure." },
  { q: "how many continents are there", a: "There are 7 continents: Africa, Antarctica, Asia, Australia (Oceania), Europe, North America, and South America." },
  { q: "how many countries in the world", a: "There are 195 countries in the world — 193 United Nations member states plus Vatican City and Palestine as observer states." },
  { q: "what is the largest ocean", a: "The Pacific Ocean is the largest and deepest ocean, covering about 165 million km² — more than all land combined." },
  { q: "what is the smallest country in the world", a: "Vatican City is the world's smallest country, covering only about 44 hectares (0.44 km²) within Rome, Italy." },
  { q: "how far is the moon from earth", a: "The average distance from Earth to the Moon is about 384,400 km (238,855 miles). It varies because the Moon's orbit is elliptical." },
  { q: "how far is the sun from earth", a: "The average distance from Earth to the Sun is about 149.6 million km (93 million miles), defined as 1 Astronomical Unit (AU)." },
  { q: "how old is the earth", a: "Earth is approximately 4.54 billion years old, based on radiometric dating of meteorites and Earth's oldest rocks." },
  { q: "how old is the universe", a: "The universe is approximately 13.8 billion years old, based on measurements of the cosmic microwave background radiation." },
  { q: "what does html stand for", a: "HTML stands for HyperText Markup Language. It is the standard language for creating web pages." },
  { q: "what does css stand for", a: "CSS stands for Cascading Style Sheets. It is used to style and layout web pages written in HTML." },
  { q: "what is a variable in programming", a: "A variable is a named storage location in memory that holds a value which can be read or modified during program execution." },
  { q: "what is an algorithm", a: "An algorithm is a finite, step-by-step set of instructions designed to solve a problem or accomplish a task." },
  { q: "what is recursion", a: "Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem. Every recursive function needs a base case to stop infinite recursion." },
  { q: "what is the chemical formula for water", a: "The chemical formula for water is H₂O — two hydrogen atoms bonded to one oxygen atom." },
  { q: "what is the chemical formula for salt", a: "Table salt is sodium chloride, with the chemical formula NaCl." },
  { q: "what is the chemical formula for carbon dioxide", a: "Carbon dioxide has the formula CO₂ — one carbon atom and two oxygen atoms." },
  { q: "how many bones in the human body", a: "An adult human body has 206 bones. Babies are born with around 270–300 bones, many of which fuse together during childhood." },
  { q: "how many chambers does the heart have", a: "The human heart has 4 chambers: the right atrium, right ventricle, left atrium, and left ventricle." },
  { q: "when did world war 1 start", a: "World War I started on 28 July 1914 when Austria-Hungary declared war on Serbia, following the assassination of Archduke Franz Ferdinand." },
  { q: "when did world war 2 end", a: "World War II ended in 1945: Germany surrendered on 8 May (V-E Day) and Japan surrendered on 2 September (V-J Day)." },
  { q: "who was the first president of the united states", a: "George Washington was the first President of the United States, serving from 1789 to 1797." },
];

const EXAMPLE_STOP_WORDS = new Set([
  "a","an","the","is","are","was","were","what","who","where","when","how",
  "why","which","do","does","did","in","of","to","for","and","or","it","its","i",
]);

function exampleTokens(text: string): Set<string> {
  return new Set(tokenise(text).filter(t => !EXAMPLE_STOP_WORDS.has(t)));
}

export function matchExample(query: string): string | null {
  const qTokens = exampleTokens(query);
  if (qTokens.size === 0) return null;

  let bestScore = 0;
  let bestAnswer: string | null = null;

  for (const ex of EXAMPLES) {
    const eTokens = exampleTokens(ex.q);
    const union = new Set([...qTokens, ...eTokens]);
    const inter = [...qTokens].filter(t => eTokens.has(t));
    const score = union.size > 0 ? inter.length / union.size : 0;
    if (score > bestScore) {
      bestScore = score;
      bestAnswer = ex.a;
    }
  }

  return bestScore >= 0.45 ? bestAnswer : null;
}

// ── Capitals ──────────────────────────────────────────────────────────────────

export const CAPITALS: Record<string, string> = {
  afghanistan:"Kabul", albania:"Tirana", algeria:"Algiers", argentina:"Buenos Aires",
  australia:"Canberra", austria:"Vienna", bangladesh:"Dhaka", belgium:"Brussels",
  brazil:"Brasília", canada:"Ottawa", chile:"Santiago", china:"Beijing",
  colombia:"Bogotá", cuba:"Havana", czechia:"Prague", denmark:"Copenhagen",
  egypt:"Cairo", ethiopia:"Addis Ababa", finland:"Helsinki", france:"Paris",
  germany:"Berlin", ghana:"Accra", greece:"Athens", hungary:"Budapest",
  india:"New Delhi", indonesia:"Jakarta", iran:"Tehran", iraq:"Baghdad",
  ireland:"Dublin", israel:"Jerusalem", italy:"Rome", japan:"Tokyo",
  jordan:"Amman", kenya:"Nairobi", malaysia:"Kuala Lumpur", mexico:"Mexico City",
  morocco:"Rabat", netherlands:"Amsterdam", "new zealand":"Wellington",
  nigeria:"Abuja", "north korea":"Pyongyang", norway:"Oslo", pakistan:"Islamabad",
  peru:"Lima", philippines:"Manila", poland:"Warsaw", portugal:"Lisbon",
  romania:"Bucharest", russia:"Moscow", "saudi arabia":"Riyadh",
  "south africa":"Pretoria", "south korea":"Seoul", spain:"Madrid",
  sweden:"Stockholm", switzerland:"Bern", syria:"Damascus", thailand:"Bangkok",
  turkey:"Ankara", ukraine:"Kyiv", "united arab emirates":"Abu Dhabi",
  "united kingdom":"London", uk:"London", "united states":"Washington, D.C.",
  usa:"Washington, D.C.", venezuela:"Caracas", vietnam:"Hanoi", zimbabwe:"Harare",
};

export function lookupCapital(query: string): string | null {
  const q = query.toLowerCase();
  for (const [country, capital] of Object.entries(CAPITALS)) {
    if (q.includes(country)) return `The capital of ${country.replace(/\b\w/g, c => c.toUpperCase())} is ${capital}.`;
  }
  return null;
}

// ── Elements ──────────────────────────────────────────────────────────────────

interface Element { symbol: string; number: number; mass: number }

export const ELEMENTS: Record<string, Element> = {
  hydrogen:{symbol:"H",number:1,mass:1.008}, helium:{symbol:"He",number:2,mass:4.003},
  lithium:{symbol:"Li",number:3,mass:6.941}, carbon:{symbol:"C",number:6,mass:12.011},
  nitrogen:{symbol:"N",number:7,mass:14.007}, oxygen:{symbol:"O",number:8,mass:15.999},
  neon:{symbol:"Ne",number:10,mass:20.180}, sodium:{symbol:"Na",number:11,mass:22.990},
  silicon:{symbol:"Si",number:14,mass:28.086}, phosphorus:{symbol:"P",number:15,mass:30.974},
  sulfur:{symbol:"S",number:16,mass:32.06}, chlorine:{symbol:"Cl",number:17,mass:35.45},
  argon:{symbol:"Ar",number:18,mass:39.948}, potassium:{symbol:"K",number:19,mass:39.098},
  calcium:{symbol:"Ca",number:20,mass:40.078}, iron:{symbol:"Fe",number:26,mass:55.845},
  copper:{symbol:"Cu",number:29,mass:63.546}, zinc:{symbol:"Zn",number:30,mass:65.38},
  silver:{symbol:"Ag",number:47,mass:107.868}, gold:{symbol:"Au",number:79,mass:196.967},
  mercury:{symbol:"Hg",number:80,mass:200.592}, lead:{symbol:"Pb",number:82,mass:207.2},
  uranium:{symbol:"U",number:92,mass:238.029},
};

const SYMBOL_TO_ELEMENT = Object.fromEntries(
  Object.entries(ELEMENTS).map(([name, el]) => [el.symbol.toLowerCase(), name])
);

export function lookupElement(query: string): string | null {
  const tokens = (query.toLowerCase().match(/[a-z]+/g) ?? []);
  for (const token of tokens) {
    if (ELEMENTS[token]) {
      const el = ELEMENTS[token];
      return `Element: ${token.charAt(0).toUpperCase() + token.slice(1)} (${el.symbol})\n  Atomic number: ${el.number}\n  Atomic mass: ${el.mass} u`;
    }
    if (SYMBOL_TO_ELEMENT[token]) {
      const name = SYMBOL_TO_ELEMENT[token];
      const el = ELEMENTS[name];
      return `Element: ${name.charAt(0).toUpperCase() + name.slice(1)} (${el.symbol})\n  Atomic number: ${el.number}\n  Atomic mass: ${el.mass} u`;
    }
  }
  return null;
}

// ── Unit Conversion ───────────────────────────────────────────────────────────

export function lookupConversion(query: string): string | null {
  const q = query.toLowerCase();

  // Temperature
  const tempMatch = q.match(/(-?\d+(?:\.\d+)?)\s*°?\s*(celsius|fahrenheit|kelvin|c|f|k)(?:\s+(?:in|to|into))?\s*(celsius|fahrenheit|kelvin|c|f|k)/);
  if (tempMatch) {
    const value = parseFloat(tempMatch[1]);
    const from = tempMatch[2][0];
    const to = tempMatch[3][0];
    const result = convertTemp(value, from, to);
    if (result !== null) {
      const names: Record<string, string> = { c: "Celsius", f: "Fahrenheit", k: "Kelvin" };
      return `${value} ${names[from] ?? from} = ${result.toFixed(2)} ${names[to] ?? to}`;
    }
  }

  // General conversions
  const numMatch = q.match(/(-?\d+(?:\.\d+)?)/);
  if (!numMatch) return null;
  const value = parseFloat(numMatch[1]);

  const conversions: [string, string, number, string][] = [
    ["km", "miles", 0.621371, "miles"],
    ["miles", "km", 1.60934, "km"],
    ["kg", "lbs", 2.20462, "lbs"],
    ["lbs", "kg", 0.453592, "kg"],
    ["m", "ft", 3.28084, "ft"],
    ["ft", "m", 0.3048, "m"],
    ["cm", "inches", 0.393701, "inches"],
    ["inches", "cm", 2.54, "cm"],
  ];

  for (const [from, to, factor, label] of conversions) {
    if (q.includes(from) && q.includes(to)) {
      return `${value} ${from} = ${(value * factor).toFixed(4)} ${label}`;
    }
  }
  return null;
}

function convertTemp(value: number, from: string, to: string): number | null {
  if (from === to) return value;
  let celsius = value;
  if (from === "f") celsius = (value - 32) * 5 / 9;
  else if (from === "k") celsius = value - 273.15;
  if (to === "f") return celsius * 9 / 5 + 32;
  if (to === "k") return celsius + 273.15;
  return celsius;
}

// ── Math Evaluator ────────────────────────────────────────────────────────────

export function evaluateMath(query: string): string | null {
  const q = query.toLowerCase();
  const match = q.match(/(?:what(?:'s| is)?|calculate|compute|evaluate|solve)?\s*([-+]?\d[\d\s+\-*/.()\^%]*)/);
  if (!match) return null;

  let expr = match[1].trim().replace(/\^/g, "**");
  if (!/[+\-*/^]/.test(expr)) return null;

  try {
    // Safe eval: only allow numbers and operators
    if (!/^[\d\s+\-*/.()%**]+$/.test(expr)) return null;
    const result = Function(`"use strict"; return (${expr})`)() as number;
    if (typeof result !== "number" || !isFinite(result)) return null;
    const display = Number.isInteger(result) ? result : parseFloat(result.toFixed(8));
    return `${expr} = ${display}`;
  } catch {
    return null;
  }
}
