# Adobe Stock AI Prompt Evaluation Rubric

**Story:** #88
**Profile:** `stock/adobe-stock`
**Purpose:** Objective measurement of AI prompt quality for story #25. Defines pass/fail rules for each output field and the overall acceptance threshold for MVP2.

---

## Evaluation Asset Set

Five fixed assets, one per scenario type. Each asset has a CAR input file (`scenario-x-car.json`) and an expected-output record (`scenario-x-expected.md`) in `Reqs/adobe-stock-eval/assets/`.

| Scenario | File Stem | Description |
|---|---|---|
| A | `scenario-a` | Commercial photo, no people — alpine mountain trail |
| B | `scenario-b` | Commercial photo with identifiable person — woman at home office desk |
| C | `scenario-c` | Editorial photo (`risk.editorial_only = true`) — protest march |
| D | `scenario-d` | Commercial photo with visible logo (`risk.trademark_flag = true`) — laptop on desk |
| E | `scenario-e` | Scene with primary activity — chef cooking in restaurant kitchen |

---

## Scoring Overview

Each asset is scored independently across four fields: **Title**, **Keywords**, **Category**, and **Releases**. Each field scores **pass** or **fail**. An asset passes if and only if all four fields pass.

A field fails if any single condition within it is not met — partial credit is not applied.

---

## Field 1 — Title

### Pass conditions (all four must be met)

| Condition ID | Rule | Check |
|---|---|---|
| `title-max-length` | Length ≤ 200 characters | Count characters in the generated title; fail if > 200 |
| `title-sentence-case` | First word capitalised; remaining words lowercase unless proper nouns | Inspect each word; fail if any non-proper-noun word after position 1 is capitalised |
| `title-no-brand-names` | No brand names when `risk.trademark_flag = true` or `text.logo_marks_detected` is non-empty (commercial path only; does not apply when `risk.editorial_only = true`) | Check the generated title against every entry in `text.logo_marks_detected`; fail if any brand name appears and the asset is on the commercial path |
| `title-subject-accuracy` | The title describes the primary subject identified in `objects.primary_subject` | Confirm the primary subject noun or equivalent is present in the title; fail if the title omits or contradicts the primary subject |

**Title passes** if and only if all four conditions pass.

---

## Field 2 — Keywords

### Pass conditions (all four must be met)

| Condition ID | Rule | Check |
|---|---|---|
| `min-keyword-count` | ≥ 5 keywords | Count comma-separated terms; fail if < 5 |
| `max-keyword-count` | ≤ 49 keywords | Count comma-separated terms; fail if > 49 |
| `keywords-no-brand-names` | No term matching any entry in `text.logo_marks_detected` when `risk.trademark_flag = true` (commercial path only; brand names are permitted on the editorial path when `risk.editorial_only = true`) | Check each keyword against `text.logo_marks_detected`; fail if a brand name appears and the asset is on the commercial path |
| `keywords-separator-format` | All keywords lowercase; comma-separated with no whitespace around commas | Inspect capitalisation of every term; inspect every comma for surrounding whitespace; fail if any term is not lowercase or any comma has surrounding whitespace |
| `keywords-top5-relevance` | The first 5 keywords are directly relevant to `objects.primary_subject` or `activities.primary_activity` as recorded in the CAR input | Check the first 5 keywords against `objects.primary_subject` and `activities.primary_activity`; fail if fewer than 4 of the first 5 keywords are directly relevant to these two fields |

**Keywords pass** if and only if all five conditions pass.

> **Note on `keywords-top5-relevance`:** Allows one irrelevant keyword in the top 5 (4-of-5 rule) to accommodate legitimate scene-setting terms that rank high by commercial relevance but are not the primary subject or activity (e.g., "indoor" as keyword 4 on a workplace scene). Adjust this tolerance at implementation time if the prompt consistently includes off-topic terms in the top 5.

---

## Field 3 — Category

### Pass conditions (all three must be met)

| Condition ID | Rule | Check |
|---|---|---|
| `category-must-be-numeric` | The value is an integer — not a string, empty value, or zero | Confirm the value is a positive integer; fail if it is a string, empty, or zero |
| `category-valid-code` | The integer appears in the Adobe Stock category taxonomy table in `docs/adobe-stock-submission-rules.md` §4.2 | Look up the value in the taxonomy table; fail if the code is not listed |
| `category-matches-expected` | The code matches the expected category code recorded in the expected-output record for the asset | Compare to the Expected Category in `scenario-x-expected.md`; fail if the code differs |

**Category passes** if and only if all three conditions pass.

---

## Field 4 — Releases

### Pass conditions (all two must be met)

| Condition ID | Rule | Check |
|---|---|---|
| `releases-state-correct` | The releases state letter (A, B, or C) implied by the generated output matches the expected state letter in the expected-output record, applying the state definitions from `docs/adobe-stock-release-rules.md` §3 | Determine the applicable state from the CAR risk flags and compare the generated output to the expected state; fail if the state does not match |
| `releases-model-release-required-state-b` | When `risk.model_release_required = true` and no confirmed release is present in the CAR input, the releases state must be B — empty `Releases` column, output held pending human review (`docs/adobe-stock-release-rules.md` §3.2) | Read `risk.model_release_required` from the CAR input; if `true` and no reviewer confirmation is in the CAR, fail if the generated output does not produce an empty `Releases` value |
| `releases-no-flags-state-c` | When neither `risk.model_release_required` nor `risk.property_release_required` is active on the CAR (both absent or `false`), the releases state must be C — empty `Releases` column, no release gating (`docs/adobe-stock-release-rules.md` §3.3) | Read both release flags from the CAR input; if neither is `true`, fail if the generated output implies State A or State B |
| `releases-editorial-exemption` | When `risk.editorial_only = true` (Scenario C), the releases state must be C (editorial exemption per `docs/adobe-stock-release-rules.md` §5.1) regardless of whether `risk.model_release_required` is also `true` | For Scenario C assets, fail if the generated output implies State A or State B |

**Releases pass** if and only if all four conditions pass.

---

## Per-Asset Scorecard Template

Use this template when evaluating each prompt version. Complete one scorecard per asset per prompt version.

```
Asset: Scenario [X] — [description]
Prompt version: [version identifier]
Evaluation date: [YYYY-MM-DD]

| Field     | Pass / Fail | Failing condition IDs (if fail) | Notes |
|-----------|-------------|----------------------------------|-------|
| Title     |             |                                  |       |
| Keywords  |             |                                  |       |
| Category  |             |                                  |       |
| Releases  |             |                                  |       |

Asset result: PASS (all four fields pass) / FAIL (one or more fields fail)
```

---

## Overall Pass Threshold

> **⚠ PO sign-off required (AC8).** The threshold value below is pending explicit PO approval. This story is not closeable until the PO records approval of the threshold value in a comment on issue #88.

**The Adobe Stock AI prompt is acceptable for MVP2 if 3 of 5 assets score pass on all four fields (Title, Keywords, Category, Releases).**

**PO-approved threshold: 3 of 5.** Signed off by PO in issue #88 comment, 2026-09-29.

---

## Evaluation Procedure

1. Run the AI prompt under test against each of the five CAR input files.
2. Record the generated Title, Keywords, Category, and Releases value for each asset.
3. Apply each field's pass conditions independently against the generated output.
4. Complete a per-asset scorecard for each asset.
5. Count the number of assets that received PASS on all four fields.
6. Compare the count to the PO-approved threshold. If count ≥ threshold, the prompt is acceptable for MVP2.

---

## References

- `docs/adobe-stock-output-spec.md` — column definitions and validation rule IDs
- `docs/adobe-stock-submission-rules.md` §4.2 — category taxonomy
- `docs/adobe-stock-release-rules.md` §3 — three-state release behaviour; §5.1 — editorial exemption
- `docs/car-field-catalogue.md` — CAR field dot-notation names
- `docs/confidence-and-risk-rules.md` — risk flag handling policies
- `docs/car-risk-flags-spec.md` — risk flag field specifications and propagation rules (story #22)
