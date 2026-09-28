# AssetForge Domain Glossary

This glossary defines the canonical terms used across all AssetForge documentation, stories, agent outputs, and implementation work. Every contributor — human or AI — must use these definitions consistently. Where a term is commonly confused with a neighbouring concept, a *Not:* clarification is provided. This is a living document; changes require Product Owner approval.

---

## A

**ArchiveForge** — The AssetForge module responsible for generating metadata packages for digital asset management systems and personal archive destinations. *Not:* a storage or backup service; AssetForge does not own asset storage.

**Asset** — A single uploadable visual file — photo, video, or vector — that is the primary input to the AssetForge platform. *Not:* a metadata record, a derivative export, or a collection of files; one asset is one source file.

**Asset Intelligence Layer** — Layer 1 of the three-layer architecture; it analyses the raw asset and produces the Canonical Asset Record without any knowledge of intended channels or audiences. *Not:* a content generation or formatting service; it makes no decisions about titles, descriptions, or output structure.

**Asset Type** — The primary classification of a source asset (photo, video, or vector), which determines which CAR fields apply and which processing pipeline is used. *Not:* the file format (JPEG, MP4, SVG); asset type is a domain concept, not a technical format specification.

**Audit Trail** — A versioned, time-stamped record of every change made to a metadata package, including which profile was applied and by whom; planned for MVP4.

---

## B

**Batch** — A processing run that applies one or more Content Profiles to a set of multiple assets in a single operation, rather than processing each asset individually. *Not:* a queue or background job technology; batch is a product-level workflow concept independent of the underlying implementation.

**Boundary Contract** — A formal specification of the input artifact, output artifact, and prohibited responsibilities for each of the three layers, ensuring that implementation work never violates the architecture.

---

## C

**Canonical Asset Record (CAR)** — The structured, channel-agnostic record produced by the Asset Intelligence Layer, containing neutral factual observations about the asset (objects, people, locations, text/logos, activities, risk flags, confidence scores) that serve as the sole input to the Content Generation Layer. *Not:* a metadata package ready for export; the CAR contains facts about the asset, not content generated for any audience.

**Caption** — A short, contextual text field that describes or accompanies an image for display alongside it, distinct from a title or keyword list; used primarily in social media and editorial contexts. *Not:* a description (which is longer and prose-oriented) or an alt-text (which is accessibility-focused).

**Channel** — A specific distribution destination or platform category that requires its own metadata format and content rules (e.g., Adobe Stock, Instagram, a DAM system). *Not:* a communication channel or notification mechanism; in AssetForge, a channel is always a metadata distribution target.

**Channel Adaptation Layer** — Layer 3 of the three-layer architecture; it formats and validates generated content for a specific destination's required output format (CSV, IPTC/XMP, JSON, etc.) without generating or modifying content. *Not:* a content generation service; it transforms and validates only — it does not alter the meaning of generated text.

**Commercial Use** — A classification applied to an asset or Output Package indicating that the content is licensed or distributed for advertising, marketing, or any for-profit promotional purpose, including product promotion, brand campaigns, and lifestyle imagery sold without usage restriction. A commercially classified Output Package asserts that all rights clearance conditions are met: model releases are confirmed for identifiable persons (`risk.model_release_required`), property releases are confirmed for recognisable private property (`risk.property_release_required`), and no editorial-only signal (`risk.editorial_only`) is present in the Canonical Asset Record. The CAR fields that carry commercial classification evidence are specified in [docs/commercial-editorial-classification.md](commercial-editorial-classification.md). *Not:* a legal determination; AssetForge uses platform-practical definitions informed by stock marketplace policies, not legal advice. *Not:* a quality tier; commercial classification describes permitted usage context, not the aesthetic or creative quality of the asset. See also: Editorial Use.

**CommerceForge** — The AssetForge module responsible for generating metadata and product content packages for e-commerce and marketplace distribution destinations. *Not:* a payment processor, checkout engine, or storefront; AssetForge generates product content metadata, not transaction or fulfilment functionality.

**Confidence Score** — A numeric value (typically 0–1) attached to each field or field category in the Canonical Asset Record, indicating the Asset Intelligence Layer's certainty in its analysis of that field. *Not:* a quality score for the asset itself; the confidence score reflects analytical certainty, not the visual or commercial quality of the source asset.

**Content Generation Layer** — Layer 2 of the three-layer architecture; it takes the Canonical Asset Record plus a Content Profile as inputs and generates text content (titles, descriptions, keywords, captions) for a specific purpose and audience. *Not:* a formatting or export layer; it produces human-readable content but does not determine output format or validate against channel constraints.

**Content Profile** — The central platform abstraction that defines the full set of generation rules for a specific purpose and audience: audience definition, tone, required and optional fields, length limits, keyword rules, forbidden content, language, output format, validation rules, and approval requirements. *Not:* a channel adapter or output template; the Content Profile governs what content is generated, not how it is formatted for export.

**CSV** — Comma-separated values; one of the planned output delivery formats for channel exports (e.g., Shutterstock bulk upload format).

---

## D

**DAM (Digital Asset Management)** — A system used by organisations to store, organise, and retrieve digital assets; a planned distribution destination category in ArchiveForge (MVP9). *Not:* AssetForge itself; AssetForge generates metadata for DAM systems but does not function as a DAM.

**Description** — A prose text field providing a detailed, audience-oriented account of what an asset depicts, generated by the Content Generation Layer according to Content Profile rules. *Not:* the Canonical Asset Record itself; a description is generated content shaped by audience and tone, whereas the CAR is channel-neutral factual data.

**Distribution Destination** — The specific platform, system, or channel to which a completed Output Package is intended to be delivered (e.g., Adobe Stock, Shutterstock, an Instagram post, a DAM schema). *Not:* the AssetForge platform itself; AssetForge generates packages for delivery elsewhere.

---

## E

**Editorial Use** — A classification applied to an asset or Output Package indicating that the content depicts a real-world person, event, or place in its actual context, and is licensed exclusively for informational, journalistic, educational, or documentary purposes. An editorially classified Output Package must not be used in advertising, promotional material, or any for-profit persuasive application. The primary CAR signal for editorial classification is `risk.editorial_only` = `true` in the Canonical Asset Record; it is set by the Asset Intelligence Layer when the asset contains signals consistent with a real-world unscripted event, a public figure, or a news occurrence (`activities.editorial_event_signal`). A Content Profile targeting a commercial channel must block Output Package generation when this flag is present without a human review override. The full domain definition, supporting CAR fields, and platform mapping examples are specified in [docs/commercial-editorial-classification.md](commercial-editorial-classification.md). *Not:* a quality tier; editorial classification describes permitted usage context, not asset quality or ranking. *Not:* a negative classification; editorial assets are commercially valuable within their permitted licensing context. See also: Commercial Use.

---

## F

**Field Catalogue** — A structured list of all named fields in the Canonical Asset Record, including field name, data type, cardinality, and description; the field catalogue is the implementation-level complement to the CAR concept document.

**Forbidden Content** — A configurable Content Profile dimension specifying subject matter, keywords, or content types that must never appear in generated output for a given profile. *Not:* a universal platform-wide block list; forbidden content is profile-specific and may vary between channels.

---

## H

**Handoff** — The transfer of a named artifact from one layer to the next in the three-layer architecture (e.g., the CAR is the handoff artifact from Layer 1 to Layer 2). *Not:* an informal exchange of data; a handoff is a defined contract with a named artifact and specified format.

---

## I

**Integration Touch-point** — A named point at which AssetForge receives an external input (an asset plus a profile identifier) or returns an output (an Output Package) to an external system; defines the platform boundary for system context documentation. *Not:* an internal interface between the three layers; handoffs between layers are governed by Boundary Contracts.

**IPTC/XMP** — Industry-standard metadata schemas (International Press Telecommunications Council / Extensible Metadata Platform) embedded in image files; one of the planned output delivery formats for channel exports. *Not:* a proprietary AssetForge format; IPTC/XMP are open industry standards.

---

## K

**Keyword** — A single word or short phrase attached to an asset's metadata package to enable search and discovery on a distribution platform; keyword lists are generated by the Content Generation Layer according to Content Profile rules (count limits, format, language). *Not:* a tag applied internally within AssetForge for platform organisation; keywords in this context are always destination-facing metadata.

---

## L

**Layer** — One of the three strictly separated architectural components of AssetForge (Asset Intelligence, Content Generation, Channel Adaptation), each with a defined input artifact, output artifact, and prohibited responsibilities.

**Length Limit** — A configurable Content Profile dimension specifying the minimum and maximum character or word count allowed for a generated text field on a given channel. *Not:* a storage constraint; length limits reflect destination platform requirements, not AssetForge storage or API limits.

---

## M

**Metadata** — Structured data that describes an asset — including titles, descriptions, keywords, captions, and technical attributes — intended for use by distribution platforms, search engines, or DAM systems. *Not:* the asset content itself (pixels, frames, paths); metadata describes the asset but is separate from it.

**Metadata Package** — See Output Package.

**Model Release** — A signed legal document granting permission to use the likeness of an identifiable person depicted in an asset for commercial purposes; the presence or absence of a model release is a critical factor in editorial vs. commercial classification. *Not:* a technical document or file format; it is a legal instrument that the platform tracks as metadata.

**MVP (Minimum Viable Product)** — A numbered product milestone in the AssetForge roadmap representing the smallest set of capabilities that delivers a defined slice of product value; MVP0 is the domain model, MVP1 the Canonical Asset Record specification, and so on through MVP12. *Not:* a release to end users in all cases; early MVPs (0–2) are internal specification milestones.

---

## O

**Output Format** — A configurable Content Profile dimension specifying the technical format in which the Channel Adaptation Layer delivers the final Output Package (e.g., CSV, JSON, IPTC/XMP, REST API response). *Not:* the content format (prose vs. keyword list); output format describes the delivery container, not the generated content structure.

**Output Package** — The complete, channel-ready metadata artifact produced for a single asset against a single Content Profile, containing all generated fields (titles, descriptions, keywords, captions) formatted and validated for delivery to a specific distribution destination. *Not:* the Canonical Asset Record; the Output Package is generated, audience-specific content, while the CAR is channel-neutral factual data.

---

## P

**Persona** — A named, representative user archetype (e.g., content creator, developer, metadata consumer) used to anchor user stories and acceptance criteria in real user needs. *Not:* a real individual; a persona is a composite archetype used as a product design tool.

**Photo** — A primary asset type representing a raster photographic image; the first asset type introduced in the MVP roadmap (MVP0–MVP6 scope). *Not:* a vector or illustration; photos are pixel-based raster files.

**Pipeline** — The end-to-end sequence of processing operations that transforms a raw asset into an Output Package, passing through all three layers in order. *Not:* a single layer; the pipeline spans the full three-layer architecture from input to delivery.

**Portfolio** — A curated collection of an asset creator's work presented on a web or portfolio platform; one of the distribution destination categories served by PortfolioForge.

**PortfolioForge** — The AssetForge module responsible for generating metadata packages for personal portfolio websites and web pages.

**Profile** — Short form of Content Profile (see above); used interchangeably in documentation. When used without qualification, "profile" always refers to a Content Profile, not a user account or system configuration profile.

**Profile Author** — A role responsible for defining and maintaining a Content Profile for a specific distribution destination; analogous to a configuration engineer for platform-specific generation rules.

**Profile Identifier** — The slash-separated string that uniquely names a Content Profile within the platform (e.g., `stock/adobe-stock`, `marketing/instagram`); the first segment is the category, the second is the specific profile name.

**Property Release** — A signed legal document granting permission to use depictions of private property (buildings, artworks, branded objects) for commercial purposes; tracked alongside model releases as a risk/compliance flag in the CAR. *Not:* a model release; a property release covers private property, not people.

---

## R

**Release (model/property)** — A legal permission document (model release or property release) granting rights to use a depicted person's likeness or private property for commercial purposes; the presence or absence of releases is recorded as a risk/compliance flag in the Canonical Asset Record.

**Risk Flag** — A structured marker in the Canonical Asset Record indicating that the asset contains content requiring special handling — such as an identifiable person, a visible brand or logo, adult content, or violence — before an Output Package can be generated or approved for certain channels. *Not:* a quality or rejection flag; a risk flag does not mean the asset is unsuitable, only that downstream handling rules must be applied.

---

## S

**SocialForge** — The AssetForge module responsible for generating metadata packages (captions, hashtags) for social media distribution destinations.

**StockForge** — The AssetForge module responsible for generating metadata packages for stock photography marketplace distribution destinations (Adobe Stock, Shutterstock, iStock, Alamy, and others).

**Sub-type** — A secondary classification within a primary asset type (e.g., editorial photo, lifestyle photo, illustration, motion graphic) that may affect which CAR fields are applicable or which processing path is used.

---

## T

**Taxonomy** — A structured classification system; in AssetForge, refers specifically to the asset type taxonomy that classifies assets by primary type (photo, video, vector) and sub-type, determining CAR scope and pipeline routing.

**Title** — A short, headline-style text field summarising the subject or theme of an asset, generated by the Content Generation Layer; typically the most prominent searchable text field on a distribution platform. *Not:* the asset file name; a title is generated metadata content, not a filesystem identifier.

**Tone** — A configurable Content Profile dimension specifying the voice and register in which generated text content should be written for a given channel (e.g., factual and neutral for stock, conversational for social media). *Not:* a brand guideline; tone in a Content Profile is a generation instruction, not a brand identity document.

---

## V

**Validation Rule** — A configurable Content Profile dimension specifying checks that generated output must pass before being included in an Output Package (e.g., minimum keyword count, prohibited term check, field character limit compliance). *Not:* a quality review by a human; validation rules are automated, profile-defined constraints applied by the Channel Adaptation Layer.

**Vector** — A primary asset type representing a resolution-independent graphic defined by mathematical paths rather than pixels (e.g., SVG, EPS, AI); introduced as a processing scope in MVP10. *Not:* a photo or video; vectors have distinct analysis and processing requirements.

**Versioning** — The practice of tracking changes to a document, artifact, or Content Profile over time so that prior states are recoverable; referenced in the MVP roadmap at MVP4 for human review and audit trail features.

**Video** — A primary asset type representing a time-based moving image file; introduced as a processing scope in MVP10. *Not:* an animated GIF or motion graphic vector; video is a distinct asset type with frame-based analysis requirements.
