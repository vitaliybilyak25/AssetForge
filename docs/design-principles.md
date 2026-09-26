# AssetForge Design Principles and Naming Conventions

## Purpose

This document records the agreed design principles that govern every architectural, product, and implementation decision in AssetForge, together with the naming conventions that ensure consistency across all documentation, profiles, code, and agent outputs. All contributors — human and AI — must apply these principles and conventions from the moment they begin work on any artifact. This is a living document; changes require Product Owner approval following the governance process described in the final section. All terms used here are defined in the [AssetForge Domain Glossary](glossary.md).

---

## Design Principles

### Principle 1: Profile-Driven, Not Hardcoded Per-Site

**The Content Profile is the central platform abstraction. Adding a new distribution channel means authoring a new Content Profile — it does not mean writing new code, creating new processing paths, or modifying existing layer logic.**

**Rationale**

AssetForge must serve a wide and growing range of distribution destinations: stock marketplaces, social media platforms, e-commerce systems, DAM schemas, and portfolio sites. If the platform were built by hardcoding generation logic for each destination directly into the pipeline, every new channel would require a code change, a deployment, and a regression risk to existing channels. That approach does not scale and violates the separation of concerns that makes the three-layer architecture maintainable.

The Content Profile abstraction solves this by externalising everything that is destination-specific — audience, tone, field requirements, length limits, keyword rules, forbidden content, language, output format, and validation rules — into a configurable artifact that the Content Generation Layer and Channel Adaptation Layer consume at runtime. The layers themselves remain stable; only profiles change when channels change. This means a Profile Author can onboard a new distribution destination without touching implementation code, and a developer adding a new capability to the Content Generation Layer does not need to know which channels exist.

**How to apply**

When a new feature, integration, or output requirement arises, the first question must be: "Can this be expressed as a Content Profile configuration?" If the answer is yes, it belongs in a profile — not in code.

_Example:_ AssetForge needs to support Alamy as a new stock marketplace. The correct approach is to author a new Content Profile at `profiles/stock/alamy` defining Alamy's field requirements, keyword count limits, tone conventions, and CSV output format. The approach that violates this principle would be to add an Alamy-specific conditional branch inside the Content Generation Layer or Channel Adaptation Layer.

---

### Principle 2: Stock Marketplaces Are the First Use Case, Not the Scope

**Every architectural decision must be evaluated against the full range of intended channel types — stock, social, web, commerce, and library — not only against the current stock marketplace use case. If a decision would prevent or complicate future channel categories, it should be reconsidered.**

**Rationale**

Stock marketplace profiles (StockForge) are the first business case because they have well-defined field requirements, clear validation rules, and an established CSV export format that makes them a tractable starting point. However, the AssetForge platform is designed to serve fundamentally different channel types: social media captions with hashtags, SEO-optimised web descriptions, e-commerce product content, and DAM archive metadata. These channels have very different tone requirements, field structures, length limits, and output formats.

Building the platform architecture to fit only stock marketplace patterns — for example, by assuming all output is CSV, that all fields are title/description/keywords, or that all destinations are search-driven — would create technical debt that undermines every subsequent module. The principle forces contributors to consider the broadest intended scope at every decision point, ensuring that the architecture remains extensible without requiring fundamental rework as each new module is introduced.

**How to apply**

When making a structural decision about the Canonical Asset Record, the Content Generation Layer, or the Channel Adaptation Layer, ask: "Does this decision assume stock marketplace conventions, or does it work equally well for a social media caption, a DAM schema, and an e-commerce product listing?"

_Example:_ When specifying the CAR field structure in MVP1, it would violate this principle to include only the fields relevant to stock marketplace submission (title, description, keyword list, editorial flag). The correct approach is to include all channel-agnostic factual observations the Asset Intelligence Layer can produce — objects, people, locations, text/logos, activities, risk flags, confidence scores — so that SocialForge, CommerceForge, and ArchiveForge can later draw on the same record without requiring a CAR redesign.

---

### Principle 3: Strict Layer Separation

**The three layers — Asset Intelligence, Content Generation, and Channel Adaptation — must not cross their defined boundaries. Each layer knows only its own inputs and outputs; it must have no knowledge of, or dependency on, the internal workings of another layer.**

**Rationale**

The three-layer architecture is the primary mechanism for keeping AssetForge maintainable, testable, and independently scalable. If the Asset Intelligence Layer were to embed audience assumptions (a Content Generation Layer concern), or if the Channel Adaptation Layer were to generate or rewrite content (a Content Generation Layer concern), the separation would collapse. Each layer would then carry implicit dependencies on the others, making it impossible to change one without auditing the others.

Strict separation also preserves the Canonical Asset Record as a stable, channel-agnostic contract. Because the CAR is the only artifact passed from Layer 1 to Layer 2, it can serve as the single source of truth for any number of Content Profiles applied in parallel against the same asset — the analytical work is done once, and every profile draws from the same factual record. This is the architectural feature that enables one asset to produce Output Packages for multiple distribution destinations simultaneously.

**How to apply**

Before assigning any responsibility to a layer, verify it against the Boundary Contract for that layer. If the responsibility involves analysing the raw asset, it belongs in Layer 1. If it involves generating human-readable content shaped by audience and tone, it belongs in Layer 2. If it involves formatting, validating, or structuring output for a specific destination format, it belongs in Layer 3.

_Example:_ A requirement to "ensure the keyword list contains no prohibited terms for Adobe Stock" belongs in the Channel Adaptation Layer (Layer 3), because it is a validation step against a specific profile's rules. Implementing it inside the Content Generation Layer would be a boundary violation, because Layer 2 must not know which distribution destination is being targeted.

---

## Naming Conventions

Consistent naming across documentation, profiles, code, and agent outputs prevents ambiguity and ensures that every contributor — human or AI — can locate and reference artifacts without guesswork. The conventions below are mandatory. New names that do not follow these patterns require Product Owner approval.

---

### Profile Identifiers

**Format:** `{category}/{profile-name}`

- Both segments are lowercase and hyphen-separated.
- The category segment must be one of the five defined profile categories: `stock`, `marketing`, `web`, `commerce`, `library`.
- The profile-name segment is a short, descriptive identifier for the specific distribution destination or purpose.
- Profile Identifiers are the canonical reference used in all documentation, Pipeline calls, and Content Profile file paths.

| Category | Profile Name | Full Identifier |
|---|---|---|
| stock | adobe-stock | `stock/adobe-stock` |
| stock | istock-editorial | `stock/istock-editorial` |
| stock | shutterstock | `stock/shutterstock` |
| marketing | instagram | `marketing/instagram` |
| marketing | linkedin | `marketing/linkedin` |
| web | seo-page | `web/seo-page` |
| web | accessibility-alt-text | `web/accessibility-alt-text` |
| commerce | ecommerce-product | `commerce/ecommerce-product` |
| library | dam | `library/dam` |
| library | personal-archive | `library/personal-archive` |

**Anti-pattern:** Do not use destination brand names as standalone identifiers without a category prefix (e.g., `adobe-stock` alone is ambiguous). Always use the full `category/profile-name` form.

---

### Layer Names

**Format:** Title Case, full descriptive name; always used with the word "Layer" appended.

The three layers have fixed canonical names. These names must not be abbreviated or paraphrased in any documentation, story, or code comment.

| Canonical Name | Abbreviation (permitted in tables only) | Layer Number |
|---|---|---|
| Asset Intelligence Layer | Layer 1 | 1 |
| Content Generation Layer | Layer 2 | 2 |
| Channel Adaptation Layer | Layer 3 | 3 |

**Examples of correct usage:**

- "The Asset Intelligence Layer produces the Canonical Asset Record."
- "Validation Rules are applied by the Channel Adaptation Layer."
- "Layer 2 receives the CAR and a Content Profile as inputs."

**Anti-pattern:** Do not refer to layers as "the analysis layer", "the generation engine", or "the export module" — these informal names introduce ambiguity. Always use the canonical names.

---

### Artifact Names

**Format:** Title Case for named platform artifacts; acronyms in all-caps.

Platform artifacts are the named data structures that cross layer boundaries or external Integration Touch-points. Their names are fixed and must be used exactly as defined in the Domain Glossary.

| Artifact | Correct Form | Incorrect Forms |
|---|---|---|
| Canonical Asset Record | Canonical Asset Record / CAR | canonical record, asset analysis, analysis output |
| Content Profile | Content Profile / Profile | profile config, generation template, channel config |
| Output Package | Output Package | metadata export, generated output, delivery package |
| Profile Identifier | Profile Identifier | profile ID, profile key, profile slug |
| Boundary Contract | Boundary Contract | layer contract, interface spec, handoff spec |

**Examples of correct usage:**

- "The Content Generation Layer receives the Canonical Asset Record and a Content Profile."
- "A Profile Identifier is supplied at the Integration Touch-point alongside the Asset."
- "The Channel Adaptation Layer produces the Output Package."

---

### Module Names

**Format:** PascalCase compound noun ending in "Forge"; always used as a proper noun.

The five platform modules follow a fixed naming pattern. Each module name is a single word formed from a domain descriptor and the "Forge" suffix.

| Module | Scope |
|---|---|
| StockForge | Stock photography marketplace metadata |
| SocialForge | Social media captions and hashtags |
| PortfolioForge | Portfolio website metadata |
| CommerceForge | E-commerce and marketplace product content |
| ArchiveForge | DAM and personal archive metadata |

**Examples of correct usage:**

- "MVP2 delivers the first StockForge profile: `stock/adobe-stock`."
- "CommerceForge is scoped to MVP8."
- "ArchiveForge serves DAM and personal archive destinations."

**Anti-pattern:** Do not use lowercase module names (`stockforge`), split forms (`Stock Forge`), or abbreviated forms (`StockF`) in documentation or story titles. The PascalCase compound form is always correct.

---

### MVP Milestone Labels

**Format:** `MVP` followed immediately by a zero-padded single digit where the number is 0–9; double digit for 10 and above.

| Correct | Incorrect |
|---|---|
| MVP0 | MVP 0, mvp0, Mvp0 |
| MVP2 | MVP-2, MVP02 |
| MVP10 | MVP10 is correct as written |
| MVP12 | mvp12, MVP 12 |

---

## Governance

### Purpose of This Process

Design principles and naming conventions only deliver value if they are stable and consistently applied. Ad hoc changes introduce inconsistency, break existing documentation and agent context, and undermine the shared understanding that makes cross-contributor work coherent. This governance process ensures that changes are deliberate, justified, and visible to all contributors.

---

### Proposing a New Principle or Convention

Any contributor — human or AI — may propose a new design principle or naming convention by raising a GitHub issue against the AssetForge repository with the label `documentation` and the label `design-principles-proposal`.

The proposal must include:

1. **Statement** — the principle or convention rule in one or two sentences.
2. **Rationale** — why this principle is needed; what problem it prevents or what value it protects.
3. **How to Apply** — a concrete example showing correct and incorrect application.
4. **Affected Artifacts** — a list of existing documents, stories, or profiles that would need to be updated to conform.
5. **Proposer** — the name or agent identifier of the contributor raising the proposal.

---

### Proposing a Change to an Existing Principle or Convention

Changes to existing entries follow the same process as new proposals. The issue must additionally identify:

- The specific principle or convention being changed (by section heading).
- The exact current wording.
- The proposed replacement wording.
- The reason the existing wording is inadequate or incorrect.

---

### Approval

The **Product Owner** is the sole approver for all changes to this document. No principle or naming convention takes effect, and no existing entry may be modified or removed, until the Product Owner has reviewed the proposal issue and granted explicit written approval on that issue.

Upon approval, the Product Owner or a delegated contributor must:

1. Update `docs/design-principles.md` with the approved change.
2. Update any directly affected documents (e.g., `docs/glossary.md`, `CLAUDE.md`) to reflect the change.
3. Close the proposal issue with a comment referencing the commit that applied the change.

---

### Stability Expectation

Design principles established before MVP1 should be treated as foundational and subject to a higher bar for change. Any proposal to modify a pre-MVP1 principle requires the Product Owner to also confirm that no in-flight stories, profiles, or implementation work would be invalidated by the change before approval is granted.
