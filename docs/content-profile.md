# Content Profile — Concept Definition

This document defines the Content Profile as a platform concept. It describes its purpose, its position in the three-layer architecture, its ten configurable dimensions, and its boundary with the Channel Adaptation Layer. This document does not define a schema, a template, or a storage or versioning mechanism; those are the subjects of story #79 (Content Profile schema and authoring template). All terms used below are defined in the [AssetForge Domain Glossary](glossary.md).

---

## 1. Purpose

**The Content Profile is the central platform abstraction that defines the full set of generation rules for a specific purpose and audience, governing what content is generated and how that content must behave — but not how the raw asset is analysed, not how generated content is formatted for export, and not what the destination platform's internal structure looks like.**

A Content Profile explicitly does NOT control:

- **Asset analysis** — the Content Profile has no influence over what the Asset Intelligence Layer observes or records in the Canonical Asset Record; factual observations about the asset are channel-agnostic and are made before any profile is consulted.
- **Output formatting and delivery structure** — the Content Profile does not specify how generated content is arranged in a CSV file, how IPTC/XMP fields are serialised, or how a JSON response is structured for a REST API; those are Channel Adaptation Layer responsibilities.
- **Destination platform taxonomies and internal catalogues** — the Content Profile does not manage category hierarchies, collection structures, or any internal organisation maintained by the distribution destination itself.

---

## 2. Relationship to the Three Layers

The Content Profile exists to keep the Content Generation Layer and the Channel Adaptation Layer stable as new distribution channels are added. It externalises all destination-specific rules into a configurable artifact, so adding a new channel means authoring a new Content Profile — not writing new code or modifying layer logic.

**Asset Intelligence Layer (Layer 1) — unaware of the Content Profile.**
The Asset Intelligence Layer analyses the raw Asset and produces the Canonical Asset Record. It has no knowledge of which Content Profile will be applied downstream. The CAR is produced once, channel-agnostically, before any profile is consulted.

**Content Generation Layer (Layer 2) — reads the Content Profile.**
The Content Generation Layer takes the Canonical Asset Record and a resolved Content Profile as its sole inputs. It applies the profile's rules — audience, tone, length limits, keyword rules, forbidden content, and language — to generate titles, descriptions, keywords, and captions. Every generation decision is governed by the active Content Profile; without one, the Content Generation Layer cannot operate.

**Channel Adaptation Layer (Layer 3) — applies two dimensions from the Content Profile.**
The Channel Adaptation Layer reads the Output Format and Validation Rules dimensions from the active Content Profile to format and validate generated content into a delivery-ready Output Package. It does not generate or modify content; it transforms and validates only. The Channel Adaptation Layer is not a consumer of all ten profile dimensions — only those two govern its behaviour.

The Profile Identifier (`category/profile-name`, for example `stock/adobe-stock` or `marketing/instagram`) is the token supplied at the Integration Touch-point that resolves to a specific Content Profile within the platform. It is the mechanism by which the Pipeline knows which Content Profile to apply.

---

## 3. Configurable Dimensions

A Content Profile is defined by ten configurable dimensions. Every profile — whether for a stock marketplace, a social media platform, a portfolio site, or a DAM schema — specifies each of these dimensions. The ten dimensions are the complete and exclusive definition of what a Content Profile contains.

**Audience** — The intended human or system consumer of the generated content, such as a stock marketplace buyer searching for commercial imagery, a social media follower expecting casual discovery content, or an archivist querying a DAM system for internal use.

**Tone** — The voice and register in which generated text content must be written for the given channel, such as factual and neutral for editorial stock submissions, aspirational and descriptive for lifestyle marketing, or terse and structured for machine-readable DAM metadata.

**Required and Optional Fields** — The set of named content fields the Content Generation Layer must produce for an Output Package to be valid (required), and the set of fields it may produce when sufficient information is available in the Canonical Asset Record (optional), such as a title and keyword list being required for stock while a caption is optional.

**Length Limits** — The minimum and maximum character or word counts permitted for each generated text field on the given channel, reflecting destination platform requirements rather than platform storage constraints — for example, a stock title capped at 200 characters or a social media caption with a target range of 150–300 characters.

**Keyword Rules** — The rules governing the generation of the keyword list for the given channel, including the minimum and maximum number of keywords, permitted keyword formats (single words, short phrases, or both), capitalisation conventions, and any channel-specific ordering or relevance-weighting requirements.

**Forbidden Content** — The subject matter, keywords, or content types that must never appear in generated output for this profile, such as competitor brand names prohibited on a stock platform or politically sensitive terms excluded from a commercial marketing profile; forbidden content is profile-specific and does not represent a platform-wide block list.

**Language** — The language and locale in which all generated text fields must be written for the given channel, such as English (US) for the majority of stock marketplaces or a specific locale pairing required by a regional e-commerce destination.

**Output Format** — The technical delivery format the Channel Adaptation Layer must use when producing the Output Package for this channel, such as CSV for stock marketplace bulk upload, IPTC/XMP for file-embedded metadata, or JSON for a REST API response.

**Validation Rules** — The automated checks that generated output must pass before it is included in a completed Output Package, such as a minimum keyword count, a prohibited-term scan, a field character-limit compliance check, or confirmation that all required fields are present and non-empty.

**Approval Requirements** — The specification of whether a generated Output Package requires human review before it is considered delivery-ready, and if so, which conditions trigger that review — for example, any asset carrying a Risk Flag related to an identifiable person may require human approval before a commercial stock Output Package is finalised.

---

## 4. Content Profile vs Channel Adaptation Layer

The Content Profile governs **what content is generated and what rules that content must meet**. The Channel Adaptation Layer governs **how conformant content is structured and delivered in a specific technical format**. These two concerns must never be merged into a single responsibility.

**Concrete example — CSV column order:**

The `stock/shutterstock` profile specifies that a stock submission requires a title field (maximum 200 characters), a description field (maximum 1500 characters), and a keyword list (25–50 keywords, comma-separated, English US). These are Content Profile concerns: they define what fields exist, how long they may be, and what rules govern their content.

The Shutterstock CSV export format specifies that the column order in the bulk upload file must be: `Filename`, `Description`, `Keywords`, `Categories`, `Editorial`, `Mature content`. That column order is a Channel Adaptation Layer concern. It is not a rule about what content is generated — it is a rule about how already-generated, already-validated content is arranged in a specific delivery artifact. Adding, removing, or reordering CSV columns is a Channel Adaptation Layer change. It requires no changes to the Content Profile.

This separation is what makes the platform profile-driven: the Content Profile is stable across any number of output format changes, and the Channel Adaptation Layer can be updated to match a destination's technical requirements without altering any content generation rules.

A useful test: if a change would affect the meaning, completeness, or rule compliance of the generated text, it belongs in the Content Profile. If a change would affect only the shape, structure, or serialisation of the delivery artifact, it belongs in the Channel Adaptation Layer.

---

## 5. Relationship to the Field Catalogue and Schema

This document defines the Content Profile as a concept: its purpose, its architectural position, and its ten configurable dimensions. It intentionally contains no field names, data types, cardinality specifications, schema definitions, or template structures.

**Story #78 (CAR Field Catalogue)** specifies the Canonical Asset Record at the field level. The Content Profile's required and optional fields dimension names the fields that a profile expects to be generated; those field names must be consistent with the vocabulary established in the CAR Field Catalogue so that the Content Generation Layer can map CAR observations to profile-expected outputs without ambiguity.

**Story #79 (Content Profile schema and authoring template)** is the implementation-level complement to this concept document. Story #79 translates the ten configurable dimensions defined here into a structured schema with field names, data types, required/optional status, allowed values, and at least one example value per dimension. Any profile authored for MVP2 (`stock/adobe-stock`) or later must conform to the schema produced in story #79. The ten dimensions defined in Section 3 of this document are intended to serve as the organising structure for that schema: each schema field in story #79 should be traceable to one of the ten dimensions defined here.
