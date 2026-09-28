# Adobe Stock — Model and Property Release Rules

This document specifies the trigger conditions, export behaviour, CSV column values, and editorial exemption path for model releases and property releases in the `stock/adobe-stock` Content Profile. It is the deliverable for **story #85**.

These rules govern the Channel Adaptation Layer's production of the Adobe Stock CSV `Releases` column, and the Content Generation Layer's export-blocking behaviour when required release documentation is absent or unconfirmed.

> **Out of scope.** This document defines the rules that govern release requirements. It does not define how release presence is confirmed, how release documents are stored, or how the confirmation mechanism is implemented. The confirmation mechanism is deferred to a separate design story.

---

## Cross-References

The following documents are authoritative sources for field names, handling policies, and classification logic referenced throughout this document.

| Document | Story | What it provides |
|---|---|---|
| [docs/car-field-catalogue.md](car-field-catalogue.md) | #78 | Field names, data types, and cardinality for all CAR fields referenced in this document (`persons.*`, `text.logo_marks_detected`, `risk.*`) |
| [docs/confidence-and-risk-rules.md](confidence-and-risk-rules.md) | #84 | Canonical handling policy vocabulary (`suppress output`, `require human review`, `block output entirely`); default policies for `risk.model_release_required` and `risk.property_release_required`; propagation rule (CAR Consumer Rule 4) |
| [docs/commercial-editorial-classification.md](commercial-editorial-classification.md) | #86 | Definition of commercial and editorial use; `risk.editorial_only` field semantics; classification decision sequence (Section 5); Adobe Stock platform mapping table (Section 4) |

---

## 1. Model Release Trigger Conditions

The Asset Intelligence Layer sets `risk.model_release_required = true` on a Photo CAR when `persons.present` is `true` and at least one person in the image is potentially identifiable. The following conditions constitute the defined set of triggering signals for the `stock/adobe-stock` profile. Each trigger must be evaluated independently; the presence of any single trigger is sufficient to set the flag.

### 1.1 Identifiable face detected

**Trigger:** `persons.faces_detected = true`

**CAR fields carrying the signal:**
- `persons.present` (boolean, Required) — confirms human presence; must be `true` before any People category conditional fields are evaluated
- `persons.faces_detected` (boolean, Conditional — present when `persons.present` is `true`) — `true` when at least one face is sufficiently visible to be potentially identifiable

**Rule:** When `persons.present = true` and `persons.faces_detected = true`, the Asset Intelligence Layer must set `risk.model_release_required = true`. A visible face is the most direct identifiability signal; no additional contextual evidence is required.

**Example:** A portrait photograph in which the subject's face, eyes, and distinguishing features are clearly visible. The face alone is sufficient to make the person potentially identifiable.

### 1.2 Person prominently featured without a visible face

**Trigger:** `persons.present = true` and `persons.faces_detected = false` but the person is visually prominent and their overall appearance, silhouette, or physical context makes them a focal subject of the image

**CAR fields carrying the signal:**
- `persons.present` (boolean, Required)
- `persons.faces_detected` (boolean, Conditional) — `false` confirms no face is visible
- `persons.activity_posture` (string, Conditional — present when `persons.present` is `true` and a dominant posture is detectable) — a value such as `"facing camera"`, `"standing"`, or similar indicates the person is actively presented as a subject, not incidental to the scene
- `objects.primary_subject` (string, Conditional) — when the person is identified as the primary subject, this field corroborates prominent feature status

**Rule:** When `persons.present = true`, `persons.faces_detected = false`, and the person is determined by the Asset Intelligence Layer to be a prominently featured subject of the image (evidenced by `persons.activity_posture` and/or `objects.primary_subject` pointing to the person), `risk.model_release_required` must be set to `true`. A person is considered prominently featured when their depiction is the intended visual focus of the image, regardless of whether their face is visible.

**Example:** A full-body photograph taken from behind in which a person stands centrally in the frame in styled clothing, intentionally posed for the camera. The face is not visible but the person is clearly the subject of the image.

### 1.3 Person identifiable by a distinctive physical characteristic

**Trigger:** `persons.present = true` and the person is identifiable through a distinctive, non-facial physical characteristic such as a visible tattoo, distinctive clothing used as an identification marker, or a unique physical attribute

**CAR fields carrying the signal:**
- `persons.present` (boolean, Required)
- `persons.faces_detected` (boolean, Conditional) — may be `false`
- `objects.detected_subjects` (Array\<string\>, Required) — may contain entries describing the identifying characteristic (e.g., `"full-sleeve tattoo"`, `"distinctive uniform"`)
- `persons.activity_posture` (string, Conditional) — provides compositional context about the person's visibility in the frame

**Rule:** When `persons.present = true` and the Asset Intelligence Layer detects a distinctive non-facial physical characteristic that is widely known, publicly associated with a specific individual, or sufficiently unique to enable identification, `risk.model_release_required` must be set to `true`. The characteristic need not uniquely identify the person with certainty; it is sufficient that a reasonable viewer could identify the individual from the characteristic depicted.

**Example:** A close-up photograph of a person's forearm displaying a large, elaborate tattoo design that has been publicly documented as belonging to a known individual. No face is visible, but the tattoo is an identifying mark.

---

## 2. Property Release Trigger Conditions

The Asset Intelligence Layer sets `risk.property_release_required = true` on a Photo CAR when recognisable private property — buildings, branded structures, or private artworks — is identifiable in the image. The following conditions constitute the defined set of triggering signals for the `stock/adobe-stock` profile. Each trigger must be evaluated independently.

### 2.1 Identifiable private building or residence

**Trigger:** An identifiable private structure — a residential building, private commercial facility, or privately owned architectural landmark — is prominently visible in the image

**CAR fields carrying the signal:**
- `location.setting_descriptor` (string, Conditional — present when the setting is classifiable with sufficient visual evidence) — a value such as `"private residence"`, `"corporate headquarters"`, or `"privately owned venue"` provides the classification signal
- `location.visual_landmark` (string, Conditional — present when an identifiable landmark is visible with high confidence) — when this field names a privately owned structure, it confirms identifiability
- `objects.detected_subjects` (Array\<string\>, Required) — may contain the building type as a detected subject

**Rule:** When the Asset Intelligence Layer determines that a private building or structure is the primary or prominently featured subject of the image, and the structure is identifiable as a specific privately owned property (as evidenced by `location.visual_landmark` naming it, or `location.setting_descriptor` classifying it as a private structure), `risk.property_release_required` must be set to `true`.

**Example:** A wide-angle architectural photograph of a distinctive privately owned residence in which the building's unique facade design, address-indicating features, or widely known appearance makes the specific property identifiable.

### 2.2 Recognisable private artwork or sculpture

**Trigger:** A privately owned artwork, sculpture, mural, or installation that is not in the public domain is prominently visible in the image

**CAR fields carrying the signal:**
- `objects.detected_subjects` (Array\<string\>, Required) — may contain a description of the artwork or sculpture as a detected subject
- `objects.primary_subject` (string, Conditional) — when the artwork is identified as the primary subject, this field confirms its visual prominence
- `text.logo_marks_detected` (Array\<string\>, Conditional — present when brand marks are detectable) — some privately commissioned artworks incorporate branded elements that aid identification

**Rule:** When the Asset Intelligence Layer identifies a prominent artwork, sculpture, mural, or installation that is potentially protected by copyright and privately owned — not a historical public artwork in the public domain — `risk.property_release_required` must be set to `true`. Visual prominence is assessed by whether the artwork occupies a significant portion of the frame or is clearly the subject of the image, not merely incidental background.

**Example:** A street photograph in which a large, privately commissioned mural painted on the exterior wall of a commercial building is the primary visual subject, with the artist's signature visible and the work recognisable as a specific contemporary piece.

### 2.3 Branded private structure or custom-built branded installation

**Trigger:** A privately designed and branded structure — a custom-built brand installation, a branded architectural element, or a privately commissioned structure bearing a specific brand identity — is prominently visible in the image

**CAR fields carrying the signal:**
- `text.logo_marks_detected` (Array\<string\>, Conditional — present when one or more brand marks are detectable) — when a brand mark is detected on a structure, this field names the brand mark or marks identified
- `risk.trademark_flag` (boolean, Conditional — present when `text.logo_marks_detected` is non-empty or a brand mark is detected) — `true` confirms that a third-party trademark is present; when this flag and the structural context together indicate a branded private installation, `risk.property_release_required` must also be set
- `objects.detected_subjects` (Array\<string\>, Required) — may contain the structural type as a detected subject
- `location.setting_descriptor` (string, Conditional) — provides environmental context for the structure

**Rule:** When the Asset Intelligence Layer detects a custom-built branded installation, branded architectural element, or privately commissioned structure that incorporates a specific brand identity — and that structure is prominently featured in the image — `risk.property_release_required` must be set to `true`. The concurrent setting of `risk.trademark_flag = true` does not replace or supersede `risk.property_release_required`; both flags must be set independently when their respective conditions are met.

**Example:** A product launch photograph featuring a custom-fabricated brand pavilion — an architectural structure purpose-built for a corporate event, bearing the sponsoring brand's logo and distinctive design language — as the primary background element.

---

## 3. Adobe Stock CSV `Releases` Column Behaviour

The Adobe Stock CSV bulk upload format includes a `Releases` column. This column records the name or names of release files that have been uploaded to the Adobe Stock contributor portal for the associated asset. The three states and their corresponding `Releases` column values are specified below.

### 3.1 State A — Release confirmed present

**Condition:** `risk.model_release_required = true` or `risk.property_release_required = true`, and a human reviewer has confirmed that a valid, signed release document is on file for the asset.

**`Releases` column value:** The exact file name or names of the release document(s) as uploaded to the Adobe Stock contributor portal. If multiple releases are on file (for example, a model release and a property release, or releases for multiple identifiable persons), the column value is a comma-separated list of the release file names with no surrounding whitespace between the comma and the next name.

**Format:** `release-filename-1.pdf,release-filename-2.pdf`

**Example:** An image of a person in a privately owned kitchen — `risk.model_release_required = true` and `risk.property_release_required = true` — with a confirmed model release file named `model-release-jane-doe-2025-03.pdf` and a confirmed property release file named `property-release-brooklyn-loft-2025-03.pdf`. The `Releases` column value is:

```
model-release-jane-doe-2025-03.pdf,property-release-brooklyn-loft-2025-03.pdf
```

> **Note on release file naming.** The file names written to the `Releases` column must match exactly the file names used when uploading the release documents to the Adobe Stock contributor portal. AssetForge does not manage release file storage or naming; the names are provided as human-reviewer input during the Approval Requirements review step. See the PO-confirmed decision in story #85: the confirmation mechanism for release presence is out of scope and deferred to a separate design story.

### 3.2 State B — Release required but absent or unconfirmed

**Condition:** `risk.model_release_required = true` or `risk.property_release_required = true`, and no confirmed release record is available for the asset (either no release has been uploaded, or the human reviewer has not yet confirmed release presence).

**`Releases` column value:** Empty string (`""`).

**Export behaviour:** The Output Package must not be delivered. The asset is held in the Approval Requirements review queue pending human reviewer confirmation. See Section 4 for the full export handling policy.

**Note:** An empty `Releases` column value in the Adobe Stock CSV format signals to the Adobe Stock portal that no release documentation is attached. Submitting an asset in this state with `risk.model_release_required = true` or `risk.property_release_required = true` active would expose the submission to rejection by Adobe Stock. The export-blocking rule in Section 4 ensures the Output Package is never delivered in this state without human sign-off.

### 3.3 State C — Release not required

**Condition:** `risk.model_release_required` is absent or `false` on the CAR, and `risk.property_release_required` is absent or `false` on the CAR. No release flag is active.

**`Releases` column value:** Empty string (`""`).

**Export behaviour:** The Output Package may proceed to delivery without any release-related gating, subject to all other profile validation rules.

**Distinguishing State B from State C:** Both states produce an empty `Releases` column value. They are distinguished by the presence or absence of active risk flags on the CAR, not by the CSV column value itself. In State B, at least one release flag is `true` and the export-blocking rule in Section 4 applies. In State C, no release flag is active and no blocking applies. Downstream systems and human reviewers must read the CAR risk flag values — not only the CSV column value — to determine which state applies.

---

## 4. Export Handling Policy

### 4.1 Governing canonical term

The export handling policy for `risk.model_release_required` and `risk.property_release_required` in the `stock/adobe-stock` profile is:

**Require human review**

This is the domain default policy for both release flags, as established in `docs/confidence-and-risk-rules.md` Section 2.2. The `stock/adobe-stock` profile does not escalate this to `block output entirely`. The policy is applied as follows.

### 4.2 What `require human review` means for these flags

- **Automated generation may proceed.** The Content Generation Layer is permitted to generate titles, descriptions, and keywords for the asset. Generation is not blocked by the presence of an active release flag.
- **Delivery is blocked until review is complete.** The Output Package must not be delivered — exported as a CSV row, written to a file, or transmitted to any downstream system — until a human reviewer has recorded a release confirmation or an explicit override decision.
- **The asset is routed to the Approval Requirements review queue.** The Content Profile's Approval Requirements dimension governs the routing. The human reviewer receives the asset along with the review message specified in Section 4.3.
- **The `Releases` column is left empty in the held Output Package.** Until the reviewer records confirmation of a release file name, the column value is empty (State B in Section 3.2). On reviewer confirmation, the column value is updated to the release file name(s) (State A in Section 3.1) and the Output Package is released for delivery.

This policy is consistent with `docs/confidence-and-risk-rules.md` Section 2.2, row 1 (`risk.model_release_required`) and row 2 (`risk.property_release_required`), which both specify: "Automated generation may proceed; delivery is blocked until review is complete."

### 4.3 Reviewer messages

When an asset is routed to human review due to an active release flag, the following messages must be surfaced to the reviewer.

**When `risk.model_release_required = true` and no confirmed release is on file:**

> This asset contains one or more potentially identifiable persons. A signed model release is required for commercial distribution on Adobe Stock. Confirm that a valid model release is uploaded to the Adobe Stock contributor portal and provide the exact release file name(s). If no release is available, mark the asset as Editorial only or remove it from the Adobe Stock submission queue.

**When `risk.property_release_required = true` and no confirmed release is on file:**

> This asset contains recognisable private property. A signed property release is required for commercial distribution on Adobe Stock. Confirm that a valid property release is uploaded to the Adobe Stock contributor portal and provide the exact release file name(s). If no release is available, mark the asset as Editorial only or remove it from the Adobe Stock submission queue.

**When both `risk.model_release_required = true` and `risk.property_release_required = true` and no confirmed releases are on file:**

> This asset contains one or more potentially identifiable persons AND recognisable private property. Signed model and property releases are both required for commercial distribution on Adobe Stock. Confirm that valid release documents are uploaded to the Adobe Stock contributor portal and provide the exact release file name(s) for each. If releases are not available, mark the asset as Editorial only or remove it from the Adobe Stock submission queue.

### 4.4 Multiple-flag interaction

When `risk.model_release_required` or `risk.property_release_required` is active simultaneously with other risk flags, the most-restrictive-wins rule from `docs/confidence-and-risk-rules.md` Section 3.1 applies. In practice:

- If `risk.editorial_only = true` is also active, the governing policy escalates to `block output entirely` for commercial channel profiles (as specified in Section 5 of this document). The release flag policies in this section apply only to the editorial Output Package path, which does not require release confirmation.
- If `risk.trademark_flag = true` is also active alongside a release flag, `require human review` (from the release flag) governs the asset disposition. The trademark flag's default policy of `suppress output` for trademark-referencing fields continues to apply at the field level. Both policies are in force simultaneously; neither cancels the other.

---

## 5. Editorial Exemption

### 5.1 When `risk.editorial_only = true`

When the Asset Intelligence Layer sets `risk.editorial_only = true` on a CAR — because `activities.editorial_event_signal` is `true`, or because a public figure or real-world news event is detected — the `stock/adobe-stock` Content Profile applies the editorial classification path.

**Under the editorial path, model and property release requirements do not block Output Package generation for the editorial submission.** This is because:

1. An editorially classified Output Package does not assert that releases are present; it asserts instead that the intended licensing context — informational, journalistic, or documentary use — makes release clearance inapplicable (see `docs/commercial-editorial-classification.md` Section 1, Editorial Use definition).
2. Adobe Stock's editorial submission rules do not require model or property release documentation for assets submitted under the editorial licence type (see `docs/commercial-editorial-classification.md` Section 4, Adobe Stock platform mapping table).

The editorial exemption operates as follows: when `risk.editorial_only = true`, the Content Generation Layer must generate an editorial Output Package. The Approval Requirements for the editorial Output Package do not include a release confirmation step. The `Releases` column in the Adobe Stock CSV is left empty (State C semantics — release not required for this submission type).

### 5.2 Commercial Output Package from the same asset is still gated

The editorial exemption applies only to the editorial Output Package. If a human reviewer records an override of `risk.editorial_only` — explicitly reclassifying the asset as eligible for commercial submission — the commercial Output Package generated from the same CAR is subject to the full release rules in Sections 2, 3, and 4.

- `risk.model_release_required = true` on the CAR does not disappear because an editorial Output Package was generated first.
- Any commercial Output Package generated after an editorial override must still route through the Approval Requirements release confirmation step before delivery.
- The override of `risk.editorial_only` must not be treated as an implicit release confirmation. Each active release flag must be resolved independently.

### 5.3 Relationship to the classification decision sequence

The editorial exemption described in this section is consistent with Step 1 of the classification decision sequence in `docs/commercial-editorial-classification.md` Section 5:

> Check `risk.editorial_only`. If `true`, apply the editorial content profile rules. If the active Content Profile targets a commercial channel, block generation and route to Approval Requirements.

For the `stock/adobe-stock` profile, "apply the editorial content profile rules" at Step 1 means: proceed with editorial Output Package generation without requiring release confirmation. Steps 2 and 3 of the classification decision sequence — which check release flags — apply only when the commercial channel path is active.

---

## 6. Worked Example: Image of a Person at a Private Venue

**Asset:** A photograph of a professional chef — face visible, standing in a characteristically designed private restaurant kitchen — preparing a dish. A prominent logo is visible on the kitchen equipment.

**CAR signals:**
- `persons.present = true`
- `persons.faces_detected = true` → triggers model release trigger condition 1.1
- `location.setting_descriptor = "commercial kitchen"` (private venue) → triggers property release trigger condition 2.1
- `text.logo_marks_detected = ["KitchenBrand logo"]` → `risk.trademark_flag = true`
- `risk.editorial_only` — absent (no editorial event signal detected)

**Risk flags set:**
- `risk.model_release_required = true`
- `risk.property_release_required = true`
- `risk.trademark_flag = true`

**Multiple-flag interaction (most restrictive wins):** The active policies are `require human review` (model release), `require human review` (property release), and `suppress output` (trademark). Most restrictive: `require human review`. The asset is routed for human review.

**Export behaviour:** Automated generation proceeds. Delivery is blocked. The human reviewer receives the combined release reviewer message (Section 4.3). Trademark-referencing content fields are suppressed from generated output.

**`Releases` column value before review:** `""` (State B)

**`Releases` column value after review, if reviewer confirms both releases:** `"chef-model-release-2025-09.pdf,restaurant-property-release-2025-09.pdf"`

**`Releases` column value if reviewer reclassifies as editorial:** `""` (State C semantics under editorial exemption — Section 5)

---

## 7. Design Principle Alignment

These rules apply the AssetForge principle of **strict layer separation**: the Asset Intelligence Layer sets risk flags based on factual observations; the Content Generation Layer applies release-gating rules based on the active Content Profile; the Channel Adaptation Layer writes the `Releases` column value. No layer makes a release determination that belongs to another layer.

The `require human review` policy also applies the principle of **conservative defaults**: when in doubt, route to a human rather than automate a decision that carries legal or commercial consequences.
