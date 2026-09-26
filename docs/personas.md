# AssetForge User Personas

> MVP0 draft — personas will evolve as user research is conducted and later MVPs are delivered.

This document defines the representative user archetypes that anchor AssetForge user stories, acceptance criteria, and product decisions. Each persona is a composite archetype, not a real individual. The personas are used consistently across all documentation, stories, and agent outputs; the term **Persona** is defined in the [Domain Glossary](glossary.md).

---

## Persona 1 — The Content Creator

**Name:** Alex the Photographer

**Role:** Freelance photographer or videographer who produces visual assets and distributes them across multiple channels simultaneously — stock marketplaces, personal portfolio, social media, and client DAMs.

**Primary goal:** Upload an asset once and receive ready-to-submit metadata packages for every distribution destination without manually re-writing titles, descriptions, and keywords per channel.

**Key frustration:** Repeating the same metadata work for every platform — writing a Shutterstock title, then a different Adobe Stock title, then an Instagram caption, then a portfolio description — is time-consuming, error-prone, and pulls focus away from shooting. Getting keywords wrong or violating a platform's field rules means rejection and re-submission delays.

**Primary AssetForge benefit:** The Asset Intelligence Layer analyses the asset once, producing a Canonical Asset Record, and the Content Generation Layer produces channel-appropriate metadata for every requested profile in a single Pipeline run. Alex submits to ten channels from one upload session.

---

## Persona 2 — The Developer

**Name:** Dana the Platform Engineer

**Role:** Software engineer building, extending, or maintaining the AssetForge platform — implementing new layers, writing profile logic, integrating external APIs, and ensuring the three-layer Boundary Contract is respected in all implementation work.

**Primary goal:** Understand the precise inputs, outputs, and prohibited responsibilities of each architectural layer so that implementation work stays within scope, avoids cross-layer leakage, and can be extended cleanly as new profiles and channels are added.

**Key frustration:** Vague or inconsistent specifications cause rework. If the Canonical Asset Record concept is unclear, the field catalogue will be incorrectly scoped. If Boundary Contracts are not explicit, Layer 2 logic drifts into Layer 3 concerns, creating tight coupling that breaks every time a new Channel is added.

**Primary AssetForge benefit:** The MVP0 domain model — the Domain Glossary, system boundaries document, CAR concept, and Content Profile concept — provides Dana with unambiguous definitions and layer contracts before a single line of implementation code is written.

---

## Persona 3 — The Profile Author

**Name:** Morgan the Integration Specialist

**Role:** Configuration engineer or platform specialist responsible for designing and maintaining Content Profiles for specific distribution destinations — defining audience, tone, required fields, length limits, keyword rules, forbidden content, validation rules, and output format for a given Channel.

**Primary goal:** Add a new distribution Channel to AssetForge by authoring a Content Profile, without requiring code changes and without violating the three-layer separation — profile configuration must not bleed into Channel Adaptation Layer concerns.

**Key frustration:** Without a clear Content Profile schema or authoring template, each new profile is invented ad hoc. Fields are added inconsistently, generation rules overlap with formatting rules, and validating whether a profile is correctly scoped requires reading the entire codebase rather than checking a specification.

**Primary AssetForge benefit:** The Content Profile is the central platform abstraction: adding a new Channel means adding a new profile, not new code. A rigorous conceptual definition and schema ensures Morgan can author the `stock/adobe-stock` profile (MVP2), then `marketing/instagram` (MVP7), using the same authoring template and the same understanding of what a profile controls versus what it does not.

---

## Persona 4 — The Metadata Consumer

**Name:** The Distribution Destination (e.g., Adobe Stock, a DAM system)

**Role:** An external platform or system that receives a completed Output Package from AssetForge — a stock marketplace ingesting a CSV submission, a DAM system receiving a JSON metadata record, or a CMS accepting an IPTC/XMP-embedded file.

**Primary goal:** Receive a correctly structured, validated, channel-compliant metadata package that can be ingested without manual correction — fields present, length limits respected, forbidden content absent, and output format matching the platform's intake specification.

**Key frustration:** Receiving metadata packages that violate field rules (keyword count out of range, title too long, missing required fields, prohibited terms present) causes automated rejection, delays asset availability, and requires the submitter to reprocess and resubmit.

**Primary AssetForge benefit:** The Channel Adaptation Layer formats and validates each Output Package against the destination's Validation Rules before delivery. The Metadata Consumer receives a package that meets its intake specification without requiring manual review of every field.

---

## Persona-to-Story Mapping (MVP0, Stories #13–#16)

This table identifies which personas are primary for each MVP0 story. It is provided as a cross-reference and does not require edits to the individual story issues.

| Story | Title | Primary Persona(s) | Rationale |
|-------|-------|--------------------|-----------|
| #13 | Define domain glossary | Dana the Developer, Morgan the Profile Author | The glossary exists to ensure consistent terminology across implementation work and profile authoring. It directly unblocks all subsequent MVP0 stories and is foundational for both technical contributors. |
| #14 | Document system boundaries | Alex the Content Creator, Dana the Developer | The boundary document answers "what does AssetForge do?" — directly relevant to Alex understanding the platform's scope and Dana avoiding out-of-scope implementation. The Product Owner (stakeholder persona) is explicitly named in issue #14 as the user story subject. |
| #15 | Define the Canonical Asset Record concept | Dana the Developer | The CAR concept document is written explicitly for a developer beginning MVP1 — its purpose is to ensure Dana understands the handoff artifact's scope before designing the schema. Morgan also benefits as the CAR is the sole input to the Content Generation Layer that profiles govern. |
| #16 | Define the Content Profile concept | Morgan the Profile Author, Dana the Developer | The Content Profile is the central abstraction that Morgan will author in MVP2. Dana needs the layer ownership rules to implement the Content Generation Layer correctly. Both personas are named explicitly in the issue #16 user story. |

---

## Notes

- Persona names are illustrative mnemonic handles, not role titles. Use the role label (Content Creator, Developer, Profile Author, Metadata Consumer) in user stories and acceptance criteria.
- A fifth persona — the **Product Owner / Stakeholder** — appears in the user story for #14 ("As a product owner…"). This persona is not fully elaborated here because their needs are served by documentation generally rather than by specific platform capabilities. It will be formalised if a human review UI (MVP4) or governance features (MVP12) require dedicated story anchoring.
- The Metadata Consumer persona is non-human (a platform or system). This is intentional: external distribution destinations impose constraints on every Output Package, and making those constraints explicit through a persona prevents the team from treating channel compliance as an afterthought.
- As the platform expands beyond MVP2, additional personas may emerge: a **Batch Operator** (MVP5), a **DAM Administrator** (MVP9), or an **Enterprise Governance Reviewer** (MVP12). This document should be revisited at each MVP boundary.
