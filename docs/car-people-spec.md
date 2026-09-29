# CAR People Category — Field Specification

> **Story #19 — Implementation-ready field specification for the People category of the Canonical Asset Record.**
> All field names, types, cardinalities, and conditions in this document are consistent with the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)). Any conflict between this document and the Field Catalogue must be resolved in favour of the Field Catalogue, with a corresponding update here.

---

## Overview

The People category of the Canonical Asset Record (CAR) records observable facts about human presence in a Photo asset. It answers the question: are persons present, how many, are faces visible, what broad age signals are observable, how is any group composed, and what posture or activity is dominant?

All observations in this category are factual and channel-agnostic. The People category makes no content decisions, generates no metadata, and does not serve any specific distribution destination. It is produced exclusively by the Asset Intelligence Layer (Layer 1) as part of the CAR, and is consumed exclusively by the Content Generation Layer (Layer 2) alongside a Content Profile.

This specification covers all seven People fields. A Layer 1 developer reading this document should know exactly what to populate, under what conditions, and with what values in order to produce a valid CAR Handoff for the People category.

---

## Scope

This specification covers Photo assets only. Photo is the sole Asset Type in scope through MVP6. Video and Vector asset types are out of scope; their People field behaviour will be addressed in a future revision at MVP10.

The following are explicitly out of scope for this document:

- Confidence score threshold values — those are defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md).
- Storage format and serialisation structure (JSON, Protobuf, etc.) — an MVP1 decision.
- Content Profile rules that consume People fields — those belong in individual Content Profile specifications.
- Risk Flags that are triggered by People fields — `risk.model_release_required` is specified in the CAR Field Catalogue and in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md); it is cross-referenced here but not re-specified.

---

## Privacy Constraints

No field in the People category may record the identity of any individual depicted in an asset. The Asset Intelligence Layer must not attempt facial recognition or any identity-resolution technique.

`persons.faces_detected` is the only People field that relates to faces. It records only whether at least one face is sufficiently visible to be potentially identifiable — a binary signal for downstream compliance routing (specifically, `risk.model_release_required` evaluation). It does not record who the person is, store a facial embedding, or produce any identity claim.

This constraint is absolute. An implementation that stores any individual identity signal — name, identity hash, biometric descriptor, or similar — in any People field constitutes a defect regardless of confidence level.

---

## Gender Field Exclusion

The CAR People category contains no field recording or inferring the gender of any person depicted in an asset. This is a final Product Owner decision, not a placeholder or an omission pending future implementation.

**Rationale recorded for implementers:** Gender inference from visual analysis is unreliable, carries a high rate of misclassification, and introduces discrimination risk across downstream channel metadata. No downstream Content Profile has been identified that requires a gender signal from the CAR that cannot be served through other observable signals (group composition, activity, age range, posture). Adding a gender field in the future would require an explicit PO decision and a revision to this specification.

Implementers must not add a gender field to the People category. Any model output relating to gender must be discarded and must not be stored or surfaced in the CAR.

---

## persons.present Dependency Chain

`persons.present` is the root gate for the entire People category. All other People fields depend on it directly or indirectly. The evaluation chain is as follows:

```
1. Evaluate persons.present (Required — always populated)
   │
   ├─ persons.present = false
   │     → persons.count          ABSENT (do not evaluate)
   │     → persons.faces_detected ABSENT (do not evaluate)
   │     → persons.age_range_signals ABSENT (do not evaluate)
   │     → persons.group_composition ABSENT (do not evaluate)
   │     → persons.activity_posture  ABSENT (do not evaluate)
   │     (persons.confidence_score is still populated — Required)
   │
   └─ persons.present = true
         │
         ├─ Evaluate persons.count (Required when present = true)
         │     │
         │     ├─ persons.count = 1
         │     │     → persons.group_composition  ABSENT (condition not met)
         │     │
         │     └─ persons.count >= 2
         │           → Evaluate persons.group_composition (Conditional — condition met)
         │           → Also: activities.social_context in Activities category is evaluated
         │
         ├─ Evaluate persons.faces_detected (Conditional — present = true)
         │
         ├─ Evaluate persons.age_range_signals (Conditional — present = true
         │     AND age signals are detectable with sufficient confidence)
         │
         ├─ Evaluate persons.activity_posture (Conditional — present = true
         │     AND a dominant posture or activity is detectable)
         │
         └─ persons.confidence_score is populated (Required — always)
```

The key invariant: `persons.present = false` means ALL other People fields are absent. They are not evaluated, not set to null, and not set to a default value — they are entirely absent from the CAR. A CAR consumer reading an absent People field when `persons.present` is `false` must treat that absence as a confirmed negative (no persons present), consistent with how the dependency chain was evaluated. This is the one case in the CAR where an absent Conditional field has a known interpretation rather than an unknown one, because the gate field (`persons.present`) is Required and explicitly states the reason for absence.

---

## Field Specifications

### persons.present

| Attribute | Value |
|---|---|
| **Field name** | `persons.present` |
| **Data type** | boolean |
| **Cardinality** | Required |
| **Condition** | None — always evaluated and always present in every valid CAR for a Photo asset |
| **Allowed values** | `true` or `false` |
| **Absence rule** | This field is never absent. Absence constitutes an invalid Handoff 1. |

**Description:** `true` if one or more persons are detectable anywhere in the image; `false` if no persons are detectable. This field is the root gate for the entire People category. When `false`, all other People fields must be absent.

**Evaluation guidance:** The Asset Intelligence Layer should set `persons.present = true` whenever any human figure is detectable — including partial figures (a hand, a silhouette, a figure at a distance), figures photographed from behind, figures partially obscured, or figures in the extreme background. The threshold is detectability, not clear visibility or identifiability.

**Example — true:** An image of a person working at a standing desk. `persons.present = true`.

**Example — false:** An image of a standing desk with a laptop and a potted plant and no human visible anywhere. `persons.present = false`. All other People fields are absent.

---

### persons.count

| Attribute | Value |
|---|---|
| **Field name** | `persons.count` |
| **Data type** | integer |
| **Cardinality** | Conditional |
| **Condition** | Present when `persons.present` is `true` |
| **Allowed values** | Any positive integer ≥ 1. The value `0` must never appear. |
| **Absence rule** | Absent when `persons.present` is `false`. Absent when `persons.present` is `true` but the count cannot be determined with sufficient confidence (treat as unknown per CAR Consumer Rule 2 — see note below). |

**Description:** The number of individual persons detected in the image. This field enables group composition evaluation and drives `activities.social_context` eligibility.

**Zero-value prohibition:** `persons.count = 0` is never valid. If analysis produces a count of zero, the correct representation is `persons.present = false` and `persons.count` absent. A count of zero is a logical contradiction — if no persons are detected, `persons.present` must be `false`. Any implementation path that would produce `persons.count = 0` is a defect.

**Note on absence when present = true:** In rare cases where `persons.present` is `true` (a person is detectable) but the Asset Intelligence Layer cannot determine a reliable count (for example, a crowd so dense that individual figures cannot be separated), `persons.count` may be absent even when `persons.present` is `true`. Consumers must apply CAR Consumer Rule 1 (treat absent field as unknown) in that case. This does not affect the presence of `persons.group_composition`; if count is absent, `group_composition` is also absent.

**Example:** An image showing two people at a conference table. `persons.count = 2`.

**Example:** An image showing a single athlete running. `persons.count = 1`.

---

### persons.faces_detected

| Attribute | Value |
|---|---|
| **Field name** | `persons.faces_detected` |
| **Data type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when `persons.present` is `true` |
| **Allowed values** | `true` or `false` |
| **Absence rule** | Absent when `persons.present` is `false`. |

**Description:** `true` if at least one face in the image is sufficiently visible that the person could potentially be identified from the image. `false` if persons are present but no face is sufficiently visible — for example, figures photographed from behind, figures at significant distance with no face discernible, or figures whose faces are obstructed by objects.

**Privacy constraint:** This field signals identifiability potential only. It does not record who the person is, store any facial descriptor, or perform identity resolution. Its sole purpose is to enable accurate evaluation of `risk.model_release_required` in the Risk Flags category.

**Downstream dependency:** When `persons.faces_detected = true`, the Risk Flags category must evaluate `risk.model_release_required`. When `persons.faces_detected = false`, `risk.model_release_required` may still be evaluated if persons are prominently featured even without a visible face (see the CAR Field Catalogue, Risk Flags section).

**Example — true:** A portrait photograph showing a person's face clearly. `persons.faces_detected = true`.

**Example — false:** A photograph of two cyclists shot from behind on a trail, no faces visible. `persons.faces_detected = false`.

---

### persons.age_range_signals

| Attribute | Value |
|---|---|
| **Field name** | `persons.age_range_signals` |
| **Data type** | Array\<string\> |
| **Cardinality** | Conditional |
| **Condition** | Present when `persons.present` is `true` AND age signals are detectable with sufficient confidence |
| **Allowed values** | Closed enum — exactly the following four values: `child`, `adult`, `senior`, `other` |
| **Absence rule** | Absent when `persons.present` is `false`. Absent when `persons.present` is `true` but no age signals are detectable with sufficient confidence. |

**Description:** An array of broad age-range labels observable in the image. Each entry represents a detectable age signal for one or more persons in the image. The array may contain multiple values when persons of different age ranges are present (e.g., a child and an adult together).

**Closed enum — no additional values permitted:**

| Value | Meaning |
|---|---|
| `child` | One or more persons with visual signals consistent with childhood (typically pre-adolescent) |
| `adult` | One or more persons with visual signals consistent with adulthood |
| `senior` | One or more persons with visual signals consistent with older adulthood |
| `other` | One or more persons display detectable age signals that cannot be reliably mapped to `child`, `adult`, or `senior` |

The value `other` is the correct choice when the Asset Intelligence Layer detects age signals but cannot classify them into one of the three primary labels with sufficient confidence. It must not be used as a catch-all for all persons; it is specifically for cases where signals are present but indeterminate relative to the primary three.

No additional values are permitted. The implementer must not introduce values such as `teenager`, `middle_aged`, `elderly`, or any numeric age estimate. The enum is final.

**Array semantics:** The array reflects the set of distinct age signals observable across all persons in the image. If the image contains two adults and one child, the array is `["adult", "child"]`. Each value appears at most once regardless of how many persons match it.

**Example:** A lifestyle photograph of a grandparent with a grandchild. `persons.age_range_signals = ["adult", "child"]` or `["senior", "child"]` depending on what signals are observable.

**Example:** A headshot of a single professional. `persons.age_range_signals = ["adult"]`.

**Example — absent:** A photograph of a distant crowd in which no individual age signals are detectable with sufficient confidence. `persons.present = true`, `persons.count` present, but `persons.age_range_signals` absent.

---

### persons.group_composition

| Attribute | Value |
|---|---|
| **Field name** | `persons.group_composition` |
| **Data type** | string (enum) |
| **Cardinality** | Conditional |
| **Condition** | Present when `persons.count` is 2 or more |
| **Allowed values** | Closed enum: `couple`, `small_group`, `large_group`, `crowd` |
| **Absence rule** | Absent when `persons.present` is `false`. Absent when `persons.count` is 1 (single person — no group). Absent when `persons.count` is absent. |

**Description:** A high-level descriptor of the group composition of persons detected in the image. Enables the Content Generation Layer to anchor group-appropriate descriptions, lifestyle keyword sets, and social context signals.

**Closed enum with count ranges:**

| Value | Count range | Meaning |
|---|---|---|
| `couple` | Exactly 2 | Two persons; the composition suggests a pair (does not infer relationship type) |
| `small_group` | 3–5 | Three to five persons identifiable as individuals |
| `large_group` | 6 or more | Six or more individually distinguishable persons |
| `crowd` | Indeterminate large number | A large undifferentiated group where individual figures are not separately countable |

**Count-to-value mapping rule:** The Asset Intelligence Layer must select the enum value based on `persons.count` where count is known. When `persons.count` is not determinable (dense crowd) but persons are clearly present in large numbers, `crowd` is the appropriate value and `persons.count` may be absent.

**Relationship note:** `persons.group_composition` does not infer relationship type (e.g., it does not assert that two persons are a romantic couple, family members, or colleagues). It records only the observable group size class. The label `couple` means exactly two persons in the frame; relationship interpretation belongs to the Content Generation Layer, guided by the active Content Profile.

**Example:** An image of two people shaking hands. `persons.count = 2`, `persons.group_composition = "couple"`.

**Example:** A team photo with four people. `persons.count = 4`, `persons.group_composition = "small_group"`.

**Example:** A street photograph of a busy market with more than twenty people. `persons.group_composition = "crowd"`. `persons.count` may be absent.

---

### persons.activity_posture

| Attribute | Value |
|---|---|
| **Field name** | `persons.activity_posture` |
| **Data type** | string |
| **Cardinality** | Conditional |
| **Condition** | Present when `persons.present` is `true` AND a dominant posture or activity is detectable |
| **Allowed values** | Free-form short label (concise noun phrase or verb phrase) — not an enum; examples below |
| **Absence rule** | Absent when `persons.present` is `false`. Absent when no dominant posture or activity is detectable with sufficient confidence. |

**Description:** A concise label for the person's or group's dominant observable posture or interaction state. This field complements the Activities category for lifestyle and editorial assets. It captures the physical state or posture of the primary person or group at the moment depicted, rather than a full activity classification (which belongs in `activities.detected_activities`).

**Format guidance:** The value should be a short plain-language noun phrase or verb phrase (typically two to four words). It is not an enum; the Asset Intelligence Layer should select the label that most accurately and concisely describes the observable posture or state. Overly specific or interpretive labels should be avoided; the label should be factually observable.

**Representative examples (not exhaustive):**

- `"standing"` — person or group is standing upright
- `"seated"` — person or group is seated
- `"facing camera"` — primary person is oriented toward the camera
- `"in profile"` — primary person is oriented sideways to the camera
- `"walking"` — person or group in motion, walking
- `"gesturing"` — person's hands or arms are in an expressive gesture
- `"hands on keyboard"` — person interacting with a keyboard

**Relationship to Activities category:** `persons.activity_posture` captures the dominant physical posture or immediate state. The Activities category (`activities.detected_activities`, `activities.primary_activity`) captures the activity or event being performed. Both fields may be present simultaneously and complement each other. Neither is a substitute for the other.

**Example:** A photograph of a professional giving a presentation to a small group. `persons.activity_posture = "gesturing"`. The Activities category may simultaneously record `activities.primary_activity = "presenting"`.

**Example — absent:** A dense crowd photograph where no single dominant posture is identifiable. `persons.present = true`, but `persons.activity_posture` is absent.

---

### persons.confidence_score

| Attribute | Value |
|---|---|
| **Field name** | `persons.confidence_score` |
| **Data type** | float (0–1) |
| **Cardinality** | Required |
| **Condition** | None — always present in every valid CAR for a Photo asset |
| **Allowed values** | Any float in the closed interval [0.0, 1.0] inclusive |
| **Absence rule** | This field is never absent. Absence constitutes an invalid Handoff 1. |

**Description:** The Asset Intelligence Layer's analytical certainty in its People category findings as a whole. A score of 1.0 represents maximum certainty; 0.0 represents minimum certainty. This score reflects confidence in the category analysis, not the quality or commercial value of the asset.

**Important — this field is always present, even when `persons.present = false`.** If the Asset Intelligence Layer determines with high confidence that no persons are present, `persons.confidence_score` should reflect that confidence (e.g., a high score). If the layer is uncertain whether persons are present (for example, an ambiguous silhouette), the score reflects that uncertainty and `persons.present` reflects the best determination under that uncertainty.

**Threshold policy:** The minimum threshold value for acting on People category fields as confirmed observations is defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md). When `persons.confidence_score` is below that threshold, consumers must apply CAR Consumer Rule 2 and treat all People fields as unknown. Threshold values are provisional at MVP0 (0.70, provisional — confirm at MVP1).

**Relationship to `confidence.low_confidence_categories`:** If `persons.confidence_score` is below the minimum threshold, the Asset Intelligence Layer must include `"persons"` in `confidence.low_confidence_categories`.

**Example:** A clear portrait photograph with high-quality face detection. `persons.confidence_score = 0.95`.

**Example:** An image with an ambiguous distant silhouette that may or may not be a person. `persons.present = true` (best determination), `persons.confidence_score = 0.52` (low confidence — consumers must apply Rule 2).

---

## Cross-Category Note: activities.social_context

The Activities category field `activities.social_context` (string enum: `solo`, `pair_interaction`, `group_activity`, `crowd_event`) is Conditional on the presence of multiple persons and a detectable social interaction.

**The threshold that links People and Activities:** `persons.count >= 2` is the necessary condition for `activities.social_context` to be evaluated. When `persons.count` is 1 or `persons.count` is absent, `activities.social_context` must not be populated.

This coupling must be maintained consistently across both categories:

- The People category establishes the count; the Activities category consumes it.
- If `persons.count` is updated or its evaluation logic changes, the `activities.social_context` condition must be reviewed simultaneously to ensure both categories remain consistent.
- A CAR where `activities.social_context` is present but `persons.count` is 1 (or absent) is internally inconsistent and constitutes an invalid Handoff.

Layer 1 implementers working on both categories must coordinate to ensure this threshold is applied identically in both evaluation paths.

---

## Edge Cases

**1. Exactly one person, no face visible, small in frame**
`persons.present = true`, `persons.count = 1`, `persons.faces_detected = false`. `persons.group_composition` is absent (count = 1). `persons.age_range_signals` may be absent if no age signals are detectable. `persons.activity_posture` populated if posture is determinable (e.g., `"walking"`).

**2. Dense crowd, individual count indeterminate**
`persons.present = true`. `persons.count` absent (count not determinable reliably — treat as unknown per Rule 1). `persons.group_composition = "crowd"`. `persons.faces_detected` evaluated based on any individually visible face in the crowd. `activities.social_context` may be absent if `persons.count` is absent (condition not met).

**3. Partial figure — hand only visible**
A close-up of hands on a keyboard. A human hand is a person-detectable signal. `persons.present = true`. `persons.count = 1` (if only one set of hands is visible). `persons.faces_detected = false`. `persons.age_range_signals` may be absent or populated if the hands provide age signals (e.g., visibly aged hands → `["senior"]`). `persons.activity_posture = "hands on keyboard"`.

**4. Mixed age group**
An image with a child, an adult, and a senior. `persons.count = 3`, `persons.group_composition = "small_group"`, `persons.age_range_signals = ["child", "adult", "senior"]`.

**5. persons.present = true, persons.confidence_score below threshold**
The Asset Intelligence Layer detected a person but with low confidence. `persons.present = true`, `persons.confidence_score = 0.48` (below provisional 0.70 threshold). `"persons"` is added to `confidence.low_confidence_categories`. All downstream consumers must treat all People fields as unknown (CAR Consumer Rule 2). Risk flag evaluation for `risk.model_release_required` still applies — CAR Consumer Rule 4 requires risk flags to be propagated regardless of confidence score.

**6. persons.present = false, confidence is high**
No persons anywhere in the image. `persons.present = false`, `persons.confidence_score = 0.97`. All other People fields are absent. `risk.model_release_required` is absent (condition `persons.present = true` not met).

---

## Consistency with Field Catalogue

This specification is derived from and must remain consistent with the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md), story #78). The following table maps each field in this document to its catalogue entry and confirms alignment.

| Field | Catalogue Type | Catalogue Cardinality | Catalogue Condition | Consistent with this spec |
|---|---|---|---|---|
| `persons.present` | boolean | Required | — | Yes |
| `persons.count` | integer | Conditional | `persons.present` is `true` | Yes |
| `persons.faces_detected` | boolean | Conditional | `persons.present` is `true` | Yes |
| `persons.age_range_signals` | Array\<string\> | Conditional | `persons.present` is `true` AND age signals detectable | Yes — enum values (`child`, `adult`, `senior`, `other`) are a refinement of the catalogue's indicative examples |
| `persons.group_composition` | string (enum) | Conditional | `persons.count` is 2 or more | Yes — enum values and count ranges are a refinement of the catalogue's indicative entry |
| `persons.activity_posture` | string | Conditional | `persons.present` is `true` AND dominant posture detectable | Yes |
| `persons.confidence_score` | float (0–1) | Required | — | Yes |

**Note on refinements:** The CAR Field Catalogue provides indicative descriptions and examples for `persons.age_range_signals` and `persons.group_composition`. This specification adds the closed enum definitions and count-range mappings that the catalogue did not fully enumerate. These additions are refinements, not conflicts. If any future revision of the catalogue modifies the field types, conditions, or cardinalities above, this document must be updated accordingly.

---

## Cross-References

- **CAR concept definition (story #15):** [docs/canonical-asset-record.md](canonical-asset-record.md) — People category concept definition; Consumer Rules 1–4 that govern interpretation of all People fields.
- **CAR Field Catalogue (story #78):** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative source for all People field names, types, and cardinalities. This document is consistent with and subordinate to the catalogue.
- **Confidence score thresholds (story #84):** [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) — minimum threshold for `persons.confidence_score`; `confidence.low_confidence_categories` population rule; risk flag handling policies including `risk.model_release_required`.
- **Domain Glossary:** [docs/glossary.md](glossary.md) — Canonical Asset Record, Asset Intelligence Layer, Content Generation Layer, Confidence Score, Risk Flag, Handoff, Content Profile, Output Package.
