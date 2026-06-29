export default function handler(_req: any, res: any) {
  res.status(200).json({
    suggestions: [
      "What is photosynthesis?",
      "Tell me about black holes",
      "What is the capital of Japan?",
      "Calculate 25 * (4 + 6)",
      "10 km in miles",
      "What is the speed of light?",
      "Who invented the telephone?",
      "Element oxygen",
      "100 fahrenheit in celsius",
      "What is artificial intelligence?",
      "Explain the Pythagorean theorem",
      "Search for latest tech news",
    ],
  });
}
