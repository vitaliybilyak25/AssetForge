# CAR Objects and Subjects Category — Field Specification

> **Story #18 — Implementation-ready field specification.**
> This document specifies all fields in the Objects and Subjects category of the Canonical Asset Record (CAR). It is intended for developers implementing the Asset Intelligence Layer (Layer 1) and must be read alongside the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)) and the CAR concept definition ([docs/canonical-asset-record.md](canonical-asset-record.md)).

---

## Overview

The Objects and Subjects category records the identifiable physical things depicted in a photo asset. These fields capture what is observable in the image — objects, their composition, colour, and spatial arrangement — without reference to any audience, distribution channel, or intended use. This is a factual, channel-agnostic record produced exclusively by the Asset Intelligence Layer.

The category contains eight fields. Two are Required and must always be present in a valid CAR Handoff. Three are Conditional and are present only when the stated detection condition is met. Two are Optional and may be present at the Asset Intelligence Layer's discretion. One Required field (`objects.confidence_score`) provides a category-level certainty signal for all downstream consumers.

The Asset Intelligence Layer must produce this category as part of every CAR Handoff for a Photo asset. An incomplete Objects and Subjects category — specifically, the absence of either Required field — constitutes an invalid Handoff 1 (see [docs/boundary-contracts.md](boundary-contracts.md), Handoff 1 validity condition 1).

---

## Scope

This specification covers Photo assets only, consistent with the scope of the CAR Field Catalogue through MVP6. Video and vector variants of these fields are deferred to MVP10.

This document specifies what the Asset Intelligence Layer must populate. It does not specify:

- How the Asset Intelligence Layer detects or infers these values (implementation decision).
- Storage format or serialisation structure (MVP1 decision).
- Confidence score threshold values — those are defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md); this document cross-references threshold values only.
- Any Content Profile rules or Output Package formatting.

---

## Field Specifications

### objects.detected_subjects

| Attribute | Value |
|---|---|
| **Field name** | `objects.detected_subjects` |
| **Data type** | Array\<string\> |
| **Cardinality** | Required |
| **Condition** | None — always present |

**Description.** A flat list of every identifiable object, subject, or physical element detected in the image. Each entry is a plain noun or noun phrase naming a single observable thing. Entries are not ranked and carry no implied order.

**Allowed values and format.** Each array entry must be a plain noun or noun phrase in lowercase (e.g., `"standing desk"`, `"laptop"`, `"potted plant"`, `"window"`, `"wooden floor"`). Entries must describe observable physical things only — they must not include adjectives conveying tone, quality, or channel-relevant interpretation (e.g., `"professional laptop"` is not valid; `"laptop"` is).

**Empty array rule.** An empty array (`[]`) is a valid value for this field and means no objects were detected. This field does NOT follow the standard absence rule that applies to Conditional fields. It is always present in the CAR, even when detection yields nothing. This distinguishes `objects.detected_subjects` from Conditional fields, which are absent when their condition is not met: `objects.detected_subjects` is never absent — it is either populated or empty.

**Example values.**
- `["standing desk", "laptop", "potted plant", "window", "office chair"]` — office scene with multiple objects detected.
- `[]` — no objects detected (e.g., a solid-colour background or completely abstract image).
- `["coffee cup"]` — single object detected.

---

### objects.primary_subject

| Attribute | Value |
|---|---|
| **Field name** | `objects.primary_subject` |
| **Data type** | string |
| **Cardinality** | Conditional |
| **Condition** | Present when the Asset Intelligence Layer can identify a single dominant subject with high confidence |

**Description.** The single most visually prominent subject in the image. This field enables the Content Generation Layer to anchor title and description generation around one central element. It must be a single noun or noun phrase, consistent with entries in `objects.detected_subjects`.

**Condition detail.** The field is present only when one subject is clearly dominant — occupying the majority of the frame, positioned at the focal point, or otherwise unambiguously primary. When the image contains multiple subjects of roughly equal visual weight, or when no clear dominant subject exists, this field is absent. Absence is valid and must be treated as unknown by downstream consumers (CAR Consumer Rule 1, [docs/canonical-asset-record.md](canonical-asset-record.md)).

**Allowed values and format.** A single plain noun or noun phrase. Must also appear in `objects.detected_subjects`. Must not be a value absent from `objects.detected_subjects`.

**Absence rule.** Absent when the condition is not met. Downstream consumers must not infer a primary subject from `objects.detected_subjects` when this field is absent.

**Example values.**
- `"laptop"` — single laptop centred and in sharp focus against a blurred background.
- `"red umbrella"` — an umbrella is the clear subject of a street photography composition.
- *(absent)* — flat lay of five equally sized products with no dominant focal subject.

---

### objects.scene_type

| Attribute | Value |
|---|---|
| **Field name** | `objects.scene_type` |
| **Data type** | string (enum) |
| **Cardinality** | Required |
| **Condition** | None — always present |

**Description.** A broad compositional classification of the image's content and structure. This field enables downstream channel profile routing — certain profiles apply only to specific scene types (e.g., a product isolation profile targets `object_isolated`; an editorial lifestyle profile targets `scene_with_context` or `multiple_subjects`).

**Allowed values.** Exactly the following five values; no other values are valid:

| Value | Meaning |
|---|---|
| `object_isolated` | A single object or subject appears against a plain, uniform, or deliberately neutral background (e.g., a product shot on white). |
| `scene_with_context` | One or more subjects appear within a recognisable environmental or situational context (e.g., a person at a desk, a coffee cup on a café table). |
| `abstract` | The image has no clearly identifiable subjects or objects; content is non-representational (e.g., paint textures, light bokeh, out-of-focus colour fields). |
| `pattern_texture` | The image depicts a repeating or tiled visual pattern, material texture, or surface detail (e.g., fabric weave, brick wall close-up, wood grain). |
| `multiple_subjects` | Two or more subjects of comparable visual weight are present, with no single dominant subject (e.g., a group of products, a pair of people interacting). |

**Absence rule.** This field is Required and must be present. Absence constitutes an invalid Handoff 1. The Asset Intelligence Layer must always assign one of the five values; when the image is genuinely ambiguous, it must assign the value that best fits the predominant compositional characteristic and record any uncertainty in `objects.confidence_score`.

**Example values.**
- `"object_isolated"` — a white ceramic mug centred on a pure white background.
- `"scene_with_context"` — a woman working at a laptop in a home office setting.
- `"abstract"` — blurred coloured lights forming a bokeh background.
- `"pattern_texture"` — close-up photograph of a woven linen fabric.
- `"multiple_subjects"` — three different smartphones arranged side by side on a flat surface.

---

### objects.colour_palette

| Attribute | Value |
|---|---|
| **Field name** | `objects.colour_palette` |
| **Data type** | Array\<string\> |
| **Cardinality** | Conditional |
| **Condition** | Present when colour analysis produces a reliable result |

**Description.** An ordered list of the dominant colours in the image, from most to least dominant, based on colour analysis of the image content. This field supports downstream product, commerce, and design channel descriptions where colour is a searchable attribute.

**Condition detail.** The field is present when the Asset Intelligence Layer's colour analysis produces a result with sufficient confidence. Absent when colour analysis fails, produces unreliable output (e.g., extremely dark or overexposed image), or when the image does not have a meaningful colour composition (e.g., pure black-and-white). Absence is valid and must be treated as unknown by downstream consumers.

**Allowed values and format.** Each entry must be a plain colour name in English. Plain colour names are required; hex codes must not be used. Compound colour names are permitted (e.g., `"navy blue"`, `"forest green"`, `"burnt orange"`). The array must contain no more than five entries per instance. Entries should be ordered from most to least dominant.

**Examples of valid entries:** `"red"`, `"white"`, `"navy blue"`, `"forest green"`, `"charcoal grey"`, `"pale yellow"`, `"burnt orange"`, `"black"`, `"teal"`.

**Examples of invalid entries (must not appear):** `"#FF5733"`, `"rgb(255,87,51)"`, `"#FFFFFF"` — hex and RGB codes are not permitted in this field.

**Absence rule.** Absent when the condition is not met. The array must never be empty; if colour analysis does not produce a reliable result, the field is absent rather than present as `[]`.

**Example values.**
- `["white", "silver", "black"]` — a silver laptop on a white desk with a dark background.
- `["forest green", "brown", "pale yellow"]` — a woodland landscape scene.
- `["red", "white", "navy blue"]` — a product shot with patriotic colour scheme.
- *(absent)* — colour analysis failed due to extreme underexposure.

---

### objects.brand_objects_detected

| Attribute | Value |
|---|---|
| **Field name** | `objects.brand_objects_detected` |
| **Data type** | Array\<string\> |
| **Cardinality** | Conditional |
| **Condition** | Present when one or more branded consumer goods (distinct from logos — see Text and Logos category) are visible |

**Description.** A list of branded consumer goods or brand-adjacent objects detected in the image. This field records the physical objects themselves — not the brand identity, logo text, or trademark marks associated with them. See the Cross-Category Boundary section for the explicit boundary with `text.logo_marks_detected`.

**Condition detail.** The field is present when the Asset Intelligence Layer detects one or more consumer goods that are commonly associated with specific brands or product categories, or that carry visible brand-related physical features (e.g., a distinctive device form factor, branded packaging shape, or a cup bearing a brand mark). Absent when no such objects are present. Absence is valid and must be treated as unknown.

**Allowed values and format.** Each entry is a plain noun or noun phrase describing the consumer product or brand-adjacent object (e.g., `"laptop"`, `"smartphone"`, `"coffee cup with brand mark"`, `"branded shopping bag"`, `"sneaker"`). Entries describe what the object is, not what brand it is. Where the brand is identifiable but the object also carries a visible brand mark or logo symbol, the brand mark is recorded separately in `text.logo_marks_detected`.

**Absence rule.** Absent when the condition is not met. Must not be present as an empty array.

**Example values.**
- `["laptop", "smartphone"]` — a desk scene with a laptop and phone visible.
- `["coffee cup with brand mark", "paper bag"]` — a café scene where takeaway packaging with a visible brand mark is present.
- `["sneaker"]` — close-up of an athletic shoe with a detectable brand form factor.
- *(absent)* — an outdoor landscape image with no consumer goods present.

---

### objects.foreground_elements

| Attribute | Value |
|---|---|
| **Field name** | `objects.foreground_elements` |
| **Data type** | Array\<string\> |
| **Cardinality** | Optional |
| **Condition** | None — present at the Asset Intelligence Layer's discretion when spatial decomposition is reliable |

**Description.** Primary subjects or objects that occupy the foreground of the image — those closest to the camera or positioned in the compositional foreground plane. This field records spatial placement for foreground objects, complementing `objects.detected_subjects` which records all objects without spatial annotation.

**Condition detail.** This field is Optional; it may be populated when the Asset Intelligence Layer can reliably distinguish foreground from background elements based on depth, focus, or compositional cues. It is not required and its absence does not constitute an invalid Handoff. Downstream consumers must treat absence as unknown (CAR Consumer Rule 1).

**Allowed values and format.** Each entry is a plain noun or noun phrase, consistent with the format of `objects.detected_subjects` entries. Entries in this field should also appear in `objects.detected_subjects`. This field does not replace `objects.detected_subjects`; it annotates a spatial subset of it.

**Absence rule.** Absent when spatial decomposition is not reliable or when the Asset Intelligence Layer does not populate it. Must not be present as an empty array; if no foreground elements are identifiable, the field is absent.

**Example values.**
- `["coffee cup", "open notebook"]` — a café table composition where the cup and notebook are closest to the camera.
- `["woman", "laptop"]` — a portrait-orientation scene where a seated woman with a laptop occupies the foreground.
- *(absent)* — a flat lay with uniform depth where foreground/background distinction is not meaningful.

---

### objects.background_elements

| Attribute | Value |
|---|---|
| **Field name** | `objects.background_elements` |
| **Data type** | Array\<string\> |
| **Cardinality** | Optional |
| **Condition** | None — present at the Asset Intelligence Layer's discretion when spatial decomposition is reliable |

**Description.** Scene elements or environmental context visible in the background of the image — those furthest from the camera or positioned in the compositional background plane. This field provides spatial context that the Content Generation Layer may use to enrich descriptions and scene-setting keywords, without conflating background detail with the primary subject.

**Condition detail.** This field is Optional; it follows the same discretionary population rule as `objects.foreground_elements`. Downstream consumers must treat absence as unknown.

**Allowed values and format.** Each entry is a plain noun or noun phrase. Entries may overlap with `objects.detected_subjects`; this field annotates their spatial placement. Abstract environmental descriptors are permitted where specific objects cannot be named (e.g., `"blurred greenery"`, `"out-of-focus city lights"`).

**Absence rule.** Absent when spatial decomposition is not reliable or when the Asset Intelligence Layer does not populate it. Must not be present as an empty array.

**Example values.**
- `["bookshelf", "window", "plants"]` — background elements in a home office scene.
- `["blurred city street", "pedestrians"]` — a street photography scene where background context is partially identifiable.
- `["plain white wall"]` — a product shot where the background is deliberately minimal.
- *(absent)* — `object_isolated` scene with a uniform background and no distinguishable background elements.

---

### objects.confidence_score

| Attribute | Value |
|---|---|
| **Field name** | `objects.confidence_score` |
| **Data type** | float (0–1) |
| **Cardinality** | Required |
| **Condition** | None — always present |

**Description.** A numeric confidence score for the Objects and Subjects category as a whole. This value reflects the Asset Intelligence Layer's analytical certainty in the category's combined findings — not the quality of the asset itself. A score of `1.0` represents maximum certainty; a score of `0.0` represents minimum certainty. The score covers all fields in this category collectively.

**Threshold and consumer behaviour.** The minimum confidence threshold for this category is **0.70 [PROVISIONAL — confirm at MVP1]**, as defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md), Section 1.2. When `objects.confidence_score` is below this threshold, downstream consumers (Content Generation Layer) must treat all fields in the Objects and Subjects category as unknown and apply CAR Consumer Rule 2. The category name `"objects"` will appear in `confidence.low_confidence_categories` when this threshold is not met.

This document does not re-specify threshold values; it cross-references [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) as the authoritative source. Threshold values must not be hardcoded from this document.

**Allowed values.** Any float value in the closed range `[0.0, 1.0]` inclusive. Values outside this range are invalid. The Asset Intelligence Layer must not produce a value below `0.0` or above `1.0`.

**Absence rule.** This field is Required. Absence constitutes an invalid Handoff 1. The Asset Intelligence Layer must always produce a score, even when confidence is minimal (in which case the score is a low value near `0.0`, not an absent field).

**Example values.**
- `0.94` — high-confidence detection of multiple clearly visible objects in a well-lit image.
- `0.71` — confidence just above the provisional threshold; observation is valid but borderline.
- `0.45` — below the provisional threshold; all Objects and Subjects fields must be treated as unknown by consumers.
- `0.10` — very low confidence; category findings are highly uncertain.

---

## Cross-Category Boundary: Brand Objects vs Logo Marks

The boundary between `objects.brand_objects_detected` (this category) and `text.logo_marks_detected` (Text and Logos category) is a common source of recording error. This section defines the boundary unambiguously.

### The Rule

**`objects.brand_objects_detected` records physical objects** — the consumer goods themselves — without reference to any brand identity, trademark, or logo mark they may carry.

**`text.logo_marks_detected` records brand marks and logo symbols** — the visual trademark identifiers applied to or associated with objects — without duplicating the object description.

A single physical object can generate entries in both fields simultaneously. The fields are complementary, not mutually exclusive.

### Examples

**Scenario 1: Laptop with visible manufacturer logo.**
- `objects.brand_objects_detected` → `["laptop"]` — records the physical consumer good.
- `text.logo_marks_detected` → `["Apple logo"]` — records the brand mark detected on the device.

**Scenario 2: Coffee cup with a printed brand mark.**
- `objects.brand_objects_detected` → `["coffee cup with brand mark"]` — records the physical branded object.
- `text.logo_marks_detected` → `["Starbucks logo"]` (if identified) or `["unidentified_brand_mark"]` (if not identified) — records the brand mark.

**Scenario 3: Branded shopping bag with visible logotype.**
- `objects.brand_objects_detected` → `["shopping bag"]` — records the physical object.
- `text.logo_marks_detected` → `["Nike swoosh"]` — records the visible trademark symbol.
- `text.detected_strings` → `["NIKE"]` — records the readable brand text (Text and Logos category, separate field).

**Scenario 4: Unbranded glass bottle.**
- `objects.brand_objects_detected` → *(absent, or not included)* — the object carries no brand mark or brand-adjacent feature.
- `text.logo_marks_detected` → *(absent)* — no brand mark detected.

### What Does Not Belong in `objects.brand_objects_detected`

The following must not be recorded in this field:

- Logo text or readable brand names (record in `text.detected_strings`).
- Brand mark symbols, trademark symbols, or logo graphics (record in `text.logo_marks_detected`).
- Non-consumer-good objects such as furniture, architectural elements, or natural objects (record in `objects.detected_subjects`).
- People wearing branded clothing where the brand is only incidentally visible (the person is recorded in the People category; if the brand mark is clearly visible and identifiable, it is recorded in `text.logo_marks_detected`).

---

## AC7/AC8 Resolution Note

During story #18 specification work, two acceptance criteria gaps were identified:

**AC7** — The Objects and Subjects category had no field for recording foreground compositional elements separately from the full detected subject list.

**AC8** — The Objects and Subjects category had no field for recording background environmental elements separately from the full detected subject list.

Both gaps have been resolved. `objects.foreground_elements` and `objects.background_elements` were added to the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)) as Optional fields in the Objects and Subjects category. Their full specifications are included in this document above.

AC7 and AC8 are satisfied by the inclusion of these two fields. The Field Catalogue is the authoritative record of this addition.

---

## Edge Cases

The following edge cases require explicit Asset Intelligence Layer behaviour decisions.

**1. Image with no detectable objects.**
`objects.detected_subjects` must be set to `[]`. `objects.primary_subject` must be absent. `objects.scene_type` should be set to `abstract` or `pattern_texture` depending on the image content. `objects.confidence_score` must still be present.

**2. Image with a single object and a plain background.**
`objects.scene_type` must be `object_isolated`. `objects.primary_subject` must be present and must match the single detected subject. `objects.detected_subjects` contains one entry.

**3. Object that is also a brand-adjacent consumer good.**
The object appears in both `objects.detected_subjects` (as a factual object record) and `objects.brand_objects_detected` (as a brand-adjacent consumer good). This double-recording is correct and expected.

**4. Image where foreground and background are indistinguishable.**
`objects.foreground_elements` and `objects.background_elements` must be absent (not populated as `[]`). Only `objects.detected_subjects` is populated. This applies to flat lay images, macro shots, and uniform-depth scenes.

**5. More than five dominant colours detected.**
`objects.colour_palette` must contain the five most dominant colours only. Additional colours beyond five are discarded. The array must never exceed five entries.

**6. Colour analysis produces exactly one reliable dominant colour.**
`objects.colour_palette` may contain a single entry (e.g., `["red"]`). There is no minimum entry count; the array may contain one to five entries when the field is present.

**7. Brand mark visible but object type is ambiguous.**
`objects.brand_objects_detected` should record the most accurate object description possible (e.g., `"branded packaging"` when the specific product type cannot be determined). The brand mark is still recorded in `text.logo_marks_detected` regardless of object ambiguity.

**8. `objects.scene_type` is genuinely ambiguous between two values.**
The Asset Intelligence Layer must select the single value that best describes the predominant compositional characteristic. It must not produce multiple values or leave the field absent. The ambiguity should be reflected in a lower `objects.confidence_score`.

---

## Consistency with Field Catalogue

This specification is derived from and must remain consistent with the Objects and Subjects section of [docs/car-field-catalogue.md](car-field-catalogue.md). The following items clarify or extend the Field Catalogue without conflicting with it.

| Clarification | Catalogue entry | This specification's extension |
|---|---|---|
| `objects.colour_palette` format | Catalogue updated to plain colour names only; hex codes must not be used | Consistent — catalogue and spec both prohibit hex codes. |
| `objects.brand_objects_detected` scope | Catalogue says "does not include logo text; that is recorded in `text.detected_strings`" | This spec additionally clarifies that brand marks and logo symbols are recorded in `text.logo_marks_detected`, not `text.detected_strings`, and provides worked examples of the boundary. |
| `objects.detected_subjects` empty array | Catalogue states "an empty array is valid" | This spec explicitly states the field does not follow the standard absence rule and is always present, distinguishing it from Conditional fields. |
| `objects.foreground_elements` and `objects.background_elements` | Added to the catalogue as Optional fields during story #18 work | Specified in full in this document; AC7/AC8 resolution confirmed. |

Any future change to the Objects and Subjects fields in the CAR Field Catalogue must be reflected in a corresponding update to this document. Conflicts must be resolved in favour of the Field Catalogue, with this document updated to match.

---

## Cross-References

- **CAR Field Catalogue:** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative field names, data types, and cardinality for all eight fields specified here.
- **CAR concept definition:** [docs/canonical-asset-record.md](canonical-asset-record.md) — Consumer Rules 1–4 governing how all fields in this category must be interpreted by downstream consumers.
- **Confidence and Risk Rules:** [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) — threshold values for `objects.confidence_score` and the population rule for `confidence.low_confidence_categories`.
- **Boundary Contracts:** [docs/boundary-contracts.md](boundary-contracts.md) — Handoff 1 validity conditions, including the requirement that all Required fields be present.
- **Domain Glossary:** [docs/glossary.md](glossary.md) — Canonical Asset Record, Asset Intelligence Layer, Content Generation Layer, Handoff, Confidence Score, Output Package, Content Profile.
