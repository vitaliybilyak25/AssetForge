# CAR Locations Category — Field Specification

> **Story #88 — Draft v0.1**
> This document is the implementation-ready field specification for the Locations category of the Canonical Asset Record (CAR). It is the authoritative reference for any Layer 1 (Asset Intelligence Layer) developer producing Locations fields in a CAR Handoff. All field names, types, and cardinality in this document are taken from the **CAR Field Catalogue** ([docs/car-field-catalogue.md](car-field-catalogue.md), story #78) and must not conflict with it. In any conflict, the Field Catalogue governs and this document must be updated accordingly.

---

## Overview

The Locations category records the geographic and environmental context observable in the asset or asserted by its embedded technical metadata. It answers the question: *Where was this asset captured, and what kind of environment does it depict?* — independently of any audience, channel, or intended use.

Location observations are factual findings derived exclusively from visual analysis of the asset or from hardware-recorded metadata embedded at the moment of capture (EXIF). They are never fabricated, assumed, or inferred from channel requirements. The Content Generation Layer reads these fields to anchor geographic keywords, location-specific descriptions, and editorial classification logic.

The Locations category contains seven fields: two Required fields (environment type and confidence score) and five Conditional fields (setting descriptor, GPS coordinates, GPS-derived region, visual landmark, and urban/rural signal).

---

## Scope

**In scope:** Photo assets only. All location analysis is single-frame inference — what is observable from a still image, or what is asserted by EXIF metadata attached to that image.

**Out of scope until MVP10:** Video and vector assets. Time-based location inference (movement tracking, scene transitions, location changes across frames) is deferred. No Locations field in this specification may be populated using temporal reasoning; every value must be derivable from a single image frame or from metadata embedded in the asset file.

---

## Field Specifications

### location.environment_type

| Attribute | Value |
|---|---|
| **Field name** | `location.environment_type` |
| **Data type** | string (enum) |
| **Cardinality** | Required |
| **Condition** | — (always present) |

**Allowed values:**

| Value | Definition |
|---|---|
| `indoor` | The depicted scene is wholly inside an enclosed or roofed structure — a room, building interior, vehicle cabin, or similar enclosed space. |
| `outdoor` | The depicted scene is wholly outside an enclosed structure — open sky, natural landscape, street, or any exterior setting. |
| `mixed` | The depicted scene contains a combination of indoor and outdoor elements that are both compositionally significant — for example, a covered outdoor market, a conservatory, a building entrance with both interior and exterior visible in the frame, or a roofed structure open on multiple sides. |

**Absence rule:** None — this field is Required. Its absence constitutes an invalid CAR Handoff (see [docs/boundary-contracts.md](boundary-contracts.md), Handoff 1 validity conditions).

**Classification rule:** `location.environment_type` is always determinable from a photo by visual analysis. Even an abstract or macro image carries observable cues — lighting characteristics, surface textures, material types, architectural elements, or visible sky — sufficient to classify the environment. The value `mixed` must only be used when both indoor and outdoor elements are genuinely compositionally present and neither alone describes the scene; it must not be used as a fallback when the classification is uncertain. Uncertainty about environment type must be reflected in `location.confidence_score`, not in the choice of enum value.

**Example values:**
```json
"location.environment_type": "indoor"
"location.environment_type": "outdoor"
"location.environment_type": "mixed"
```

---

### location.setting_descriptor

| Attribute | Value |
|---|---|
| **Field name** | `location.setting_descriptor` |
| **Data type** | string |
| **Cardinality** | Conditional |
| **Condition** | Present when the setting is classifiable with sufficient visual evidence |

**Allowed values / format:** A short descriptive label identifying the specific type of setting depicted in the image. The label is a plain noun phrase describing what kind of place the environment represents — not a proper name for a specific location (that is recorded in `location.visual_landmark`). Examples: `"home office"`, `"urban street"`, `"forest trail"`, `"commercial kitchen"`, `"beach"`, `"hospital corridor"`, `"retail store"`, `"conference room"`, `"public park"`, `"warehouse"`. The value is inferred from visible environmental cues such as furnishings, equipment, architectural style, natural elements, signage context, and surface characteristics.

**Absence rule:** The field is absent when the available visual evidence is insufficient to classify the setting with reasonable confidence. Absence means the Asset Intelligence Layer could not identify the setting type with sufficient certainty, not that the asset has no setting. A downstream consumer must treat an absent `location.setting_descriptor` as unknown, not as confirmation that the setting is unclassifiable (CAR Consumer Rule 1). The consumer must not substitute a default label or infer a setting from other Locations fields.

**Format constraint:** The value is a plain, lowercase descriptive phrase. Proper place names, brand names, and geographic identifiers must not appear in this field; those belong in `location.visual_landmark` or `location.gps_derived_region`.

**Example values:**
```json
"location.setting_descriptor": "home office"
"location.setting_descriptor": "forest trail"
"location.setting_descriptor": "commercial kitchen"
"location.setting_descriptor": "urban rooftop"
```

---

### location.gps_coordinates

| Attribute | Value |
|---|---|
| **Field name** | `location.gps_coordinates` |
| **Data type** | object `{lat: float, lon: float}` |
| **Cardinality** | Conditional |
| **Condition** | Present when valid GPS coordinates are embedded in the asset's EXIF metadata |

**Object structure:** The field is an object with exactly two required properties:
- `lat` — latitude as a floating-point decimal degree value (negative values indicate south of the equator).
- `lon` — longitude as a floating-point decimal degree value (negative values indicate west of the prime meridian).

An optional `alt` property (altitude, in metres, as a float) may be present when EXIF `GPSAltitude` is also available, but is not a separately catalogued CAR field.

**GPS-from-EXIF-only constraint (story #87, Sections 2.1 and 3.1):** `location.gps_coordinates` is populated exclusively from EXIF metadata (`GPSLatitude` and `GPSLongitude` tags). **Visual inference of GPS coordinates is explicitly prohibited.** The Asset Intelligence Layer must not estimate, approximate, or derive latitude/longitude values from visual content — even when a landmark, skyline, landscape, or other geographic feature is recognisably identified. GPS coordinates entered in the CAR must be direct, unmodified readings from the asset's EXIF block.

**Ingestion rule (story #87, Section 2.1):** Both `GPSLatitude` and `GPSLongitude` must be present and parseable for the field to be populated. Partial GPS — where one tag is present but the other is absent or malformed — must not be ingested. A malformed or unparseable GPS tag results in an absent `location.gps_coordinates` and a processing log entry recording the parse failure; it does not cause a Handoff failure.

**Absence rule (CAR Consumer Rule 1):** When no valid GPS is embedded in the asset, `location.gps_coordinates` is absent. This is a valid CAR state — the field's absence means GPS data was not available, not that the asset was taken in an indoor space, a GPS-denied zone, or any other specific location. Downstream consumers must treat an absent `location.gps_coordinates` as **unknown** — not as "no location" and not as any negative assertion. Consumers must not infer a location from this field's absence, and must not default to any geographic assumption (CAR Consumer Rule 1, [docs/canonical-asset-record.md](canonical-asset-record.md), Section 4, Rule 1).

**Reference:** [docs/embedded-metadata-ingestion.md](embedded-metadata-ingestion.md), story #87, Sections 2.1 and 3.1.

**Example values:**
```json
"location.gps_coordinates": {"lat": 48.8584, "lon": 2.2945}
"location.gps_coordinates": {"lat": 40.7580, "lon": -73.9855}
"location.gps_coordinates": {"lat": -33.8688, "lon": 151.2093, "alt": 42.0}
```

---

### location.gps_derived_region

| Attribute | Value |
|---|---|
| **Field name** | `location.gps_derived_region` |
| **Data type** | string |
| **Cardinality** | Conditional |
| **Condition** | Present when `location.gps_coordinates` is present and reverse-geocoding produces a result, or when IPTC IIM location fields are available and GPS is absent |

**Allowed values / format:** A human-readable geographic region string identifying the location at city, region, and country granularity (e.g., `"San Francisco, California, United States"`, `"Paris, Île-de-France, France"`, `"Kyoto, Kyoto Prefecture, Japan"`). The format follows the result of the reverse-geocoding service and may vary with the service used; implementers must document the specific geocoding provider and format convention applied.

**Source hierarchy — GPS primary, IPTC supplementary, absent when neither available:**

This field has a defined authority hierarchy for its source:

1. **GPS-derived (primary authority):** When `location.gps_coordinates` is present, `location.gps_derived_region` is derived by reverse-geocoding the GPS latitude and longitude. This is the highest-authority source. The GPS-derived value is the primary value for this field.

2. **IPTC IIM supplementary (lower authority):** When `location.gps_coordinates` is absent, the IPTC IIM fields `City` (2:90), `Province-State` (2:95), and `Country-Primary Location Name` (2:101) may be used to populate `location.gps_derived_region` as a supplementary signal. When this source is used, it must be documented as a supplementary, lower-authority signal — not as GPS-derived data. IPTC location fields represent assertions made by a photographer or editorial workflow at an earlier point in the production process; they may not accurately reflect the geographic coordinates of the actual capture location (story #87, Section 2.2).

3. **Absent:** When neither GPS coordinates nor IPTC IIM location fields are available, `location.gps_derived_region` is absent.

**When GPS is present and IPTC fields also exist:** The GPS-derived reverse-geocoding result takes precedence. The IPTC city/state/country fields are recorded as a supplementary annotation in processing logs only and do not override the GPS-derived value in the CAR.

**Absence rule:** The field is absent when neither GPS coordinates nor IPTC location data is available, or when reverse-geocoding of valid GPS coordinates returns no result. Consumers must treat an absent `location.gps_derived_region` as unknown (CAR Consumer Rule 1) — absence does not mean the asset was taken at an unrecognised location.

**Reference:** [docs/embedded-metadata-ingestion.md](embedded-metadata-ingestion.md), story #87, Section 2.2; [docs/canonical-asset-record.md](canonical-asset-record.md), Section 4, Rule 1.

**Example values:**
```json
"location.gps_derived_region": "San Francisco, California, United States"
"location.gps_derived_region": "Paris, Île-de-France, France"
"location.gps_derived_region": "Kyoto, Kyoto Prefecture, Japan"
```

---

### location.visual_landmark

| Attribute | Value |
|---|---|
| **Field name** | `location.visual_landmark` |
| **Data type** | string |
| **Cardinality** | Conditional |
| **Condition** | Present when an identifiable geographic landmark is visible in the image with high confidence |

**Allowed values / format:** The common name of a visually identifiable landmark or recognisable geographic place that is clearly visible in the image frame (e.g., `"Eiffel Tower"`, `"Times Square"`, `"Sydney Opera House"`, `"Golden Gate Bridge"`, `"Colosseum"`). The value is a proper name, consistently capitalised. Generic setting descriptors must not appear here; those belong in `location.setting_descriptor`.

**Visual-analysis-only constraint:** This field is populated from visual analysis of the image content only. It does not depend on GPS presence or absence. A landmark may be identified visually even when no GPS is embedded, and GPS data does not automatically populate this field. The two fields are independent.

**High-confidence-only rule:** `location.visual_landmark` must only be set when the Asset Intelligence Layer can identify the landmark with high confidence — sufficient to avoid misidentification. A partial, obscured, or ambiguous structure that might be a landmark must not be recorded here. When landmark detection is possible but below the high-confidence threshold, the field must be absent; uncertainty must not be resolved by guessing. The threshold for "high confidence" is defined in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md), story #84.

**Single-value constraint:** This field holds the name of one landmark. If multiple identifiable landmarks are present, the single most prominent or compositionally central landmark should be recorded. If two or more landmarks are equally prominent and no single dominant landmark can be identified with high confidence, the field is absent.

**Cross-category dependency — `risk.property_release_required`:** Detection of a visual landmark may contribute to the evaluation of `risk.property_release_required` in the Risk Flags category. Certain landmarks involve privately owned, architecturally protected, or commercially controlled structures where commercial photography distribution requires a property release. When `location.visual_landmark` is set, the Asset Intelligence Layer must evaluate whether the identified landmark is subject to property release requirements and, if so, set `risk.property_release_required = true`. This evaluation is not automatic for every landmark — it depends on the landmark's legal status. The full list of landmark-level property release triggers is maintained in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md). See the Cross-Category Dependencies section for the full dependency chain.

**Absence rule:** The field is absent when no landmark is identifiable with high confidence, when no landmark is present, or when the scene is generic with no recognisable specific place. Consumers must treat an absent `location.visual_landmark` as unknown (CAR Consumer Rule 1) — absence means no high-confidence landmark was detected, not that the image contains no landmark.

**Example values:**
```json
"location.visual_landmark": "Eiffel Tower"
"location.visual_landmark": "Times Square"
"location.visual_landmark": "Sydney Opera House"
```

---

### location.urban_rural_signal

| Attribute | Value |
|---|---|
| **Field name** | `location.urban_rural_signal` |
| **Data type** | string (enum) |
| **Cardinality** | Conditional |
| **Condition** | Present when `location.environment_type` is `outdoor` and sufficient environmental cues are present to classify the settlement context |

**Allowed values:**

| Value | Definition |
|---|---|
| `urban` | A densely built environment characterised by multi-storey buildings, city infrastructure, heavy commercial or residential density, city streets, or other indicators of a metropolitan or city centre setting. |
| `suburban` | A moderately built environment characterised by lower-density housing, residential neighbourhoods, local commercial areas, or the transitional zone between urban centres and rural areas. |
| `rural` | A low-density landscape primarily characterised by agricultural land, scattered buildings, villages, farmland, or managed land with visible human habitation or activity at low density. |
| `wilderness` | A natural landscape with no visible human habitation or built infrastructure — forests, mountains, deserts, oceans, wetlands, or any environment that is substantially undeveloped. |

**Applicability constraint:** This field applies exclusively to outdoor scenes. It must be absent when `location.environment_type` is `indoor` or when the setting provides insufficient cues to classify the settlement context even though the environment is outdoor (e.g., an extreme close-up of foliage with no broader landscape visible). The field must also be absent when `location.environment_type` is `mixed` and no clear outdoor context is classifiable.

**Absence rule:** Absent when: (a) `location.environment_type` is not `outdoor`; (b) the image is outdoor but environmental cues are insufficient to classify settlement context with sufficient confidence; or (c) `location.confidence_score` is below the minimum threshold. Consumers must treat an absent `location.urban_rural_signal` as unknown (CAR Consumer Rule 1).

**Example values:**
```json
"location.urban_rural_signal": "urban"
"location.urban_rural_signal": "wilderness"
"location.urban_rural_signal": "suburban"
"location.urban_rural_signal": "rural"
```

---

### location.confidence_score

| Attribute | Value |
|---|---|
| **Field name** | `location.confidence_score` |
| **Data type** | float (0–1) |
| **Cardinality** | Required |
| **Condition** | — (always present) |

**Allowed values / format:** A floating-point number in the closed interval [0.0, 1.0], inclusive. A value of `1.0` represents maximum analytical certainty in the Locations category findings. A value of `0.0` represents zero certainty. The score reflects the Asset Intelligence Layer's certainty in the Locations category as a whole — it is a category-level signal, not a per-field score.

**Semantics:** The confidence score does not indicate whether location information was found; it indicates how certain the layer is in whatever findings it produced. A high confidence score on a sparsely populated Locations category (e.g., only `location.environment_type` present and all Conditional fields absent) means the layer is confident in its findings and in the absence of classifiable Conditional fields. A low confidence score means the layer's analysis was uncertain, regardless of whether Conditional fields are populated.

**Threshold:** The minimum threshold for a downstream consumer to act on Locations category fields as confirmed observations is **0.70 (provisional — confirm at MVP1)**. If `location.confidence_score` is below this threshold, the consumer must treat all Locations fields as unknown and apply CAR Consumer Rule 2. The threshold value and its implications are fully specified in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md), story #84.

**Relationship to `confidence.low_confidence_categories`:** If `location.confidence_score` is strictly below the minimum threshold, the Asset Intelligence Layer must add `"locations"` to the `confidence.low_confidence_categories` array, as specified in the Confidence Score Thresholds document.

**Absence rule:** None — this field is Required. Its absence constitutes an invalid CAR Handoff (see [docs/boundary-contracts.md](boundary-contracts.md), Handoff 1 validity conditions).

**Example values:**
```json
"location.confidence_score": 0.94
"location.confidence_score": 0.72
"location.confidence_score": 0.48    // below threshold — "locations" added to confidence.low_confidence_categories
```

---

## Cross-Category Dependencies

### Dependency 1 — `location.visual_landmark` may trigger `risk.property_release_required` (Risk Flags category)

When `location.visual_landmark` is set, the Asset Intelligence Layer must evaluate whether the identified landmark is subject to property release requirements and set `risk.property_release_required` accordingly. The dependency flows as:

```
location.visual_landmark is present (landmark identified with high confidence)
  → Asset Intelligence Layer evaluates property release status of landmark
    → if landmark is subject to property release:
        risk.property_release_required = true
        → downstream consumers must not deliver commercial Output Packages
          without a recorded property release or human review override
    → if landmark is not subject to property release:
        no change to risk.property_release_required from this dependency
```

**Directionality:** The dependency flows from Locations to Risk Flags — not the reverse. `risk.property_release_required` does not set `location.visual_landmark`; the Locations field is the upstream detection evidence, and the Risk Flags field is the downstream compliance conclusion.

**Important:** `location.visual_landmark` is not the only condition that can trigger `risk.property_release_required`. The risk field is also evaluated when other private property or branded structures are detected through visual analysis, independently of whether a named landmark is identified. A `true` value on `risk.property_release_required` must be propagated regardless of which upstream condition triggered it.

**Consumer note:** Downstream consumers must not infer that a landmark requires a property release from the presence of `location.visual_landmark` alone. The landmark name must be evaluated against the known property release trigger list. The full list of property-release-triggering landmarks is maintained in [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md).

---

### Dependency 2 — `location.urban_rural_signal` depends on `location.environment_type = "outdoor"`

`location.urban_rural_signal` has a hard dependency on the `location.environment_type` field within the same category. The dependency chain is:

```
location.environment_type = "outdoor"
  → AND sufficient environmental cues are present
    → location.urban_rural_signal may be populated
```

When `location.environment_type` is `indoor` or `mixed`, `location.urban_rural_signal` must be absent. The field is not a general landscape classifier; it specifically characterises the settlement context of outdoor scenes. Consumers reading an absent `location.urban_rural_signal` must treat the settlement context as unknown (CAR Consumer Rule 1) — they must not infer an urban/rural signal from other fields or from the absence of this field.

---

## Edge Cases

### Edge Case 1 — GPS present but reverse-geocoding returns no result

**Scenario:** `location.gps_coordinates` is successfully populated from EXIF (`GPSLatitude` and `GPSLongitude` both present and parseable). The reverse-geocoding service is called with the coordinates but returns no result — for example, the coordinates are in a remote ocean location, a polar region, or an area not covered by the geocoding service's data set.

**Required behaviour:**
- `location.gps_coordinates` remains present with the parsed coordinate values.
- `location.gps_derived_region` is absent (the condition for its presence — "reverse-geocoding produces a result" — is not met).
- The absence of `location.gps_derived_region` is a valid Conditional absence; it does not constitute a Handoff failure.
- The processing log records the coordinates and the geocoding service's no-result response.
- Downstream consumers must treat `location.gps_derived_region` as unknown (CAR Consumer Rule 1); they must not infer a region from the numeric coordinates themselves.

---

### Edge Case 2 — GPS absent; IPTC city/state/country partially populated

**Scenario:** No EXIF GPS is embedded. IPTC IIM fields are present but only partially populated — for example, `City` (2:90) is present but `Province-State` (2:95) and `Country-Primary Location Name` (2:101) are absent.

**Required behaviour:**
- `location.gps_coordinates` is absent (valid — no EXIF GPS available).
- `location.gps_derived_region` may be populated from the available IPTC fields as a supplementary signal with lower authority than GPS-derived data. The value is assembled from whichever IPTC fields are present (e.g., `"Rome"` from city alone if state and country are absent).
- The populated value must be treated as a lower-authority supplementary signal and documented as such in processing logs.
- If only a single IPTC field is present and its value alone is insufficient to produce a meaningful geographic region (e.g., a city name that is ambiguous without country context), the Asset Intelligence Layer may choose to omit the field rather than produce a misleading value. This is an implementation decision to be confirmed at MVP1.
- Downstream consumers must apply appropriate caution to IPTC-supplemented `location.gps_derived_region` values; they reflect an editorial assertion, not a hardware-recorded position.

---

### Edge Case 3 — Landmark visually identified but GPS places asset elsewhere

**Scenario:** Visual analysis identifies `location.visual_landmark` as a specific named landmark. GPS coordinates from EXIF, when reverse-geocoded, place the asset in a different location — either because the photograph was taken from a distance, or because the GPS data is from a different device or session.

**Required behaviour (story #87, Section 3.1):**
- `location.gps_coordinates` is populated from EXIF with the GPS-sourced coordinates (EXIF GPS takes precedence for the coordinates field).
- `location.gps_derived_region` is derived from the GPS coordinates by reverse-geocoding.
- `location.visual_landmark` is set to the identified landmark based on visual analysis.
- The two fields may therefore describe different geographic locations. This is a valid and expected state — the landmark is what is visible in the image; the GPS coordinates record where the camera was positioned at capture time.
- The processing log records both values and notes the geographic discrepancy for diagnostic purposes.
- Downstream consumers must not attempt to reconcile the two fields. Each field describes a different observable fact: `location.gps_coordinates` describes camera position; `location.visual_landmark` describes what is visible in the frame.

---

### Edge Case 4 — `location.environment_type` is `mixed`; `location.urban_rural_signal` applicability

**Scenario:** `location.environment_type` is classified as `mixed` — for example, a covered outdoor market that is partially enclosed.

**Required behaviour:**
- `location.urban_rural_signal` must be absent. The field's condition requires `location.environment_type = "outdoor"` strictly. A `mixed` classification does not satisfy this condition.
- If the outdoor component of a `mixed` scene is independently classifiable as urban or rural, this information may be noted in `location.setting_descriptor` (e.g., `"covered market, urban district"`) as a descriptive label but must not be encoded in `location.urban_rural_signal`.
- Downstream consumers reading an absent `location.urban_rural_signal` where `location.environment_type` is `mixed` must treat the settlement context as unknown (CAR Consumer Rule 1).

---

## Consistency with Field Catalogue

The following table maps each field in this specification to its corresponding entry in the CAR Field Catalogue ([docs/car-field-catalogue.md](car-field-catalogue.md), story #78, Section 3) and confirms alignment.

| Field Name | Type (Catalogue) | Cardinality (Catalogue) | Alignment |
|---|---|---|---|
| `location.environment_type` | string (enum) | Required | Consistent. This spec adds the three enum values (`indoor`, `outdoor`, `mixed`), the classification rule for `mixed`, and the constraint that uncertainty is reflected in the confidence score rather than in enum selection. |
| `location.setting_descriptor` | string | Conditional | Consistent. This spec states the exact condition (sufficient visual evidence), the format constraint (no proper names), and the absence rule. |
| `location.gps_coordinates` | object `{lat: float, lon: float}` | Conditional | Consistent. This spec adds the GPS-from-EXIF-only constraint, the both-tags-required ingestion rule, the malformed-GPS handling rule, and the Consumer Rule 1 absence interpretation. References story #87, Sections 2.1 and 3.1. |
| `location.gps_derived_region` | string | Conditional | Consistent. This spec extends the catalogue condition to include the IPTC supplementary source and documents the full source hierarchy (GPS primary → IPTC supplementary → absent). References story #87, Section 2.2. |
| `location.visual_landmark` | string | Conditional | Consistent. This spec adds the visual-analysis-only constraint, the high-confidence-only rule, the single-value constraint, and the cross-category dependency on `risk.property_release_required`. |
| `location.urban_rural_signal` | string (enum) | Conditional | Consistent. This spec adds all four enum values (`urban`, `suburban`, `rural`, `wilderness`) and the applicability constraint limiting the field to outdoor scenes. |
| `location.confidence_score` | float (0–1) | Required | Consistent. This spec adds the threshold reference (0.70, provisional), the `confidence.low_confidence_categories` population rule, and the absence rule. |

**Conflict resolution:** If any value, type, condition, or cardinality in this document conflicts with the CAR Field Catalogue, the Field Catalogue governs. Raise the conflict for resolution and update this document to match the confirmed catalogue entry.

---

## Cross-References

- **CAR Field Catalogue (story #78):** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative field names, types, cardinality, and conditions for all Locations fields. Section 3 is the Locations category.
- **CAR Concept Definition (story #15):** [docs/canonical-asset-record.md](canonical-asset-record.md) — Consumer Rules 1–4, the Locations category concept definition, and the immutability rule governing the CAR Handoff. Consumer Rule 1 (absent fields are unknown, not negative) is cited throughout this specification.
- **Embedded Metadata Ingestion (story #87):** [docs/embedded-metadata-ingestion.md](embedded-metadata-ingestion.md) — EXIF GPS ingestion rules (Section 2.1), IPTC IIM location field mapping (Section 2.2), Locations category precedence rules (Section 3.1), and absent embedded metadata handling (Section 6). The GPS-from-EXIF-only constraint and the IPTC supplementary signal rule are both sourced from this document.
- **Confidence Score Thresholds and Risk Flag Handling Rules (story #84):** [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) — threshold values for `location.confidence_score`; high-confidence threshold for `location.visual_landmark`; property release trigger list for landmarks.
- **Boundary Contracts (story #77):** [docs/boundary-contracts.md](boundary-contracts.md) — Handoff 1 validity conditions, including the requirements that `location.environment_type` and `location.confidence_score` are always present.
- **Domain Glossary:** [docs/glossary.md](glossary.md) — canonical definitions for Canonical Asset Record, Asset Intelligence Layer, Confidence Score, Risk Flag, Handoff, Content Profile, Output Package, and all other capitalised terms used in this document.
