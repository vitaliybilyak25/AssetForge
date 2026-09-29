# CAR Activities Category — Field Specification

> **Story #17 — Draft v0.1**
> This document is the implementation-ready field specification for the Activities category of the Canonical Asset Record (CAR). It is the authoritative reference for any Layer 1 (Asset Intelligence Layer) developer producing activities fields in a CAR Handoff. All field names, types, and cardinality in this document are taken from the **CAR Field Catalogue** ([docs/car-field-catalogue.md](car-field-catalogue.md), story #78) and must not conflict with it. In any conflict, the Field Catalogue governs and this document must be updated accordingly.

---

## Overview

The Activities category records dynamic events and actions that are observable within the asset. It answers the question: *What is happening in this image?* — independently of any audience, channel, or intended use.

Activities observations are factual, frame-level inferences. They describe motion, interaction, and event type as visible evidence, not as editorial judgement. The Content Generation Layer reads these fields to anchor lifestyle descriptions, select relevant keywords, and apply editorial classification gatekeeping.

The Activities category contains six fields: one array of detected activity labels, one dominant activity label, two enum classification fields (social context and physical intensity), one boolean editorial event signal, and one category-level confidence score. All fields except `activities.confidence_score` are Conditional; none are Required in isolation.

---

## Scope

**In scope:** Photo assets only. All activity detection is single-frame inference — what is observable from a still image.

**Out of scope until MVP10:** Video and vector assets. Time-based inference (action sequences, motion analysis across frames, scene transitions) is deferred. No Activities field in this specification may be populated using temporal reasoning; every value must be derivable from a single image frame.

---

## Field Specifications

### activities.detected_activities

| Attribute | Value |
|---|---|
| **Field name** | `activities.detected_activities` |
| **Data type** | Array\<string\> |
| **Cardinality** | Conditional |
| **Condition** | Present when one or more activities or actions are detectable with sufficient confidence |

**Allowed values / format:** Each array entry is a short verb phrase describing a single observable activity or dynamic event (e.g., `"working at a desk"`, `"cooking"`, `"hiking"`, `"playing guitar"`, `"running"`, `"shaking hands"`). Entries are plain, lowercase verb phrases. The array must contain at least one entry when present; a zero-length array must not be produced.

**Absence rule:** The field is absent — not present as an empty array — when no activities are detectable or when detection confidence is below the minimum threshold. Absence means the Asset Intelligence Layer did not detect any activities with sufficient certainty. A downstream consumer must treat an absent `activities.detected_activities` as unknown, not as confirmation that no activities exist (CAR Consumer Rule 1). The consumer must not infer a negative or default to a "no activity" assumption.

> **CAR Consumer Rule 1 applies.** An absent field is unknown, not negative. Do not substitute an empty list or a "none detected" value when this field is absent.

**Ordering:** Entries are not required in any specific order. Ordering by detection confidence (highest first) is recommended but not mandatory.

**Example values:**
```json
"activities.detected_activities": ["hiking", "carrying a backpack"]
"activities.detected_activities": ["working at a desk", "typing", "reading documents"]
"activities.detected_activities": ["playing guitar", "sitting cross-legged"]
```

---

### activities.primary_activity

| Attribute | Value |
|---|---|
| **Field name** | `activities.primary_activity` |
| **Data type** | string |
| **Cardinality** | Conditional |
| **Condition** | Present when a single dominant activity is identifiable with high confidence |

**Allowed values / format:** A single short verb phrase, consistent in style with the entries in `activities.detected_activities`. The value must appear as an entry in `activities.detected_activities` when that field is also present; it must not introduce a label not already recorded there.

**Absence rule:** Absent when: (a) no activities are detected; (b) multiple activities are detected but none is clearly dominant; or (c) confidence in the dominant activity falls below the minimum threshold. Absence means the layer could not identify a single dominant activity with high confidence. Consumers must treat an absent `activities.primary_activity` as unknown and must not select or infer a primary activity from `activities.detected_activities` themselves (CAR Consumer Rule 1).

**Selection rule when multiple activities are detected:** The primary activity is the single activity that is most visually prominent and compositionally central in the frame — the activity that a human viewer would most likely identify as the image's main subject of action. The selection criteria, in order of priority:

1. The activity performed by the compositionally dominant subject (foreground, largest figure, or centred subject).
2. The activity occupying the greatest proportion of the image frame.
3. The activity most clearly in focus relative to the depth of field.

If no single activity satisfies these criteria clearly above the others, `activities.primary_activity` must be absent. The selection must not be based on keyword popularity or downstream channel relevance; it is a purely observational judgement about the image's visual structure.

**Relationship to `activities.detected_activities`:** `activities.primary_activity` is a derived selection from `activities.detected_activities`. If `activities.detected_activities` is absent, `activities.primary_activity` must also be absent.

**Example values:**
```json
"activities.primary_activity": "hiking"
"activities.primary_activity": "cooking"
"activities.primary_activity": "working at a desk"
```

---

### activities.social_context

| Attribute | Value |
|---|---|
| **Field name** | `activities.social_context` |
| **Data type** | string (enum) |
| **Cardinality** | Conditional |
| **Condition** | Present when multiple persons are present and a social interaction is detectable |

**Cross-category dependency:** This field has a hard dependency on the People category. It is only valid when `persons.count >= 2`. The `persons.count` field is itself Conditional on `persons.present = true`. See the Cross-Category Dependencies section for the full dependency chain and handling rules when the upstream field is absent or below threshold.

**Allowed values:**

| Value | Definition |
|---|---|
| `solo` | A single person is depicted; the social context is individual rather than interpersonal. Present only when activity detection establishes a meaningful individual context (e.g., solo sport, solitary work). Note: because this field is conditional on multiple persons being present, `solo` is a reserved value for cases where social context is evaluable but the person count resolves to one after re-evaluation. In practice, `solo` is rarely populated under the Conditional rule as stated; see Edge Cases. |
| `pair_interaction` | Two persons are depicted in an observable interaction — direct communication, physical proximity indicating relationship, collaborative action, or similar interpersonal engagement. |
| `group_activity` | Three or more persons are depicted engaging in a shared activity with a common purpose (team sport, collaborative work, group discussion, family activity). |
| `crowd_event` | A large number of persons are depicted in a public or semi-public setting, typically associated with an event, gathering, or unscripted public occurrence (protest, concert, sporting event audience, street crowd). |

> **Catalogue alignment note:** The CAR Field Catalogue (story #78, Section 5) currently lists the enum values as `solo`, `pair_interaction`, `group_activity`, `crowd_event`. This specification uses those authoritative values. Any future revision that changes the enum values must update both this document and the Field Catalogue simultaneously.

**Absence rule:** Absent when: (a) `persons.count` is absent or below the confidence threshold; (b) fewer than two persons are detectable; (c) multiple persons are present but no discernible social interaction is detectable; or (d) `activities.confidence_score` is below the minimum threshold. Consumers must treat an absent `activities.social_context` as unknown (CAR Consumer Rule 1) — absence does not mean no social context exists; it means the layer did not produce a confident finding.

**Example values:**
```json
"activities.social_context": "pair_interaction"
"activities.social_context": "group_activity"
"activities.social_context": "crowd_event"
```

---

### activities.physical_intensity

| Attribute | Value |
|---|---|
| **Field name** | `activities.physical_intensity` |
| **Data type** | string (enum) |
| **Cardinality** | Conditional |
| **Condition** | Present when a physical activity is detected and intensity is estimable from visual evidence |

**Scope of application:** This field applies to any visually detectable physical activity or dynamic event — it is not restricted to person-present scenarios. Physical intensity is equally valid for non-person subjects: a waterfall (natural physical force), a moving vehicle (mechanical energy), a ball in flight (projectile motion), breaking waves, or any other subject that exhibits observable physical energy or dynamism. The evaluating question is: *What level of physical energy or dynamic force does this image convey?*

**Allowed values:**

| Value | Definition |
|---|---|
| `sedentary` | No physical movement or force is observable. The depicted subject or scene is at rest (e.g., a person seated reading, a still landscape, a stationary vehicle). |
| `light` | Low-energy, gentle movement or mild physical activity (e.g., walking slowly, light stretching, a gentle stream, a child playing quietly). |
| `moderate` | Sustained physical effort or noticeable movement without extreme exertion (e.g., cycling, hiking with pack, cooking, a moderately flowing river, a car at normal road speed). |
| `vigorous` | High-intensity physical effort or strong dynamic force (e.g., sprinting, competitive sport, heavy labour, a waterfall at full flow, a vehicle in high-speed motion, a ball at peak trajectory). |

> **Catalogue alignment note:** The CAR Field Catalogue (story #78, Section 5) lists the enum values as `sedentary`, `light`, `moderate`, `vigorous`. This specification uses those authoritative values as the implementation-ready set.

**Absence rule:** Absent when: (a) no physical activity or dynamic event is detectable; (b) the image is fully static and no intensity estimation is meaningful; or (c) a physical event is detectable but intensity cannot be estimated from the single frame with sufficient confidence. Consumers must treat an absent `activities.physical_intensity` as unknown (CAR Consumer Rule 1).

**Example values:**
```json
"activities.physical_intensity": "vigorous"    // sprinting athlete
"activities.physical_intensity": "moderate"    // person hiking on trail
"activities.physical_intensity": "sedentary"   // person seated at desk
"activities.physical_intensity": "vigorous"    // waterfall at full flow
"activities.physical_intensity": "moderate"    // car on motorway
```

---

### activities.editorial_event_signal

| Attribute | Value |
|---|---|
| **Field name** | `activities.editorial_event_signal` |
| **Data type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when the image contains signals consistent with a real-world news or public event |

**Allowed values:** `true` or `false`. When present, the field must be explicitly set; it must never be absent as a substitute for `false`.

- `true` — The activity depicted appears to be a real-world, unscripted event: a protest, public demonstration, sports event (in progress, not a posed/studio context), political ceremony, news moment, concert, or similar occurrence that would typically require editorial rather than commercial licensing. The image signals that the depicted action is documentary in nature rather than staged.
- `false` — The image was evaluated for editorial event signals and none were detected. The depicted activity appears to be staged, posed, or otherwise consistent with a commercial stock scenario.

**When to emit `false` vs. when to omit:** The field is Conditional — it is only present when the layer evaluated an activity pattern consistent with event photography. If no such evaluation was triggered (e.g., the image is a simple object shot with no persons or public-space context), the field is absent. `false` is only set when the evaluation was performed and produced a negative result. Do not set `false` as a default for all non-event images; emit the field only when the evaluation is meaningful.

**Absence rule:** Absent when no activity pattern was evaluated for editorial event signals. Absence means the layer did not produce a finding for this field. Consumers must treat an absent `activities.editorial_event_signal` as unknown (CAR Consumer Rule 1) — absence is not an implicit commercial clearance.

**Cross-category effect — Risk Flags dependency:** Setting `activities.editorial_event_signal = true` is a direct input condition for evaluating `risk.editorial_only` in the Risk Flags category. The Asset Intelligence Layer must evaluate `risk.editorial_only` whenever `activities.editorial_event_signal` is `true`. See the Cross-Category Dependencies section for the full downstream chain. Refer to [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) for the handling policy applied when `risk.editorial_only` is set.

**Example values:**
```json
"activities.editorial_event_signal": true    // crowd at a public protest
"activities.editorial_event_signal": false   // staged business meeting scenario
```

---

### activities.confidence_score

| Attribute | Value |
|---|---|
| **Field name** | `activities.confidence_score` |
| **Data type** | float (0–1) |
| **Cardinality** | Required |
| **Condition** | — (always present) |

**Allowed values / format:** A floating-point number in the closed interval [0.0, 1.0], inclusive. A value of `1.0` represents maximum analytical certainty in the Activities category findings. A value of `0.0` represents zero certainty. The score reflects the Asset Intelligence Layer's certainty in the Activities category as a whole — it is a category-level signal, not a per-field score.

**Semantics:** The confidence score does not indicate whether activities were found or not found; it indicates how certain the layer is in whatever findings it produced. A high confidence score on an empty Activities category (no Conditional fields present) means the layer is confident there are no detectable activities. A low confidence score means the layer's analysis was uncertain, regardless of whether fields are present or absent.

**Threshold:** The minimum threshold for a downstream consumer to act on Activities category fields as confirmed observations is **0.70 (provisional — confirm at MVP1)**. If `activities.confidence_score` is below this threshold, the consumer must treat all Activities fields as unknown and apply CAR Consumer Rule 2. The threshold value and its implications are fully specified in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md).

**Relationship to `confidence.low_confidence_categories`:** If `activities.confidence_score` is strictly below the minimum threshold, the Asset Intelligence Layer must add `"activities"` to the `confidence.low_confidence_categories` array, as specified in the Confidence Score Thresholds document.

**Absence rule:** None — this field is Required. Its absence constitutes an invalid CAR Handoff (see [docs/boundary-contracts.md](boundary-contracts.md), Handoff 1 validity conditions).

**Example values:**
```json
"activities.confidence_score": 0.91
"activities.confidence_score": 0.74
"activities.confidence_score": 0.55    // below threshold — "activities" added to confidence.low_confidence_categories
```

---

## Cross-Category Dependencies

### Dependency 1 — `activities.social_context` depends on `persons.count >= 2` (People category)

`activities.social_context` is Conditional on the People category field `persons.count`. The dependency chain is:

```
persons.present = true
  → persons.count is present (integer >= 1)
    → persons.count >= 2
      → activities.social_context may be populated
```

**When `persons.present` is absent:** The People category did not produce a finding. `persons.count` is therefore absent. `activities.social_context` must be absent. Consumer Rule 1 applies: absence of social context is unknown, not a negative finding.

**When `persons.present = false`:** No persons were detected. `persons.count` is absent (a value of `0` must not appear). `activities.social_context` must be absent.

**When `persons.count` is present but below 2:** Only one person detected. `activities.social_context` must be absent (the Conditional condition `persons.count >= 2` is not met).

**When `persons.count >= 2` but `persons.confidence_score` is below threshold:** The People category is below the minimum confidence threshold (0.70, provisional). Per CAR Consumer Rule 2, all People fields including `persons.count` must be treated as unknown. `activities.social_context` must be absent, as the dependency condition cannot be confirmed. Consumer Rule 1 applies downstream: social context is unknown.

**When `persons.count >= 2` and `persons.confidence_score` is at or above threshold:** The condition is met. `activities.social_context` may be populated if a discernible social interaction is detectable in the frame.

**Summary rule:** `activities.social_context` is only valid when `persons.count >= 2` is confirmed above the confidence threshold. When the upstream condition is uncertain or unconfirmed, treat `activities.social_context` as Conditional absent and apply Consumer Rule 1.

---

### Dependency 2 — `activities.editorial_event_signal = true` triggers `risk.editorial_only` evaluation (Risk Flags category)

`activities.editorial_event_signal` is a primary input condition for the Risk Flags category field `risk.editorial_only`. The dependency flows as:

```
activities.editorial_event_signal = true
  → Asset Intelligence Layer must evaluate risk.editorial_only
    → risk.editorial_only is set to true
      → downstream consumers apply Block output entirely
        for commercial channel profiles
        (unless human review override is recorded)
```

**Specification reference:** The `risk.editorial_only` field is defined in the CAR Field Catalogue (story #78, Section 6) with the condition: *"Present when `activities.editorial_event_signal` is `true` or when a public figure or real-world news event is detected."* The handling policy for `risk.editorial_only = true` is **Block output entirely** for any commercial channel Content Profile (no Output Package targeting a commercial channel may be generated or delivered until a human reviewer records an explicit override). This policy is specified in full in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md), Section 2.2, Risk Flag #3.

**Directionality:** The dependency flows from Activities to Risk Flags — not the reverse. `risk.editorial_only` does not set `activities.editorial_event_signal`; the Activities field is the upstream evidence, and the Risk Flags field is the downstream classification conclusion.

**Important:** `activities.editorial_event_signal` is not the only condition that can trigger `risk.editorial_only`. The risk field is also set when a public figure or real-world news event is detected through other CAR categories. However, a `true` value on `activities.editorial_event_signal` always triggers the `risk.editorial_only` evaluation; the Activities layer must not suppress this effect based on other category findings.

**Consumer note:** Downstream consumers reading `activities.editorial_event_signal = true` directly (before reading `risk.editorial_only`) must treat it as a strong editorial indicator, even if `risk.editorial_only` has not yet been set or is absent. This is specified in [docs/commercial-editorial-classification.md](commercial-editorial-classification.md), Section 2, and the classification decision sequence in Section 5.

---

## Edge Cases

### Edge Case 1 — `persons.count` absent or below confidence threshold

**Scenario:** The asset contains persons, but either `persons.count` is absent (People category not evaluated, or `persons.present` is absent) or `persons.confidence_score` is below the minimum threshold (0.70, provisional).

**Required behaviour for `activities.social_context`:**
- `activities.social_context` must be absent.
- The absence is a valid Conditional absence — it does not constitute an invalid Handoff.
- A downstream consumer reading an absent `activities.social_context` must treat the social context as unknown (CAR Consumer Rule 1). The consumer must not infer a social context value from other fields, must not default to `solo`, and must not proceed as though the information is confirmed.
- If the Content Profile requires a social context value for its generation logic, it must route the asset for human review rather than substituting a default.

**Rationale:** `activities.social_context` is a cross-category derived field. Its validity depends entirely on a confirmed upstream People category finding. An uncertain or absent upstream condition invalidates the derived field; the Activities layer must not attempt to infer person count independently in order to populate social context.

---

### Edge Case 2 — Multiple activities detected; selecting `primary_activity`

**Scenario:** `activities.detected_activities` contains two or more entries and the layer must determine whether a single dominant activity can be identified.

**Required behaviour:**
1. Apply the selection criteria in priority order (see the `activities.primary_activity` field specification above): compositionally dominant subject first, then frame area, then focus.
2. If one activity satisfies the first applicable criterion clearly above the others, set `activities.primary_activity` to that activity.
3. If no activity satisfies any criterion clearly above the others — for example, two equally prominent subjects performing different activities in symmetric composition — `activities.primary_activity` must be absent.
4. Do not select `primary_activity` based on keyword commercial value, stock market relevance, or Content Profile requirements. The selection is a purely observational, frame-level determination.

**Examples:**
- A foreground subject is jogging; a background figure is walking. Primary activity: `"jogging"` (compositionally dominant foreground subject).
- Two people face each other in a handshake, symmetrically framed. Detected activities: `"shaking hands"`, `"smiling"`. `primary_activity`: `"shaking hands"` (the activity, not the expression, is the dominant action).
- A group of people are engaged in three simultaneous distinct activities across the frame with no clear dominant subject. `primary_activity`: absent.

---

### Edge Case 3 — Non-person physical activity detection and `physical_intensity`

**Scenario:** The asset contains no persons but depicts a subject with observable physical energy or dynamism (e.g., a waterfall, a breaking wave, a ball in flight, a vehicle in motion, wind-blown foliage).

**Required behaviour:**
- `activities.physical_intensity` may be populated. The field is not restricted to person-present scenarios.
- The intensity enum applies to the physical force or energy observable in the subject, regardless of whether a person is causing or involved in that force.
- `activities.detected_activities` should include a descriptive entry for the non-person dynamic event (e.g., `"water falling"`, `"vehicle in motion"`, `"ball in flight"`).
- `activities.primary_activity` may be set if the non-person dynamic event is the compositionally dominant activity in the frame.
- `activities.social_context` must be absent (no persons present to establish a social context).

**Examples:**
- A photograph of a mountain waterfall: `detected_activities: ["water falling"]`, `primary_activity: "water falling"`, `physical_intensity: "vigorous"`, `social_context: absent`.
- A photograph of a football in mid-air trajectory: `detected_activities: ["ball in flight"]`, `physical_intensity: "vigorous"`, `social_context: absent`.
- A photograph of a luxury car at speed on a track, driver not visible: `detected_activities: ["vehicle in motion"]`, `physical_intensity: "vigorous"`, `social_context: absent`.

**Rationale:** Physical intensity is an observational characteristic of the depicted scene's energy level, not a human physiological measure. Restricting it to person-present scenarios would exclude a large class of valid sports, nature, and automotive imagery for which intensity classification is commercially relevant.

---

## Consistency with Field Catalogue

The following table maps each field in this specification to its corresponding entry in the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md), story #78, Section 5) and confirms alignment.

| Field Name | Type (Catalogue) | Cardinality (Catalogue) | Alignment |
|---|---|---|---|
| `activities.detected_activities` | Array\<string\> | Conditional | Consistent. This spec adds the absence rule (no empty array) and ordering guidance not stated in the catalogue. |
| `activities.primary_activity` | string | Conditional | Consistent. This spec adds the selection priority criteria and the constraint that the value must appear in `detected_activities`. |
| `activities.social_context` | string (enum) | Conditional | Consistent. Enum values in this spec (`solo`, `pair_interaction`, `group_activity`, `crowd_event`) match the catalogue exactly. |
| `activities.physical_intensity` | string (enum) | Conditional | Consistent. Enum values in this spec (`sedentary`, `light`, `moderate`, `vigorous`) match the catalogue exactly. This spec extends the scope clarification to include non-person subjects. |
| `activities.editorial_event_signal` | boolean | Conditional | Consistent. This spec adds the `false` vs. absent distinction and the cross-category downstream effect. |
| `activities.confidence_score` | float (0–1) | Required | Consistent. This spec adds the threshold reference and the `confidence.low_confidence_categories` population rule. |

**Conflict resolution:** If any value, type, condition, or cardinality in this document conflicts with the CAR Field Catalogue, the Field Catalogue governs. Raise the conflict for resolution and update this document to match the confirmed catalogue entry.

---

## Cross-References

- **CAR Field Catalogue (story #78):** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative field names, types, cardinality, and conditions for all Activities fields. Section 5 is the Activities category.
- **CAR Concept Definition (story #15):** [docs/canonical-asset-record.md](canonical-asset-record.md) — Consumer Rules 1–4, the Activities category concept definition, and the immutability rule governing the CAR Handoff.
- **Confidence Score Thresholds and Risk Flag Handling Rules (story #84):** [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) — threshold values for `activities.confidence_score` and `persons.confidence_score`; handling policies for `risk.editorial_only` when triggered by `activities.editorial_event_signal`.
- **Commercial vs Editorial Classification (story #86):** [docs/commercial-editorial-classification.md](commercial-editorial-classification.md) — the `activities.editorial_event_signal` → `risk.editorial_only` dependency chain and its effect on commercial Output Package generation; classification decision sequence in Section 5.
- **Boundary Contracts (story #77):** [docs/boundary-contracts.md](boundary-contracts.md) — Handoff 1 validity conditions, including the requirement that `activities.confidence_score` is always present.
- **Domain Glossary:** [docs/glossary.md](glossary.md) — canonical definitions for Canonical Asset Record, Asset Intelligence Layer, Confidence Score, Risk Flag, Handoff, Content Profile, Output Package, and all other capitalised terms used in this document.
