# Adobe Stock Submission Rules

This document is the authoritative reference for Adobe Stock submission rules within the AssetForge platform. It gives profile authors the accurate, testable constraint values needed to configure the `stock/adobe-stock` Content Profile dimensions, and gives stories #24 (output fields), #25 (AI prompt), and #26 (validators) a shared, agreed baseline for all dimension values.

This document is the deliverable for **story #23**.

> **Scope note.** This document covers Adobe Stock submission rules broadly — including rules that apply to portal-direct submission. Story #24 documents the narrower CSV Output Package specification, which differs from the portal path in one important respect: the Adobe Stock bulk upload CSV has no Description column. That distinction is called out explicitly in Section 2.

---

## Overview

Adobe Stock is a commercial stock marketplace operated by Adobe Inc. Contributors submit photos, illustrations, vectors, and video under a royalty-sharing licence model. Each submitted asset must conform to Adobe Stock's content quality, metadata completeness, rights clearance, and classification requirements before it is accepted into the marketplace.

Within AssetForge, the `stock/adobe-stock` Content Profile governs the generation and delivery of metadata Output Packages for Adobe Stock. This document specifies the rules that Content Profile must enforce. The rules are organised by the metadata field category they govern, followed by cross-cutting rules for editorial classification, AI-generated content declaration, and release requirements.

---

## Source and Verification

| Item | Detail |
|---|---|
| Source date | 2026-09-28 |
| Primary source | Adobe Stock Contributor Portal — submission guidelines, CSV bulk upload specification, and editorial submission policy |
| Supplementary source | AssetForge internal boundary-contracts.md worked example (Adobe Stock, Section: Worked Example — Lifestyle Photo Submitted for Adobe Stock); AssetForge boundary-contracts.md Content Profile dimension values (keyword count: 5–49 confirmed in that example) |
| Keyword count verification | 5 minimum / 49 maximum — confirmed by sample CSV inspection and documented in docs/boundary-contracts.md worked example (Layer 2 description: "within the 5–49 keyword range") |
| Verification status | Representative set; all values should be re-verified against the live Adobe Stock Contributor Portal at implementation time, as platform policies are subject to change |

---

## 1. Title Rules

### 1.1 Constraints

| Constraint | Value |
|---|---|
| Minimum length | 1 character (non-empty) |
| Maximum length | 200 characters |
| Required | Yes — the Title field is mandatory in both the CSV bulk upload and portal-direct submission |
| Character set | UTF-8; no HTML or markdown formatting |
| Prohibited content | Contributor brand names, photographer names, file names, competitor agency names, pricing or licensing terms, keyword stuffing (repeating keywords verbatim in the title text) |
| Capitalisation | Standard title case or sentence case; all-caps is not accepted |

The Title must be a factual, descriptive label for the asset's subject matter. It must not function as a keyword list, a promotional slogan, or a SEO tag string. It must describe what is visually depicted, not what the buyer might use it for.

### 1.2 CAR fields that supply the signal

| CAR Field | Role |
|---|---|
| `objects.primary_subject` | Anchors the subject of the title |
| `objects.detected_subjects` | Provides supporting subject terms |
| `activities.primary_activity` | Supplies the verb or action phrase when a person or activity is central |
| `persons.activity_posture` | Informs compositional title phrasing (e.g., "woman standing at", "chef preparing") |
| `location.setting_descriptor` | Supplies the environmental context phrase |
| `location.gps_derived_region` | Provides a place name when geography is a meaningful title element |
| `risk.trademark_flag` | When `true`, brand names detected via `text.logo_marks_detected` must be suppressed from the title |

### 1.3 Examples

**Conformant example**

Asset: a photograph of a woman working at a standing desk in a home office, face visible, branded laptop partially visible.

- Title: `"Woman Working at Standing Desk in Bright Home Office"`
- Character count: 51 — within the 200-character limit.
- Brand name of the laptop is suppressed because `risk.trademark_flag = true`; the title references the object category ("laptop" or "computer") rather than the brand.

**Non-conformant example**

- Title: `"home office woman desk laptop apple macbook productivity remote work modern professional"`
- Reason non-conformant: this is a keyword string, not a title. It exceeds no character limit but violates the no-keyword-stuffing rule, includes a brand name when `risk.trademark_flag` is active, and does not form a grammatical description.

---

## 2. Description Rules (portal web UI only — not in CSV Output Package)

### 2.1 Scope and channel distinction

**Critical channel distinction:** The Adobe Stock bulk upload CSV has exactly five columns: Filename, Title, Keywords, Category, Releases. There is no Description column in the CSV format. Description is entered only through the Adobe Stock Contributor Portal web UI when submitting assets individually or editing submissions after bulk upload.

This means:
- Description rules apply to **portal-direct submission** and post-upload portal editing.
- The `stock/adobe-stock` **CSV Output Package does not include a Description field**.
- Story #24 (CSV output fields specification) must not add a Description column to the CSV schema.
- If AssetForge adds a portal-direct submission path in a future MVP, Description generation must be implemented and validated at that point.

The rules below are documented for completeness and for any future portal-direct submission feature.

### 2.2 Constraints (portal-direct submission)

| Constraint | Value |
|---|---|
| Field | Optional on portal; enhances discoverability when provided |
| Maximum length | Approximately 200–500 characters (Adobe Stock does not publish a hard character limit; treat 500 characters as a conservative upper bound pending implementation-time verification) |
| Required | No — omitting the description does not block submission |
| Character set | UTF-8; no HTML or markdown formatting |
| Prohibited content | Same prohibited terms as Title (competitor names, pricing, keyword stuffing) |
| Language | English (US) is recommended for maximum search reach; portal accepts other languages |

The Description, when provided, should elaborate on the Title — providing context about the scene, mood, setting, or intended use that is not captured in the short title phrase. It must not duplicate the Title verbatim or repeat the keyword list.

### 2.3 CAR fields that supply the signal

| CAR Field | Role |
|---|---|
| `objects.detected_subjects` | Populates supporting subject detail beyond the primary subject |
| `objects.scene_type` | Informs compositional description phrasing |
| `activities.detected_activities` | Supplies activity and scene-context sentences |
| `activities.social_context` | Informs group or interpersonal framing |
| `location.setting_descriptor` | Provides the environmental setting description |
| `location.gps_derived_region` | Provides geographic context when relevant |
| `persons.age_range_signals` | Informs demographic description terms |
| `persons.group_composition` | Informs group composition description |
| `objects.colour_palette` | Can be referenced for mood or aesthetic description |

### 2.4 Examples

**Conformant example**

Asset: a photograph of a professional chef preparing a dish in a commercial kitchen, face visible.

- Description: `"Professional chef in a white uniform preparing a gourmet dish in a well-lit commercial kitchen. Ideal for food industry, culinary, and restaurant-themed projects."`
- This elaborates the scene, references setting and context, and avoids keyword stuffing.

**Non-conformant example**

- Description: `"chef food cooking kitchen restaurant professional gourmet culinary meal preparation"`
- Reason non-conformant: this is a keyword string, not a sentence-form description. It repeats terms that belong in the keyword list rather than providing contextual elaboration.

---

## 3. Keyword Rules

### 3.1 Constraints

| Constraint | Value |
|---|---|
| Minimum keyword count | **5** |
| Maximum keyword count | **49** |
| Format | Comma-separated list; each keyword is a single word or short phrase (typically 1–3 words) |
| Capitalisation | Lowercase preferred; sentence case is tolerated; all-caps keywords are not accepted |
| Language | English (US) |
| Duplicates | Not permitted within the keyword list for a single asset |
| Prohibited terms | Competitor agency names; trademarked brand names when `risk.trademark_flag = true`; terms that do not describe the asset's actual content; adult content terms on non-adult-classified assets |
| Ordering | Adobe Stock recommends placing the most relevant, specific keywords first; general category terms last |

The 5-minimum / 49-maximum range is verified from the boundary-contracts.md worked example, which states the keyword list was generated with "38 keywords generated in English (US)... all within the 5–49 keyword range." This is the governing value for all Content Profile Validation Rule implementations.

### 3.2 CAR fields that supply the signal

| CAR Field | Role |
|---|---|
| `objects.detected_subjects` | Primary source for subject and object keywords |
| `objects.primary_subject` | Highest-priority keyword anchor |
| `objects.scene_type` | Drives compositional and conceptual keywords |
| `objects.colour_palette` | Can supply colour-descriptor keywords for aesthetic searches |
| `activities.detected_activities` | Supplies action and lifestyle keywords |
| `activities.primary_activity` | Highest-priority activity keyword anchor |
| `persons.age_range_signals` | Demographic keywords (e.g., "adult", "young woman") |
| `persons.group_composition` | Group composition keywords (e.g., "couple", "group") |
| `persons.activity_posture` | Posture and compositional keywords |
| `location.setting_descriptor` | Setting and environment keywords |
| `location.gps_derived_region` | Geographic keywords when location is identifiable |
| `location.visual_landmark` | Landmark name keyword when confidently identified |
| `location.urban_rural_signal` | Context keywords (e.g., "urban", "rural") |
| `text.logo_marks_detected` | Brand names that must be **excluded** from keywords when `risk.trademark_flag = true` |
| `risk.trademark_flag` | When `true`, triggers suppression of trademark-referencing keywords (default policy: Suppress output — see docs/confidence-and-risk-rules.md Section 2.2) |

### 3.3 Examples

**Conformant example**

Asset: the lifestyle home-office photograph from the boundary-contracts.md worked example.

- Keyword count: 38 keywords including: `"woman, standing desk, home office, productivity, remote work, lifestyle, working, technology, natural light, indoor, modern workplace, professional, focus, ..."` (illustrative subset).
- 38 is within the 5–49 range. Laptop brand name excluded. All terms are descriptive and relevant.

**Non-conformant example — too few keywords**

- Keyword list: `"woman, desk, office"` (3 keywords).
- Reason non-conformant: count of 3 falls below the minimum of 5. The Validation Rule in the Channel Adaptation Layer must reject this Output Package as invalid.

**Non-conformant example — too many keywords**

- Keyword list containing 52 distinct terms.
- Reason non-conformant: count of 52 exceeds the maximum of 49. The Validation Rule must reject this Output Package as invalid.

**Non-conformant example — trademark inclusion**

- Keywords include `"Apple MacBook"` when `risk.trademark_flag = true` and `text.logo_marks_detected` contains `"Apple logo"`.
- Reason non-conformant: trademark-referencing keywords must be suppressed per the default Suppress output policy for `risk.trademark_flag`.

---

## 4. Category Taxonomy

### 4.1 Overview

Adobe Stock requires each submitted asset to be assigned exactly one Category from a predefined numeric taxonomy. The Category is a required field in the CSV bulk upload (the fourth of the five columns) and in portal-direct submission.

The Category is resolved by the Content Generation Layer based on CAR signals and written to the Output Package by the Channel Adaptation Layer. Profile authors must configure the category-mapping logic in the `stock/adobe-stock` Content Profile.

### 4.2 Representative category list with numeric codes

The following categories and codes are indicative of Adobe Stock's taxonomy as of the source date. **This list must be verified against the live Adobe Stock Contributor Portal at implementation time.** Adobe Stock may update, rename, or renumber categories without notice.

| Code | Category Name |
|---|---|
| 1 | Animals |
| 2 | Buildings/Architecture |
| 3 | Business/Finance |
| 4 | Education |
| 5 | Food/Drink |
| 6 | Holidays |
| 7 | Industrial |
| 8 | Interiors |
| 9 | Miscellaneous |
| 10 | Nature |
| 11 | People |
| 12 | Religion |
| 13 | Science |
| 14 | Signs/Symbols |
| 15 | Sports/Recreation |
| 16 | Technology |
| 17 | Transportation/Vehicles |
| 18 | Travel/Locations |
| 19 | Vintage/Retro |
| 20 | Celebrities |

### 4.3 Category resolution from CAR signals

Category assignment is a Content Generation Layer responsibility. The primary mapping signals are:

| CAR Field | Role in category resolution |
|---|---|
| `objects.primary_subject` | First-priority signal; maps primary subject to the closest category |
| `objects.scene_type` | Supports disambiguation when multiple categories are plausible |
| `activities.primary_activity` | Drives category selection for activity-led images (e.g., sports, cooking) |
| `persons.present` | When `true` and persons are the primary subject, favours category 11 (People) |
| `location.setting_descriptor` | Informs category selection for location-led images (e.g., interiors, architecture) |

When no single category is unambiguously correct from the CAR signals, the Content Generation Layer must apply a configured fallback rule from the `stock/adobe-stock` Content Profile rather than default silently to category 9 (Miscellaneous). The fallback rule is a profile configuration decision for story #24.

---

## 5. Editorial vs Commercial Submission Paths

### 5.1 How Adobe Stock distinguishes the two paths

Adobe Stock labels assets as either commercial or editorial in its submission interface and applies corresponding licence restrictions in search results. Commercially licensed assets may be used in advertising and promotional materials. Editorial assets carry a licence restriction notice and may not be used for advertising, marketing, or promotional purposes.

Adobe Stock does not accept assets that occupy an ambiguous middle ground: every submitted asset must be classified as one or the other at submission time.

### 5.2 Application of the classification decision sequence to Adobe Stock

The classification decision sequence from `docs/commercial-editorial-classification.md` Section 5 applies to all `stock/adobe-stock` Output Package generation. The steps below restate the sequence with Adobe Stock-specific outcomes at each step.

**Step 1 — Check `risk.editorial_only`.**

If `risk.editorial_only = true`, the asset must follow the editorial submission path. The `stock/adobe-stock` Content Profile must block commercial Output Package generation and route the asset to Approval Requirements. Do not proceed past Step 1 without a resolved human override.

Adobe Stock editorial submission requirements (when `risk.editorial_only = true`):
- The asset is submitted under the editorial licence type.
- The Title and keywords must describe the factual event, person, or place — no promotional or aspirational phrasing.
- A caption describing the event, date, and location is required. The caption is generated from `location.setting_descriptor`, `activities.primary_activity`, and `location.gps_derived_region`.
- Model releases are not required for editorial submissions (see Section 7 and `docs/adobe-stock-release-rules.md` Section 5).

**Step 2 — Check `risk.model_release_required` and `risk.property_release_required`.**

If either flag is `true`, verify whether a confirmed release record is present. If no confirmation is available, block commercial Output Package delivery and route to Approval Requirements. The default handling policy for both flags is Require human review (`docs/confidence-and-risk-rules.md` Section 2.2, rows 1–2).

**Step 3 — Check `risk.trademark_flag`.**

If `true`, apply the trademark gate rule: suppress keyword and description content that directly references the detected trademark. Commercial generation may continue for non-trademark-referencing fields. The `stock/adobe-stock` Content Profile Validation Rules must specify the trademark tolerance rule; the domain default is Suppress output.

**Step 4 — Check `activities.editorial_event_signal`.**

If `true` and `risk.editorial_only` was not already set, treat as a strong editorial indicator. Route to Approval Requirements (human review) before commercial generation proceeds.

**Step 5 — Evaluate remaining classification signals.**

Evaluate `persons.faces_detected` and `text.logo_marks_detected` as supporting evidence for any unresolved review routing decisions. These fields do not independently determine classification but inform the human reviewer's context.

**Step 6 — Generate the Output Package with classification resolved.**

Adobe Stock does not include an explicit commercial/editorial column in its CSV (unlike Shutterstock's `Editorial` column). The classification is expressed through the submission path selection in the portal and through the presence or absence of release documentation in the `Releases` column. The Output Package must record the resolved classification value for routing and audit trail purposes (planned for MVP4), even if the classification is not a named CSV column.

### 5.3 CAR fields that carry the classification signal

See `docs/commercial-editorial-classification.md` Section 2 for the full field list. The load-bearing fields for Adobe Stock classification are:

| CAR Field | Role |
|---|---|
| `risk.editorial_only` | Primary gate — blocks commercial path when `true` |
| `activities.editorial_event_signal` | Strong editorial indicator at Step 4 |
| `risk.model_release_required` | Commercial clearance gate at Step 2 |
| `risk.property_release_required` | Commercial clearance gate at Step 2 |
| `risk.trademark_flag` | Trademark gate at Step 3 |
| `persons.faces_detected` | Supporting evidence at Step 5 |
| `text.logo_marks_detected` | Supporting evidence at Step 5 |

---

## 6. AI-Generated Content Declaration

### 6.1 Adobe Stock's requirement

Adobe Stock requires contributors to declare whether a submitted asset was generated by an AI tool (e.g., generative AI image synthesis, AI-assisted composition). This declaration is a mandatory disclosure for AI-generated content. Adobe Stock labels AI-generated assets visibly in search results.

The declaration is made at submission time — it is not a metadata field embedded in the asset file. In the portal, there is an explicit checkbox or toggle at the point of upload. In bulk upload workflows, the mechanism for declaring AI-generated status must be confirmed against the current Adobe Stock CSV specification at implementation time (the CSV column for AI declaration, if any, was not included in the five-column CSV specification current at the source date of this document; portal-direct declaration may be the only path available).

**Rule:** Any asset that was produced in whole or in part by generative AI must be declared as AI-generated at submission time. Failing to declare AI-generated content is a violation of Adobe Stock's contributor agreement and may result in account suspension.

### 6.2 Mapping to a submission-time attribute

The AI-generated content declaration is a **submission-time attribute**, not a metadata field embedded in the Output Package. This means:

- It is not a column in the Adobe Stock CSV.
- It is not a CAR field.
- It is not a Content Profile field in the current AssetForge schema.
- It must be captured and surfaced to the submitter at the point of upload or Output Package delivery, not embedded in the CSV row.

In AssetForge terms, this attribute must be supplied by the contributor at submission time — either as a property of the submission batch or as a per-asset flag — and communicated to Adobe Stock through whatever mechanism the portal provides (checkbox, API parameter, or CSV column if Adobe Stock adds one).

### 6.3 Implementation gap — CAR field catalogue

**The CAR field catalogue (`docs/car-field-catalogue.md`) does not currently contain an `ai_generated` field.** There is no CAR field that records whether the asset was produced by generative AI. This is a known gap with two implications:

1. **For story #24 and #26:** The `stock/adobe-stock` Content Profile and its validators cannot currently derive the AI-generated declaration from a CAR signal. The Validation Rules in the Channel Adaptation Layer cannot gate on this attribute because it is not present in the CAR.

2. **For story #78 (CAR field catalogue) and a future CAR revision:** A future story should add an `asset.ai_generated` field (or equivalent — field name TBD) to the CAR to carry this signal. Until that field exists, the AI-generated declaration must be handled as a manual contributor-supplied attribute outside the automated pipeline.

**Profile authors must note:** Do not add `ai_generated` to the CSV Output Package schema (story #24) as if it were a CAR-derived field. It must be treated as an out-of-band submission attribute until the CAR catalogue gap is resolved.

---

## 7. Release Requirements Summary

Full release trigger conditions, export behaviour, and editorial exemption rules are specified in `docs/adobe-stock-release-rules.md`. This section provides a summary for profile authors; do not use this summary as the implementation authority — use the full specification.

### 7.1 Model release triggers (from docs/adobe-stock-release-rules.md Section 1)

A model release is required when `risk.model_release_required = true`. This flag is set by the Asset Intelligence Layer when any of the following conditions are met:

- **Section 1.1** — `persons.faces_detected = true` (identifiable face visible).
- **Section 1.2** — Person is prominently featured without a visible face, as evidenced by `persons.activity_posture` and/or `objects.primary_subject`.
- **Section 1.3** — Person is identifiable by a distinctive physical characteristic (e.g., distinctive tattoo), as evidenced by `objects.detected_subjects` and `persons.activity_posture`.

### 7.2 Property release triggers (from docs/adobe-stock-release-rules.md Section 2)

A property release is required when `risk.property_release_required = true`. This flag is set when any of the following conditions are met:

- **Section 2.1** — An identifiable private building or residence is prominently featured, as evidenced by `location.visual_landmark` or `location.setting_descriptor` classifying it as a private structure.
- **Section 2.2** — A privately owned artwork, sculpture, or installation is prominently featured, as evidenced by `objects.detected_subjects` and `objects.primary_subject`.
- **Section 2.3** — A branded private installation is prominently featured, as evidenced by `text.logo_marks_detected`, `risk.trademark_flag`, and `objects.detected_subjects`.

### 7.3 Export behaviour

- **Release required and confirmed:** `Releases` column populated with the release file name(s) (State A in docs/adobe-stock-release-rules.md Section 3.1). Output Package delivered.
- **Release required but absent/unconfirmed:** `Releases` column empty (State B). Export blocked. Asset routed to Approval Requirements review queue (`docs/adobe-stock-release-rules.md` Section 4).
- **Release not required:** `Releases` column empty (State C). No blocking applies.

### 7.4 Editorial exemption

When `risk.editorial_only = true`, model and property release requirements do not block Output Package generation for the editorial submission path. The `Releases` column is empty under State C semantics. Full editorial exemption rules are in `docs/adobe-stock-release-rules.md` Section 5.

---

## CAR Field Cross-Reference Table

One row per rule. This table maps each submission rule to the CAR fields that supply its signal and the Content Profile dimension it governs.

| Rule | Section | CAR Field(s) | Content Profile Dimension |
|---|---|---|---|
| Title is required and non-empty | §1.1 | `objects.primary_subject`, `activities.primary_activity` | Required Fields |
| Title maximum 200 characters | §1.1 | `objects.primary_subject`, `location.setting_descriptor` | Length Limits |
| Title must not include prohibited terms | §1.1 | `risk.trademark_flag`, `text.logo_marks_detected` | Forbidden Content |
| Title must describe visual content, not keyword-stuff | §1.1 | `objects.detected_subjects` | Validation Rules |
| Description is portal-direct only; not in CSV | §2.1 | — (channel-path distinction, not a CAR signal) | Output Format |
| Description maximum ~500 characters (portal path) | §2.2 | `activities.detected_activities`, `location.setting_descriptor` | Length Limits |
| Keyword minimum 5 | §3.1 | `objects.detected_subjects`, `activities.detected_activities` | Keyword Rules / Validation Rules |
| Keyword maximum 49 | §3.1 | `objects.detected_subjects`, `activities.detected_activities` | Keyword Rules / Validation Rules |
| Trademark-referencing keywords suppressed | §3.1 | `risk.trademark_flag`, `text.logo_marks_detected` | Forbidden Content / Validation Rules |
| Keywords in English (US) | §3.1 | (language rule, not a CAR signal) | Language |
| Category is required; exactly one value | §4.1 | `objects.primary_subject`, `objects.scene_type`, `activities.primary_activity`, `persons.present`, `location.setting_descriptor` | Required Fields |
| Category code must match Adobe Stock taxonomy | §4.2 | `objects.primary_subject`, `activities.primary_activity` | Validation Rules |
| Block commercial generation when `risk.editorial_only = true` | §5.2 Step 1 | `risk.editorial_only` | Validation Rules / Approval Requirements |
| Editorial caption required when editorial path active | §5.2 Step 1 | `location.setting_descriptor`, `activities.primary_activity`, `location.gps_derived_region` | Required Fields (editorial profile) |
| Route to Approval Requirements when release flags active | §5.2 Step 2 | `risk.model_release_required`, `risk.property_release_required` | Approval Requirements |
| Suppress trademark-referencing content | §5.2 Step 3 | `risk.trademark_flag`, `text.logo_marks_detected` | Validation Rules |
| Route to human review when `activities.editorial_event_signal = true` | §5.2 Step 4 | `activities.editorial_event_signal` | Approval Requirements |
| AI-generated content must be declared at submission time | §6.1 | No CAR field — submission-time attribute (implementation gap) | Not yet mapped — see §6.3 |
| Model release required when `risk.model_release_required = true` | §7.1 | `risk.model_release_required`, `persons.faces_detected`, `persons.activity_posture` | Approval Requirements / Validation Rules |
| Property release required when `risk.property_release_required = true` | §7.2 | `risk.property_release_required`, `location.visual_landmark`, `objects.detected_subjects`, `text.logo_marks_detected` | Approval Requirements / Validation Rules |
| Releases column value from confirmed release file names | §7.3 | `risk.model_release_required`, `risk.property_release_required` | Output Format |
| Export blocked when release required but unconfirmed | §7.3 | `risk.model_release_required`, `risk.property_release_required` | Approval Requirements |
| Editorial exemption: release not required on editorial path | §7.4 | `risk.editorial_only` | Validation Rules |

---

## Cross-References

- **Commercial vs Editorial Classification (story #86):** [docs/commercial-editorial-classification.md](commercial-editorial-classification.md) — domain definitions for commercial and editorial use; CAR fields carrying classification signals; classification decision sequence (Section 5) applied in Section 5 of this document; Adobe Stock platform mapping table (Section 4).
- **Adobe Stock Release Rules (story #85):** [docs/adobe-stock-release-rules.md](adobe-stock-release-rules.md) — full specification of model and property release trigger conditions, CSV Releases column behaviour, export handling policy, and editorial exemption.
- **CAR Field Catalogue (story #78):** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative source for all CAR field dot-notation names used in this document.
- **Confidence Score and Risk Flag Rules (story #84):** [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) — handling policies for all `risk.*` flags (Suppress output, Require human review, Block output entirely) and the multiple-flag interaction rule.
- **Three-Layer Architecture Boundary Contracts (story #77):** [docs/boundary-contracts.md](boundary-contracts.md) — the Adobe Stock worked example that confirms the 5–49 keyword range and the five-column CSV format; Handoff validity conditions.
- **Domain Glossary:** [docs/glossary.md](glossary.md) — canonical definitions for all AssetForge domain terms used in this document.
- **Story #24:** Adobe Stock CSV output fields specification — the narrower CSV-only schema derived from these rules.
- **Story #25:** Adobe Stock AI generation prompt — uses the constraints in this document as the prompt specification baseline.
- **Story #26:** Adobe Stock validators — implements the testable constraints in this document as Channel Adaptation Layer Validation Rules.
