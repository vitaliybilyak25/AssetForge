---
name: Adobe Stock validators story #26 refined
description: Story #26 refined 2026-09-28 — 10 ACs, all 16 rule IDs from spec, description validator removed, brand suppression source clarified; ready label + board Status Ready
type: project
---

Story #26 ("Define field validators for Adobe Stock constraints") refined on 2026-09-28.

**Why:** The original skeleton referenced a non-existent Description column and invented special-chars rules with no rule IDs or scope. The story needed a complete rewrite grounded in the Validation Summary Table in `docs/adobe-stock-output-spec.md`.

**Key decisions made:**
- Description validator removed: there is no Description column in the Adobe Stock CSV (`docs/adobe-stock-submission-rules.md` Section 2.1).
- Special-character rule removed: not an Adobe Stock CSV constraint.
- All 16 rule IDs sourced verbatim from `docs/adobe-stock-output-spec.md` Validation Summary Table.
- Brand suppression (title-no-brand-names, keywords-no-brand-names) driven by CAR `text.logo_marks_detected` array — dynamic per-asset, not a static dictionary.
- Category taxonomy: 20 codes from `docs/adobe-stock-submission-rules.md` Section 4.2.
- Releases three-state enforcement: State B blocked from export per `docs/adobe-stock-release-rules.md` Section 3.
- Validator output contract: field name + rule ID + fix suggestion on failure; pass result on pass.
- Row-level gating: all five column validators must pass before a row is written.

**AC count:** 10 (AC1–AC10).

**State:** ready label added, board Status set to Ready (Project #3, item PVTI_lAHODHI90s4BklMlzg8m8Tw), awaiting PO approval (AC checklist item 8/8 unchecked).

**How to apply:** When refining other Channel Adaptation Layer validator stories, follow the same pattern: source rule IDs from the output spec, confirm no invented constraints, specify dynamic inputs (CAR fields) separately from static allowed-value lists.
