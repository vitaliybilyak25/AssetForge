# Commercial vs Editorial Classification — Domain Concept

This document defines commercial use and editorial use as domain-level concepts within AssetForge. It specifies which Canonical Asset Record fields carry the classification signal, how a Content Profile may restrict or expand the default classification derived from those fields, and how the domain concept maps to the practical requirements of specific distribution destinations. This document does not provide legal definitions; all definitions are platform-practical and informed by stock marketplace policy conventions, not by legal advice.

All terms used below are defined in the [AssetForge Domain Glossary](glossary.md). CAR field names used in this document are defined and specified in the [CAR Field Catalogue](car-field-catalogue.md) (story #78).

---

## 1. Domain Definitions

### Commercial Use

**Commercial use** means that a generated Output Package is intended to support the licensing or distribution of the asset for advertising, marketing, or any for-profit promotional purpose — including product promotion, brand campaigns, editorial lifestyle imagery sold without restriction, and any other use in which the asset is a means of commercial persuasion or transaction.

A commercially classified Output Package asserts that the asset is free of subjects, likenesses, or property that require rights clearance, or that all required clearances are confirmed present. Specifically:

- If an identifiable person is depicted, a signed model release must be confirmed available.
- If recognisable private property is depicted, a signed property release must be confirmed available.
- The asset must not depict a real-world news event, unscripted public occurrence, or identifiable public figure in a context that implies endorsement or association with a commercial product.
- No third-party trademark or brand mark may appear in a way that implies commercial sponsorship or association without explicit rights clearance.

Meeting these conditions does not guarantee that a given distribution destination will accept the asset for commercial licensing — each platform applies its own additional submission rules — but it establishes the domain-level baseline that commercial classification requires.

### Editorial Use

**Editorial use** means that a generated Output Package is intended to support the licensing or distribution of the asset for informational, journalistic, educational, or documentary purposes only. An editorially classified asset depicts a real person, real event, or real place in its actual context, and may not be used in advertising, promotional material, or any for-profit persuasive application.

An editorially classified Output Package:

- Does not assert the absence of model releases, property releases, or trademark clearances; it asserts instead that the asset's intended licensing context makes those clearances inapplicable.
- May include identifiable persons, real-world events, public figures, or branded objects without requiring associated release documentation.
- Must not be used to generate content that implies the depicted person, event, or property endorses or is commercially associated with any product or brand.

Editorial classification is a restriction on intended use, not a quality tier or a ranking of the asset's commercial value.

---

## 2. CAR Fields That Carry the Classification Signal

The Asset Intelligence Layer does not make a commercial/editorial classification decision. That decision belongs to the Content Generation Layer, guided by the active Content Profile. What the Asset Intelligence Layer does provide is the factual evidence from which classification decisions are derived. The following CAR fields, defined in full in the [CAR Field Catalogue](car-field-catalogue.md) (story #78), are the load-bearing signals:

### Primary classification field

| CAR Field | Category | How it drives classification |
|---|---|---|
| `risk.editorial_only` | Risk Flags | The single most authoritative classification signal. When `true`, the asset is classified as Editorial Use only, regardless of any other field. This field is set by the Asset Intelligence Layer when `activities.editorial_event_signal` is `true` or when a public figure or real-world news event is detected. Any Content Profile targeting a commercial channel must block Output Package generation when this field is `true`, unless a human review override is recorded. |

### Supporting evidence fields

| CAR Field | Category | How it contributes |
|---|---|---|
| `activities.editorial_event_signal` | Activities | `true` when the depicted activity appears to be a real-world unscripted event (protest, sports event, ceremony, news moment). Triggers `risk.editorial_only` evaluation. Even when `risk.editorial_only` has not yet been set, a `true` value here should be treated as a strong editorial indicator by any Content Profile or routing rule that reads it directly. |
| `risk.model_release_required` | Risk Flags | `true` when an identifiable person is present. In isolation, this field does not classify the asset as editorial; it signals that commercial use requires a confirmed model release. When combined with a missing or unconfirmed release record, commercial classification must be blocked or routed for human review. |
| `risk.property_release_required` | Risk Flags | `true` when recognisable private property is depicted. Analogous to `risk.model_release_required`: in isolation it does not classify the asset as editorial, but it conditions commercial classification on confirmed property release availability. |
| `risk.trademark_flag` | Risk Flags | `true` when a third-party trademark or brand mark is visible. Commercial classification may still proceed if the trademark is incidental and unemphasised, but the Content Profile must include validation logic to gate this determination. |
| `persons.faces_detected` | People | `true` when at least one face is sufficiently visible to be potentially identifiable. Feeds into the evaluation of whether `risk.model_release_required` should be set, and directly informs the Content Generation Layer's assessment of commercial viability when release status is unknown. |
| `text.logo_marks_detected` | Text and Logos | Non-empty when brand marks are present. Feeds into `risk.trademark_flag` and informs commercial classification gatekeeping for brand-adjacent content. |

### Field reading rule for classification

Because the CAR is immutable and produced without knowledge of any Content Profile, downstream consumers reading these fields must apply CAR Consumer Rules 1–4 from the [Canonical Asset Record concept document](canonical-asset-record.md). In particular:

- An absent `risk.editorial_only` field must be treated as unknown — not as an implicit commercial clearance.
- `risk.model_release_required` set to `true` must be propagated regardless of confidence score (CAR Consumer Rule 4).
- Any field below the active confidence threshold must be treated as unknown; the classification decision must route to human review rather than default to commercial.

---

## 3. How a Content Profile Restricts or Expands Classification

The Content Profile is the mechanism by which a destination's classification requirements are applied at generation time. The domain definitions in Section 1 and the CAR fields in Section 2 provide the evidence; the Content Profile provides the decision rules.

### Restriction: blocking commercial generation when CAR signals editorial

A Content Profile targeting a commercial distribution channel must specify classification gate rules in its **Validation Rules** dimension. At minimum, a commercial profile must:

1. Block Output Package generation when `risk.editorial_only` is `true`.
2. Block or require human review when `risk.model_release_required` is `true` and no confirmed model release record is present.
3. Block or require human review when `risk.property_release_required` is `true` and no confirmed property release record is present.
4. Apply any channel-specific trademark or brand mark restrictions triggered by `risk.trademark_flag`.

A commercial profile may not silently proceed when any of these signals is active. Routing to human review (as defined in the **Approval Requirements** dimension of the Content Profile) is an acceptable resolution; silent generation is not.

### Restriction: limiting editorial profiles to editorial channels

A Content Profile targeting an editorial distribution channel must specify in its **Forbidden Content** dimension that commercially restricted content types (product promotion language, brand-association framing, endorsement-implying phrasing) are excluded from all generated output. An editorial profile should not generate titles or descriptions that read as promotional or aspirational, even when the CAR contains no editorial risk signals — because the intended licensing context forbids that framing regardless of the asset's content.

### Override: human review resolution

Some Content Profiles permit a human reviewer to override a classification gate. This is expressed in the **Approval Requirements** dimension. When a human reviewer confirms that a required release is present and on file, or that a detected editorial signal does not apply to the specific submission context, the override is recorded and the Content Generation Layer may proceed. The override record must be preserved in the Audit Trail (planned for MVP4); it must not be treated as a permanent modification of the CAR.

### Override: profile-specific commercial tolerance rules

Some distribution destinations accept commercially licensed assets that include incidental trademarked objects, provided the brand mark is not the subject of the image and no commercial association is implied. A Content Profile for such a destination may specify in its **Validation Rules** dimension a less restrictive trademark gatekeeping rule than the domain default. This is a legitimate profile-level override — the domain concept permits it because the platform-practical definition of commercial use is informed by destination policy, not a universal legal standard.

No Content Profile may override `risk.editorial_only` automatically. That flag requires human review resolution in all cases.

---

## 4. Platform Mapping Examples

The following examples show how the domain concept maps to the practical requirements of two specific stock distribution destinations. These mappings are illustrative; authoritative platform-specific rules belong in each destination's Content Profile story.

### Example 1 — Adobe Stock (`stock/adobe-stock`)

Adobe Stock distinguishes commercial and editorial in its submission interface and search filtering. The mapping to AssetForge domain concepts is:

| Adobe Stock requirement | Domain concept | CAR signal |
|---|---|---|
| Assets submitted as "commercial" must include signed model releases for identifiable persons | Commercial Use condition: confirmed model release | `risk.model_release_required` + release record confirmation |
| Assets submitted as "commercial" must include signed property releases for identifiable private structures | Commercial Use condition: confirmed property release | `risk.property_release_required` + release record confirmation |
| Assets submitted as "editorial" are labelled in search results and may not be used for advertising | Editorial Use: informational/journalistic context only | `risk.editorial_only` = `true` or profile-level editorial designation |
| Editorial submissions must include a caption describing the event, date, and location | Editorial content requirement: contextual factual caption | `location.setting_descriptor`, `activities.primary_activity`, `location.gps_derived_region` fed into caption generation under the editorial profile |
| Logos and brand marks visible in commercial submissions require rights clearance or must be obscured | Commercial trademark gate | `risk.trademark_flag` = `true` → Validation Rule gate in `stock/adobe-stock` profile |

The `stock/adobe-stock` Content Profile must, at minimum, include Validation Rules that block commercial Output Package generation when `risk.editorial_only` is `true`, and that route to Approval Requirements (human review) when `risk.model_release_required` or `risk.property_release_required` is `true` without a confirmed release record on file.

### Example 2 — Shutterstock (`stock/shutterstock`)

Shutterstock uses an editorial flag in its CSV bulk upload format. The mapping to AssetForge domain concepts is:

| Shutterstock requirement | Domain concept | CAR signal |
|---|---|---|
| The `Editorial` column in the CSV bulk upload must be set to `yes` or `no` | Commercial/editorial classification is a named, required output field | `risk.editorial_only` drives the value of this field; `false` or absent maps to `no` only when all commercial conditions are met |
| Editorial-flagged assets carry a licence restriction notice in search results and cannot be used for advertising | Editorial Use: informational/journalistic context only | Same as Adobe Stock: `risk.editorial_only` = `true` |
| Model releases must be confirmed before commercial submission | Commercial Use condition: confirmed model release | `risk.model_release_required` + release record confirmation |
| Certain content categories (news events, sports events, entertainment) are accepted only as editorial | Platform-specific editorial category gate | `activities.editorial_event_signal` = `true` should trigger editorial classification review even when `risk.editorial_only` has not been set |

The `stock/shutterstock` Content Profile must map `risk.editorial_only` to the `Editorial` CSV column value, and must define Validation Rules that enforce this mapping at the Channel Adaptation Layer. Because the `Editorial` column is a required field in the Shutterstock CSV format, the Channel Adaptation Layer must never produce an Output Package for this profile without a resolved classification value for that column.

---

## 5. Classification at Generation Time: Decision Sequence

The following sequence applies when the Content Generation Layer processes an asset against a stock or commercial Content Profile. It is not a flow diagram; it is a decision ordering that profile authors and CAR implementers must follow consistently.

1. **Check `risk.editorial_only`.** If `true`, apply the editorial content profile rules. If the active Content Profile targets a commercial channel, block generation and route to Approval Requirements. Do not proceed past this step without a resolved human override.

2. **Check `risk.model_release_required` and `risk.property_release_required`.** If either is `true`, verify whether a confirmed release record is present for this asset. If no confirmation is available, block commercial generation and route to Approval Requirements. If confirmation is available, record the confirmation and continue.

3. **Check `risk.trademark_flag`.** If `true`, apply the trademark gate rule specified in the active Content Profile's Validation Rules. This may block generation, require human review, or permit continuation depending on the profile's tolerance specification.

4. **Check `activities.editorial_event_signal`.** If `true` and `risk.editorial_only` was not already set, treat as a strong editorial indicator. Apply the profile's specified behaviour for this scenario (typically: require human review before commercial generation proceeds).

5. **Evaluate remaining classification signals** (`persons.faces_detected`, `text.logo_marks_detected`) as supporting evidence for any unresolved review routing decisions.

6. **Generate the Output Package** with the classification value resolved. For profiles that include an editorial/commercial indicator field in the Output Package (such as Shutterstock's `Editorial` CSV column), that value must be set explicitly and must reflect the outcome of steps 1–5.

---

## Cross-References

- **Domain Glossary:** [docs/glossary.md](glossary.md) — Commercial Use and Editorial Use entries cross-reference this document.
- **CAR Field Catalogue (story #78):** [docs/car-field-catalogue.md](car-field-catalogue.md) — authoritative source for all field names, types, and cardinality used in Section 2 of this document.
- **Canonical Asset Record concept (story #15):** [docs/canonical-asset-record.md](canonical-asset-record.md) — Consumer Rules 1–4 that govern how the CAR fields listed in Section 2 must be read by downstream consumers.
- **Content Profile concept (story #16):** [docs/content-profile.md](content-profile.md) — the ten configurable dimensions (Validation Rules, Forbidden Content, Approval Requirements) referenced in Section 3 of this document.
- **Content Profile schema (story #79):** [profiles/content-profile-schema.md](../profiles/content-profile-schema.md) — the field schema against which all Content Profile configurations in Section 3 must be expressed.
- **Boundary Contracts (story #77):** [docs/boundary-contracts.md](boundary-contracts.md) — the Handoff 1 validity conditions that govern what constitutes a complete and valid CAR, including the requirement that Risk Flags be evaluated before the CAR is handed off to the Content Generation Layer.
