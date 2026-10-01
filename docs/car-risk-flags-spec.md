# CAR Risk Flags Category — Field Specification

> **Draft v0.1 — story #22.** This document is the implementation-ready field specification for the Risk Flags category of the Canonical Asset Record. It is the authoritative reference for Layer 1 (Asset Intelligence Layer) developers populating these fields. All field names and types are authoritative per the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)).

---

## Overview

The Risk Flags category is the sixth of seven categories of the Canonical Asset Record. It records structured compliance signals indicating that the asset contains content requiring special handling before certain Output Packages can be generated or approved.

Risk Flags are not editorial or aesthetic judgements. They are objective compliance signals — each flag signals a condition that downstream consumers and channel Content Profiles must act on. A flag set to `true` is a live signal that must be propagated to all downstream consumers regardless of the confidence score of the evaluation pass. This propagation obligation is absolute and derives from CAR Consumer Rule 4 (see Section "Propagation Rule — Consumer Rule 4").

The Risk Flags category has one unique validity requirement: the `risk.flags_evaluated` field must be `true` before the Handoff 1 is valid. A CAR that has not completed a Risk Flag evaluation pass is not a valid Handoff artifact, regardless of the completeness of the other six categories.

---

## Scope

This specification covers the eight fields within the `risk.*` namespace:

1. `risk.flags_evaluated`
2. `risk.model_release_required`
3. `risk.property_release_required`
4. `risk.editorial_only`
5. `risk.adult_content`
6. `risk.violence_flag`
7. `risk.trademark_flag`
8. `risk.confidence_score`

**Confidence score threshold values** are defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) (story #84). This specification references those threshold values but does not define them.

**Channel-specific restrictions** triggered by individual flags (e.g., which platforms block adult content, what review workflows are triggered) are defined in individual Content Profile specifications. This specification defines the flags themselves — their conditions, semantics, and cross-category dependencies — not the downstream channel responses.

**Photo assets only.** This specification covers Photo assets. Video and Vector workflows are deferred to MVP10, consistent with the Field Catalogue scope.

---

## Propagation Rule — Consumer Rule 4

**Every Risk Flag set to `true` must always be surfaced to all downstream consumers, regardless of `risk.confidence_score`.**

This rule derives directly from CAR Consumer Rule 4 ([docs/canonical-asset-record.md](canonical-asset-record.md), Section 4, Rule 4): "A Risk Flag recorded in the CAR must always be surfaced to downstream consumers, even if the confidence score for the underlying observation is low. The purpose of a Risk Flag is to signal that human review or rights clearance may be required; a low-confidence detection of an identifiable person is still a signal that must not be silently discarded."

The practical consequence is that a low `risk.confidence_score` — including one below the routing threshold — cannot suppress, downgrade, or remove any active flag. When `risk.confidence_score` is below threshold, two simultaneous obligations apply:

1. **CAR Consumer Rule 2 applies to absent fields:** If `risk.confidence_score` is below threshold and a Conditional Risk Flag field is absent from the CAR, the consumer must not conclude that the corresponding risk condition does not exist. Absent fields must be treated as unknown, not as confirmed negatives.
2. **CAR Consumer Rule 4 applies to present `true` fields:** Any `risk.*` field that is present and set to `true` must be propagated and acted on. A below-threshold confidence score cannot silence an active flag.

These two obligations govern different conditions and do not conflict. Together they make a below-threshold Risk Flags category always a conservative signal: it can never relax an active flag, and it can never confirm that an undetected risk is absent.

---

## Editorial-Only Blocking Rule

When `risk.editorial_only = true`, commercial channel Content Profiles are blocked from generating Output Packages without a human review override.

This is a Layer 1 output constraint, not a Layer 2 implementation rule. The Asset Intelligence Layer, by setting `risk.editorial_only = true`, signals that the asset has been classified as Editorial Use only. The Content Generation Layer must honour this classification. A commercial channel Content Profile (e.g., `stock/adobe-stock`) must not generate an Output Package for an asset where `risk.editorial_only = true` unless a human reviewer has explicitly authorised an override.

The human review override mechanism is planned for MVP4 and is out of scope for this specification. Implementations prior to MVP4 must treat `risk.editorial_only = true` as an absolute block on commercial Output Package generation.

The downstream impact of a false positive on this flag is significant: a staged commercial photograph incorrectly classified as a news event will have its entire commercial Output Package blocked. The implementation team must tune detection sensitivity for `activities.editorial_event_signal` and public figure detection accordingly.

---

## Field Specifications

### risk.flags_evaluated

| Attribute | Value |
|---|---|
| **Type** | boolean |
| **Cardinality** | Required |
| **Condition** | Always present |

**What it records:** Confirms that the Asset Intelligence Layer completed a Risk Flag evaluation pass for this asset. This is the validity gate for the Risk Flags category.

**Semantics:**
- `risk.flags_evaluated = true` — the Asset Intelligence Layer has completed a full Risk Flag evaluation pass for this asset. All applicable Conditional flag fields have been evaluated and populated where triggered. The Risk Flags category is complete.
- `risk.flags_evaluated = false` or field absent — the evaluation pass is incomplete. The Handoff is invalid until this field is `true`.

**Handoff 1 validity:** `risk.flags_evaluated = true` is required for a valid Handoff 1. This is consistent with Handoff 1 validity condition 3 ("Risk Flags propagated") in [docs/boundary-contracts.md](boundary-contracts.md). A CAR delivered to the Content Generation Layer without `risk.flags_evaluated = true` must be rejected as an invalid Handoff. The receiving layer must surface a Handoff failure rather than proceed.

**`false` is not a valid delivered state.** The field exists to communicate completion. A value of `false` is a transient in-progress state; no valid CAR should be delivered with `risk.flags_evaluated = false`. If the evaluation pass cannot be completed, the CAR must not be delivered — it is not a valid Handoff artifact.

**Example values:**
- `true` — evaluation pass completed; Handoff is valid from a Risk Flags perspective
- `false` — evaluation pass incomplete; Handoff is invalid (must not be delivered)

---

### risk.model_release_required

| Attribute | Value |
|---|---|
| **Type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when `persons.present` is `true` AND at least one person is potentially identifiable (face visible OR person prominently featured) |

**What it records:** Signals that one or more identifiable persons are visible in the image and a model release may be required for commercial distribution.

**Trigger condition:** This field is present when both of the following are true:
1. `persons.present = true` (story #19 is authoritative for this field)
2. At least one person in the image is potentially identifiable — meaning a face is visible OR a person is so prominently featured that they could be identified from the image alone

When `persons.present = false`, this field must be absent. The `persons.present` and `persons.faces_detected` fields are specified in story #19; this specification does not redefine them and treats story #19 as authoritative for the People category.

**"Prominently featured" — open implementation decision:** The threshold for determining that a person is "prominently featured" introduces a judgment call that is difficult to automate with a bright-line rule. The specification documents the condition as the Field Catalogue states it. The concrete implementation threshold for "prominently featured" — for example, minimum percentage of frame occupied, minimum confidence of person detection, or a combination — is an MVP1 implementation decision. The implementer must document the chosen threshold in the Layer 1 implementation record.

**Propagation:** A `true` value must be propagated to all downstream consumers regardless of `risk.confidence_score` (Consumer Rule 4). A low-confidence detection of an identifiable person is still a live signal.

**Example values:**
- `true` — a face is visible; model release evaluation is required for commercial distribution
- `false` — `persons.present = true` but no person is identifiable (e.g., crowd shot where no individual face is visible and no individual is prominently featured)
- Field absent — `persons.present = false`; no persons detected; field is not produced

---

### risk.property_release_required

| Attribute | Value |
|---|---|
| **Type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when private property (buildings, branded structures, private artworks) is identifiable in the image |

**What it records:** Signals that recognisable private property is present in the image and a property release may be required for commercial distribution.

**Trigger condition:** This field is present when the Asset Intelligence Layer detects that private property is identifiable in the image. Private property in this context includes privately owned buildings with distinctive architectural features, branded commercial structures, privately commissioned artworks, and any other property whose commercial use may require rights clearance.

Unlike `risk.model_release_required`, which depends on the `persons.present` Required field as a prerequisite, `risk.property_release_required` has no direct Required predecessor field in the CAR. Detection of identifiable private property is a direct visual inference by the Asset Intelligence Layer, performed independently as part of the Risk Flag evaluation pass.

**Location category input (informative, non-authoritative):** `location.visual_landmark` (story #100) may provide a contributing signal when the detected landmark is privately owned. However, the `location.visual_landmark` field records landmark presence as a location observation — it does not make a property release determination. The Asset Intelligence Layer must make the property release determination independently. Story #100 is authoritative for the Locations category; this specification treats its fields as informative inputs, not authoritative triggers.

**What this flag does not determine:** Whether a specific property is privately owned is an implementation decision for the Asset Intelligence Layer. This specification documents the detection trigger and the flag's semantic meaning; ownership classification is not in scope.

**Example values:**
- `true` — a distinctive privately owned building is identifiable; property release evaluation required
- `false` — buildings or structures are present but none are identifiable as private property requiring a release (e.g., generic streetscape, public architecture with no distinctive private features)
- Field absent — no private property detectable in the image

---

### risk.editorial_only

| Attribute | Value |
|---|---|
| **Type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when `activities.editorial_event_signal = true` OR when a public figure or real-world news event is independently detected |

**What it records:** Classifies the asset as Editorial Use only. When `true`, the asset may not be used for commercial purposes without prior written consent of the subjects and/or copyright holder. Commercial channel Content Profiles must not generate Output Packages for this asset without a human review override.

**Trigger conditions:** This field is present when any of the following is true:
1. `activities.editorial_event_signal = true` (story #17 is authoritative for this field) — the image contains signals consistent with a real-world news or public event
2. A public figure (politician, celebrity, well-known public personality) is independently detected, regardless of `activities.editorial_event_signal`
3. A real-world news event is independently detected by the Risk Flag evaluation pass, regardless of `activities.editorial_event_signal`

Conditions 2 and 3 are independent detection paths. The Asset Intelligence Layer may detect editorial-only conditions through the Risk Flag evaluation pass even when the Activities category did not set `activities.editorial_event_signal = true`. Story #17 is authoritative for the Activities category; `activities.editorial_event_signal` is an input condition for this field, not the sole trigger.

**Commercial blocking consequence:** See "Editorial-Only Blocking Rule" above. When `risk.editorial_only = true`, commercial channel Content Profiles are blocked from generating Output Packages without a human review override. This is the flag that enforces commercial/editorial classification at the Layer 1 output boundary.

**False positive impact:** A staged commercial photograph incorrectly classified as a news event will have its entire commercial Output Package blocked. Detection sensitivity for editorial signals must be tuned with this consequence in mind.

**Example values:**
- `true` — a news event or public figure is detected; asset is Editorial Use only; commercial Output Package generation is blocked
- `false` — `activities.editorial_event_signal = true` was evaluated but determined not to require editorial-only classification upon full Risk Flag assessment; no public figure or news event independently detected
- Field absent — no editorial signal detected; field is not produced

---

### risk.adult_content

| Attribute | Value |
|---|---|
| **Type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when the image contains nudity, sexually suggestive content, or content inappropriate for general audiences |

**What it records:** Signals that the asset contains adult content. Triggers channel-specific restrictions and human review requirements as defined in individual Content Profile specifications.

**Trigger condition:** This field is present when the Asset Intelligence Layer detects any of the following:
- Nudity (full or partial)
- Sexually suggestive content or poses
- Content that is inappropriate for general audiences due to its sexual or adult nature

**Channel-specific handling:** The specific restrictions and review requirements triggered by `risk.adult_content = true` are defined in individual Content Profile specifications. This specification records the detection signal; downstream handling is a channel concern.

**Example values:**
- `true` — nudity or sexually suggestive content detected; channel-specific restrictions apply
- `false` — the image was evaluated for adult content but none was detected
- Field absent — the Risk Flag evaluation pass did not trigger an adult content detection path (implementation may omit the field when confidence is high that no adult content is present; however, if any ambiguity exists, `false` is the safer value to emit explicitly)

---

### risk.violence_flag

| Attribute | Value |
|---|---|
| **Type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when the image contains depictions of violence, injury, or distressing content |

**What it records:** Signals that the asset contains violent or distressing content. Triggers channel-specific restrictions and human review requirements as defined in individual Content Profile specifications.

**Trigger condition:** This field is present when the Asset Intelligence Layer detects any of the following:
- Depictions of physical violence or assault
- Visible injury, blood, or bodily harm
- Content that is distressing or disturbing in nature (e.g., graphic accident scenes, depictions of extreme distress)

**Channel-specific handling:** The specific restrictions and review requirements triggered by `risk.violence_flag = true` are defined in individual Content Profile specifications.

**Example values:**
- `true` — violence or distressing content detected; channel-specific restrictions apply
- `false` — the image was evaluated for violent content but none was detected
- Field absent — the Risk Flag evaluation pass did not trigger a violence detection path

---

### risk.trademark_flag

| Attribute | Value |
|---|---|
| **Type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when `text.logo_marks_detected` is non-empty OR when a third-party brand mark is detected |

**What it records:** Signals that a third-party trademark or brand mark is visible in the image. Commercial distribution may require rights clearance.

**Trigger conditions:** This field is present when either of the following is true:
1. `text.logo_marks_detected` (story #20) is non-empty — one or more logo marks have been identified in the Text and Logos category
2. A third-party brand mark is independently detected by the Risk Flag evaluation pass, even if `text.logo_marks_detected` is empty (e.g., an embossed or low-contrast brand mark that the text/logo detection did not capture)

Story #20 is authoritative for the Text and Logos category and the `text.logo_marks_detected` field. This specification treats story #20 as the primary input source for logo mark detection. The second trigger path (independent detection) exists to ensure that brand marks not captured by the Text and Logos detection pass are still flagged.

**Example values:**
- `true` — `text.logo_marks_detected` is non-empty (e.g., `["Nike swoosh"]`); trademark flag raised
- `true` — independent brand mark detection in Risk Flag pass; trademark flag raised even if `text.logo_marks_detected` is empty
- `false` — no logo marks in `text.logo_marks_detected` and no independent brand mark detected
- Field absent — no trademark detection path was triggered

---

### risk.confidence_score

| Attribute | Value |
|---|---|
| **Type** | float (0–1) |
| **Cardinality** | Required |
| **Condition** | Always present |

**What it records:** The confidence score for the Risk Flags evaluation pass as a whole. Reflects the detection sensitivity of the evaluation pass — not the certainty of any individual flag value.

**Semantics:** `risk.confidence_score` is a measure of how thoroughly and reliably the Asset Intelligence Layer was able to evaluate the asset for risk conditions. A high score means the evaluation pass had high detection sensitivity across all risk dimensions. A low score means the evaluation pass was operating under constrained detection conditions (e.g., due to image quality issues such as blur or low resolution).

**Critical distinction:** `risk.confidence_score` does not represent the certainty of any individual flag value. A flag set to `true` must be propagated regardless of this score (Consumer Rule 4). The score characterises the quality of the evaluation pass; it does not rate the reliability of individual detections.

**Valid range:** A float in the inclusive range [0.0, 1.0]. Values outside this range are invalid.

**Threshold values:** See [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) (story #84) for the provisional threshold (0.70). When `risk.confidence_score` is below threshold, `"risk"` must be added to `confidence.low_confidence_categories` by the Confidence Scores category finalisation step (story #21).

**Propagation interaction:** A `risk.confidence_score` below threshold does not suppress any flag. See "Propagation Rule — Consumer Rule 4" above for the full behaviour when `risk.confidence_score` is below threshold.

**Example values:**
- `0.92` — high detection sensitivity; Risk Flag evaluation pass ran under favourable image conditions
- `0.73` — moderate confidence; near but above the provisional 0.70 threshold
- `0.55` — below threshold; `"risk"` will appear in `confidence.low_confidence_categories`; absent flag fields must be treated as unknown by consumers, but active `true` flags must still be propagated in full

---

## Cross-Category Dependency Summary

| Risk Flag Field | Depends On | Authoritative Story |
|---|---|---|
| `risk.model_release_required` | `persons.present`, `persons.faces_detected` | Story #19 (People) |
| `risk.editorial_only` | `activities.editorial_event_signal` (primary input path) | Story #17 (Activities) |
| `risk.trademark_flag` | `text.logo_marks_detected` non-empty | Story #20 (Text and Logos) |
| `risk.property_release_required` | `location.visual_landmark` (informative, non-authoritative input) | Story #100 (Locations) |

Authoritative stories define the fields listed above. This specification documents how those fields are used as inputs to Risk Flag evaluation; it does not redefine them.

---

## Handoff 1 Validity Conditions

The Risk Flags category contributes to Handoff 1 validity in two ways:

| Handoff 1 Condition | Risk Flags Requirement |
|---|---|
| **Condition 3 — Risk Flags propagated:** all detected Risk Flags are present in the CAR regardless of confidence score ([docs/boundary-contracts.md](boundary-contracts.md)) | All `true` flag values must be present. A low `risk.confidence_score` does not permit any `true` flag to be absent. |
| **Risk Flag evaluation validity gate** | `risk.flags_evaluated = true` must be present. A CAR delivered without this field set to `true` is an invalid Handoff regardless of all other conditions. |

A CAR where `risk.flags_evaluated` is absent or `false`, or where any `true` risk flag has been omitted, does not satisfy Handoff 1. The Content Generation Layer must reject it.

---

## Edge Cases

**`risk.editorial_only = true` and commercial channel request:** The Content Generation Layer receives a request to generate an Output Package using a commercial channel Content Profile (e.g., `stock/adobe-stock`) for an asset where `risk.editorial_only = true`. The correct response is to block generation and surface the editorial-only constraint to the requesting process. Generation must not proceed without a human review override. The override mechanism is planned for MVP4.

**`risk.model_release_required` and `persons.present = false`:** If `persons.present = false`, `risk.model_release_required` must be absent from the CAR. A value of `false` is not the correct representation when no persons are present — absence is correct. Emitting `false` when `persons.present = false` is an implementation error.

**`risk.trademark_flag` and empty `text.logo_marks_detected`:** The trademark flag has two trigger paths. If `text.logo_marks_detected` is an empty array (`[]`), the flag may still be triggered by the independent detection path in the Risk Flag evaluation pass. Implementers must not skip independent brand mark detection because the Text and Logos category found nothing.

**All six Conditional fields absent:** If no risk conditions are detected, all six Conditional fields are absent from the CAR. Only `risk.flags_evaluated = true` and `risk.confidence_score` are present. This is a valid state indicating a clean evaluation pass with no flagged conditions.

**`risk.flags_evaluated = false` delivered:** This is invalid. A CAR with `risk.flags_evaluated = false` must not be delivered to the Content Generation Layer. If the evaluation pass fails mid-run, the CAR must be discarded and the failure surfaced to the producing system.

**`risk.adult_content` and `risk.violence_flag` both triggered:** Both flags may be present simultaneously. Each flag is evaluated independently. Both must be emitted if both conditions are met. Downstream channel restrictions may differ per flag; both must be propagated.

---

## Consistency with Field Catalogue

This specification is consistent with and does not supersede the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)). In any conflict between this document and the Field Catalogue, the Field Catalogue is authoritative for field names, types, and cardinality. This document is authoritative for population rules, trigger conditions, cross-category dependencies, and implementation constraints layered on top of the catalogue definitions.

**No field catalogue deviations.** This specification introduces no new field names and proposes no revisions to Section 6 of the Field Catalogue.

---

## Cross-References

- **CAR Field Catalogue** — [docs/car-field-catalogue.md](car-field-catalogue.md): Section 6, authoritative source for all eight Risk Flags field names, types, and cardinality.
- **CAR Concept Definition (story #15)** — [docs/canonical-asset-record.md](canonical-asset-record.md): Risk Flags category definition; Consumer Rules 1–4; Rule 4 (flags propagated regardless of confidence) is the governing rule for this category.
- **Boundary Contracts (story #77)** — [docs/boundary-contracts.md](boundary-contracts.md): Handoff 1 validity conditions; Condition 3 (Risk Flags propagated) and the `risk.flags_evaluated` validity gate.
- **Confidence Thresholds and Risk Flag Handling Rules (story #84)** — [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md): the provisional 0.70 threshold; risk-below-threshold special case.
- **People Category Specification (story #19)** — [docs/car-people-spec.md](car-people-spec.md): authoritative for `persons.present` and `persons.faces_detected`.
- **Activities Category Specification (story #17)** — [docs/car-activities-spec.md](car-activities-spec.md): authoritative for `activities.editorial_event_signal`.
- **Text and Logos Category Specification (story #20)** — [docs/car-text-logos-spec.md](car-text-logos-spec.md): authoritative for `text.logo_marks_detected`.
- **Locations Category Specification (story #100)** — [docs/car-locations-spec.md](car-locations-spec.md): authoritative for `location.visual_landmark`.
- **Domain Glossary** — [docs/glossary.md](glossary.md): Canonical Asset Record, Risk Flag, Handoff, Asset Intelligence Layer, Content Generation Layer, Output Package, Content Profile.
