# AssetForge System Boundaries

## Purpose

This document defines what AssetForge is and is not responsible for. It identifies the capabilities owned by the platform, the concerns explicitly outside its scope, and the Integration Touch-points at which AssetForge exchanges artifacts with the outside world. Every team member and agent contributing to AssetForge must treat these boundaries as authoritative constraints: they govern which decisions belong inside the platform and which belong to the operators, users, or external systems that surround it. All terms used below are defined in the [AssetForge Domain Glossary](glossary.md).

---

## In Scope

The following capabilities are owned by AssetForge and map to one of the three Layers of the platform architecture.

| Capability | Layer | Notes |
|---|---|---|
| Ingest a raw Asset (photo, video, or vector) and route it through the processing Pipeline | Asset Intelligence Layer | Accepts a single Asset at one Integration Touch-point; asset type taxonomy determines routing |
| Analyse the Asset to produce a Canonical Asset Record containing objects, people, locations, text/logos, activities, risk flags, and confidence scores | Asset Intelligence Layer | Output is channel-agnostic; no content decisions are made here |
| Detect and record Risk Flags (identifiable people, visible brands, adult content, violence) in the Canonical Asset Record | Asset Intelligence Layer | Presence or absence of Model Releases and Property Releases is recorded as metadata, not verified legally |
| Assign a Confidence Score to each field or field category in the Canonical Asset Record | Asset Intelligence Layer | Reflects analytical certainty; has no bearing on the visual or commercial quality of the Asset |
| Accept a Content Profile identified by a Profile Identifier and apply its rules during content generation | Content Generation Layer | Profile Identifier is supplied by the caller at the Integration Touch-point alongside the Asset |
| Generate Titles, Descriptions, Keywords, and Captions from the Canonical Asset Record in accordance with Content Profile rules (audience, Tone, Length Limits, Forbidden Content, language) | Content Generation Layer | Produces human-readable content; no output formatting or validation occurs at this layer |
| Support multiple Content Profiles against the same Canonical Asset Record, enabling one Asset to produce Output Packages for multiple distribution destinations | Content Generation Layer | Architectural feature of the Pipeline; enables StockForge, SocialForge, PortfolioForge, CommerceForge, and ArchiveForge |
| Format and validate generated content into a channel-ready Output Package in the destination's required Output Format (CSV, JSON, IPTC/XMP, REST API response, filesystem export) | Channel Adaptation Layer | Validates against Validation Rules; does not modify the meaning of generated text |
| Apply Validation Rules from the active Content Profile to confirm that the Output Package meets field requirements before delivery | Channel Adaptation Layer | Automated; does not constitute a human quality review |
| Produce a complete, delivery-ready Output Package for a single Asset against a single Content Profile | Channel Adaptation Layer | The Output Package is the sole artifact returned at the output Integration Touch-point |
| Define, store, and version Content Profiles across all profile categories (stock, marketing, web, commerce, library) | Content Generation Layer | Profile authorship is performed by a Profile Author role; profile storage is a platform responsibility |
| Process a Batch of Assets by applying one or more Content Profiles across multiple Assets in a single operation | Asset Intelligence Layer / Content Generation Layer / Channel Adaptation Layer | Batch is a workflow concept spanning all three Layers; planned for MVP5 |

---

## Out of Scope

The following concerns are explicitly outside AssetForge's responsibilities.

| Concern | Rationale |
|---|---|
| Storage or hosting of source Assets | AssetForge generates Metadata from Assets; it does not own or manage the storage infrastructure where Assets live. Asset storage is the responsibility of the operator or the user's existing systems. |
| Delivery or transmission of Output Packages to Distribution Destinations | AssetForge produces Output Packages ready for delivery; it does not operate upload clients, API integrations, or submission workflows for stock marketplaces, social platforms, DAM systems, or any other Distribution Destination. |
| Legal determination of Commercial Use or Editorial Use eligibility | AssetForge records risk/compliance signals (Risk Flags, presence of Model Releases and Property Releases) in the Canonical Asset Record, but it does not provide legal advice or make legally binding use-classification decisions. |
| Acquisition, verification, or storage of Model Releases and Property Releases | AssetForge records whether a release is present as a flag in the Canonical Asset Record; it does not collect, authenticate, or archive the release documents themselves. |
| User authentication, access control, and account management | Identity and access management for platform operators and end users are infrastructure concerns outside the scope of the metadata generation Pipeline; planned for MVP12. |
| Quality review or editorial approval of generated content | Automated Validation Rules confirm structural compliance; human review of Output Package quality is a planned workflow feature (MVP4) and is never owned by the three-layer generation architecture itself. |
| Asset enhancement, retouching, or manipulation | AssetForge analyses and describes Assets; it does not alter, enhance, crop, reformat, or otherwise modify the source Asset file. |
| Pricing, licensing, and rights management for distributed Assets | Determining royalty rates, licensing terms, or rights clearance for Assets on Distribution Destinations is outside the platform scope; AssetForge generates Metadata, not contractual or commercial instruments. |
| Taxonomy or catalogue management within a Distribution Destination | AssetForge formats Output Packages to conform to destination schemas; it does not manage the categories, hierarchies, or taxonomies maintained by the Distribution Destination itself. |

---

## Integration Touch-points

Integration Touch-points are the named points at which AssetForge exchanges artifacts with the outside world. They define the platform boundary. Internal exchanges between the three Layers are governed by Boundary Contracts and are not Integration Touch-points.

### (a) What AssetForge Receives as Input

At the single inbound Integration Touch-point, AssetForge receives exactly two artifacts:

1. **An Asset** — a single uploadable visual file (photo, video, or vector). This is the primary source material for analysis. AssetForge does not accept metadata records, derivatives, or collections of files as input; one Asset is one source file.
2. **A Profile Identifier** — the slash-separated string that uniquely names the Content Profile to apply (e.g., `stock/adobe-stock`, `marketing/instagram`). The Profile Identifier tells the Pipeline which Content Profile to use for content generation and which Channel Adaptation rules to apply.

AssetForge does not own or control the systems that supply these inputs. It assumes the Asset is a valid file of a supported Asset Type and that the Profile Identifier resolves to a defined Content Profile within the platform.

### (b) What AssetForge Returns as Output

At the single outbound Integration Touch-point, AssetForge returns:

1. **An Output Package** — the complete, channel-ready Metadata artifact produced for the supplied Asset against the specified Content Profile. The Output Package contains all generated fields (Titles, Descriptions, Keywords, Captions) formatted in the destination's required Output Format and validated against the Validation Rules of the active Content Profile.

The Output Package is the only artifact AssetForge delivers externally. The Canonical Asset Record is an internal Handoff artifact between Layer 1 and Layer 2; it is not exposed at an external Integration Touch-point.

### (c) What AssetForge Does Not Own Between Input and Output

Between receiving the Asset and returning the Output Package, the following remain outside AssetForge's ownership:

- The storage location and retrieval mechanism for the source Asset
- The system that resolves or supplies the Profile Identifier to the platform
- The downstream delivery of the Output Package to any Distribution Destination
- Any human review, editorial approval, or override of generated content before or after delivery
- The legal or commercial decisions that may be informed by Risk Flags or use-classification fields in the Output Package

---

## Layer Responsibility Summary

**Asset Intelligence Layer** owns the ingestion of the raw Asset and the production of the Canonical Asset Record. Its responsibility begins when an Asset enters the Pipeline and ends when it produces a complete, channel-agnostic CAR containing factual observations — objects, people, locations, text/logos, activities, Risk Flags, and Confidence Scores. It makes no decisions about audience, Tone, or content structure, and has no knowledge of the Content Profile that will be applied downstream.

**Content Generation Layer** owns the transformation of a Canonical Asset Record into human-readable content. It takes the CAR and a resolved Content Profile as its sole inputs and produces Titles, Descriptions, Keywords, and Captions shaped by the Profile's rules — audience, Tone, Length Limits, Forbidden Content, and language. It does not receive the raw Asset, does not know the destination's Output Format, and does not apply Validation Rules. Its responsibility ends when it delivers generated text fields to the Channel Adaptation Layer.

**Channel Adaptation Layer** owns the final formatting and validation of generated content into a delivery-ready Output Package. It takes generated content from the Content Generation Layer and applies the Output Format and Validation Rules specified in the active Content Profile to produce a conformant Output Package. It does not generate or alter the meaning of any content field; it transforms and validates only. Its responsibility ends when it delivers the completed Output Package at the outbound Integration Touch-point.
