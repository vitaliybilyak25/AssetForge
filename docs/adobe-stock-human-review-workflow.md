# Adobe Stock — Human Review and Approval Workflow

**Document type:** Workflow Specification
**Profile:** `stock/adobe-stock`
**Layer scope:** Content Generation Layer (Layer 2) — routing, approval, and audit; Channel Adaptation Layer (Layer 3) — validator gate and Output Package delivery
**Status:** MVP2 — first business case specification
**Story:** #27
**Cross-references:** story #15 (`docs/canonical-asset-record.md`), story #24 (`docs/adobe-stock-output-spec.md`), story #26 (validator implementation), story #85 (`docs/adobe-stock-release-rules.md`), story #86 (`docs/commercial-editorial-classification.md`)

---

## Overview

This document formally specifies the human review and approval workflow for AI-generated Adobe Stock metadata produced by the `stock/adobe-stock` Content Profile. It defines the six workflow states, the three trigger conditions that route an asset to human review, all reviewer actions, constraints on those actions, audit log requirements for every state transition, and the validator gate that governs Output Package delivery.

The workflow sits between the Content Generation Layer (which produces titles, keywords, a category code, and a `Releases` column value) and the Channel Adaptation Layer (which serialises and validates the Output Package for delivery). It is the mechanism by which the platform's `require human review` and `block output entirely` handling policies are operationalised for the `stock/adobe-stock` profile.

---

## 1. Workflow States

Six states are defined. Every asset processed against the `stock/adobe-stock` profile occupies exactly one of these states at any point in time.

### 1.1 State Definitions

| State | Entry Condition | Exit Condition |
|---|---|---|
| `Generated` | The Content Generation Layer has produced metadata for the asset. No trigger condition (Section 2) is currently active on the CAR. | If a trigger condition fires: transitions to `Pending Review`. If no trigger condition is active and validators pass: transitions directly to `Exported`. |
| `Pending Review` | One or more trigger conditions (Section 2) are active on the CAR. The system routes the asset to the review queue. | Reviewer approves the asset (transitions to `Approved — Editorial` or `Approved — Commercial` depending on the approval path taken) or rejects the asset (transitions to `Rejected`). |
| `Approved — Editorial` | The reviewer has confirmed editorial submission. `risk.editorial_only` is active on the CAR and has not been overridden. | Validators (story #26) pass against the generated output; the Channel Adaptation Layer writes the Output Package (transitions to `Exported`). |
| `Approved — Commercial` | The reviewer has confirmed commercial submission. All active release flags (`risk.model_release_required`, `risk.property_release_required`) are resolved via confirmed release file names. Any prior editorial override has been explicitly recorded. | Validators (story #26) pass against the generated output; the Channel Adaptation Layer writes the Output Package (transitions to `Exported`). |
| `Rejected` | The reviewer has explicitly rejected the asset with a logged reason. | Terminal state. No Output Package is generated. No further transitions are possible. |
| `Exported` | The Output Package has been written to CSV and delivered at the outbound Integration Touch-point. All validators passed; reviewer approval was obtained or no trigger condition required review. | Terminal state. |

### 1.2 State-Transition Table

| From State | Trigger / Action | To State | Actor |
|---|---|---|---|
| `Generated` | One or more trigger conditions fire (Section 2) | `Pending Review` | System (automated routing) |
| `Generated` | No trigger condition active; validators pass | `Exported` | System (automated export) |
| `Pending Review` | Reviewer approves as editorial (`risk.editorial_only` not overridden) | `Approved — Editorial` | Reviewer |
| `Pending Review` | Reviewer approves as commercial (all release flags resolved; editorial override recorded if applicable) | `Approved — Commercial` | Reviewer |
| `Pending Review` | Reviewer rejects with logged reason | `Rejected` | Reviewer |
| `Approved — Editorial` | Validators pass; Output Package written | `Exported` | System (Channel Adaptation Layer) |
| `Approved — Editorial` | Validator failure | Returns to `Pending Review` with validator failure flagged | System |
| `Approved — Commercial` | Validators pass; Output Package written | `Exported` | System (Channel Adaptation Layer) |
| `Approved — Commercial` | Validator failure | Returns to `Pending Review` with validator failure flagged | System |

> **Note:** `Rejected` and `Exported` are terminal. No transition out of either state is permitted.

---

## 2. Trigger Conditions for Human Review

An asset transitions from `Generated` to `Pending Review` when any of the following conditions is detected on the CAR. Trigger conditions are evaluated after content generation is complete and before any export path is attempted.

Multiple triggers may be active simultaneously. Each trigger must be resolved independently; resolving one trigger does not clear others.

### Trigger 1 — Release required, absent (State B)

**Condition:** `risk.model_release_required = true` or `risk.property_release_required = true` on the CAR, and no confirmed release record is on file for the asset.

**Effect:** The asset is routed to the review queue pending release confirmation. The `Releases` CSV column holds an empty string (State B semantics) until the reviewer provides confirmed release file names. The Output Package must not be delivered while this trigger is unresolved.

**Source:** `docs/adobe-stock-release-rules.md` Sections 3.2 and 4.

### Trigger 2 — Editorial classification

**Condition:** `risk.editorial_only = true` on the CAR.

**Effect:** The asset is routed for editorial review. The reviewer may confirm editorial submission (transitions to `Approved — Editorial`) or override the classification and approve commercial submission (transitions to `Approved — Commercial`, at which point full release rules apply — see Section 3.2).

**Source:** `docs/commercial-editorial-classification.md` Section 2; `docs/adobe-stock-release-rules.md` Section 5.2.

### Trigger 3 — Risk content

**Condition:** `risk.adult_content = true` or `risk.violence_flag = true` on the CAR.

**Effect:** The asset is held in the review queue. No automated export path exists for these flags. A reviewer must evaluate the asset before any Output Package is generated. Reviewer approval for an asset with these flags active requires a secondary approval step: the override must be explicitly logged with the approving actor's identity and a mandatory comment (see Section 4.3).

---

## 3. Reviewer Actions

The following actions are available to a reviewer when an asset is in the `Pending Review` state. Each action must be recorded in the audit log (Section 4).

### 3.1 Release Confirmation

**Description:** The reviewer records the exact file name or names of the release document(s) that have been uploaded to the Adobe Stock contributor portal for this asset.

**What the reviewer provides:** The exact file name(s) matching the names used at upload to the Adobe Stock contributor portal. If multiple release documents are on file (for example, a model release and a property release, or releases for multiple identifiable persons), all file names are recorded as a comma-separated list.

**Effect on the `Releases` CSV column:** The confirmed file name(s) are written verbatim to the `Releases` column in the Output Package. This is State A behaviour as defined in `docs/adobe-stock-output-spec.md` Section 5 and `docs/adobe-stock-release-rules.md` Section 3.1.

**Effect on workflow state:** Release confirmation resolves Trigger 1 (State B) for the confirmed release type. If all active release triggers are now resolved and no other unresolved triggers remain, the asset may proceed toward `Approved — Commercial`. Release confirmation is a prerequisite for `Approved — Commercial`; it is not required for `Approved — Editorial`.

**Scope limitation:** Release confirmation does not modify the CAR. The reviewer records file names against the Output Package record only. The `risk.model_release_required` and `risk.property_release_required` flags on the CAR are unchanged.

**Source:** `docs/adobe-stock-release-rules.md` Section 3.1.

> **Note on confirmation mechanism:** This specification defines what the reviewer must record (release file name(s)). The mechanism by which the reviewer inputs and the system persists this confirmation is deferred to a separate design story, per the note in `docs/adobe-stock-release-rules.md` Section 3.1.

### 3.2 Editorial Override

**Description:** The reviewer explicitly reclassifies an asset from editorial to commercial, overriding `risk.editorial_only` on the CAR for the purpose of this submission.

**Conditions for use:** Available only when `risk.editorial_only = true` is the active trigger. The override must be explicitly recorded; it does not happen implicitly.

**Effect on workflow state:** The override allows the asset to be assessed for commercial submission. It does not advance the asset to `Approved — Commercial` on its own; all remaining triggers must still be resolved:

- If `risk.model_release_required = true` or `risk.property_release_required = true` are active on the CAR, these flags must each be resolved via release confirmation (Section 3.1) before `Approved — Commercial` is reached.
- The override does not constitute implicit release confirmation. Each active release flag must be resolved independently.

**Scope limitation:** The editorial override does not modify the CAR. `risk.editorial_only` remains `true` on the CAR record. The override is recorded as a decision against the Output Package, not as a change to the source data. This is consistent with the immutability rule in `docs/canonical-asset-record.md` Section 2.

**Source:** `docs/adobe-stock-release-rules.md` Section 5.2.

### 3.3 Content Edit

**Description:** The reviewer may edit generated content fields before approving.

**Editable fields:** Title, Keywords, and Category only.

**Non-editable fields:** `Filename`, CAR fields, risk flags, and any field not listed above. In particular, the reviewer may not modify `risk.editorial_only`, `risk.model_release_required`, `risk.property_release_required`, `risk.adult_content`, or `risk.violence_flag` on the CAR.

**Re-validation requirement:** Any edit to Title, Keywords, or Category requires validators (story #26) to be re-run before approval is permitted. The reviewer may not approve the asset while edited fields remain unvalidated.

**Source:** Issue #27 Scope and Acceptance Criteria AC5.

### 3.4 Rejection

**Description:** The reviewer explicitly rejects the asset. Rejection is available from the `Pending Review` state at any point.

**Requirements:** Rejection must be accompanied by a logged reason. The reason is mandatory and must be recorded in the audit log (Section 4).

**Effect:** The asset transitions to `Rejected`. The `Rejected` state is terminal: no Output Package is generated, no CSV row is produced, and no further state transitions are possible.

---

## 4. Constraints on Reviewer Actions

### 4.1 CAR Immutability

Reviewer actions must not modify the Canonical Asset Record. The CAR is immutable after production by the Asset Intelligence Layer (Layer 1). This rule is defined in `docs/canonical-asset-record.md` Section 2 (Immutability Rule).

All reviewer changes — content edits to Title, Keywords, and Category; release file name confirmations; editorial overrides; rejections — are recorded against the Output Package record, not against the CAR. The CAR that Layer 1 produced remains unchanged throughout the review process and after export.

If a reviewer identifies an error in the CAR (for example, an incorrect risk flag), the correct resolution is to reject the asset and request re-processing through the Asset Intelligence Layer, not to edit the CAR in place.

### 4.2 Risk Content Override Requirement

A reviewer may not approve commercial or editorial submission for an asset with `risk.adult_content = true` or `risk.violence_flag = true` without a secondary approval step. Any override of these flags must be:

- Explicitly recorded in the audit log (Section 5).
- Logged with the approving actor's identity.
- Accompanied by a mandatory comment explaining the basis for the override.

The secondary approval step is a logging and accountability requirement. The policy governing who may perform secondary approval and what the escalation path is falls outside the scope of this specification (see Section 7, Risks).

### 4.3 Validator Gate

Validators (story #26) must pass before the Output Package may be written or delivered. This gate applies regardless of reviewer approval state. Reviewer approval and validator pass are independent and both required:

- An asset that a reviewer has approved but that fails validators may not be exported.
- An asset for which validators pass but that a reviewer has not yet approved (where review is required) may not be exported.
- Both conditions must be satisfied before the Channel Adaptation Layer writes the Output Package.

This is consistent with `docs/adobe-stock-output-spec.md` which specifies all validation rule IDs that govern the five CSV columns.

---

## 5. Audit Log Requirements

Every state transition must be recorded with the following fields:

| Field | Required | Notes |
|---|---|---|
| Actor identifier | Always | The reviewer's user ID for reviewer-initiated transitions; a system actor identifier for automated transitions (e.g., routing, validator pass). |
| Timestamp (UTC) | Always | ISO 8601 format. |
| Previous state | Always | The state name as defined in Section 1. |
| New state | Always | The state name as defined in Section 1. |
| Reviewer comment | Conditional — see below | Optional for system-initiated transitions; mandatory for Rejection; mandatory for any `risk.adult_content` or `risk.violence_flag` override (see Section 4.2). |

### 5.1 Mandatory Comment Scenarios

A reviewer comment is mandatory (not optional) in the following scenarios:

1. **Rejection:** The comment must state the reason for rejection.
2. **`risk.adult_content` override:** The comment must identify the approving actor and state the basis for overriding the flag.
3. **`risk.violence_flag` override:** Same requirement as adult content override.

### 5.2 Release File Name Persistence

Confirmed release document file names recorded by a reviewer (Section 3.1) must be persisted and traceable to the specific Output Package in which they appear. The audit record for the release confirmation transition must include the file name(s) confirmed. This ensures that the connection between a specific reviewer's confirmation and the `Releases` column value in the delivered CSV row is auditable after delivery.

---

## 6. Consistency with Referenced Specifications

### 6.1 `Releases` Column Three-State Behaviour

The trigger conditions and reviewer actions in this workflow are consistent with the three-state `Releases` column behaviour defined in `docs/adobe-stock-output-spec.md` Section 5 and `docs/adobe-stock-release-rules.md` Section 3:

| State | Condition | `Releases` column value | Export behaviour | Workflow state |
|---|---|---|---|---|
| **A — Release confirmed present** | Release flag(s) `true`; reviewer has confirmed release file name(s) | Reviewer-confirmed file name(s), comma-separated | Output Package may proceed | Reviewer has completed release confirmation; asset may reach `Approved — Commercial` |
| **B — Release required, absent** | Release flag(s) `true`; no confirmed release on file | `""` (empty string) | Output Package must not be delivered | Asset is in `Pending Review` — Trigger 1 is unresolved |
| **C — Release not required** | No release flags active on CAR | `""` (empty string) | Output Package may proceed | No release trigger; asset may reach `Generated` → `Exported` directly or `Approved — Editorial` |

Both State B and State C produce an empty `Releases` column value. They are distinguished by CAR risk flag values, not by the column value alone. Downstream systems must read the CAR to determine which state applies, per `docs/adobe-stock-output-spec.md` Section 5.

### 6.2 Editorial Exemption

When `risk.editorial_only = true`, the editorial exemption from `docs/adobe-stock-release-rules.md` Section 5.1 applies: model and property release requirements do not block Output Package generation for the editorial submission. The `Releases` column is left empty (State C semantics) in the editorial Output Package.

If a reviewer subsequently overrides `risk.editorial_only` and a commercial Output Package is generated from the same CAR, the full release rules from `docs/adobe-stock-release-rules.md` Sections 3 and 4 apply to that commercial Output Package. The editorial override does not carry over.

### 6.3 `risk.editorial_only` Semantics

The workflow's Trigger 2 and editorial override action are consistent with the `risk.editorial_only` semantics defined in `docs/commercial-editorial-classification.md` Section 2: `risk.editorial_only = true` is the single most authoritative classification signal; it cannot be overridden automatically; it requires human review resolution in all cases.

### 6.4 CAR Immutability

The constraint in Section 4.1 of this document is directly derived from the Immutability Rule in `docs/canonical-asset-record.md` Section 2: "The CAR is immutable after production. No layer, process, or actor may modify the Canonical Asset Record once the Asset Intelligence Layer has produced it."

---

## 7. Out of Scope

The following topics are referenced by this workflow specification but are explicitly excluded from its scope:

- **UI design or screen layouts** for the review interface — deferred to MVP4, story #35.
- **Validator implementation** — specified in story #26; this document references validator rule IDs but does not implement them.
- **Release document storage or file management** — deferred per `docs/adobe-stock-release-rules.md` Section 3.1 note. This workflow defines what the reviewer must record (release file names); the storage and confirmation mechanism is a separate design story.
- **Batch review workflows** — deferred to MVP5.
- **Secondary approval escalation policy** for `risk.adult_content` and `risk.violence_flag` overrides — this workflow specifies the logging requirement (mandatory comment with actor identity); the full escalation policy (who may perform secondary approval) is out of scope for this story.

---

## 8. Dependencies

| Dependency | Document | What it provides |
|---|---|---|
| Story #15 | `docs/canonical-asset-record.md` | CAR immutability rule (Section 2); Risk Flags category definition (Section 3) |
| Story #26 | Validator implementation | Validator rule IDs that the validator gate in Section 4.3 references |
| Story #85 | `docs/adobe-stock-release-rules.md` | Three-state release behaviour; export handling policy (Section 4); editorial exemption (Section 5) |
| Story #24 | `docs/adobe-stock-output-spec.md` | `Releases` column three-state behaviour (Section 5); all CSV column validation rule IDs |
| Story #86 | `docs/commercial-editorial-classification.md` | `risk.editorial_only` semantics (Section 2); classification decision sequence (Section 5) |
