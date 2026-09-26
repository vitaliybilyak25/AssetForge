# Canonical Asset Record — Concept Definition

This document defines the Canonical Asset Record (CAR) as a platform concept. It describes its purpose, its position in the three-layer architecture, the seven categories of information it contains, and the rules that downstream consumers must follow when a field is absent or below confidence threshold. This document does not define field names, data types, or schema; those are the subject of story #78 (CAR Field Catalogue). All terms used below are defined in the [AssetForge Domain Glossary](glossary.md).

---

## 1. Purpose

**The question the CAR answers:** What is in this asset, as a matter of observable, channel-agnostic fact?

The CAR is the Asset Intelligence Layer's answer to that single question. It records neutral, factual observations about the asset — what objects are present, who is depicted, where it was taken, what text or logos appear, what activities are occurring, what compliance risks are signalled, and how certain the layer is about each finding. Every observation in the CAR is independent of any intended audience, distribution channel, or content tone.

**The question the CAR explicitly does NOT answer:** What should the metadata say about this asset for a specific audience or channel?

The CAR contains no titles, descriptions, captions, or keyword lists. It makes no decisions about tone, language, length, or channel requirements. It does not know which Content Profile will be applied to it, and it does not produce content shaped by any distribution destination. Generating channel-specific content from the CAR is the sole responsibility of the Content Generation Layer, guided by a Content Profile.

---

## 2. Position in the Architecture

**Produced by:** The Asset Intelligence Layer (Layer 1). The CAR is the only output the Asset Intelligence Layer produces. Layer 1's responsibility begins when a raw Asset enters the Pipeline and ends when it delivers a complete CAR. It has no knowledge of the Content Profile that will be applied downstream and makes no content decisions.

**Consumed by:** The Content Generation Layer (Layer 2). The CAR is one of two inputs the Content Generation Layer requires; the other is a resolved Content Profile. Layer 2 reads the CAR's factual observations and uses them, combined with the Content Profile's rules, to generate titles, descriptions, keywords, and captions.

**Immutability rule:** The CAR is immutable after production. No layer, process, or actor may modify the Canonical Asset Record once the Asset Intelligence Layer has produced it. The Content Generation Layer reads the CAR but does not alter it. The Channel Adaptation Layer has no access to the CAR. If a CAR is found to be incorrect, it must be discarded and reproduced by the Asset Intelligence Layer; it may never be edited in place. This rule is what makes the CAR a reliable, single source of factual truth throughout the Pipeline.

The CAR is an internal Handoff artifact between Layer 1 and Layer 2. It is not exposed at any external Integration Touch-point and is not included in Output Packages delivered to distribution destinations.

---

## 3. Information Categories

The CAR contains observations organised into seven categories. The categories define what the Asset Intelligence Layer is responsible for detecting and recording. They do not prescribe field names or data structures; those are specified in the Field Catalogue (story #78).

**Objects and Subjects** — The identifiable physical things depicted in the asset: everyday objects, consumer goods, natural elements, architectural features, vehicles, or any other tangible subject that can be observed and named without reference to audience or channel.

**People** — Observations about human presence in the asset: whether persons are detectable, the approximate number of individuals, whether faces are identifiable, and — for asset types where it applies — the nature of any group or demographic composition visible to analysis.

**Locations** — Geographic and environmental context derived from the asset: scene type (indoor, outdoor, urban, natural), identifiable place references detectable from visual content or embedded metadata (such as GPS), and any geographic or regional signals present in the asset.

**Text and Logos** — Readable text strings and brand marks visible within the asset: words, phrases, numbers, signage, product labels, watermarks, and any trademark symbols or commercial brand marks that are legible or visually detectable.

**Activities** — Dynamic events and actions occurring within the asset: what people or subjects are doing, what physical or social situations are depicted, and — for time-based asset types — what events unfold across the asset's duration.

**Risk Flags** — Structured compliance signals indicating that the asset contains content requiring special handling before certain Output Packages can be generated or approved: identifiable persons (triggering model release evaluation), visible private property (triggering property release evaluation), adult content, violence, editorial-use-only classification, and any other category that downstream channels or human reviewers must act on.

**Confidence Scores** — Numeric certainty values attached to observations in the preceding categories, indicating how certain the Asset Intelligence Layer is in each finding; a low confidence score does not discard the observation but signals that downstream consumers must treat it with appropriate caution rather than act on it as established fact.

---

## 4. Consumer Rules

The following rules apply to any layer, process, or system that reads a Canonical Asset Record. They are binding constraints, not guidelines.

**Rule 1 — Absent fields must be treated as unknown, not as negative.** If a CAR field or category is absent, the consumer must treat the information as unknown. An absent People category does not mean no persons are present; it means the Asset Intelligence Layer did not produce a finding for that category. The consumer must not infer a negative conclusion from an absence, and must not proceed as though the information is known.

**Rule 2 — Fields below the confidence threshold must be treated as unknown.** Each Content Profile or Channel Adaptation rule set defines the minimum confidence score required to act on a given CAR field. If a confidence score is below that threshold, the consumer must treat the field as unknown and apply Rule 1. The consumer must not use a below-threshold value as if it were a confirmed observation.

**Rule 3 — Unknown information must not be resolved by inference.** When a consumer encounters an absent or below-threshold field, the correct response is to treat the fact as unknown. The consumer must not substitute a guess, a default assumption, or a value derived from other fields to fill the gap. Downstream content or validation logic that depends on an absent or low-confidence field must either skip that logic path or route the asset for human review, according to the rules of the active Content Profile.

**Rule 4 — Risk Flags must be propagated regardless of confidence.** A Risk Flag recorded in the CAR must always be surfaced to downstream consumers, even if the confidence score for the underlying observation is low. The purpose of a Risk Flag is to signal that human review or rights clearance may be required; a low-confidence detection of an identifiable person is still a signal that must not be silently discarded.

---

## 5. Relationship to the Field Catalogue

This document defines the CAR as a concept: its purpose, its architectural role, its seven information categories, and the rules that govern its use. It intentionally contains no field names, data types, cardinality specifications, or schema definitions.

The complete field-level specification of the CAR — including every named field, its data type, cardinality, validation rules, confidence score applicability, and mapping to the seven categories above — is the subject of **story #78 (CAR Field Catalogue)**. The Field Catalogue is the implementation-level complement to this concept document.

The seven information categories defined in Section 3 are intended to serve as the organising structure for the Field Catalogue. Each field in story #78 should be traceable to one of the seven categories defined here. Any conflict between the conceptual framing in this document and the field-level decisions in story #78 must be resolved in favour of story #78, with a corresponding update to this document if the concept itself changes.
