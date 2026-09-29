# CAR Text and Logos Category — Field Specification

> **Story #20 — Implementation-ready field specification.**
> This document specifies all fields in the Text and Logos category of the Canonical Asset Record (CAR). It is intended for developers implementing the Asset Intelligence Layer (Layer 1) and must be read alongside the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md)) and the CAR concept definition ([docs/canonical-asset-record.md](canonical-asset-record.md)).

---

## Overview

The Text and Logos category records readable text strings and brand marks visible within a photo asset. These fields capture what is observable in the image — words, phrases, signage, watermarks, and trademark symbols — without reference to any audience, distribution channel, or intended use. This is a factual, channel-agnostic record produced exclusively by the Asset Intelligence Layer.

The category contains seven fields. Two are Required and must always be present in a valid CAR Handoff. Four are Conditional and are present only when the stated detection conditions are met. One is Optional and may be present at the Asset Intelligence Layer's discretion. One Required field (`text.confidence_score`) provides a category-level certainty signal for all downstream consumers.

Accuracy of text extraction is critical in this category. Inaccurate strings propagate directly to keyword and description generation errors. The Asset Intelligence Layer must prefer verbatim accuracy over OCR correction; the implications of this trade-off are detailed in the `text.detected_strings` field specification.

The Asset Intelligence Layer must produce this category as part of every CAR Handoff for a Photo asset. Absence of either Required field constitutes an invalid Handoff 1 (see [docs/boundary-contracts.md](boundary-contracts.md), Handoff 1 validity condition 1).

---

## Scope

This specification covers Photo assets only, consistent with the scope of the CAR Field Catalogue through MVP6. Video and vector variants of these fields are deferred to MVP10.

This document specifies what the Asset Intelligence Layer must populate. It does not specify:

- How the Asset Intelligence Layer performs OCR or brand detection (implementation decision).
- Storage format or serialisation structure (MVP1 decision).
- Confidence score threshold values — those are defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md); this document cross-references threshold values only.
- Any Content Profile rules or Output Package formatting.

---

## text.strings_present Dependency Chain

`text.strings_present` is the gateway field for the Text and Logos category. Its value determines which conditional fields the Asset Intelligence Layer must evaluate and, by consequence, which fields may appear in the CAR.

**When `text.strings_present = false`:**
The Asset Intelligence Layer has determined that no readable text is detectable in the image. The following conditional fields are dependent on `text.strings_present` being `true` and must therefore be **absent** from the CAR:

- `text.detected_strings`
- `text.watermark_present`
- `text.dominant_language`

These three fields are not evaluated and must not appear in the CAR when `text.strings_present = false`.

**When `text.strings_present = true`:**
The Asset Intelligence Layer has detected readable text. All three conditional fields above must be evaluated. Whether each appears in the CAR then depends on its own individual condition (detailed in the field specifications below).

**Logo-only exception — confirmed PO decision:**
`text.logo_marks_detected` is **independently Conditional** on brand mark detectability. It is NOT part of the `text.strings_present` dependency chain. `text.logo_marks_detected` MAY be present even when `text.strings_present = false`. A symbol-only logo — for example, the Apple logo or the Nike swoosh appearing on an object with no readable accompanying text — is a valid and sufficient condition for `text.logo_marks_detected` to be populated. This independence from `text.strings_present` is a confirmed Product Owner decision and must be implemented as specified. The two conditions are evaluated separately: text detectability drives `text.strings_present`; brand mark detectability drives `text.logo_marks_detected`.

**Summary of dependency rules:**

| Field | Conditional On | Must be absent when |
|---|---|---|
| `text.detected_strings` | `text.strings_present = true` | `text.strings_present = false` |
| `text.watermark_present` | `text.strings_present = true` | `text.strings_present = false` |
| `text.dominant_language` | `text.strings_present = true` AND five or more words AND language determinable | `text.strings_present = false` OR fewer than five words OR language not determinable |
| `text.logo_marks_detected` | Brand mark detectable (independent of `text.strings_present`) | No brand mark detected |
| `text.bounding_boxes` | Optional — Asset Intelligence Layer discretion | No requirement; may be absent even when text or logos are detected |

---

## Field Specifications

### text.strings_present

| Attribute | Value |
|---|---|
| **Field name** | `text.strings_present` |
| **Data type** | boolean |
| **Cardinality** | Required |
| **Condition** | None — always present |

**Description.** A boolean gate field that indicates whether any readable text is detectable in the image. `true` means one or more readable strings were detected; `false` means none were detected. This field is the primary condition controlling the three text-dependent conditional fields: `text.detected_strings`, `text.watermark_present`, and `text.dominant_language`. It does not control `text.logo_marks_detected`, which has its own independent condition.

**Allowed values.** `true` or `false`. No other value is valid. The field must not be absent and must not carry a null value.

**Relationship to logos.** `text.strings_present = true` does not imply that `text.logo_marks_detected` is present, and `text.strings_present = false` does not imply that `text.logo_marks_detected` is absent. The two fields reflect separate detection passes. An image may have readable text and no logos, logos and no readable text, both, or neither.

**Absence rule.** This field is Required. Absence constitutes an invalid Handoff 1.

**Example values.**
- `true` — a product photo where the packaging includes a brand name in readable text.
- `true` — a street photograph where a shop sign is legible in the background.
- `false` — a natural landscape photo with no signage, product labels, or visible text.
- `false` — a portrait photo where a Nike swoosh is visible on a shirt but no readable text appears (note: `text.logo_marks_detected` may still be populated independently).

---

### text.detected_strings

| Attribute | Value |
|---|---|
| **Field name** | `text.detected_strings` |
| **Data type** | Array\<string\> |
| **Cardinality** | Conditional |
| **Condition** | Present when `text.strings_present` is `true` |

**Description.** An array of verbatim text strings detected in the image. Each entry is a distinct readable string as it appears visually. This field records what the OCR process read — not what the text was intended to say. No OCR correction, normalisation, spell-checking, or capitalisation adjustment is applied by the Asset Intelligence Layer.

**OCR verbatim rule.** The Asset Intelligence Layer must record strings exactly as they appear in the image, including OCR errors. If the image displays "COFEE" (misspelled), the entry must be `"COFEE"`, not `"COFFEE"`. If OCR misreads a letterform (e.g., reading "0" for "O"), the misread version must be recorded. This trade-off is acknowledged: OCR inaccuracies in this field will propagate as-is to keyword and description generation in the Content Generation Layer. The Layer 2 consumer is responsible for any downstream treatment of uncertain strings; the Asset Intelligence Layer's obligation is verbatim fidelity, not accuracy correction. If the Asset Intelligence Layer has confidence that a string is unreliably read, that uncertainty should be reflected in `text.confidence_score`, not by altering the string value.

**Allowed values and format.** Each array entry is a string. Entries may be single words, multi-word phrases, or numbers as they appear in the image (e.g., `"OPEN"`, `"Sale 50%"`, `"Nikon"`, `"EXIT"`, `"No Smoking"`). Entries must not include surrounding punctuation that is not part of the visible text. Each distinct visual text block or label should be a separate array entry. There is no maximum entry count.

**Absence rule.** Absent when `text.strings_present = false`. Must not be present as an empty array; if `text.strings_present = true` but no individual strings could be isolated (e.g., text is present but entirely illegible), `text.strings_present` should be re-evaluated. When the field is present, it must contain at least one entry.

**Example values.**
- `["OPEN", "Mon-Fri 9-5"]` — a shop door with an opening hours sign.
- `["Nikon"]` — a camera body with a manufacturer label visible.
- `["Sale 50%", "CLEARANCE"]` — a retail display with promotional signage.
- `["CAUTION", "WET FLOOR"]` — a safety sign in the background of an office scene.
- *(absent)* — `text.strings_present = false`; no readable text detected.

---

### text.logo_marks_detected

| Attribute | Value |
|---|---|
| **Field name** | `text.logo_marks_detected` |
| **Data type** | Array\<string\> |
| **Cardinality** | Conditional |
| **Condition** | Present when one or more brand mark or logo symbols are detectable, regardless of whether associated text is legible or whether `text.strings_present` is `true` |

**Description.** An array of identified brand mark names or descriptions. This field records the visual trademark identifiers — symbol logos, graphic marks, and brand symbols — that are detectable in the image. It is evaluated and populated independently of `text.strings_present`. A symbol-only logo (e.g., the Apple logo appearing on a device with no readable text in the image) is a valid and sufficient reason for this field to be populated even when `text.strings_present = false`.

**Independence from `text.strings_present`.** This field's condition is brand mark detectability alone. The Asset Intelligence Layer must evaluate brand marks regardless of the text detection result. An image with `text.strings_present = false` and a visible Nike swoosh must produce `text.logo_marks_detected: ["Nike swoosh"]`. An image with `text.strings_present = true` and no brand marks must produce `text.logo_marks_detected` absent (or not present). The two fields are independent.

**Sentinel value for unidentified brand marks.** When the Asset Intelligence Layer detects a visual element that is clearly a brand mark or logo symbol but cannot determine its identity, the entry must be `"unidentified_brand_mark"`. This sentinel value must be used exactly as written; no variation (e.g., `"unknown logo"`, `"unidentified logo"`) is valid. Multiple unidentified marks in a single image each produce one `"unidentified_brand_mark"` entry.

**Allowed values and format.** Each entry is a plain string naming the brand mark (e.g., `"Nike swoosh"`, `"Apple logo"`, `"Adidas three stripes"`, `"Starbucks logo"`) or the sentinel value `"unidentified_brand_mark"`. Entries describe the logo or symbol, not the physical object it appears on. The physical object is recorded separately in `objects.brand_objects_detected` (see Cross-Category Boundary below).

**Absence rule.** Absent when no brand mark is detected. Must not be present as an empty array.

**Cross-category trigger.** A non-empty `text.logo_marks_detected` is an input condition for `risk.trademark_flag` in the Risk Flags category. When this field is populated, the Asset Intelligence Layer must evaluate `risk.trademark_flag` and set it to `true`. See [docs/car-field-catalogue.md](car-field-catalogue.md), Risk Flags section, and [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md), Section 2.2, for the default handling policy for `risk.trademark_flag`.

**Example values.**
- `["Apple logo"]` — a laptop with the Apple logo visible; `text.strings_present` may be `false` if no readable text is present.
- `["Nike swoosh"]` — a trainer visible in a lifestyle photograph.
- `["Starbucks logo", "unidentified_brand_mark"]` — a café scene where a Starbucks cup and an unidentifiable branded cup are both present.
- `["unidentified_brand_mark"]` — a brand symbol is clearly visible in the image but cannot be attributed to a known brand.
- *(absent)* — no brand marks or logo symbols detected; consumer goods may still be recorded in `objects.brand_objects_detected`.

---

### text.watermark_present

| Attribute | Value |
|---|---|
| **Field name** | `text.watermark_present` |
| **Data type** | boolean |
| **Cardinality** | Conditional |
| **Condition** | Present when `text.strings_present` is `true` |

**Description.** A boolean flag indicating whether a watermark is detected in the image. A watermark is any overlaid text used for ownership, credit, or access control purposes — for example, a photographer credit (e.g., `"© Jane Smith"`), a stock agency mark (e.g., `"Shutterstock"`), a preview watermark (e.g., `"SAMPLE"` or `"PROOF"`), or a similar text overlay that is not part of the image's depicted content. Downstream channel profiles typically require watermark-free assets; this flag enables routing logic to identify assets that require watermark removal before distribution.

**Condition detail.** This field is present only when `text.strings_present = true`. When `text.strings_present = false`, `text.watermark_present` must be absent. It is possible for `text.strings_present = true` and `text.watermark_present = false` — that is, readable text is present but none of it is a watermark.

**Allowed values.** `true` or `false`. When the field is present, it must carry one of these two values.

**Absence rule.** Absent when `text.strings_present = false`. Absence when `text.strings_present = true` is not valid; when text strings are present, the watermark evaluation must be completed and the result recorded.

**Example values.**
- `true` — the image has `"© 2024 John Doe Photography"` overlaid in a corner.
- `true` — a preview image with `"WATERMARK"` printed across it diagonally.
- `false` — a product label reads `"OPEN"` but no watermark overlay is present.
- *(absent)* — `text.strings_present = false`; no text of any kind was detected.

---

### text.dominant_language

| Attribute | Value |
|---|---|
| **Field name** | `text.dominant_language` |
| **Data type** | string (BCP 47) |
| **Cardinality** | Conditional |
| **Condition** | Present when `text.strings_present` is `true` AND the detected text contains five or more words sufficient to determine a language |

**Description.** The dominant language of the readable text detected in the image, expressed as a BCP 47 language tag. This field supports geographic and editorial classification of assets and enables downstream Content Profiles to apply language-specific keyword generation or to flag an asset's primary text language for channel relevance decisions.

**Five-word threshold.** This field is present only when the detected text contains five or more words that together provide sufficient evidence to determine a language. Fewer than five words are insufficient for reliable language determination; in that case, the field must be absent. Single-word entries in `text.detected_strings` (e.g., `"OPEN"`, `"EXIT"`, `"Nikon"`) rarely constitute evidence of a language and do not individually contribute to the threshold. The Asset Intelligence Layer must evaluate the combined readable vocabulary across all detected strings.

**BCP 47 format requirement.** The field value must be a valid BCP 47 language tag. In practice, two-letter ISO 639-1 codes are used for the most common cases (e.g., `en` for English, `fr` for French, `zh` for Chinese, `de` for German, `es` for Spanish, `ja` for Japanese). Extended tags (e.g., `zh-Hant`, `pt-BR`) are permitted where the script or regional variant can be determined with confidence.

**Absence rule.** Absent when `text.strings_present = false`. Also absent when `text.strings_present = true` but fewer than five words are present, or when the detected words span multiple languages with no dominant language, or when the language cannot be determined. Absence is valid in all these cases and must be treated as unknown by downstream consumers (CAR Consumer Rule 1).

**Example values.**
- `"en"` — an English-language sign with a full sentence of visible text.
- `"fr"` — a French café menu with multiple readable lines.
- `"zh"` — a product label with Chinese characters forming five or more words.
- `"de"` — a German street banner with sufficient readable text.
- *(absent)* — `text.strings_present = true` but detected strings are only `["OPEN", "EXIT"]` — fewer than five words; language cannot be determined.
- *(absent)* — `text.strings_present = false`.

---

### text.bounding_boxes

| Attribute | Value |
|---|---|
| **Field name** | `text.bounding_boxes` |
| **Data type** | Array\<object\> |
| **Cardinality** | Optional |
| **Condition** | None — present at the Asset Intelligence Layer's discretion |

**Description.** Approximate positional descriptors for detected text strings and logo marks in the image. This field provides spatial context that allows downstream consumers to understand roughly where in the frame a text string or brand mark appears. Positional descriptors are high-level compass-zone labels — not pixel coordinates.

**Not pixel-precise.** Entries in this field use a fixed vocabulary of nine positional descriptors (see below). They are approximate zone labels, not bounding rectangles or pixel-coordinate pairs. This design choice keeps the CAR format stable and profile-agnostic — precise coordinates would require consumers to handle different image dimensions and resolutions. Spatial precision is intentionally traded for simplicity and portability at this stage.

**Object schema.** Each entry in the array is an object with the following keys:

| Key | Type | Required | Description |
|---|---|---|---|
| `"target"` | string | Yes | The text string or brand mark name that this positional entry refers to. Must match a value in `text.detected_strings` or `text.logo_marks_detected`. |
| `"position"` | string (enum) | Yes | An approximate positional descriptor for the target within the image frame. Must be one of the nine permitted values listed below. |

**Permitted values for `"position"`:**

| Value | Zone |
|---|---|
| `"top-left"` | Upper-left quadrant of the image |
| `"top-centre"` | Upper-centre strip of the image |
| `"top-right"` | Upper-right quadrant of the image |
| `"centre-left"` | Middle-left area of the image |
| `"centre"` | Central area of the image |
| `"centre-right"` | Middle-right area of the image |
| `"bottom-left"` | Lower-left quadrant of the image |
| `"bottom-centre"` | Lower-centre strip of the image |
| `"bottom-right"` | Lower-right quadrant of the image |

No values other than these nine are valid for the `"position"` key.

**Optional cardinality.** This field may be absent even when text strings or logo marks are detected. Its absence is valid and must be treated as unknown by downstream consumers (CAR Consumer Rule 1). It is not required for a valid Handoff.

**Absence rule.** Absent when the Asset Intelligence Layer does not populate it. Must not be present as an empty array. May also be absent for individual detected items — not every entry in `text.detected_strings` or `text.logo_marks_detected` need have a corresponding bounding box entry.

**Complete example object.**

```json
{
  "target": "Nike swoosh",
  "position": "bottom-right"
}
```

A second example with a text string target:

```json
{
  "target": "OPEN",
  "position": "centre"
}
```

An example showing a multi-entry array with mixed targets:

```json
[
  { "target": "Starbucks logo", "position": "top-left" },
  { "target": "Sale 50%", "position": "bottom-centre" },
  { "target": "unidentified_brand_mark", "position": "centre-right" }
]
```

---

### text.confidence_score

| Attribute | Value |
|---|---|
| **Field name** | `text.confidence_score` |
| **Data type** | float (0–1) |
| **Cardinality** | Required |
| **Condition** | None — always present |

**Description.** A numeric confidence score for the Text and Logos category as a whole. This value reflects the Asset Intelligence Layer's analytical certainty in the category's combined findings — not the quality of the asset or the readability of any individual string. A score of `1.0` represents maximum certainty; a score of `0.0` represents minimum certainty. The score covers all fields in this category collectively.

**Relationship to OCR verbatim rule.** When OCR confidence is low (e.g., text is partially obscured, at an angle, in an unusual font, or in low-resolution), this must be reflected in a lower `text.confidence_score`. The verbatim text strings are still recorded as detected — the lower score signals to consumers that the detected strings should be treated with caution. The confidence score is the correct channel for surfacing OCR uncertainty; string values must not be omitted or altered to communicate uncertainty.

**Threshold and consumer behaviour.** The minimum confidence threshold for this category is **0.70 [PROVISIONAL — confirm at MVP1]**, as defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md), Section 1.2. When `text.confidence_score` is below this threshold, downstream consumers must treat all fields in the Text and Logos category as unknown and apply CAR Consumer Rule 2. The category name `"text"` will appear in `confidence.low_confidence_categories` when this threshold is not met.

**Risk flag exception.** Even when `text.confidence_score` falls below the minimum threshold, any `risk.trademark_flag` triggered by `text.logo_marks_detected` must still be propagated to downstream consumers. A below-threshold confidence score on the Text and Logos category does not suppress active risk flags. This rule is defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md), Section 1.3 (special case) and CAR Consumer Rule 4.

**Allowed values.** Any float value in the closed range `[0.0, 1.0]` inclusive. Values outside this range are invalid.

**Absence rule.** This field is Required. Absence constitutes an invalid Handoff 1. The Asset Intelligence Layer must always produce a score, even when confidence is minimal (in which case the score is a low value near `0.0`, not an absent field).

**Example values.**
- `0.97` — high-confidence text detection from a well-lit, clearly legible sign at close range.
- `0.82` — good confidence with one partially obscured string included in `text.detected_strings`.
- `0.71` — confidence just above the provisional threshold; observations are valid but borderline.
- `0.48` — below the provisional threshold; all Text and Logos fields must be treated as unknown by consumers, but any active risk flags must still be propagated.
- `0.12` — very low confidence; OCR result is highly uncertain.

---

## Cross-Category Dependencies

### Risk Flags — `risk.trademark_flag`

A non-empty `text.logo_marks_detected` is an input condition for `risk.trademark_flag` in the Risk Flags category. When `text.logo_marks_detected` contains one or more entries (including `"unidentified_brand_mark"`), the Asset Intelligence Layer must:

1. Evaluate the Risk Flags category for trademark presence.
2. Set `risk.trademark_flag = true`.

The default handling policy for `risk.trademark_flag` is **Suppress output** — content fields that directly reference the trademark or brand name are suppressed from generated output, but the asset is not blocked from proceeding. Individual Content Profiles may escalate this default policy. Full policy definition is in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md), Section 2.2.

`risk.trademark_flag` must be propagated regardless of `text.confidence_score`. A low confidence score on the Text and Logos category does not suppress an already-triggered trademark flag.

### Objects and Subjects — `objects.brand_objects_detected`

`text.logo_marks_detected` and `objects.brand_objects_detected` are complementary, not mutually exclusive. A single physical object in the image may produce entries in both fields simultaneously — the object itself in the Objects category, and the brand mark on it in the Text and Logos category. See the Cross-Category Boundary section below for worked examples and boundary rules.

---

## Edge Cases

The following edge cases require explicit Asset Intelligence Layer behaviour decisions.

**1. Image with a symbol-only logo and no readable text.**
`text.strings_present` must be `false`. `text.logo_marks_detected` must be populated with the identified brand mark (or `"unidentified_brand_mark"` if identity is unknown). `text.detected_strings`, `text.watermark_present`, and `text.dominant_language` must be absent. `risk.trademark_flag` must be set to `true`. This is the canonical case for the logo-only exception.

**2. Image where text is present but entirely illegible.**
If the Asset Intelligence Layer can visually determine that text-like forms exist but cannot read any characters, `text.strings_present` should be `false` — unreadable forms do not constitute detected strings. If OCR reads partial characters, `text.strings_present = true` and the partial strings are recorded verbatim in `text.detected_strings`, with a low `text.confidence_score` reflecting the uncertainty.

**3. Image with fewer than five words — dominant language absent.**
`text.strings_present = true`. `text.detected_strings` is populated with the detected words. `text.dominant_language` is absent. This is not an error condition; it reflects the five-word threshold for language determination. `text.watermark_present` must still be evaluated and populated.

**4. Multiple brand marks detected, one identified and one not.**
`text.logo_marks_detected` contains the identified brand name (e.g., `"Apple logo"`) and the sentinel value `"unidentified_brand_mark"` as separate entries. `risk.trademark_flag` is set to `true`. Both entries are valid; the sentinel does not replace identified entries.

**5. Watermark and regular text both present.**
`text.strings_present = true`. `text.detected_strings` contains all detected strings, including the watermark text (verbatim). `text.watermark_present = true`. The watermark text appears in `text.detected_strings` as a verbatim string because it is a readable text form — the `text.watermark_present` boolean is an additional signal, not a replacement for the string entry.

**6. Image with branded text (e.g., "NIKE" readable) and a brand symbol (Nike swoosh) simultaneously.**
- `text.strings_present = true`.
- `text.detected_strings` → `["NIKE"]` — records the readable brand text verbatim.
- `text.logo_marks_detected` → `["Nike swoosh"]` — records the brand mark symbol separately.
- Both fields are populated; they are not mutually exclusive. If a branded consumer good (e.g., a trainer) is also present, `objects.brand_objects_detected` records the physical object. All three fields may be populated simultaneously for one physical object.

**7. `text.bounding_boxes` present for some but not all detected items.**
`text.bounding_boxes` is Optional and may contain entries for a subset of detected strings and logo marks. The Asset Intelligence Layer is not required to provide a bounding box entry for every item in `text.detected_strings` or `text.logo_marks_detected`. Partial coverage is valid. Entries in `text.bounding_boxes` whose `target` does not match any value in `text.detected_strings` or `text.logo_marks_detected` must not be produced.

**8. `text.strings_present = true` but OCR produces only noise characters.**
If the OCR pass produces character sequences that do not form recognisable strings (e.g., `"%%##@@"` from a highly degraded image region), these must be recorded verbatim in `text.detected_strings` if the Asset Intelligence Layer's OCR pipeline produced them. `text.confidence_score` must reflect the very low confidence in these findings. Downstream consumers applying CAR Consumer Rule 2 will treat the category as unknown when the score falls below the threshold.

---

## Cross-Category Boundary: Logo Marks vs Brand Objects

The boundary between `text.logo_marks_detected` (this category) and `objects.brand_objects_detected` (Objects and Subjects category, story #18) is a common source of recording error. This section defines the boundary unambiguously and is consistent with the Objects and Subjects category specification in [docs/car-objects-spec.md](car-objects-spec.md).

### The Rule

**`text.logo_marks_detected` records brand mark symbols** — the visual trademark identifiers: logo graphics, symbol marks, and brand icons that are detectable as brand identity elements, whether or not they contain readable text.

**`objects.brand_objects_detected` records physical consumer goods** — the objects themselves that happen to carry brand marks, without recording the brand identity or mark.

A single physical object can generate entries in both fields simultaneously. The fields are complementary, not mutually exclusive.

### Examples

**Scenario 1: Laptop with a visible manufacturer logo.**
- `objects.brand_objects_detected` → `["laptop"]` — records the physical consumer good.
- `text.logo_marks_detected` → `["Apple logo"]` — records the brand mark detected on the device.

**Scenario 2: Coffee cup with a printed brand mark.**
- `objects.brand_objects_detected` → `["coffee cup with brand mark"]` — records the physical branded object.
- `text.logo_marks_detected` → `["Starbucks logo"]` (if identified) or `["unidentified_brand_mark"]` (if not identified) — records the brand mark.

**Scenario 3: Trainer with a visible brand symbol and readable brand text.**
- `objects.brand_objects_detected` → `["sneaker"]` — records the physical object.
- `text.logo_marks_detected` → `["Nike swoosh"]` — records the visible trademark symbol.
- `text.detected_strings` → `["NIKE"]` — records the readable brand text as a verbatim string.

**Scenario 4: Symbol-only logo with no readable text and no associated consumer good visible.**
- `objects.brand_objects_detected` → *(absent or not populated for this element)*.
- `text.logo_marks_detected` → `["Apple logo"]` — records the brand mark.
- `text.strings_present` → `false` (if no other readable text is present).

### What Does Not Belong in `text.logo_marks_detected`

The following must not be recorded in this field:

- Readable brand names or brand text (record in `text.detected_strings`).
- Physical consumer goods themselves (record in `objects.brand_objects_detected`).
- Non-trademark visual elements such as decorative patterns, abstract shapes, or artistic symbols that are not associated with a specific brand identity.

---

## Consistency with Field Catalogue

This specification is derived from and must remain consistent with the Text and Logos section of [docs/car-field-catalogue.md](car-field-catalogue.md). The following items clarify or extend the Field Catalogue without conflicting with it.

| Clarification | Catalogue entry | This specification's extension |
|---|---|---|
| `text.logo_marks_detected` independence from `text.strings_present` | Catalogue states "regardless of whether associated text is legible" | This spec makes the independence explicit: `text.logo_marks_detected` is evaluated on its own condition and may be present when `text.strings_present = false`. This is a confirmed PO decision. |
| `text.logo_marks_detected` sentinel value | Catalogue states `"unidentified_brand_mark"` as the entry for unidentified marks | This spec states the exact sentinel string, prohibits variations, and clarifies that multiple unidentified marks each produce one `"unidentified_brand_mark"` entry. |
| `text.detected_strings` verbatim rule | Catalogue states "no OCR correction or normalisation is applied" | This spec explains the trade-off explicitly: OCR errors propagate as-is; the confidence score is the correct mechanism for surfacing uncertainty, not string alteration. |
| `text.dominant_language` threshold | Catalogue states "five or more words sufficient to determine a language" | This spec clarifies that single brand-name entries do not individually count toward the threshold and that the five words are evaluated across all `text.detected_strings` entries. |
| `text.bounding_boxes` object schema | Catalogue states "approximate positional descriptor" without a schema | This spec defines the full object schema: `target` and `position` keys, nine permitted `position` values, and partial coverage validity. |
| `text.confidence_score` and risk flag interaction | Not stated in catalogue | This spec adds the risk flag exception: below-threshold confidence does not suppress `risk.trademark_flag`. Cross-references [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md). |

Any future change to the Text and Logos fields in the CAR Field Catalogue must be reflected in a corresponding update to this document. Conflicts must be resolved in favour of the Field Catalogue, with this document updated to match.

---

## Cross-References

- **CAR Field Catalogue:** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative field names, data types, and cardinality for all seven fields specified here.
- **CAR concept definition:** [docs/canonical-asset-record.md](canonical-asset-record.md) — Consumer Rules 1–4 governing how all fields in this category must be interpreted by downstream consumers.
- **Confidence and Risk Rules:** [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) — threshold values for `text.confidence_score`, the population rule for `confidence.low_confidence_categories`, and the default handling policy for `risk.trademark_flag`.
- **Objects and Subjects field specification:** [docs/car-objects-spec.md](car-objects-spec.md) — Cross-Category Boundary section; defines `objects.brand_objects_detected` and its relationship to `text.logo_marks_detected`.
- **Boundary Contracts:** [docs/boundary-contracts.md](boundary-contracts.md) — Handoff 1 validity conditions, including the requirement that all Required fields be present.
- **Domain Glossary:** [docs/glossary.md](glossary.md) — Canonical Asset Record, Asset Intelligence Layer, Content Generation Layer, Handoff, Confidence Score, Risk Flag, Output Package, Content Profile.
