---
name: Story #84 — Confidence thresholds and risk flag handling rules
description: Story #84 complete — docs/confidence-and-risk-rules.md delivered, Epic #1 updated, comment on GH issue #84, awaiting PO approval
type: project
---

Story #84 "Define confidence score thresholds and risk/compliance flag handling rules" deliverable written on 2026-09-27.

**Deliverable:** `docs/confidence-and-risk-rules.md`

**PO-confirmed decisions recorded in the document:**
1. All threshold values set to 0.70 provisional across all 7 categories — each individually marked [PROVISIONAL — confirm at MVP1].
2. Canonical handling policy vocabulary: `suppress output`, `require human review`, `block output entirely`.
3. Multiple-flag interaction: most restrictive policy wins (policy rank: suppress < require human review < block entirely).

**Key rules in the document:**
- `risk.editorial_only` = `true` always triggers Block output entirely for commercial channel profiles; no other flag combination can downgrade this.
- `risk.trademark_flag` default is Suppress output (field-level only) — the only flag that does not halt the Pipeline.
- Below-threshold `risk.confidence_score` never suppresses an active `true` flag (Rule A), but does make an absent flag's non-presence unknown rather than confirmed (Rule B).
- `confidence.low_confidence_categories` must list every failing category; partial population is invalid Handoff 1.
- If `"risk"` is in `confidence.low_confidence_categories`, active risk flags still propagate — low score means detection sensitivity is uncertain, not that flags are silenced.

**GitHub:** Comment posted at https://github.com/vitaliybilyak25/AssetForge/issues/84#issuecomment-5860376015. Epic #1 body updated with reference entry.

**Status:** Awaiting PO approval. Story remains open.

**How to apply:** Story #84 is complete from the BA perspective. Do not rewrite the document; if the PO changes a threshold or policy during MVP1 confirmation, update the relevant rows in the document's tables.
