# Required JSON output

Return one JSON object per assigned chapter:

```json
{
  "book": 1,
  "chapter": 1,
  "chapter_title": "Into the Woods",
  "questions": [
    {
      "number": 1,
      "standard": "RL.5.1",
      "skill": "Explicit comprehension",
      "dok": 1,
      "stem": "Question text",
      "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "answer": "A",
      "evidence": ["Exact quotation from the assigned chapter."],
      "rationale": "One concise sentence explaining why the answer follows."
    }
  ]
}
```

## Structural requirements

- Exactly five questions numbered 1-5.
- Q1-Q5 follow the blueprint slot order.
- `evidence` is an array; inference items contain at least two quotations.
- `answer` matches an existing option key.
- No Markdown fences or commentary around the JSON.
