# CAR Field Catalogue

> **Draft v0.1 — field names and types will be confirmed during MVP1 implementation.**
> This catalogue is indicative. Field names, data types, cardinality, and conditions are subject to change as implementation work proceeds in MVP1. All conflicts between this draft and any MVP1 implementation decision must be resolved in favour of the implementation, with a corresponding update to this document.

---

## Introduction

This document is the field-level complement to the Canonical Asset Record (CAR) concept defined in **story #15** ([docs/canonical-asset-record.md](canonical-asset-record.md)). Where story #15 defines the CAR's purpose, its position in the three-layer architecture, its seven information categories, and the consumer rules that govern its use, this catalogue names every field within those categories and specifies its data type, cardinality, and — for conditional fields — the condition under which the field is present.

The seven information categories used to organise this catalogue are taken directly from story #15, Section 3. Every field is traceable to one category; no field spans two categories. The dot-notation naming convention (e.g., `objects.detected_subjects`, `persons.count`) is consistent with the indicative field names introduced in the [AssetForge Asset Type Taxonomy](asset-type-taxonomy.md) and used as planning labels throughout MVP0 documentation.

**Scope:** This catalogue covers Photo assets only. Photo is the sole Asset Type in scope through MVP6. Video and Vector fields are documented in the Asset Type Taxonomy as indicative planning references and will be specified in a future revision of this catalogue at MVP10.

**What this catalogue does not define:**
- Confidence score threshold values — those are the subject of **story #84**.
- Storage format or serialisation structure (JSON, Protobuf, etc.) — an MVP1 decision.
- Any implementation of the Asset Intelligence Layer itself.

---

## Cardinality Key

| Cardinality | Meaning |
|---|---|
| **Required** | Always present in every CAR produced for a Photo asset; absence constitutes an invalid Handoff (see [Boundary Contracts](boundary-contracts.md), Handoff 1 validity condition 1). |
| **Conditional** | Present only when the stated condition is met; absence when the condition is not met is valid and must be treated as unknown by downstream consumers (CAR Consumer Rule 1). |

---

## 1. Objects and Subjects

The identifiable physical things depicted in the asset. These fields record what is observable in the image without reference to audience, channel, or intended use.

| Field Name | Type | Cardinality | Condition | Description |
|---|---|---|---|---|
| `objects.detected_subjects` | Array\<string\> | Required | — | List of identifiable objects, subjects, and physical elements detected in the image (e.g., "standing desk", "laptop", "potted plant", "window"). Each entry is a plain noun or noun phrase. An empty array is valid when no objects are detected. |
| `objects.primary_subject` | string | Conditional | Present when the Asset Intelligence Layer can identify a single dominant subject with high confidence | The most visually prominent subject in the image; used by the Content Generation Layer to anchor title and description generation. |
| `objects.scene_type` | string (enum) | Required | — | Broad compositional classification of the image content: `object_isolated`, `scene_with_context`, `abstract`, `pattern_texture`, or `multiple_subjects`. Enables downstream profile routing. |
| `objects.colour_palette` | Array\<string\> | Conditional | Present when colour analysis produces a reliable result | Up to five dominant plain colour names (e.g., "red", "navy blue", "forest green") describing the image's colour composition. Hex codes must not be used. Relevant for product and commerce channel descriptions. |
| `objects.brand_objects_detected` | Array\<string\> | Conditional | Present when one or more branded consumer goods (distinct from logos — see Text and Logos category) are visible | List of consumer product categories or brand-adjacent objects detected (e.g., "laptop", "smartphone", "coffee cup with brand mark"). Does not include logo text; that is recorded in `text.detected_strings`. |
| `objects.foreground_elements` | Array\<string\> | Optional | — | Primary subjects or objects in the foreground of the image, distinct from background scene elements. |
| `objects.background_elements` | Array\<string\> | Optional | — | Scene elements or environmental context in the background of the image. |
| `objects.confidence_score` | float (0–1) | Required | — | Confidence score for the Objects and Subjects category as a whole. See **story #84** for threshold values. |

---

## 2. People

Observations about human presence in the asset. These fields do not identify individuals; they record observable demographic and compositional signals that drive downstream compliance logic.

| Field Name | Type | Cardinality | Condition | Description |
|---|---|---|---|---|
| `persons.present` | boolean | Required | — | `true` if one or more persons are detectable in the image; `false` if no persons are detectable. This field is always present and drives all downstream conditional People fields. |
| `persons.count` | integer | Conditional | Present when `persons.present` is `true` | Number of individual persons detected. A value of `0` must not appear; if no persons are detected, `persons.present` is `false` and this field is absent. |
| `persons.faces_detected` | boolean | Conditional | Present when `persons.present` is `true` | `true` if at least one face is sufficiently visible to be potentially identifiable; `false` if persons are present but no face is visible (e.g., figures photographed from behind or at a distance). |
| `persons.age_range_signals` | Array\<string\> | Conditional | Present when `persons.present` is `true` and age signals are detectable with sufficient confidence | Broad age-range labels observable in the image (e.g., "adult", "child", "elderly"). Does not provide a numeric age estimate. Used by the Content Generation Layer for lifestyle keyword and description generation. |
| `persons.group_composition` | string (enum) | Conditional | Present when `persons.count` is 2 or more | High-level group composition descriptor: `couple`, `small_group` (3–5), `large_group` (6+), `crowd`. |
| `persons.activity_posture` | string | Conditional | Present when `persons.present` is `true` and a dominant posture or activity is detectable | Concise label for the person's dominant posture or interaction state (e.g., "standing", "seated", "facing camera", "in profile"). Complements the Activities category for lifestyle and editorial assets. |
| `persons.confidence_score` | float (0–1) | Required | — | Confidence score for the People category as a whole. See **story #84** for threshold values. |

---

## 3. Locations

Geographic and environmental context derived from the asset. Locations are inferred from visual content, embedded technical metadata (EXIF GPS), or identifiable landmarks — never fabricated or assumed.

| Field Name | Type | Cardinality | Condition | Description |
|---|---|---|---|---|
| `location.environment_type` | string (enum) | Required | — | Broad environmental classification: `indoor`, `outdoor`, or `mixed` (e.g., a covered outdoor market). Always determinable from visual analysis of a photo. |
| `location.setting_descriptor` | string | Conditional | Present when the setting is classifiable with sufficient visual evidence | Descriptive label for the specific setting type (e.g., "home office", "urban street", "forest trail", "commercial kitchen"). Inferred from visible environmental cues. |
| `location.gps_coordinates` | object {lat: float, lon: float} | Conditional | Present when valid GPS coordinates are embedded in the asset's EXIF metadata | Latitude and longitude extracted from EXIF; not inferred from visual content. Absent when no GPS data is embedded. |
| `location.gps_derived_region` | string | Conditional | Present when `location.gps_coordinates` is present and reverse-geocoding produces a result | Human-readable geographic region derived from GPS coordinates (e.g., "San Francisco, California, United States"). Resolution varies with geocoding service accuracy. |
| `location.visual_landmark` | string | Conditional | Present when an identifiable geographic landmark is visible in the image with high confidence | Name of a visually identifiable landmark or recognisable place (e.g., "Eiffel Tower", "Times Square"). Used only when confidence is high enough to avoid misidentification. |
| `location.urban_rural_signal` | string (enum) | Conditional | Present when outdoor and sufficient environmental cues are present | Broad settlement context: `urban`, `suburban`, `rural`, `wilderness`. |
| `location.confidence_score` | float (0–1) | Required | — | Confidence score for the Locations category as a whole. See **story #84** for threshold values. |

---

## 4. Text and Logos

Readable text strings and brand marks visible within the asset. Accuracy of text extraction is critical; inaccurate strings in this category propagate directly to keyword and description generation errors.

| Field Name | Type | Cardinality | Condition | Description |
|---|---|---|---|---|
| `text.strings_present` | boolean | Required | — | `true` if any readable text string is detectable in the image; `false` otherwise. Drives conditional fields `text.detected_strings`, `text.watermark_present`, and `text.dominant_language`. Note: `text.logo_marks_detected` is independently conditional on brand mark detectability and may be present regardless of this field's value. |
| `text.detected_strings` | Array\<string\> | Conditional | Present when `text.strings_present` is `true` | Array of verbatim text strings detected in the image (e.g., "OPEN", "Nikon", "Sale 50%"). Each entry is a distinct readable string as it appears visually; no OCR correction or normalisation is applied. |
| `text.logo_marks_detected` | Array\<string\> | Conditional | Present when one or more brand mark or logo symbols are detectable, regardless of whether associated text is legible | Array of identified brand mark names or descriptions (e.g., "Nike swoosh", "Apple logo"). Where a brand mark is detected but not identified, the entry is `"unidentified_brand_mark"`. |
| `text.watermark_present` | boolean | Conditional | Present when `text.strings_present` is `true` | `true` if a watermark (photographer credit, stock agency mark, or similar overlay text) is detected. Downstream channels typically require watermark-free assets; this flag enables routing logic. |
| `text.dominant_language` | string (BCP 47) | Conditional | Present when detected text contains five or more words sufficient to determine a language | Language code for the dominant readable language detected in the image (e.g., `en`, `fr`, `zh`). Relevant for geographic and editorial classification. |
| `text.bounding_boxes` | Array\<object\> | Optional | — | Approximate position descriptors for detected text strings and logo marks (e.g. top-left, centre, bottom-right); not pixel-precise coordinates. |
| `text.confidence_score` | float (0–1) | Required | — | Confidence score for the Text and Logos category as a whole. See **story #84** for threshold values. |

---

## 5. Activities

Dynamic events and actions occurring within the asset. For Photo assets, activities are inferred from a single frame; time-based inference (clips, sequences) is out of scope until MVP10.

| Field Name | Type | Cardinality | Condition | Description |
|---|---|---|---|---|
| `activities.detected_activities` | Array\<string\> | Conditional | Present when one or more activities or actions are detectable with sufficient confidence | List of activities or dynamic events inferred from the image (e.g., "working at a desk", "cooking", "hiking", "playing guitar"). Each entry is a short verb phrase. An empty array is not produced; absence of the field indicates no activities were detected. |
| `activities.primary_activity` | string | Conditional | Present when a single dominant activity is identifiable with high confidence | The most prominent activity or action in the image; used by the Content Generation Layer to anchor lifestyle and commercial descriptions. |
| `activities.social_context` | string (enum) | Conditional | Present when multiple persons are present and a social interaction is detectable | Broad social context descriptor: `solo`, `pair_interaction`, `group_activity`, `crowd_event`. |
| `activities.physical_intensity` | string (enum) | Conditional | Present when a physical activity is detected and intensity is estimable from visual evidence | Broad intensity classification: `sedentary`, `light`, `moderate`, `vigorous`. Relevant for sport and wellness channel keyword generation. |
| `activities.editorial_event_signal` | boolean | Conditional | Present when the image contains signals consistent with a real-world news or public event | `true` if the activity depicted appears to be a real-world event (protest, sports event, ceremony) rather than a staged scenario; triggers `risk.editorial_only` evaluation in the Risk Flags category. |
| `activities.confidence_score` | float (0–1) | Required | — | Confidence score for the Activities category as a whole. See **story #84** for threshold values. |

---

## 6. Risk Flags

Structured compliance signals indicating that the asset contains content requiring special handling before certain Output Packages can be generated or approved. Risk Flags must always be propagated to downstream consumers regardless of the confidence score of the underlying observation (CAR Consumer Rule 4, [docs/canonical-asset-record.md](canonical-asset-record.md)).

| Field Name | Type | Cardinality | Condition | Description |
|---|---|---|---|---|
| `risk.flags_evaluated` | boolean | Required | — | `true` confirms that the Asset Intelligence Layer completed a Risk Flag evaluation pass for this asset. `false` or absence indicates the evaluation was incomplete; the Handoff is invalid until this field is `true`. |
| `risk.model_release_required` | boolean | Conditional | Present when `persons.present` is `true` and at least one person is potentially identifiable (faces visible or person is prominently featured) | `true` signals that one or more identifiable persons are present and a model release may be required for commercial distribution. Must be propagated at any confidence level. |
| `risk.property_release_required` | boolean | Conditional | Present when private property (buildings, branded structures, private artworks) is identifiable in the image | `true` signals that recognisable private property is present and a property release may be required for commercial distribution. |
| `risk.editorial_only` | boolean | Conditional | Present when `activities.editorial_event_signal` is `true` or when a public figure or real-world news event is detected | `true` classifies the asset as Editorial Use only. Must block commercial channel profiles from generating Output Packages without human review override. |
| `risk.adult_content` | boolean | Conditional | Present when the image contains nudity, sexually suggestive content, or content inappropriate for general audiences | `true` signals that the asset contains adult content. Triggers channel-specific restrictions and human review requirements. |
| `risk.violence_flag` | boolean | Conditional | Present when the image contains depictions of violence, injury, or distressing content | `true` signals that the asset contains violent or distressing content. Triggers channel-specific restrictions and human review requirements. |
| `risk.trademark_flag` | boolean | Conditional | Present when `text.logo_marks_detected` is non-empty or when a third-party brand mark is detected | `true` signals that a third-party trademark or brand mark is visible and commercial distribution may require rights clearance. |
| `risk.confidence_score` | float (0–1) | Required | — | Confidence score for the Risk Flags category as a whole. Applies to the detection sensitivity of the evaluation pass, not to individual flag values — a flag set to `true` must be propagated regardless of this score. See **story #84** for threshold values. |

---

## 7. Confidence Scores

Numeric certainty values attached to observations in all preceding categories. A confidence score reflects the Asset Intelligence Layer's analytical certainty in its findings, not the quality of the asset itself (see the Confidence Score glossary entry in [docs/glossary.md](glossary.md)).

Each category above includes its own `*.confidence_score` field (e.g., `objects.confidence_score`, `persons.confidence_score`). The fields below provide summary-level and field-level score support.

| Field Name | Type | Cardinality | Condition | Description |
|---|---|---|---|---|
| `confidence.overall_score` | float (0–1) | Required | — | Single aggregate confidence score for the CAR as a whole; calculated by the Asset Intelligence Layer as a weighted composite of per-category scores. Provides a fast-path signal for downstream routing without requiring consumers to evaluate all seven category scores. |
| `confidence.analysis_model_version` | string | Required | — | Identifier for the version of the Asset Intelligence Layer model or pipeline that produced this CAR (e.g., `"ail-v0.1"`). Enables reproducibility tracking and supports future re-processing when model versions are updated. |
| `confidence.low_confidence_categories` | Array\<string\> | Conditional | Present when one or more categories have a score below the platform's minimum routing threshold (threshold value defined in story #84) | List of category names (e.g., `["locations", "activities"]`) for which confidence is below the routing threshold. Consumers must apply CAR Consumer Rule 2 to all fields within listed categories. |
| `confidence.analysis_timestamp` | string (ISO 8601) | Required | — | Date and time at which the Asset Intelligence Layer completed the CAR and sealed it as immutable. Supports audit trail requirements planned for MVP4. |
| `confidence.asset_quality_signal` | string (enum) | Required | — | Classification of detected technical quality issues: `blur`, `low_resolution`, `poor_exposure`, `noise`, or `none`. Value is `none` when no quality issues are detected. Does not rate commercial or aesthetic quality; records only technical properties that may reduce detection confidence. |

---

## Cross-References

- **CAR concept definition (story #15):** [docs/canonical-asset-record.md](canonical-asset-record.md) — purpose, architectural position, seven information categories, immutability rule, and consumer rules that govern how all fields in this catalogue must be interpreted by downstream consumers.
- **Asset Type Taxonomy (story #82):** [docs/asset-type-taxonomy.md](asset-type-taxonomy.md) — the indicative field names used in this catalogue are consistent with the planning labels introduced there; story #78 is the authoritative source once complete.
- **Boundary Contracts (story #77):** [docs/boundary-contracts.md](boundary-contracts.md) — the Handoff 1 validity conditions (completeness, confidence scores present, risk flags propagated, immutability, no content decisions, profile-agnosticism) define what constitutes a complete and valid CAR for delivery to the Content Generation Layer.
- **Confidence score thresholds (story #84):** Threshold values for all `*.confidence_score` fields are out of scope for this catalogue. Story #84 will define the minimum score required to act on each category and the routing logic applied when a score falls below threshold.
- **Domain Glossary:** [docs/glossary.md](glossary.md) — all terms used in this document (Asset, Canonical Asset Record, Confidence Score, Risk Flag, Handoff, Content Profile, Output Package) are defined there.
