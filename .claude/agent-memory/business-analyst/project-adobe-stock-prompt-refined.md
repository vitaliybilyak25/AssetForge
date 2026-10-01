---
name: Adobe Stock AI prompt story #25 refined
description: Story #25 fully refined 2026-09-28 — 11 ACs covering CAR input, 3-field output, generation rules, brand suppression, editorial handling, version identifier, and evaluation rubric link; ready label applied and board set to Ready
type: project
---

Story #25 ("Design AI prompt for Adobe Stock metadata generation") refined from skeleton to full ready state on 2026-09-28.

**Why:** The skeleton had only 4 bare ACs with no scope, no output format definition, no dependencies, and no evaluation reference. The story is the core Layer 2 story for MVP2 and needed full production-quality AC before developer pickup.

**Key decisions captured in the refined body:**
- Output is exactly Title, Keywords, Category plus Releases as a fixed empty-string constant — no Description, no extra fields
- Brand suppression reads both `text.logo_marks_detected` AND `objects.brand_objects_detected` (not just trademark_flag)
- Editorial handling (risk.editorial_only = true) adapts tone without blocking — routing/blocking belongs to Layer 3 (story #26)
- Category fallback rule deferred to developer (AC5) — must be stated explicitly in the prompt file, not left implicit
- Prompt file path fixed as `prompts/stock/adobe-stock-v{N}.md` (or equivalent extension)
- Version identifier output field maps to `confidence.analysis_model_version`
- AC10 explicitly gates acceptance on story #88 rubric and pass threshold; story #88 must be Ready before #25 moves to In Progress

**State:** ready label applied; board Status set to Ready (Project #3); PO approval checkbox is the only remaining open item.

**How to apply:** When referencing prompt generation rules for Adobe Stock, treat this issue as the authoritative Layer 2 spec. The prompt file, once created, lives at `prompts/stock/adobe-stock-v{N}.md`.
