# CAR Confidence Scores Category — Field Specification

> **Draft v0.1 — story #21.** This document is the implementation-ready field specification for the Confidence Scores category of the Canonical Asset Record. It is the authoritative reference for Layer 1 (Asset Intelligence Layer) developers populating these fields. All field names and types are authoritative per the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)).

---

## Overview

The Confidence Scores category is the seventh and final category of the Canonical Asset Record. It records how certain the Asset Intelligence Layer is in its findings across all preceding six categories, provides a single aggregate score for fast-path downstream routing, and captures supplementary metadata about the analysis run itself (model version, timestamp, and asset technical quality).

Unlike the six observation categories that precede it, the Confidence Scores category does not describe what is in the asset. It describes how reliably the Asset Intelligence Layer observed what is in the asset. This distinction is fundamental: a high confidence score does not mean the asset is commercially valuable or technically well-composed; it means the analytical pipeline produced findings it is certain of.

The Confidence Scores category is produced last. Its completion is the act that seals the CAR as immutable and ready for Handoff 1. No other category may be modified after the Confidence Scores category is written.

---

## Scope

This specification covers the five fields within the `confidence.*` namespace:

1. `confidence.overall_score`
2. `confidence.analysis_model_version`
3. `confidence.low_confidence_categories`
4. `confidence.analysis_timestamp`
5. `confidence.asset_quality_signal`

This specification does not redefine the per-category confidence score fields (`objects.confidence_score`, `persons.confidence_score`, `location.confidence_score`, `text.confidence_score`, `activities.confidence_score`, `risk.confidence_score`). Those fields are specified in their respective category sections of the CAR Field Catalogue. The `confidence.*` fields described here are the summary-level and run-level support fields that complement them.

**Confidence score threshold values** are defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) (story #84). The provisional threshold is **0.70** for all categories. That document is the normative source for threshold values; this specification references them but does not define them.

---

## CAR Sealing and Immutability

The Confidence Scores category occupies a special position in the CAR production sequence: it is produced last, after all six observation categories have been populated and their per-category confidence scores have been set.

The reason is structural: `confidence.overall_score` is a weighted composite of all per-category scores (see Section "Field Specifications — confidence.overall_score"), and `confidence.low_confidence_categories` is computed by evaluating all six per-category scores against the routing threshold. Neither field can be correctly populated until every observation category is complete.

**Sealing rule:** Once the Asset Intelligence Layer writes `confidence.analysis_timestamp`, the CAR is sealed. From that moment the CAR is immutable — no field in any category may be altered by any layer, process, or actor. The `confidence.analysis_timestamp` value is therefore both a record of when analysis completed and the marker that formally closes the CAR as a mutable object.

This sealing behaviour is the concrete implementation of the immutability rule defined in the CAR concept document ([docs/canonical-asset-record.md](canonical-asset-record.md), Section 2): "The CAR is immutable after production. No layer, process, or actor may modify the Canonical Asset Record once the Asset Intelligence Layer has produced it."

If a CAR is found to be incorrect after sealing, it must be discarded and reproduced from the original raw asset by the Asset Intelligence Layer. It must never be edited in place.

---

## Field Specifications

### confidence.overall_score

| Attribute | Value |
|---|---|
| **Type** | float (0–1) |
| **Cardinality** | Required |
| **Condition** | Always present |

**What it records:** A single aggregate confidence score summarising the Asset Intelligence Layer's overall certainty across all observations in the CAR. Provides a fast-path signal for downstream routing without requiring consumers to evaluate all seven per-category scores individually.

**Calculation method — open implementation decision:** The weighting formula for `confidence.overall_score` is an open MVP1 implementation decision. The Layer 1 implementer has full authority to choose the appropriate approach (e.g., simple arithmetic mean of per-category scores, weighted mean with weights assigned by category criticality, median, or another aggregation method). No PO approval is required before implementation. However, the implementer **must** record the chosen approach — including the formula, any per-category weights, and the rationale — in the Layer 1 implementation record before the first CAR is produced for use downstream. This record is required for reproducibility and must be updated if the approach changes in a subsequent model version.

**Valid range:** A float in the inclusive range [0.0, 1.0]. Values outside this range are invalid.

- `1.0` — maximum certainty across all categories.
- `0.0` — the pipeline produced observations but has no certainty in any of them.
- Values may be stored and compared at full float precision; rounding conventions are an implementation decision.

**Example values:**
- `0.91` — high confidence across all categories; typical for a well-lit studio photo with clear subjects
- `0.74` — moderate confidence; one or two categories may be close to threshold
- `0.52` — low confidence; likely below threshold, `"confidence"` will appear in `confidence.low_confidence_categories`

**Relation to per-category scores:** `confidence.overall_score` is derived from the six per-category scores. It does not replace them; both must be present. Downstream consumers may use `confidence.overall_score` for fast-path routing decisions (e.g., "is this CAR above the overall threshold?") and then inspect individual category scores for field-level decisions.

**Downstream use:** The routing threshold for `confidence.overall_score` is 0.70 (provisional, per `docs/confidence-and-risk-rules.md`, Table 1.2). If `confidence.overall_score` is below this threshold, `"confidence"` must be added to `confidence.low_confidence_categories` (see that field's specification below).

---

### confidence.analysis_model_version

| Attribute | Value |
|---|---|
| **Type** | string |
| **Cardinality** | Required |
| **Condition** | Always present |

**What it records:** The version identifier of the Asset Intelligence Layer model or pipeline that produced this CAR. Enables two downstream capabilities:

1. **Reproducibility tracking** — for any given CAR, a consumer or auditor can determine exactly which model version produced the observations, making it possible to understand or reproduce the analysis.
2. **Re-processing support** — when the model is updated, the platform can identify CARs produced by older model versions and queue them for re-analysis if the update changes the scope or accuracy of detection.

**Format:** A short string identifier. The provisional format convention is `"ail-v<major>.<minor>"` (e.g., `"ail-v0.1"` for the first MVP1 implementation). The exact versioning scheme is an implementation decision for the Layer 1 implementer, but the chosen scheme must be documented in the Layer 1 implementation record alongside the `confidence.overall_score` weighting formula. The version string must uniquely identify the pipeline configuration; two pipeline configurations that produce materially different outputs must not share a version string.

**Immutability:** This field is set at analysis time and sealed with the CAR. It is never updated in place. If a CAR is re-processed under a new model version, a new CAR is produced with the new version string; the original CAR is discarded or archived.

---

### confidence.low_confidence_categories

| Attribute | Value |
|---|---|
| **Type** | Array\<string\> |
| **Cardinality** | Conditional |
| **Condition** | Present when one or more per-category confidence scores are strictly below the routing threshold (< 0.70, provisional) |

**What it records:** The list of CAR information categories for which the Asset Intelligence Layer's confidence is below the platform routing threshold. Any downstream consumer reading a category name from this array must apply CAR Consumer Rule 2 to every field within that category, treating all fields in that category as unknown.

**Population rule:** After all six per-category confidence scores have been finalised, the Asset Intelligence Layer must evaluate each score against the threshold. Any category whose score is strictly below the threshold (< 0.70, provisional) must have its category name string added to this array. This evaluation is performed as the final step before `confidence.analysis_timestamp` is written.

**Enumerated category name strings:** The exact string values that must appear in this array are fixed. No other string values are valid. The complete set of seven permitted values is:

| Category Name String | Corresponding Confidence Score Field |
|---|---|
| `"objects"` | `objects.confidence_score` |
| `"persons"` | `persons.confidence_score` |
| `"locations"` | `location.confidence_score` |
| `"text"` | `text.confidence_score` |
| `"activities"` | `activities.confidence_score` |
| `"risk"` | `risk.confidence_score` |
| `"confidence"` | `confidence.overall_score` |

Note that `"confidence"` refers to the aggregate score for the Confidence Scores category as a whole (`confidence.overall_score`), not to any individual per-category score. If the aggregate score itself falls below threshold, `"confidence"` is added to the array.

**Presence rule:**

- **All categories pass (all scores ≥ 0.70):** The field is **absent** from the CAR. Absence means all categories met the routing threshold and is a valid state. Consumers must not treat absence as an error.
- **One or more categories fail (any score < 0.70):** The field **must be present** and must list the name of **every** failing category. Listing some but not all failing categories is invalid.

**Example values:**
- `["locations"]` — only the Locations category failed (e.g., no GPS data and no identifiable landmark)
- `["locations", "risk"]` — two categories below threshold; both must appear
- Field absent — all six per-category scores ≥ 0.70; no categories failed

**Partial population = invalid Handoff 1.** If any failing category is omitted from this array when the field is present, the CAR does not satisfy Handoff 1 validity condition 2 (Confidence Scores present) and must be treated as an invalid Handoff. The receiving layer must surface a Handoff failure rather than proceed.

**Threshold value:** The 0.70 threshold is provisional and marked `[PROVISIONAL — confirm at MVP1]` in `docs/confidence-and-risk-rules.md`. Implementations must use the threshold value from that document as the authoritative source; any update to the threshold in that document supersedes this reference.

---

### confidence.analysis_timestamp

| Attribute | Value |
|---|---|
| **Type** | string (ISO 8601) |
| **Cardinality** | Required |
| **Condition** | Always present |

**What it records:** The date and time at which the Asset Intelligence Layer completed analysis and sealed the CAR as immutable. This is the moment the CAR transitions from a mutable work-in-progress to a sealed Handoff artifact.

**Format:** ISO 8601 combined date and time, including timezone offset or UTC designator. Examples of valid values:

- `"2025-03-14T09:26:53Z"` — UTC
- `"2025-03-14T11:26:53+02:00"` — explicit offset
- `"2025-03-14T09:26:53.421Z"` — with millisecond precision (permitted)

The timezone must always be specified explicitly. Local time without a timezone designator is not a valid value for this field. UTC is recommended for consistency across deployment environments.

**Sealing semantics:** This field is written last, after all other Confidence Scores fields have been populated. Its presence signals that the CAR is sealed. Any process that reads a CAR and finds `confidence.analysis_timestamp` absent must treat the CAR as incomplete and not proceed with Handoff 1.

**Audit trail:** `confidence.analysis_timestamp` supports the audit trail requirements planned for MVP4. It provides a point-in-time record of when each CAR was produced, enabling traceability for any Output Package back to the specific analysis run that produced the underlying CAR.

---

### confidence.asset_quality_signal

| Attribute | Value |
|---|---|
| **Type** | string (enum) |
| **Cardinality** | Required |
| **Condition** | Always present |

**What it records:** A classification of detected technical quality issues in the asset that may reduce the accuracy of the Asset Intelligence Layer's analysis. This field records technical properties of the asset that affect detection confidence — it does not rate the asset's commercial value, aesthetic quality, or suitability for any distribution channel.

**Permitted enum values (five total):**

| Value | Meaning |
|---|---|
| `blur` | The image is blurred (camera shake, motion blur, or focus miss) to a degree that impairs object or face detection accuracy. |
| `low_resolution` | The image resolution is insufficient to support reliable detection for one or more categories (e.g., small faces that cannot be assessed for identifiability). |
| `poor_exposure` | The image is significantly underexposed or overexposed, reducing visibility of subjects, text, or scene detail to a degree that impairs analysis. |
| `noise` | The image contains significant digital noise (e.g., high-ISO grain) that degrades detection accuracy. |
| `none` | No technical quality issues are detected. This is the required value when the asset presents no technical properties that reduce analysis confidence. |

**Example values:**
- `"blur"` — camera shake on a handheld shot reduces face detection reliability
- `"low_resolution"` — image is 640×480; small faces cannot be assessed for identifiability
- `"none"` — sharp, well-exposed, sufficient-resolution image; no technical issues detected

**`none` is the required value when no issues are detected.** The field is always present (Required cardinality); when the asset is technically sound and no quality issues are identified, the value must be `"none"`. Absence of this field is invalid even when the asset is high quality.

**Single-value field:** `confidence.asset_quality_signal` records a single enum value, not an array. If multiple technical quality issues are detected, the implementer must select the single most significant issue — the one most likely to be the primary driver of any reduction in analysis confidence. The selection criterion (e.g., "most impactful to detection accuracy") is an implementation decision that should be documented in the Layer 1 implementation record.

**Scope limitation:** This field does not assess commercial or aesthetic quality. It does not indicate whether an image is "good enough" to sell on a stock marketplace or whether it meets a platform's quality standards. Its sole purpose is to signal to downstream consumers whether a technical property of the asset may have constrained the Layer 1 analysis, so that consumers can apply appropriate caution to confidence scores when a quality issue is present.

> **Note on field catalogue authority:** The authoritative list of permitted enum values is the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)). This specification confirms **five** permitted values: `blur`, `low_resolution`, `poor_exposure`, `noise`, and `none`. Any reference to six values is incorrect; the Field Catalogue is the authoritative source.

---

## Risk-Below-Threshold Special Case

If the string `"risk"` appears in `confidence.low_confidence_categories`, the Risk Flags category's confidence score (`risk.confidence_score`) is below the routing threshold. This condition does not suppress, invalidate, or downgrade any individual risk flag.

**The rule (restating CAR Consumer Rule 4 and `docs/confidence-and-risk-rules.md`, Section 1.3):** Each `risk.*` boolean field set to `true` must still be propagated to all downstream consumers in full, regardless of the value of `risk.confidence_score`. A below-threshold risk confidence score means the evaluation pass's overall detection sensitivity is uncertain — but any flag already triggered is a live signal that must not be silently discarded.

**Practical consequence:** The presence of `"risk"` in `confidence.low_confidence_categories` has two simultaneous effects:

1. **Consumer obligation (Rule 2 applies):** Absent `risk.*` fields must be treated as unknown, not as confirmed negatives. If `risk.confidence_score` is below threshold and `risk.model_release_required` is absent from the CAR, the consumer must not conclude that no model release is required. The correct response is to treat model release status as unknown and route accordingly.
2. **Propagation obligation (Rule 4 applies):** Any `risk.*` field that is present and set to `true` must be propagated and acted on. Low confidence on the Risk category cannot silence an active flag.

These two obligations are not in conflict. They apply to different conditions: Rule 2 governs absent fields when confidence is low; Rule 4 governs present `true` fields regardless of confidence. Together they mean that a below-threshold Risk Flags category is always a conservative signal — it can never relax an active flag, and it can never confirm that an undetected risk does not exist.

**Routing implication:** When `"risk"` appears in `confidence.low_confidence_categories`, the CAR should, in practice, be routed to human review rather than proceeding with automated output generation. This is consistent with the principle that a low-confidence risk evaluation is too uncertain to rely on for automated commercial channel decisions.

---

## Handoff 1 Validity Conditions

The following Confidence Scores fields are directly referenced in the Handoff 1 validity conditions defined in [docs/boundary-contracts.md](boundary-contracts.md):

| Handoff 1 Condition | Confidence Scores Field(s) Referenced |
|---|---|
| **Condition 2 — Confidence Scores present:** every non-absent observation carries a confidence score; no observation is included without an associated certainty value. | `confidence.overall_score` must be present. `confidence.low_confidence_categories` must be present (and complete) if any per-category score is below threshold; absent only if all pass. |
| **Condition 3 — Risk Flags propagated:** all detected Risk Flags are present regardless of the confidence score of the underlying observation (CAR Consumer Rule 4). | `confidence.low_confidence_categories` containing `"risk"` does not exempt the implementation from propagating `true` risk flags. |
| **Condition 4 — Immutability:** the CAR has been sealed by the Asset Intelligence Layer and is not subject to further modification. | `confidence.analysis_timestamp` is the sealing marker. Its presence confirms the CAR has been sealed; its absence means the CAR is not yet sealed and the Handoff is invalid. |

A CAR that is missing `confidence.overall_score`, that has an incomplete `confidence.low_confidence_categories` array (partial population), or that lacks `confidence.analysis_timestamp` does not satisfy Handoff 1. The Content Generation Layer must not proceed with an invalid Handoff.

---

## Edge Cases

**All per-category scores exactly equal the threshold (0.70):** A score of exactly 0.70 meets the threshold (the failing condition is strictly below: `< 0.70`). No category at exactly 0.70 should appear in `confidence.low_confidence_categories`. Absence of the field is correct when all scores are ≥ 0.70.

**`confidence.overall_score` falls below threshold independently:** It is possible for the aggregate score to fall below 0.70 even if no individual per-category score does (depending on the weighting formula chosen). In this case `"confidence"` must be added to `confidence.low_confidence_categories` even though all six per-category scores individually passed.

**`confidence.overall_score` passes threshold but one or more per-category scores do not:** It is equally possible for the aggregate score to be ≥ 0.70 while one or more per-category scores are below threshold. In this case `confidence.low_confidence_categories` must list the failing categories; the aggregate passing does not exempt failing categories from appearing in the array.

**`confidence.asset_quality_signal` and below-threshold scores:** A technical quality issue (e.g., `blur`) is correlated with, but not equivalent to, a low confidence score. The `blur` signal indicates an asset property; a low confidence score is the analytical result. Both may be present simultaneously, or either may be present independently. The implementer must set both fields from their own evidence; one does not derive from the other.

**Re-processing after model update:** When a CAR is re-processed under a new model version, a completely new CAR is produced. The new CAR receives a new `confidence.analysis_timestamp` and a new `confidence.analysis_model_version`. The old CAR must be archived or discarded. Timestamps from two different CARs for the same asset must not be compared as if they represent a single analysis run.

**`confidence.low_confidence_categories` present but empty array:** An empty array (`[]`) is not a valid value for this field. The field is either absent (all categories passed) or present with at least one category name string. An empty array constitutes an invalid Handoff.

---

## Consistency with Field Catalogue

This specification is consistent with and does not supersede the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)). In any conflict between this document and the Field Catalogue, the Field Catalogue is authoritative for field names, types, and cardinality. This document is authoritative for population rules, calculation guidance, and implementation constraints layered on top of the catalogue definitions.

**Cross-references:**

- **CAR Field Catalogue** — [docs/car-field-catalogue.md](car-field-catalogue.md): source definitions for all five fields in this specification.
- **CAR Concept Definition (story #15)** — [docs/canonical-asset-record.md](canonical-asset-record.md): Consumer Rules 1–4; immutability rule.
- **Confidence Score Thresholds and Risk Flag Handling Rules (story #84)** — [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md): the 0.70 provisional threshold; `confidence.low_confidence_categories` population rule; risk-below-threshold special case.
- **Boundary Contracts (story #77)** — [docs/boundary-contracts.md](boundary-contracts.md): Handoff 1 validity conditions referenced in the Handoff 1 Validity Conditions section above.
- **Domain Glossary** — [docs/glossary.md](glossary.md): Canonical Asset Record, Confidence Score, Risk Flag, Handoff, Asset Intelligence Layer, Content Generation Layer.
