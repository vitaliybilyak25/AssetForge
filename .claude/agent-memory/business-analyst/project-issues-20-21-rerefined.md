---
name: Issues #20 and #21 re-refined with PO decisions and catalogue revisions
description: Issues #20 (Text & Logos) and #21 (Confidence Scores) updated 2026-09-27 with PO decisions; three revisions applied to docs/car-field-catalogue.md
type: project
---

Issues #20 and #21 re-refined on 2026-09-27 after PO decisions. Three revisions applied to `docs/car-field-catalogue.md` first, then both issue bodies and comments updated.

**Why:** PO provided four decisions (two per story) that changed field scope, cardinality, and AC content.

**How to apply:** Use these decisions as settled facts in any downstream story that references the Text and Logos or Confidence Scores categories.

## Catalogue revisions applied (docs/car-field-catalogue.md)

**Revision 1 — Objects and Subjects:** Added two Optional fields after `objects.brand_objects_detected`:
- `objects.foreground_elements` — Array<string>, Optional: primary subjects/objects in the foreground
- `objects.background_elements` — Array<string>, Optional: scene elements/environmental context in the background

**Revision 2 — Text and Logos:** Added one Optional field after `text.dominant_language`:
- `text.bounding_boxes` — Array<object>, Optional: approximate position descriptors (e.g., top-left, centre, bottom-right) for detected text strings and logo marks; not pixel-precise coordinates

**Revision 3 — Confidence Scores:** Changed `confidence.asset_quality_signal` from Conditional to Required. Updated description to include "Value is `none` when no quality issues are detected." Enum values confirmed as: `blur`, `low_resolution`, `poor_exposure`, `noise`, `none`.

No conflicts with `docs/confidence-and-risk-rules.md` — that document covers only the seven category-level `*.confidence_score` fields; `confidence.asset_quality_signal` is not enumerated there.

## Issue #20 — Text, Logos, and Embedded Graphics

PO decisions incorporated:
1. `text.bounding_boxes` added to catalogue and now in scope — AC7 specifies it (Optional, Array<object>, approximate descriptors, example required)
2. `text.logo_marks_detected` may be present when `text.strings_present = false` (symbol-only logo) — documented in AC3 explicitly

Field count increased from 6 to 7. AC count increased from 10 to 11. Ready checklist: 7/8 (awaiting PO approval).

## Issue #21 — Confidence Scores

PO decisions incorporated:
1. `confidence.overall_score` weighting formula: implementation decision for developer — not a PO-gated AC; AC5 updated to record-and-move-on framing
2. `confidence.asset_quality_signal`: Required cardinality confirmed; `none` is a valid and required enum value when no quality issues are detected — AC2 and AC7 updated

AC count: 10. Ready checklist: 7/8 (awaiting PO approval).
