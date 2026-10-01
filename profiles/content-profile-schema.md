# Content Profile Schema Reference

**Schema version:** 0.1
**Cross-reference:** [docs/content-profile.md](../docs/content-profile.md) (story #16)
**Status:** MVP0 — authoritative schema for all Content Profile authoring from MVP2 onwards

---

## Purpose

This document is the field-level schema reference for every Content Profile in AssetForge. It translates the ten configurable dimensions defined in `docs/content-profile.md` into named fields, data types, required/optional status, shared-vs-channel-specific classification, and allowed values or format constraints. Profile Authors must use this schema as the authoritative specification when authoring any new Content Profile. Every field produced in the YAML authoring template (`profiles/content-profile-template.yaml`) corresponds to a row in this reference.

All terms used below are defined in the [AssetForge Domain Glossary](../docs/glossary.md). Layer responsibilities referenced below are governed by the [Three-Layer Architecture Boundary Contracts](../docs/boundary-contracts.md).

---

## Consumed Dimensions by Layer

Before reading the field catalogue below, note which dimensions each layer consumes, as established in the Boundary Contracts:

| Layer | Dimensions Consumed |
|---|---|
| Content Generation Layer (Layer 2) | Audience, Tone, Required and Optional Fields, Length Limits, Keyword Rules, Forbidden Content, Language, Approval Requirements |
| Channel Adaptation Layer (Layer 3) | Output Format, Validation Rules |

The Asset Intelligence Layer (Layer 1) does not consume any Content Profile dimension.

---

## Field Classification Key

- **Required** — must be present and non-empty in every conformant Content Profile. A Content Profile missing a Required field is invalid.
- **Optional** — may be omitted; when omitted, the default behaviour is specified in the field description.
- **Shared** — the field has the same structural definition across all profiles; its value may differ per profile but its presence and meaning are universal.
- **Channel-specific** — the field exists only for profiles where the parent dimension is applicable to that channel type. A channel-specific field omitted from a profile implies the profile does not use that feature.

---

## 0. Profile Identity Fields

These fields are not one of the ten configurable dimensions; they are administrative identity fields required on every Content Profile. They are all Shared.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `schema_version` | string | Required | Shared | Identifies which version of this schema the profile conforms to; enables forward-compatible tooling. | Semver string, e.g. `"0.1"` |
| `cross_reference` | string | Required | Shared | Links the profile back to the concept definition document and story number; provides traceability. | Free string, e.g. `"docs/content-profile.md (story #16)"` |
| `profile_id` | string | Required | Shared | The Profile Identifier in `category/profile-name` format; the canonical name by which the Pipeline resolves this Content Profile. Category must be one of: `stock`, `marketing`, `web`, `commerce`, `library`, `general`. Both segments are lowercase and hyphen-separated. | `{category}/{profile-name}`, e.g. `stock/adobe-stock` or `general/short-description` |
| `profile_name` | string | Required | Shared | A human-readable display name for the profile; used in UI and reporting contexts. | Free string, e.g. `"Adobe Stock"` |
| `module` | string | Required | Shared | The AssetForge module this profile belongs to. | One of: `StockForge`, `SocialForge`, `PortfolioForge`, `CommerceForge`, `ArchiveForge`, `General` (for channel-agnostic profiles in `profiles/general/`) |
| `description` | string | Required | Shared | A one- to two-sentence plain-language description of what this profile is for and which Distribution Destination it targets. | Free string |
| `asset_types` | list of strings | Required | Shared | The Asset Types this profile supports processing. Determines which CAR fields are expected to be populated. | Any combination of: `photo`, `video`, `vector` |
| `created` | string (date) | Required | Shared | The date this profile was first authored. | ISO 8601 date: `YYYY-MM-DD` |
| `last_updated` | string (date) | Required | Shared | The date this profile was last modified. Must be updated on every change. | ISO 8601 date: `YYYY-MM-DD` |

---

## 1. Audience Dimension

Consumed by: Content Generation Layer (Layer 2).
Defines who the generated content is written for. The Content Generation Layer uses this to shape vocabulary, assumed knowledge level, and content priorities.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `audience.primary` | string | Required | Shared | Names the primary human or system consumer of the generated content. This is the first-priority framing for all generated text. | Free string, e.g. `"Stock marketplace buyers seeking commercial lifestyle imagery"` |
| `audience.secondary` | string | Optional | Channel-specific | Names a secondary audience when the Distribution Destination serves more than one type of consumer. Omit if there is only one audience. | Free string, e.g. `"Search engine indexing algorithms"` |
| `audience.use_context` | string | Required | Shared | Describes the context in which the audience encounters the generated content — browsing, searching, purchasing, archiving, etc. | Free string, e.g. `"Search-driven discovery on a stock marketplace"` |

**Example values (for a stock marketplace profile):**
- `audience.primary`: `"Stock marketplace buyers seeking commercial or editorial imagery"`
- `audience.use_context`: `"Keyword-driven search on a stock photography marketplace"`

---

## 2. Tone Dimension

Consumed by: Content Generation Layer (Layer 2).
Specifies the voice and register in which generated text must be written.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `tone.register` | string | Required | Shared | The primary voice register for all generated text fields. | One of: `factual`, `descriptive`, `conversational`, `aspirational`, `technical`, `formal` |
| `tone.style_notes` | string | Optional | Channel-specific | Additional instructions refining the register — for example, whether to use active or passive voice, sentence length guidance, or brand-voice caveats. | Free string, e.g. `"Use active voice. Avoid exclamation marks. Do not use first person."` |

**Example values:**
- `tone.register`: `"factual"`
- `tone.style_notes`: `"Use active voice and present tense. Avoid superlatives."`

---

## 3. Required and Optional Fields Dimension

Consumed by: Content Generation Layer (Layer 2). Also governs Handoff 2 validity (all required fields must be present and non-empty before Generated Content is passed to the Channel Adaptation Layer).

Each entry in `fields` describes one content field the Content Generation Layer may be asked to produce. The `required` flag determines whether its absence invalidates the Output Package.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `fields[].name` | string | Required | Shared | The canonical name of the content field. Must match a field name recognised by the Content Generation Layer. | One of: `title`, `description`, `keywords`, `caption`, `alt_text`, `headline`, `summary` |
| `fields[].required` | boolean | Required | Shared | If `true`, the field must be present and non-empty in the Generated Content for the Output Package to be valid. If `false`, the field is produced only when the CAR contains sufficient information. | `true` or `false` |
| `fields[].purpose` | string | Optional | Shared | A brief note explaining why this field is required or optional for this specific Distribution Destination. Used as authoring guidance; not consumed by the Pipeline. | Free string |

**Example values:**
```yaml
fields:
  - name: title
    required: true
    purpose: "Primary searchable text field on Adobe Stock; highest SEO weight."
  - name: description
    required: true
    purpose: "Secondary search field; supports editorial context."
  - name: keywords
    required: true
    purpose: "Primary discoverability mechanism; Adobe Stock indexes all keywords."
  - name: caption
    required: false
    purpose: "Optional contextual note; used for editorial submissions only."
```

---

## 4. Length Limits Dimension

Consumed by: Content Generation Layer (Layer 2). Governs Handoff 2 validity condition 2.

Specifies the minimum and maximum character or word counts for each text field. One entry per field listed in the Required and Optional Fields dimension.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `length_limits[].field` | string | Required | Shared | The name of the content field this limit applies to. Must match a name in `fields[].name`. | One of: `title`, `description`, `keywords`, `caption`, `alt_text`, `headline`, `summary` |
| `length_limits[].unit` | string | Required | Shared | Whether the limit is expressed in characters or words. | One of: `characters`, `words` |
| `length_limits[].min` | integer | Optional | Channel-specific | Minimum count. Omit if the destination has no minimum. | Non-negative integer |
| `length_limits[].max` | integer | Required | Shared | Maximum count. Every text field must have a maximum to prevent rejection by the Distribution Destination. | Positive integer |

**Example values:**
```yaml
length_limits:
  - field: title
    unit: characters
    min: 5
    max: 200
  - field: description
    unit: characters
    min: 10
    max: 200
  - field: keywords
    unit: words
    min: 25
    max: 49
```

---

## 5. Keyword Rules Dimension

Consumed by: Content Generation Layer (Layer 2). Governs Handoff 2 validity condition 3.

Governs the generation of the keyword list. This dimension applies only to profiles that include `keywords` in their Required and Optional Fields dimension.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `keyword_rules.min_count` | integer | Required | Channel-specific | Minimum number of keywords the generated list must contain. | Non-negative integer |
| `keyword_rules.max_count` | integer | Required | Channel-specific | Maximum number of keywords permitted. Exceeding this count invalidates the Output Package. | Positive integer, must be >= `min_count` |
| `keyword_rules.formats_allowed` | list of strings | Required | Channel-specific | Which keyword formats the destination accepts. | Any combination of: `single_word`, `phrase` |
| `keyword_rules.capitalisation` | string | Required | Channel-specific | Case convention for all keywords. | One of: `lowercase`, `title_case`, `as_generated` |
| `keyword_rules.separator` | string | Required | Channel-specific | The separator used between keywords in the generated list when serialised. | One of: `comma`, `semicolon`, `newline` |
| `keyword_rules.ordering` | string | Optional | Channel-specific | Whether keywords must be ordered in a specific way. Omit if the destination has no ordering requirement. | One of: `relevance_descending`, `alphabetical`, `none` |

**Example values:**
```yaml
keyword_rules:
  min_count: 25
  max_count: 49
  formats_allowed:
    - single_word
    - phrase
  capitalisation: lowercase
  separator: comma
  ordering: relevance_descending
```

---

## 6. Forbidden Content Dimension

Consumed by: Content Generation Layer (Layer 2). Governs Handoff 2 validity condition 4.

Lists subject matter, terms, or content types that must never appear in any generated field for this profile. This list is profile-specific and does not represent a platform-wide block list.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `forbidden_content.terms` | list of strings | Optional | Channel-specific | Specific words or phrases that must not appear in any generated field. Omit if the profile has no term-level restrictions. | List of lowercase strings |
| `forbidden_content.content_types` | list of strings | Optional | Channel-specific | Categories of subject matter that must not appear in generated output. Omit if the profile has no content-type restrictions. | Free strings describing content categories, e.g. `"competitor brand names"`, `"adult content"`, `"politically sensitive terms"` |
| `forbidden_content.rationale` | string | Optional | Shared | A brief explanation of why these restrictions are in place; aids profile authors in understanding the intent. Not consumed by the Pipeline. | Free string |

**Example values:**
```yaml
forbidden_content:
  terms:
    - shutterstock
    - getty
    - istock
  content_types:
    - "competitor brand names"
    - "politically sensitive terms"
    - "adult or explicit content references"
  rationale: "Adobe Stock submission guidelines prohibit competitor references and
    require politically neutral descriptions for commercial licensing."
```

---

## 7. Language Dimension

Consumed by: Content Generation Layer (Layer 2). Governs Handoff 2 validity condition 5.

Specifies the language and locale in which all generated text fields must be written.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `language.primary` | string | Required | Shared | The language and locale for all generated text fields. | IETF BCP 47 language tag, e.g. `en-US`, `en-GB`, `de-DE`, `fr-FR` |
| `language.secondary` | list of strings | Optional | Channel-specific | Additional locales if the Distribution Destination requires multi-language output. Omit for single-language destinations. | List of IETF BCP 47 language tags |

**Example values:**
- `language.primary`: `"en-US"`

---

## 8. Output Format Dimension

Consumed by: Channel Adaptation Layer (Layer 3).
Specifies the technical delivery format the Channel Adaptation Layer must use when producing the Output Package. This dimension governs Layer 3 only; it has no effect on content generation.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `output_format.type` | string | Required | Channel-specific | The primary delivery format for the Output Package. | One of: `csv`, `json`, `iptc_xmp`, `rest_api`, `cms_integration`, `filesystem_export` |
| `output_format.notes` | string | Optional | Channel-specific | Any additional formatting guidance relevant to the Channel Adaptation Layer for this specific destination — for example, file encoding, line-ending convention, or required header row. Not a content-generation instruction. | Free string |

**Example values:**
```yaml
output_format:
  type: csv
  notes: "UTF-8 encoding, comma delimiter, header row required. Column order is
    a Channel Adaptation Layer responsibility; see destination adapter spec."
```

---

## 9. Validation Rules Dimension

Consumed by: Channel Adaptation Layer (Layer 3). Governs Output Package validity before delivery.
Specifies the automated checks that generated output must pass before being included in a completed Output Package.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `validation_rules[].rule_id` | string | Required | Shared | A short unique identifier for this validation rule within the profile; used in error reporting. | Lowercase hyphen-separated string, e.g. `min-keyword-count` |
| `validation_rules[].check` | string | Required | Shared | A plain-language description of what this rule verifies. | Free string |
| `validation_rules[].field` | string | Optional | Shared | The specific content field this rule applies to. Omit for rules that apply to the full Output Package rather than one field. | One of: `title`, `description`, `keywords`, `caption`, `alt_text`, `headline`, `summary`, or omit for package-level rules |
| `validation_rules[].condition` | string | Required | Shared | The machine-readable condition that must be true for validation to pass. Written as a constraint expression referencing field attributes. | Constraint expression, e.g. `"keywords.count >= 25"`, `"title.length <= 200"`, `"description != empty"` |

**Example values:**
```yaml
validation_rules:
  - rule_id: title-required
    check: "Title field is present and non-empty."
    field: title
    condition: "title != empty"
  - rule_id: title-max-length
    check: "Title does not exceed 200 characters."
    field: title
    condition: "title.length <= 200"
  - rule_id: description-required
    check: "Description field is present and non-empty."
    field: description
    condition: "description != empty"
  - rule_id: min-keyword-count
    check: "Keyword list contains at least 25 keywords."
    field: keywords
    condition: "keywords.count >= 25"
  - rule_id: max-keyword-count
    check: "Keyword list does not exceed 49 keywords."
    field: keywords
    condition: "keywords.count <= 49"
  - rule_id: no-forbidden-terms
    check: "No forbidden terms appear in any generated field."
    condition: "all_fields contain_none_of forbidden_content.terms"
```

---

## 10. Approval Requirements Dimension

Consumed by: Content Generation Layer (Layer 2) — specifically to flag whether the Output Package requires human review before delivery; the flag is preserved through to the Output Package by the Channel Adaptation Layer.

| Field | Type | Required / Optional | Shared / Channel-specific | Purpose | Allowed Values / Format |
|---|---|---|---|---|---|
| `approval_requirements.human_review_required` | boolean | Required | Shared | If `true`, every Output Package generated under this profile requires human review before delivery. If `false`, Output Packages are delivery-ready immediately upon passing all Validation Rules. | `true` or `false` |
| `approval_requirements.conditional_triggers` | list of strings | Optional | Channel-specific | Conditions under which human review is required even when `human_review_required` is `false`. Each entry references a CAR Risk Flag category or a content attribute. | Free strings referencing CAR Risk Flag categories, e.g. `"risk_flag: identifiable_person"`, `"risk_flag: visible_brand_mark"`, `"content: adult_content"` |
| `approval_requirements.notes` | string | Optional | Shared | Plain-language explanation of the approval policy for this profile; aids profile authors and reviewers in understanding the intent. Not consumed by the Pipeline. | Free string |

**Example values:**
```yaml
approval_requirements:
  human_review_required: false
  conditional_triggers:
    - "risk_flag: identifiable_person"
    - "risk_flag: visible_brand_mark"
  notes: "Output Packages for assets with an identifiable person or a visible brand
    mark require human review before Adobe Stock submission, because model or
    property releases must be confirmed."
```

---

## Shared vs Channel-specific Field Summary

The following table consolidates the shared-vs-channel-specific classification across all ten dimensions for quick reference.

| Dimension | Shared Fields | Channel-specific Fields |
|---|---|---|
| Profile Identity | All identity fields | — |
| Audience | `audience.primary`, `audience.use_context` | `audience.secondary` |
| Tone | `tone.register` | `tone.style_notes` |
| Required and Optional Fields | `fields[].name`, `fields[].required` | `fields[].purpose` |
| Length Limits | `length_limits[].field`, `length_limits[].unit`, `length_limits[].max` | `length_limits[].min` |
| Keyword Rules | — | All keyword rule fields |
| Forbidden Content | `forbidden_content.rationale` | `forbidden_content.terms`, `forbidden_content.content_types` |
| Language | `language.primary` | `language.secondary` |
| Output Format | — | All output format fields |
| Validation Rules | `validation_rules[].rule_id`, `validation_rules[].check`, `validation_rules[].condition` | `validation_rules[].field` |
| Approval Requirements | `approval_requirements.human_review_required`, `approval_requirements.notes` | `approval_requirements.conditional_triggers` |

---

## Authoring Notes

1. Every new Content Profile must conform to this schema. Any field marked Required must be present.
2. Profile Identifiers must follow the `{category}/{profile-name}` format defined in `docs/design-principles.md`. The category must be one of: `stock`, `marketing`, `web`, `commerce`, `library`, `general`. The `general` category is for channel-agnostic, reusable profiles that are not tied to a specific distribution destination.
3. The ten dimensions map directly to the ten configurable dimensions in `docs/content-profile.md` (story #16). If the concept document and this schema appear to conflict, raise the discrepancy with the Product Owner before authoring.
4. Do not include Output Format or Validation Rules decisions in the Audience, Tone, or Keyword Rules fields. These cross-layer concerns are governed by the Boundary Contracts in `docs/boundary-contracts.md`.
5. The YAML authoring template at `profiles/content-profile-template.yaml` provides a copy-and-fill starting point. Use that template; do not author profiles from a blank file.
