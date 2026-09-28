# Embedded Metadata Ingestion — Specification

This document specifies how the Asset Intelligence Layer reads existing embedded metadata from a Photo asset file (EXIF, IPTC IIM, and XMP) and maps that data into the Canonical Asset Record (CAR). It is a Layer 1 design specification, not an implementation task. All field names and categories follow the authoritative definitions in [docs/car-field-catalogue.md](car-field-catalogue.md). All architectural constraints follow [docs/boundary-contracts.md](boundary-contracts.md). All CAR concepts follow [docs/canonical-asset-record.md](canonical-asset-record.md).

**Story:** #87 (MVP1)
**PO decisions applied:** see [issue #87 comments](https://github.com/vitaliybilyak25/AssetForge/issues/87) for the three confirmed PO decisions that shaped this specification.

---

## 1. Scope and Purpose

Many Photo assets carry metadata embedded at capture time (camera EXIF), at editorial production time (IPTC IIM), or at post-processing time (XMP). This embedded data can include GPS coordinates, rights assertions, subject classifications, and creator identity. Discarding this data forces the Asset Intelligence Layer to re-infer facts that the asset itself asserts, wasting inference budget and introducing avoidable uncertainty.

This specification defines:

- Which embedded fields are ingested and mapped to which CAR fields.
- Which embedded fields are explicitly excluded and why.
- The precedence rule applied per CAR category when an embedded value and an AI-detected value disagree.
- How the Asset Intelligence Layer handles assets where some or all embedded metadata blocks are absent.
- How conflicts that the precedence rules do not cleanly resolve are recorded.

**What this specification does not define:**

- Implementation code, parsing libraries, or byte-level tag extraction.
- Writing metadata back to the source file — that is a Channel Adaptation Layer concern.
- Validation of the accuracy or authority of embedded assertions — the CAR records what is asserted, not whether it is correct.
- New field names for rights and provenance fields not yet in the field catalogue — those are MVP1 implementation decisions (see Section 5 for placeholders).

---

## 2. Mapping Tables

For each source standard the table states: the source field name or tag identifier, the target CAR field name (from story #78 where the field exists, or a placeholder where it does not), the CAR category (from the seven categories defined in story #15), and any notes required for implementers.

### 2.1 EXIF Fields

EXIF data is embedded by the camera or capture device at the moment of recording. It is the highest-authority source for GPS and hardware-level provenance data.

| Source Standard | Source Field | Target CAR Field | CAR Category | Notes |
|---|---|---|---|---|
| EXIF 2.32 | `GPSLatitude` + `GPSLongitude` | `location.gps_coordinates` (object `{lat, lon}`) | Locations | Both tags must be present and parseable; partial GPS is not ingested. Already defined in story #78. |
| EXIF 2.32 | `GPSAltitude` | Annotation on `location.gps_coordinates` | Locations | Stored as an optional `alt` property on the `location.gps_coordinates` object. Not a separate CAR field. |
| EXIF 2.32 | `DateTimeOriginal` | **Provenance — outside the seven categories** | — | PO decision: treated as asset provenance metadata, not added to the CAR field catalogue in this story. Field name and placement to be determined in MVP1 implementation. Flagged as placeholder — see Section 5. |
| EXIF 2.32 | `Make` + `Model` (camera) | **Provenance — outside the seven categories** | — | Camera make and model are hardware provenance metadata. Not added to the CAR field catalogue in this story. Field name and placement to be determined in MVP1 implementation. Flagged as placeholder — see Section 5. |
| EXIF 2.32 | `Orientation` | **Provenance — outside the seven categories** | — | Technical orientation tag. Relevant to image rendering, not to factual content analysis. Field name and placement to be determined in MVP1 implementation. Flagged as placeholder — see Section 5. |

### 2.2 IPTC IIM Fields

IPTC IIM data is embedded by photographers, editorial production workflows, or digital asset management systems. It is the authoritative source for rights assertions and creator identity.

| Source Standard | Source Field (Tag ID) | Target CAR Field | CAR Category | Notes |
|---|---|---|---|---|
| IPTC IIM | `City` (2:90), `Province-State` (2:95), `Country-Primary Location Name` (2:101) | `location.gps_derived_region` (supplementary) | Locations | Used only when `location.gps_coordinates` is absent. These fields supplement — they do not override — GPS-derived region data. If GPS is present, this embedded text is recorded as a supplementary annotation, not as the primary `location.gps_derived_region` value. |
| IPTC IIM | `Subject Reference` (2:12) — IPTC Subject News Codes | `objects.detected_subjects` (advisory signal) | Objects and Subjects | Supplementary signal only. AI detection takes precedence. Embedded subject codes may enrich the `objects.detected_subjects` array but do not override AI-detected values. See precedence rules in Section 3. |
| IPTC IIM | `By-line` (2:80) | `rights.creator` | Rights | **PLACEHOLDER — new field, not yet in story #78.** PO decision: deferred; no catalogue update required in this story. Mapping recorded for MVP1 implementers. See Section 5. |
| IPTC IIM | `Copyright Notice` (2:116) | `rights.copyright_notice` | Rights | **PLACEHOLDER — new field, not yet in story #78.** PO decision: deferred; no catalogue update required in this story. Mapping recorded for MVP1 implementers. See Section 5. |
| IPTC IIM | `Credit` (2:110) | `rights.credit_line` | Rights | **PLACEHOLDER — new field, not yet in story #78.** PO decision: deferred; no catalogue update required in this story. Mapping recorded for MVP1 implementers. See Section 5. |

**Excluded IPTC IIM field:**

| Source Field | Exclusion Reason |
|---|---|
| `Caption/Abstract` (2:120) | Narrative text field — see Section 4. |

### 2.3 XMP Fields

XMP metadata is embedded by image-editing software (Adobe Lightroom, Photoshop, Capture One) and often mirrors IPTC IIM values. It is the authoritative source for rights presence signals.

| Source Standard | Source Field | Target CAR Field | CAR Category | Notes |
|---|---|---|---|---|
| XMP / Dublin Core | `dc:subject` (keyword bag) | `objects.detected_subjects` (advisory signal) | Objects and Subjects | Supplementary signal only. AI detection takes precedence. Embedded keywords may enrich the `objects.detected_subjects` array but do not override AI-detected values. See precedence rules in Section 3. |
| XMP / Dublin Core | `dc:rights` | `rights.copyright_notice` | Rights | **PLACEHOLDER — maps to the same new field as IPTC `Copyright Notice` (2:116).** PO decision: deferred; no catalogue update required in this story. See Section 5. |
| XMP Rights Management | `xmpRights:Marked` | `rights.rights_metadata_present` | Rights | **PLACEHOLDER — new boolean field, not yet in story #78.** `true` when the XMP Rights Management block is present and `xmpRights:Marked` is set. PO decision: deferred; no catalogue update required in this story. See Section 5. |
| XMP / IPTC Core | `Iptc4xmpCore:CreatorContactInfo` | `rights.creator` (supplementary) | Rights | **PLACEHOLDER — same target new field as IPTC `By-line`.** Supplementary to the IPTC IIM value when both are present; IPTC IIM takes precedence for rights fields. PO decision: deferred. See Section 5. |

**Excluded XMP fields:**

| Source Field | Exclusion Reason |
|---|---|
| `dc:description` | Narrative text field — see Section 4. |
| `dc:title` | Narrative text field — see Section 4. |

---

## 3. Precedence Rules

When the Asset Intelligence Layer produces an AI-detected value for a CAR field and an embedded metadata value is also available for the same field, the following per-category rules determine which value is recorded in the CAR.

These rules apply at the category level. Within a category, all sub-fields follow the same precedence direction.

### 3.1 Locations Category

**Embedded EXIF GPS takes precedence over AI-detected location signals.**

GPS coordinates are a hardware-recorded assertion made at the moment of capture by a receiver with direct positional data. Visual inference of location cannot achieve the same precision or authority. When `GPSLatitude` and `GPSLongitude` are both present and parseable:

- `location.gps_coordinates` is populated from EXIF.
- AI-detected location signals (e.g., visual landmark inference) are recorded in `location.visual_landmark` where applicable but do not override the GPS coordinates.
- `location.gps_derived_region` is derived from the GPS coordinates; IPTC city/state/country fields supplement this value only when GPS is absent.

When GPS is absent, IPTC IIM location fields (`City`, `Province-State`, `Country-Primary Location Name`) may be used to populate `location.gps_derived_region` as a supplementary signal with lower authority than GPS-derived data.

### 3.2 Objects and Subjects Category

**AI detection takes precedence over embedded IPTC Subject Codes and XMP keywords.**

AI analysis of the visual content produces `objects.detected_subjects` from what is actually visible in the image. Embedded IPTC Subject News Codes (2:12) and XMP `dc:subject` keywords reflect classifications applied at an earlier point in a production workflow and may not accurately reflect the visual content of the specific asset.

Embedded subject signals are treated as advisory: they may be used to enrich the `objects.detected_subjects` array (e.g., to surface a concept the AI did not detect with sufficient confidence) but they do not replace, remove, or reorder AI-detected values.

### 3.3 People Category

**AI detection takes precedence.** There are no embedded metadata standards that reliably encode person-detection signals at the level of specificity required by the CAR People category fields (`persons.present`, `persons.count`, `persons.faces_detected`, etc.). These fields are populated exclusively from AI analysis.

### 3.4 Text and Logos Category

**AI detection takes precedence.** Embedded metadata does not encode the text strings visible within the image frame. `text.detected_strings`, `text.logo_marks_detected`, and related fields are populated exclusively from AI visual analysis (OCR and logo detection).

### 3.5 Activities Category

**AI detection takes precedence.** Embedded metadata does not encode activity or event classification at the field level required by the CAR Activities category. These fields are populated exclusively from AI analysis.

### 3.6 Risk Flags Category

**AI detection takes precedence, with embedded signals as supplementary input.** Risk flags (`risk.model_release_required`, `risk.editorial_only`, `risk.trademark_flag`, etc.) are generated by the Asset Intelligence Layer from visual analysis. An embedded IPTC `xmpRights:Marked` flag or editorial classification tag may serve as a supplementary signal to the risk evaluation pass but does not replace the AI-generated risk assessment.

### 3.7 Rights Category (When Confirmed in a Future Story)

**Embedded IPTC/XMP values take precedence** for rights fields (`rights.creator`, `rights.copyright_notice`, `rights.credit_line`, `rights.rights_metadata_present`). These fields represent explicit assertions made by the rights holder or photographer; AI analysis has no basis to override them. This rule is recorded here for completeness; the fields themselves are deferred to a future story (see Section 5).

When both IPTC IIM and XMP carry the same rights field (e.g., `Copyright Notice` from IPTC 2:116 and `dc:rights` from XMP), the IPTC IIM value takes precedence; the XMP value is recorded as a supplementary annotation if they differ.

---

## 4. Explicit Exclusions

The following embedded metadata fields must not be ingested into the CAR under any circumstances.

| Excluded Field | Standard | Reason |
|---|---|---|
| `dc:description` | XMP / Dublin Core | Narrative text generated by a human editor or AI tool for a specific audience and channel. This is channel-specific content, not a neutral factual observation. Ingesting it into the CAR would violate the CAR's purpose statement ("channel-agnostic facts only") and the Layer 1 Boundary Contract, which prohibits the Asset Intelligence Layer from producing titles, descriptions, captions, or any text shaped by audience or channel requirements. |
| `dc:title` | XMP / Dublin Core | As above. An embedded title is an authored content field, not a factual observation. |
| `Caption/Abstract` (2:120) | IPTC IIM | As above. IPTC captions are human-authored editorial or descriptive text fields intended for a specific publication or channel. They are not factual observations about the asset's visual content. |
| `Headline` (2:105) | IPTC IIM | As above. An IPTC headline is a short editorial content string authored for a specific editorial context. |

**Rationale anchored to architecture:** The CAR purpose statement (story #15, Section 1) defines the CAR as the answer to one question: "What is in this asset, as a matter of observable, channel-agnostic fact?" The Layer 1 Boundary Contract (story #77) prohibits the Asset Intelligence Layer from generating "titles, descriptions, keywords, captions, or any other text content shaped by audience, tone, or channel requirements." Embedded narrative text fields are exactly this: channel-shaped human-authored content. Including them in the CAR would contaminate the factual record and invalidate Handoff 1 validity condition 5 ("no content decisions embedded").

If the team later revisits the decision to exclude these fields (e.g., to pre-populate a notes field in the ArchiveForge module), that decision requires a separate story and a CAR concept update (story #15), not a revision of this specification.

---

## 5. New Field Placeholders

The following CAR fields are identified by this story as the correct targets for embedded metadata ingestion but are not yet defined in the story #78 field catalogue. Per PO decision, no catalogue update is required in this story. Each placeholder is recorded here with its proposed field name, proposed CAR category, and the data it would hold, so that MVP1 implementers can add these fields to the catalogue when the time comes.

| Proposed Field Name | CAR Category | Type | Source | Notes |
|---|---|---|---|---|
| `rights.creator` | Rights (new) | string | IPTC `By-line` (2:80); XMP `Iptc4xmpCore:CreatorContactInfo` | Photographer or creator name as asserted by the rights holder. IPTC IIM value takes precedence over XMP when both are present. |
| `rights.copyright_notice` | Rights (new) | string | IPTC `Copyright Notice` (2:116); XMP `dc:rights` | Full copyright notice string (e.g., "© 2024 Jane Smith. All rights reserved."). IPTC IIM value takes precedence over XMP when both are present. |
| `rights.credit_line` | Rights (new) | string | IPTC `Credit` (2:110) | Credit line as specified by the photographer or agency (e.g., "Jane Smith / Getty Images"). |
| `rights.rights_metadata_present` | Rights (new) | boolean | XMP `xmpRights:Marked` | `true` when the XMP Rights Management block is present and the asset has been explicitly marked with rights metadata. Used as a downstream routing signal. |
| `provenance.capture_date` | Provenance (outside seven categories) | string (ISO 8601) | EXIF `DateTimeOriginal` | Date and time the photo was captured as recorded by the camera. Treated as asset provenance metadata, not a factual observation about visual content. Placement outside the seven categories confirmed by PO decision. |
| `provenance.camera_make` | Provenance (outside seven categories) | string | EXIF `Make` | Camera manufacturer (e.g., "Canon", "Nikon", "Sony"). |
| `provenance.camera_model` | Provenance (outside seven categories) | string | EXIF `Model` | Camera model name (e.g., "EOS R5", "Z7 II", "A7R V"). |
| `provenance.orientation` | Provenance (outside seven categories) | integer (EXIF enum 1–8) | EXIF `Orientation` | EXIF orientation tag value. Relevant to rendering; placement and naming to be confirmed in MVP1 implementation. |

**Implementation note:** When any of these placeholder fields are added to the field catalogue (story #78 update), the Rights fields should carry cardinality of `Conditional` (present only when the corresponding embedded tag is readable and non-empty). The Provenance fields are outside the seven CAR categories; their cardinality model and catalogue placement are for the MVP1 implementation team to decide.

---

## 6. Absent Embedded Metadata

Many Photo assets are submitted without any EXIF, IPTC, or XMP block — or with only one or two of the three standards present. The Asset Intelligence Layer must handle all such cases without error.

**Rule:** If an embedded metadata block (EXIF, IPTC IIM, or XMP) is absent from the asset file, the Asset Intelligence Layer must treat all fields that would have been sourced from that block as unknown and proceed to AI analysis without raising a Handoff failure.

This rule is aligned with CAR Consumer Rule 1 (story #15, Section 4): "If a CAR field or category is absent, the consumer must treat the information as unknown ... The consumer must not infer a negative conclusion from an absence." The same principle applies within Layer 1: absence of an EXIF GPS block does not mean the photo was taken indoors or at an unknown location — it means GPS data is not available, and the Asset Intelligence Layer must proceed on that basis.

**Specific cases:**

| Scenario | Required behaviour |
|---|---|
| No EXIF block | `location.gps_coordinates` is absent (valid). Provenance placeholder fields are absent (valid). AI analysis proceeds normally. |
| EXIF present but no GPS tags | `location.gps_coordinates` is absent (valid). Other EXIF tags are processed normally. |
| No IPTC IIM block | All IPTC-sourced fields are absent (valid). AI analysis proceeds normally. |
| No XMP block | All XMP-sourced fields are absent (valid). AI analysis proceeds normally. |
| All three blocks absent | CAR is produced from AI analysis alone. All embedded-metadata-sourced fields are absent. This is a fully valid CAR. |
| EXIF GPS present but unparseable (malformed coordinates) | `location.gps_coordinates` is absent (valid). A processing log entry records the parse failure. AI analysis proceeds. |

Absence of embedded metadata does not constitute a Handoff failure and must not surface as an error to the Content Generation Layer.

---

## 7. Conflict Handling

A conflict occurs when the Asset Intelligence Layer produces an AI-detected value for a field and an embedded metadata value is also present for the same field, and the two values are materially different.

**Rule (per PO decision):** Conflicts are recorded in processing logs only. No `conflict_flag` field or annotation is added to the CAR. The CAR carries the value determined by the category precedence rule in Section 3; the discarded value and the nature of the conflict are recorded in the processing log for the asset.

**Rationale:** Adding a conflict annotation field to the CAR would require a story #78 update and introduce a new field that downstream consumers would need to interpret. At MVP1, processing logs are sufficient for diagnostic and audit purposes. If production use reveals that conflict visibility in the CAR is needed (e.g., for human review routing), that is a separate story.

**Logging requirement:** The processing log entry for a conflict must record:
- The asset identifier.
- The CAR field affected.
- The value selected (and the source — AI or embedded).
- The value discarded (and the source — AI or embedded).
- The precedence rule applied (referencing the category from Section 3).

Example: if EXIF GPS coordinates place an asset in Paris and AI visual analysis detects the Eiffel Tower but at coordinates inconsistent with the GPS position, the processing log records the GPS value (selected, per Section 3.1), the visual landmark value (discarded), and the Locations precedence rule applied.

---

## 8. Cross-References

- **CAR concept definition (story #15):** [docs/canonical-asset-record.md](canonical-asset-record.md) — purpose, seven information categories, immutability rule, and Consumer Rules (especially Rule 1 on absent fields).
- **CAR field catalogue (story #78):** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative source for all target field names, types, and cardinality used in Section 2 mapping tables.
- **Boundary Contracts (story #77):** [docs/boundary-contracts.md](boundary-contracts.md) — Layer 1 prohibited responsibilities; Handoff 1 validity conditions (especially condition 5: no content decisions embedded).
- **Domain Glossary:** [docs/glossary.md](glossary.md) — definitions for Asset, Canonical Asset Record, Confidence Score, Risk Flag, Handoff, and related terms.
- **Confidence and Risk Rules (story #84):** [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) — threshold values applied to `location.confidence_score` and other category scores referenced in Section 3.
