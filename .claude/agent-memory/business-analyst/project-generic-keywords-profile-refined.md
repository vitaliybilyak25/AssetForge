---
name: Generic keywords profile refined (issue #31)
description: Issue #31 refined 2026-09-28 — general/keywords Content Profile, 12 ACs, open question on profile category path, ready label + board Status Ready
type: project
---

Issue #31 (Define generic keyword generation profile) was a 4-line skeleton. Refined 2026-09-28 into a full story.

**Why:** MVP3 needs a reusable, channel-agnostic keyword profile as the first general-purpose profile to establish patterns for the `general/` category.

**Key decisions made during refinement:**
- Profile path proposed as `general/keywords` — PO decision outstanding on whether to use a new `general/` category or map into an existing canonical category (e.g., `stock/generic-keywords`)
- min_count: 20, max_count: 50 (no channel ceiling)
- Deduplication: exact duplicates removed; singular/plural near-duplicates reduced to one; prefer plural when depicted count ≥ 2
- Phrase rule: 2–3 words allowed; 4+ words forbidden
- Filler terms: photo, image, picture, photograph, stock, file, asset, jpeg, png
- Logo marks (`text.logo_marks_detected`) excluded; generic object brand names are NOT suppressed (distinction from adobe-stock profile)
- Quality signal handling: per-value category omission table; fallback to human review when reduced set cannot meet 20-keyword minimum
- 12 ACs covering: dimensions, count range, ordering, format, phrases, deduplication, fillers, CAR mapping, quality signals, file location, examples, validation rules
- Comparison table with adobe-stock profile included

**How to apply:** When implementing story #31, confirm the `general/` vs canonical category decision with PO before creating the profile file. All other spec is fully defined.
