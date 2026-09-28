# Confidence Score Thresholds and Risk Flag Handling Rules

This document defines the policy rules that govern how downstream layers must react to confidence scores and risk/compliance flags in the Canonical Asset Record (CAR). These are domain model decisions — the authoritative, implementation-facing specification of threshold values and handling policies that every consumer of the CAR must follow.

This document is the deliverable for **story #84**. It is the normative source for:

- The minimum confidence threshold per CAR field category.
- How the `confidence.low_confidence_categories` field is populated.
- The default handling policy for each of the six `risk.*` flag types.
- The interaction rule when multiple risk flags are simultaneously present.

All field names used in this document are specified in the **CAR Field Catalogue** ([docs/car-field-catalogue.md](car-field-catalogue.md), story #78). All consumer obligations referenced below (Rules 1–4) are defined in the **CAR concept document** ([docs/canonical-asset-record.md](canonical-asset-record.md), story #15). All terms are defined in the [AssetForge Domain Glossary](glossary.md).

> **Provisional values notice:** All numeric threshold values in this document are set to **0.70** as a provisional placeholder, pending PO confirmation during MVP1 implementation. Every threshold value is individually marked **[PROVISIONAL — confirm at MVP1]**. No implementation decision should treat these values as permanent policy until that confirmation is recorded.

---

## 1. Confidence Threshold Policy

### 1.1 What a confidence score measures

A confidence score reflects the Asset Intelligence Layer's analytical certainty in its findings for a given category. A score of 1.0 means maximum certainty; a score of 0.0 means the layer produced an observation but has no certainty in it. A low score does not discard the observation — it signals that downstream consumers must apply CAR Consumer Rule 2 and treat the field as unknown rather than as confirmed fact.

This definition is unchanged from the CAR concept document. This story adds the numeric threshold that triggers Rule 2 and the population rule for `confidence.low_confidence_categories`.

### 1.2 Minimum threshold per category

The table below states the minimum confidence score required for each CAR field category for a consumer to act on that category's fields as confirmed observations. A score below the minimum must be treated as unknown (CAR Consumer Rule 2). A score at or above the minimum may be acted on as a confirmed observation.

| CAR Field Category | Confidence Score Field | Minimum Threshold | Status |
|---|---|---|---|
| Objects and Subjects | `objects.confidence_score` | 0.70 | **[PROVISIONAL — confirm at MVP1]** |
| People | `persons.confidence_score` | 0.70 | **[PROVISIONAL — confirm at MVP1]** |
| Locations | `location.confidence_score` | 0.70 | **[PROVISIONAL — confirm at MVP1]** |
| Text and Logos | `text.confidence_score` | 0.70 | **[PROVISIONAL — confirm at MVP1]** |
| Activities | `activities.confidence_score` | 0.70 | **[PROVISIONAL — confirm at MVP1]** |
| Risk Flags | `risk.confidence_score` | 0.70 | **[PROVISIONAL — confirm at MVP1]** |
| Aggregate (overall) | `confidence.overall_score` | 0.70 | **[PROVISIONAL — confirm at MVP1]** |

**Why a single threshold is acceptable at this stage.** Differentiating thresholds by category (e.g., setting a stricter threshold for People to account for biometric sensitivity, or a looser threshold for Activities because activity labels are more tolerant to slight uncertainty) requires empirical data from the MVP1 Asset Intelligence Layer implementation. Without a working model producing scores across a representative dataset, any per-category differentiation would be arbitrary. A uniform provisional threshold of 0.70 provides a consistent policy baseline that MVP1 implementers can test against and replace with per-category values once empirical distributions are available. The placeholder is deliberately conservative: 0.70 filters out low-quality detections while preserving observations with reasonable certainty.

### 1.3 Threshold value for `confidence.low_confidence_categories`

The `confidence.low_confidence_categories` field (cardinality: Conditional, field type: Array\<string\>) is populated by the Asset Intelligence Layer at CAR production time. It must be populated as follows:

**Population rule:** After evaluating all seven category confidence scores, the Asset Intelligence Layer must add the name of any category whose confidence score is strictly below the minimum threshold (< 0.70, provisional) to the `confidence.low_confidence_categories` array.

**Enumerated category names** (the exact string values that must appear in the array):

| Category Name String | Corresponding Confidence Score Field |
|---|---|
| `"objects"` | `objects.confidence_score` |
| `"persons"` | `persons.confidence_score` |
| `"locations"` | `location.confidence_score` |
| `"text"` | `text.confidence_score` |
| `"activities"` | `activities.confidence_score` |
| `"risk"` | `risk.confidence_score` |
| `"confidence"` | `confidence.overall_score` |

**Presence rule:** If no category score is below the threshold, the field is absent from the CAR (valid; absence means all categories met the threshold). If one or more category scores fall below the threshold, the field must be present and must contain the name of every failing category. Partial population (listing some but not all failing categories) constitutes an invalid Handoff 1.

**Consequence for consumers:** Any downstream consumer (Content Generation Layer or routing logic) that reads a category name from `confidence.low_confidence_categories` must apply CAR Consumer Rule 2 to every field within that category — treating all fields in that category as unknown, consistent with CAR Consumer Rule 1.

**Special case — Risk Flags category below threshold:** If `"risk"` appears in `confidence.low_confidence_categories`, the `risk.confidence_score` is below threshold. This does not suppress or invalidate any individual risk flag. Each `risk.*` boolean field that is set to `true` must still be propagated to downstream consumers in full compliance with CAR Consumer Rule 4. The low confidence score on the Risk Flags category means the evaluation pass's overall detection sensitivity is uncertain — but any flag already triggered must be treated as a live signal. The presence of `"risk"` in `confidence.low_confidence_categories` should, in practice, prompt routing to human review rather than proceeding with automated output generation.

---

## 2. Risk Flag Handling Policies

### 2.1 Canonical handling policy vocabulary

All default handling policies in this section use exactly one of three canonical terms:

- **Suppress output** — the Content Generation Layer must not generate content fields that depend on the flagged observation. Fields dependent on the suppressed observation are absent from the Generated Content Handoff artifact. The asset may still proceed through the Pipeline for other non-dependent fields.
- **Require human review** — the Pipeline must pause and route the asset to a human reviewer before the Output Package can be finalised and delivered. Automated generation may proceed, but the Output Package must not be delivered until a human reviewer records an approval or override. This is expressed in the Content Profile's Approval Requirements dimension.
- **Block output entirely** — no Output Package may be generated or delivered for any channel profile until the blocking condition is resolved. This is the most restrictive policy; it halts the Pipeline completely for the affected asset.

These three terms are the only permitted values for default handling policy. No other policy vocabulary is valid in this document, in story documentation, or in Content Profile specifications.

### 2.2 Risk Flags: field-by-field specification

The following table enumerates all six `risk.*` flag fields from the CAR Field Catalogue. Each entry states the field name, a plain-language description of what the flag signals, and the default handling policy.

| # | Field Name | Description | Default Handling Policy |
|---|---|---|---|
| 1 | `risk.model_release_required` | Signals that one or more identifiable persons are present in the asset and a model release may be required before commercial distribution. Set to `true` when `persons.present` is `true` and at least one person is potentially identifiable (face visible or person is prominently featured). | **Require human review** — the asset must be routed for human review to confirm whether a signed model release is on file before any commercially classified Output Package is finalised. Automated generation may proceed; delivery is blocked until review is complete. |
| 2 | `risk.property_release_required` | Signals that recognisable private property (buildings, branded structures, private artworks) is identifiable in the image and a property release may be required for commercial distribution. | **Require human review** — analogous to model release: automated generation may proceed; delivery of any commercially classified Output Package is blocked until a reviewer confirms release status. |
| 3 | `risk.editorial_only` | Signals that the asset is classified as Editorial Use only because a real-world public event, public figure, or unscripted news moment has been detected. When `true`, the asset must not be used to generate commercially classified output without a recorded human override. | **Block output entirely** for any commercial channel Content Profile — no Output Package targeting a commercial channel may be generated or delivered until a human reviewer records an explicit override. For editorial channel profiles, generation proceeds normally. |
| 4 | `risk.adult_content` | Signals that the asset contains nudity, sexually suggestive content, or content inappropriate for general audiences. | **Require human review** — automated generation must not proceed for any channel profile until a human reviewer confirms that the asset is appropriate for the intended distribution destination and that any channel-specific age-restriction requirements are met. |
| 5 | `risk.violence_flag` | Signals that the asset contains depictions of violence, injury, or distressing content. | **Require human review** — same as adult content: automated generation must not proceed until a human reviewer confirms suitability for the intended channel. |
| 6 | `risk.trademark_flag` | Signals that a third-party trademark or brand mark is visible in the asset and commercial distribution may require rights clearance. Set when `text.logo_marks_detected` is non-empty or when a brand mark is otherwise detected. | **Suppress output** for any keyword or description field that directly references the detected trademark or brand name. The asset is not blocked from proceeding; other fields that do not reference the trademarked element may be generated normally. Content Profiles for individual channels may override this default with a stricter policy (require human review or block output entirely) if the destination's trademark policy requires it. |

### 2.3 Propagation rule (restatement of CAR Consumer Rule 4)

Every `risk.*` flag set to `true` must be propagated to all downstream consumers regardless of the confidence score of the underlying observation. A `risk.*` flag is never silenced by a low confidence score. The purpose of a risk flag is to signal that human review or rights clearance may be required; a low-confidence detection of an identifiable person is still a live signal that must not be discarded.

This is a hard constraint. An implementation that silently drops a `true` risk flag because its associated observation had a low confidence score constitutes a defect.

---

## 3. Multiple-Flag Interaction Rule

### 3.1 The governing principle: most restrictive policy wins

When two or more `risk.*` flags are simultaneously present and set to `true` on a single asset, the handling policy applied to the asset is the most restrictive policy among all active flags.

Ranked from least to most restrictive:

1. **Suppress output** (least restrictive — affects specific fields only; asset continues)
2. **Require human review** (asset paused; automated output held pending review)
3. **Block output entirely** (most restrictive — Pipeline halted for all channel profiles)

**Rule:** The effective policy for the asset is determined by the single most restrictive policy in the set of active flags. Each flag is evaluated independently; the most restrictive result governs the overall asset disposition.

### 3.2 Worked examples

**Example 1 — `risk.trademark_flag` and `risk.model_release_required` both `true`.**
Active policies: Suppress output (trademark) and Require human review (model release). Most restrictive: Require human review. The asset must be routed for human review before delivery. Additionally, any trademark-referencing content fields must be suppressed from generated output, consistent with the trademark flag's own policy.

**Example 2 — `risk.editorial_only` and `risk.adult_content` both `true`.**
Active policies: Block output entirely (editorial only, for commercial profiles) and Require human review (adult content). Most restrictive: Block output entirely. No Output Package for any commercial channel profile may be generated or delivered. Human review for adult content suitability must also be completed before any editorial channel Output Package is delivered, since Require human review is the standing adult content policy.

**Note on Example 2:** Block output entirely and Require human review are not mutually exclusive. When Block output entirely is the governing policy for one channel profile type (commercial) but Require human review governs another (editorial), both policies apply simultaneously to their respective channel profile types. "Most restrictive wins" determines the asset's overall routing disposition; it does not cancel a lower-ranked policy that applies to a separate channel profile type.

**Example 3 — `risk.editorial_only` combined with any other flag.**
`risk.editorial_only` set to `true` always triggers Block output entirely for commercial channel profiles. Any other flag present simultaneously must still be propagated and its own policy applied to its applicable channel profile type. No combination of flags may resolve `risk.editorial_only` to a less restrictive outcome. A human reviewer recording an explicit override for `risk.editorial_only` does not automatically resolve other simultaneously active flags; each flag must be individually reviewed and resolved.

### 3.3 Implementation implication

A downstream consumer evaluating risk flags on a multi-flag asset must:

1. Collect all `risk.*` fields that are `true`.
2. Look up the default handling policy for each.
3. Apply the most restrictive policy as the governing asset-level disposition.
4. Preserve and apply all individual field-level policies (e.g., trademark suppression) that operate below the asset level, even when a more restrictive asset-level policy is also in force.

No flag may be skipped, downgraded, or ignored because another flag already triggered a more restrictive policy.

---

## 4. Relationship to Content Profile Overrides

The policies in this document are **default** handling policies. They apply when no Content Profile specifies an alternative.

Individual Content Profile stories (beginning with the Adobe Stock profile in MVP2) may define profile-level overrides of these defaults within the **Validation Rules** and **Approval Requirements** dimensions of the Content Profile schema. For example:

- A stock marketplace profile may impose a stricter policy on `risk.trademark_flag` (escalating from Suppress output to Block output entirely for certain trademark categories).
- An editorial channel profile may define different review routing behaviour for `risk.adult_content`.

No Content Profile may relax the policy for `risk.editorial_only` automatically. That flag always requires human review resolution before commercial generation proceeds, regardless of profile-level configuration.

Content Profile-level overrides of these defaults are out of scope for this story and are not defined here. They belong in the specification for each individual Content Profile.

---

## 5. Confidence Score vs Risk Flag Interaction

Confidence scores and risk flags operate independently. Two rules govern their interaction:

**Rule A — Risk flags are immune to confidence threshold suppression.** A `risk.*` flag set to `true` must be propagated and acted on regardless of the value of `risk.confidence_score` or `confidence.overall_score`. A below-threshold confidence score on the Risk Flags category does not suppress any active flag. (See Section 1.3, special case, and CAR Consumer Rule 4.)

**Rule B — Risk flag absence is subject to confidence threshold evaluation.** If `risk.confidence_score` is below the minimum threshold (< 0.70, provisional) and a specific `risk.*` field is absent from the CAR, the consumer must treat that absence as unknown — not as confirmation that the flag does not apply. For example: if `risk.confidence_score` is 0.55 and `risk.model_release_required` is absent, the consumer must not conclude that no model release is required. The correct response is to treat the model release status as unknown and route accordingly (typically: human review).

This interaction means that a low Risk Flags confidence score is always a conservative signal: it cannot relax an active flag, and it cannot confirm the absence of a flag that was not detected.

---

## Cross-References

- **CAR concept definition (story #15):** [docs/canonical-asset-record.md](canonical-asset-record.md) — Consumer Rules 1–4 that this document operationalises with numeric thresholds and handling policies.
- **CAR Field Catalogue (story #78):** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative source for all seven `*.confidence_score` fields and all six `risk.*` flag fields enumerated in this document.
- **Boundary Contracts (story #77):** [docs/boundary-contracts.md](boundary-contracts.md) — Handoff 1 validity conditions, including the requirement that all Risk Flags be propagated before the CAR is delivered to the Content Generation Layer.
- **Commercial vs Editorial Classification (story #86):** [docs/commercial-editorial-classification.md](commercial-editorial-classification.md) — decision sequence for commercial/editorial classification at generation time, which depends on `risk.editorial_only` and other risk flags enumerated in this document.
- **Domain Glossary:** [docs/glossary.md](glossary.md) — Confidence Score, Risk Flag, Handoff, Content Profile, Output Package, and all other capitalised terms used in this document.
