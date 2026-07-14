---
name: grade5-literary-item-writer
description: Write and review text-dependent four-option literary reading questions for strong Grade 5 multilingual learners. Use after a standards-aligned blueprint exists to draft stems, plausible distractors, answers, evidence quotes, rationales, and quality-control records.
---

# Grade 5 Literary Item Writer

Read [references/item-spec.md](references/item-spec.md) and [references/output-schema.md](references/output-schema.md) completely before drafting.

## Workflow

1. Write the correct answer directly from the planned evidence and reasoning.
2. Write a concise stem that asks only one question and does not reveal the answer.
3. Write three same-category distractors based on plausible local misunderstandings.
4. Verify every distractor is contradicted by, unsupported by, or less complete than the chapter.
5. Shuffle answer positions across a chapter; do not follow a visible pattern.
6. Add an exact evidence quote and a one-sentence rationale for the answer.
7. Run the quality checklist and output valid JSON only.

## Review gate

Reject or rewrite an item when:

- it can be answered without reading the chapter;
- two options are defensible;
- the correct option is conspicuously longer or more specific;
- the stem uses `NOT`, `EXCEPT`, trick wording, or avoidable double negatives;
- distractors come from unrelated chapters;
- the vocabulary clue is absent from local context;
- the inference rests on one weak clue or outside knowledge;
- the standard label does not match the actual mental action.
