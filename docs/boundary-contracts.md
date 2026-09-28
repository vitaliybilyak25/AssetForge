# Three-Layer Architecture Boundary Contracts

This document defines the formal Boundary Contracts for AssetForge's three-layer architecture. For each Layer it names the single input artifact, the single output artifact, and the responsibilities that Layer explicitly does not own. It then specifies what constitutes a valid Handoff between each pair of Layers and traces a single Asset through all three Layers to illustrate the data transformation at each boundary. These contracts are authoritative constraints: no implementation decision, agent output, or team discussion may assign a responsibility to a Layer that is prohibited here. All terms used below are defined in the [AssetForge Domain Glossary](glossary.md).

---

## Layer 1 — Asset Intelligence Layer

### Input Artifact

**Raw Asset** — a single uploadable visual file (photo, video, or vector) received at the inbound Integration Touch-point, accompanied by a Profile Identifier that is passed downstream but not read by this Layer.

### Output Artifact

**Canonical Asset Record (CAR)** — a structured, channel-agnostic record containing neutral, factual observations about the Asset organised into seven categories: Objects and Subjects, People, Locations, Text and Logos, Activities, Risk Flags, and Confidence Scores. The CAR is immutable after production. It is an internal Handoff artifact passed to the Content Generation Layer; it is never exposed at an external Integration Touch-point.

### Prohibited Responsibilities

The Asset Intelligence Layer must not:

- Read, interpret, or be influenced by the Content Profile or Profile Identifier in any way.
- Generate titles, descriptions, keywords, captions, or any other text content shaped by audience, Tone, or channel requirements.
- Apply Length Limits, Keyword Rules, Forbidden Content rules, or Validation Rules to its output.
- Make decisions about the intended distribution destination or the Output Format for the final Output Package.
- Determine or record whether an Asset is suitable for any specific channel or use classification.
- Modify, enrich, enhance, or alter the source Asset file.
- Produce or contribute to the Output Package.
- Access the resolved Content Profile object — it receives the Profile Identifier as a pass-through only.

---

## Layer 2 — Content Generation Layer

### Input Artifacts

Two artifacts are required simultaneously; this Layer cannot operate without both:

1. **Canonical Asset Record** — the immutable factual record produced by the Asset Intelligence Layer, containing all seven observation categories and their associated Confidence Scores.
2. **Resolved Content Profile** — the full Content Profile object identified by the Profile Identifier, specifying the eight content-governing dimensions (Audience, Tone, Required and Optional Fields, Length Limits, Keyword Rules, Forbidden Content, Language, and Approval Requirements) that govern generation decisions.

### Output Artifact

**Generated Content** — a set of human-readable text fields (Titles, Descriptions, Keywords, Captions) produced in accordance with the active Content Profile's rules. This is an internal Handoff artifact passed to the Channel Adaptation Layer; it is not yet formatted or validated for delivery.

### Prohibited Responsibilities

The Content Generation Layer must not:

- Analyse the raw Asset or produce any field that was not derived from the Canonical Asset Record and a Content Profile.
- Modify or annotate the Canonical Asset Record — the CAR is read-only at this Layer.
- Apply Output Format rules (CSV column order, IPTC/XMP serialisation, JSON structure) — those are Channel Adaptation Layer responsibilities.
- Execute Validation Rules against generated output — validation belongs to the Channel Adaptation Layer.
- Produce a delivery-ready Output Package or expose generated content at an external Integration Touch-point.
- Infer, substitute, or fabricate content for any CAR field that is absent or below the minimum Confidence Score required by the active Content Profile — absent or below-threshold fields must be treated as unknown in accordance with CAR Consumer Rules 1–3.
- Make decisions about the technical delivery mechanism or destination platform taxonomy.

---

## Layer 3 — Channel Adaptation Layer

### Input Artifacts

Two artifacts are required simultaneously:

1. **Generated Content** — the set of text fields (Titles, Descriptions, Keywords, Captions) produced by the Content Generation Layer.
2. **Resolved Content Profile** — specifically its Output Format and Validation Rules dimensions, which govern how this Layer operates. The Channel Adaptation Layer reads only these two dimensions; the remaining eight dimensions are not its concern.

### Output Artifact

**Output Package** — the complete, channel-ready Metadata artifact formatted in the destination's required Output Format and validated against the active Content Profile's Validation Rules. The Output Package is the only artifact AssetForge delivers at the outbound Integration Touch-point.

### Prohibited Responsibilities

The Channel Adaptation Layer must not:

- Generate any content field — titles, descriptions, keywords, or captions must arrive as Generated Content; this Layer does not author them.
- Alter the meaning, intent, or substance of any Generated Content field — it transforms and validates structure only.
- Read the raw Asset or the Canonical Asset Record — this Layer has no access to either.
- Apply content-generation rules (Audience, Tone, Keyword Rules, Forbidden Content, Language) — those are Content Generation Layer responsibilities governed by the Content Profile.
- Perform human review or editorial approval of generated content — automated Validation Rules confirm structural compliance only.
- Accept or deliver content at an external Integration Touch-point other than the single outbound Integration Touch-point where the Output Package is returned.
- Manage or modify the Content Profile — it reads the Output Format and Validation Rules dimensions as a consumer only.

---

## Valid Handoffs

A Handoff is the transfer of a named artifact from one Layer to the next. A Handoff is valid only when all conditions below are satisfied. A Layer that receives an invalid Handoff must not proceed; it must surface a Handoff failure rather than attempt processing on incomplete or malformed input.

### Handoff 1 — Asset Intelligence Layer to Content Generation Layer (Raw Asset → CAR)

A Canonical Asset Record constitutes a valid Handoff when:

1. **Completeness** — the CAR contains observations for all seven information categories, or explicitly records that a category produced no findings (absence is permissible; silence is not — each category must have a defined state).
2. **Confidence Scores present** — every non-absent observation carries a Confidence Score; no observation is included without an associated certainty value.
3. **Risk Flags propagated** — all detected Risk Flags are present in the CAR regardless of the Confidence Score of the underlying observation, in accordance with CAR Consumer Rule 4.
4. **Immutability** — the CAR has been sealed by the Asset Intelligence Layer and is not subject to further modification; the receiving Layer must treat it as read-only.
5. **No content decisions embedded** — the CAR contains no titles, descriptions, keyword lists, captions, or any field shaped by audience, Tone, or channel; if any such field is present the Handoff is invalid.
6. **Profile-agnosticism** — the CAR contains no reference to the Content Profile or Profile Identifier; its observations are unconditionally channel-agnostic.

### Handoff 2 — Content Generation Layer to Channel Adaptation Layer (Generated Content → Output Package input)

Generated Content constitutes a valid Handoff when:

1. **All required fields present** — every field designated as required by the active Content Profile's Required and Optional Fields dimension is present and non-empty.
2. **Length Limits met** — every generated text field satisfies the minimum and maximum character or word counts specified in the active Content Profile's Length Limits dimension.
3. **Keyword Rules satisfied** — the keyword list conforms to the keyword count range, format, capitalisation conventions, and any ordering requirements specified in the active Content Profile's Keyword Rules dimension.
4. **Forbidden Content absent** — no generated field contains subject matter, keywords, or content types listed in the active Content Profile's Forbidden Content dimension.
5. **Language conformant** — all generated text fields are written in the language and locale specified in the active Content Profile's Language dimension.
6. **No formatting applied** — Generated Content carries plain text fields only; no Output Format structure (CSV rows, XML serialisation, JSON keys) has been applied by the Content Generation Layer. Structural formatting is the Channel Adaptation Layer's responsibility and must not arrive pre-applied.
7. **CAR not included** — the Canonical Asset Record is not passed to the Channel Adaptation Layer; only the Generated Content fields and the active Content Profile traverse this boundary.

---

## Worked Example — Lifestyle Photo Submitted for Adobe Stock

This example traces a single Asset through all three Layers to illustrate the data transformation at each Boundary.

**Asset:** A photo of a woman in her mid-thirties working at a standing desk in a bright home office. She is facing the camera, her face is clearly visible, and a branded laptop is partially visible on the desk. No GPS metadata is embedded. The submitter intends to submit this Asset to Adobe Stock under the `stock/adobe-stock` Content Profile.

---

### What enters Layer 1

The Asset Intelligence Layer receives:
- The raw photo file.
- The Profile Identifier `stock/adobe-stock` (passed through; not read by this Layer).

### What Layer 1 does

The Asset Intelligence Layer analyses the raw photo without any knowledge of the intended channel. It detects and records the following observations:

- **Objects and Subjects:** standing desk, laptop (brand mark visible), home office environment, indoor natural light, window, desk lamp.
- **People:** one adult female, face identifiable, direct gaze toward camera.
- **Locations:** indoor scene, residential or home-office environment; no GPS data present; no identifiable geographic markers detected.
- **Text and Logos:** laptop brand mark partially visible (legible); no other readable text detected.
- **Activities:** person working at a standing desk; upright posture; stationary activity.
- **Risk Flags:** identifiable person detected (model release evaluation required); visible brand mark detected (property release evaluation may apply).
- **Confidence Scores:** all observations above threshold except Location sub-category "specific place name" (no GPS, no visual landmark) — recorded as absent with a note that geographic specificity is unknown.

### What exits Layer 1 (the Handoff artifact)

A sealed, immutable Canonical Asset Record containing all observations above, with Confidence Scores on every non-absent field and both Risk Flags explicitly propagated. The CAR contains no title, no description, no keywords, and no reference to Adobe Stock or any Content Profile.

---

### What enters Layer 2

The Content Generation Layer receives:
- The Canonical Asset Record produced by Layer 1.
- The resolved `stock/adobe-stock` Content Profile, specifying (among other dimensions): Audience — stock marketplace buyers seeking commercial lifestyle imagery; Tone — factual, descriptive, commercially oriented; Required Fields — Title, keyword list, Category, Releases; Length Limits — Title up to 200 characters, keyword list 5–49 keywords; Keyword Rules — single words and short phrases, comma-separated, English US; Forbidden Content — competitor brand names, politically sensitive terms; Language — English (US); Approval Requirements — assets carrying an identifiable-person Risk Flag require human review before the Output Package is finalised.

### What Layer 2 does

The Content Generation Layer reads the CAR's factual observations and applies the Content Profile's rules to generate content:

- **Title:** "Woman Working at Standing Desk in Bright Home Office" (factual, under 200 characters, no brand name included — laptop brand suppressed due to Forbidden Content rules on brand marks).
- **Keywords:** 38 keywords generated in English (US) covering subjects (woman, standing desk, home office, productivity, remote work, lifestyle), activities (working, standing, technology use), scene attributes (bright, natural light, indoor), and commercial themes (modern workplace, professional, focus) — all within the 5–49 keyword range and conforming to Keyword Rules; laptop brand name excluded from keyword list.
- **Category:** resolved to the appropriate Adobe Stock numeric category code for lifestyle/business imagery.
- **Releases:** no release names provided at this stage — identifiable-person Risk Flag is present; the Content Profile's Approval Requirements dimension specifies that this Output Package requires human review before delivery, at which point release documentation is confirmed.
- **Approval Requirement noted:** identifiable-person Risk Flag is present in the CAR; human review is required before the Output Package is finalised.

### What exits Layer 2 (the Handoff artifact)

Generated Content: plain-text Title, keyword list in English (US), Category code, and Releases value — all within Content Profile rules, with no CSV structure, no IPTC tags, and no JSON keys applied. The CAR is not passed forward.

---

### What enters Layer 3

The Channel Adaptation Layer receives:
- The Generated Content (Title, Description, keyword list) from Layer 2.
- The `stock/adobe-stock` Content Profile's Output Format dimension (specifying the required delivery format for Adobe Stock: Filename, Title, Keywords, Category, Releases columns) and Validation Rules dimension (minimum keyword count 5, maximum 49; Title non-empty and within 200 characters; no prohibited terms; character limit compliance per field).

### What Layer 3 does

The Channel Adaptation Layer applies the Output Format and Validation Rules without altering any content:

- **Validation:** confirms Title is present and within the 200-character limit; confirms 38 keywords are present (within the 5–49 range); confirms Category code is present; confirms no prohibited terms appear; all checks pass.
- **Formatting:** arranges the validated fields into the CSV column structure required by Adobe Stock — Filename, Title, Keywords, Category, Releases — serialised per the Output Format dimension.
- **Approval flag preserved:** the Output Package records that human review is required before delivery, in accordance with the Approval Requirements dimension surfaced from the Content Profile.

### What exits Layer 3 (the Handoff artifact)

A complete, delivery-ready Output Package for the `stock/adobe-stock` Content Profile containing the formatted Title, keyword list, Category, and Releases fields in Adobe Stock CSV column order, validated against all Validation Rules, and flagged for human review before submission — returned at the outbound Integration Touch-point. The raw Asset, the Canonical Asset Record, and the Generated Content intermediate are not included in the Output Package.

---

## Cross-References

- **Canonical Asset Record concept** — story #15: [docs/canonical-asset-record.md](canonical-asset-record.md). The CAR definition, its seven information categories, immutability rule, and Consumer Rules referenced in the Handoff 1 validity conditions above are specified in full in that document.
- **Content Profile concept** — story #16: [docs/content-profile.md](content-profile.md). The ten configurable dimensions, the rationale for separating Content Profile concerns from Channel Adaptation Layer concerns, and the distinction between content-generation rules and output-formatting rules referenced above are specified in full in that document.
- **End-to-end data flow** — story #83: [docs/data-flow.md](data-flow.md). The complete sequenced data flow from asset upload through all three layers to Output Package delivery, including error paths and actor identification per step.
