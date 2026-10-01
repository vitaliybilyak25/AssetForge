---
name: Issue #85 refined — model and property release requirements for Adobe Stock
description: Story #85 refined from needs-refinement to ready-checklist-complete; 3 PO decisions outstanding.
type: project
---

Issue #85 "Define model and property release requirements for Adobe Stock" was refined on 2026-09-27. Label remains `needs-refinement`; PO approval still required.

**Why:** The original issue had generic ACs that did not name specific CAR fields, did not use the canonical handling vocabulary from docs/confidence-and-risk-rules.md, and did not specify the Adobe Stock CSV Releases column behaviour.

**How to apply:** When authoring the story #85 deliverable, reference:
- `docs/car-field-catalogue.md` for `risk.model_release_required` and `risk.property_release_required` field definitions.
- `docs/confidence-and-risk-rules.md` Section 2.1 for canonical handling vocabulary (`suppress output`, `require human review`, `block output entirely`).
- `docs/commercial-editorial-classification.md` Section 4 (Adobe Stock platform mapping table) and Section 5 (classification decision sequence).

**Three PO decisions outstanding before label can change to `ready`:**
1. Verify the Adobe Stock CSV `Releases` column format against the live contributor portal (AC3).
2. Confirm whether the `stock/adobe-stock` profile adopts the domain default (`require human review`) or escalates to `block output entirely` for unconfirmed releases (AC4).
3. Decide whether "confirmed release present" is a human reviewer checkbox in Approval Requirements, or requires a separate design story.
