# End-to-End Asset Processing Data Flow

**Part of:** [Epic #1 — MVP0 Product Vision and Domain Model](https://github.com/vitaliybilyak25/AssetForge/issues/1)

**Cross-reference:** [Boundary Contracts](boundary-contracts.md) (story #77) — the artifact contracts, handoff validity conditions, and prohibited responsibilities referenced throughout this document are defined there. All terms are defined in the [AssetForge Domain Glossary](glossary.md).

---

## Purpose

This document specifies the runtime sequence of operations for a single asset processing run. It covers the happy-path flow from asset upload to a delivered Output Package, the named artifacts that cross each layer boundary, the actor (user or system) that triggers each step, and three error paths with their recovery or termination outcomes.

This document is a design-level reference for MVP1 implementers. It does not specify technology choices (queues, databases, containers) or non-functional flows (authentication, billing, observability) — those are out of scope until MVP1 and MVP12 respectively.

---

## Actors

| Actor | Description |
|---|---|
| User | The human submitting the asset and selecting the Content Profile |
| System | The AssetForge platform acting autonomously in response to the preceding step |

---

## Artifacts at Each Boundary

| Boundary | Artifact | Direction |
|---|---|---|
| Platform inbound | Asset (file) + Profile Identifier | User to Platform |
| L1 output / L2 input | Canonical Asset Record (CAR) | Asset Intelligence Layer to Content Generation Layer |
| L2 also requires | Resolved Content Profile | Platform (profile store) to Content Generation Layer |
| L2 output / L3 input | Generated Content | Content Generation Layer to Channel Adaptation Layer |
| L3 also requires | Output Format spec + Validation Rules (from Resolved Content Profile) | Platform (profile store) to Channel Adaptation Layer |
| Platform outbound | Output Package | Channel Adaptation Layer to User |

---

## Happy Path

### Overview

```
User                  Platform
 |                       |
 |-- (1) Submit -------->|
 |   Asset + Profile ID  |
 |                       |-- (2) Validate input
 |                       |
 |                       |-- (3) Asset Intelligence Layer
 |                       |       analyses raw Asset
 |                       |       [produces CAR]
 |                       |
 |                       |-- (4) Resolve Content Profile
 |                       |       (from Profile Identifier)
 |                       |
 |                       |-- (5) Content Generation Layer
 |                       |       reads CAR + Resolved Profile
 |                       |       [produces Generated Content]
 |                       |
 |                       |-- (6) Channel Adaptation Layer
 |                       |       reads Generated Content +
 |                       |       Output Format + Validation Rules
 |                       |       [produces Output Package]
 |                       |
 |<-- (7) Deliver --------|
     Output Package
```

---

### Step-by-Step Sequence

**Step 1 — Asset and Profile Identifier submitted**

- Actor: User
- Trigger: User uploads an Asset file and supplies a Profile Identifier (e.g., `stock/adobe-stock`) via the platform's inbound Integration Touch-point.
- Input artifacts: raw Asset file, Profile Identifier string.
- Output: submission is accepted by the platform for processing.

---

**Step 2 — Input validation**

- Actor: System
- Trigger: System event; fires immediately on receipt of the submission.
- What the system checks:
  - Asset file is present and is a recognised Asset Type (photo, video, or vector within the MVP scope).
  - Profile Identifier is a non-empty string.
- Output: submission is queued for Layer 1 processing, or — if validation fails — error path E2 is entered (see Error Paths section).

---

**Step 3 — Asset Intelligence Layer produces the Canonical Asset Record**

- Actor: System
- Trigger: System event; fires when the Asset passes input validation.
- What the layer does: analyses the raw Asset without any knowledge of the intended channel. Detects and records observations across seven categories: Objects and Subjects, People, Locations, Text and Logos, Activities, Risk Flags, and Confidence Scores. Records a Confidence Score for every non-absent observation. Propagates all Risk Flags regardless of confidence level. Seals the CAR as immutable.
- Input artifact: raw Asset file (Profile Identifier is passed through as a token; Layer 1 does not read it).
- Output artifact: Canonical Asset Record (CAR) — sealed, channel-agnostic, containing no titles, descriptions, or keyword lists.
- Handoff validity check (system): the system confirms the CAR satisfies all six conditions in Handoff 1 of the Boundary Contracts before passing it to Layer 2. If any condition fails — for example `risk.flags_evaluated` is false — the Handoff is invalid and error path E1 is entered (see Error Paths section).

---

**Step 4 — Content Profile resolved**

- Actor: System
- Trigger: System event; fires in parallel with or immediately after Step 3 completes.
- What the system does: uses the Profile Identifier to look up and retrieve the full Content Profile object from the platform's profile store.
- Input artifact: Profile Identifier string.
- Output artifact: Resolved Content Profile — the complete ten-dimension Content Profile object (Audience, Tone, Required and Optional Fields, Length Limits, Keyword Rules, Forbidden Content, Language, Output Format, Validation Rules, Approval Requirements).
- If the Profile Identifier is not found or the retrieved Content Profile is structurally invalid, error path E3 is entered (see Error Paths section).

---

**Step 5 — Content Generation Layer produces Generated Content**

- Actor: System
- Trigger: System event; fires when both the CAR (Step 3) and the Resolved Content Profile (Step 4) are available.
- What the layer does: reads the CAR's factual observations and applies the Content Profile's generation rules to produce human-readable text fields. Applies Length Limits, Keyword Rules, Forbidden Content, Language, and Audience/Tone guidance. Checks each required CAR field against the Content Profile's minimum Confidence Score threshold; fields below threshold are treated as unknown and are not used as the basis for generated content (CAR Consumer Rules 1–3). Surfaces any Risk Flags found in the CAR to the Approval Requirements logic.
- Input artifacts: Canonical Asset Record, Resolved Content Profile.
- Output artifact: Generated Content — a set of plain-text fields (Title, Description, Keywords, Caption where required) conforming to the active Content Profile's rules. No CSV structure, IPTC tags, or JSON keys are applied at this step.
- If a required field cannot be generated because the underlying CAR observation is absent or below the confidence threshold, the system enters error path E1 (see Error Paths section).
- If the Content Profile's Approval Requirements dimension specifies that this asset requires human review (e.g., due to a model release Risk Flag), the Generated Content is flagged as pending human approval before the Output Package is finalised. The flow continues to Step 6; the Output Package is held until the human review step is complete.

---

**Step 6 — Channel Adaptation Layer produces the Output Package**

- Actor: System
- Trigger: System event; fires when Generated Content passes the Handoff 2 validity check.
- What the layer does: reads the Generated Content alongside the Output Format and Validation Rules dimensions from the Resolved Content Profile. Validates every generated field against the Validation Rules (field presence, character limits, keyword count range, forbidden-term scan). Formats the validated fields into the Output Format specified by the profile (e.g., CSV rows, JSON structure, IPTC/XMP serialisation). Preserves the human review flag if set in Step 5.
- Input artifacts: Generated Content, Output Format spec and Validation Rules (from the Resolved Content Profile).
- Output artifact: Output Package — a complete, channel-ready, formatted, and validated metadata artifact.
- If any Validation Rule check fails, error path E4 is entered (see Error Paths section).

---

**Step 7 — Output Package delivered**

- Actor: System
- Trigger: System event; fires when the Output Package is complete and either (a) no human review is required, or (b) human review has been completed and approved.
- What the system does: returns the Output Package to the User at the outbound Integration Touch-point.
- Output artifact: Output Package — the only artifact exposed at an external Integration Touch-point.

---

## Error Paths

### E1 — Low-Confidence CAR Field Required by the Active Content Profile

**Where it can occur:** Step 3 (Handoff 1 validity check) or Step 5 (Content Generation Layer reading CAR fields).

**Trigger:** System. The system applies CAR Consumer Rule 2: a CAR field required by the active Content Profile has a Confidence Score below the profile's minimum threshold, or the field is absent entirely.

**Sequence:**

```
Step 3 / Step 5
     |
     |-- System detects: required CAR field is absent
     |   or below confidence threshold
     |
     +-- Field is a Risk Flag?
     |       Yes --> Risk Flag is propagated regardless
     |               (CAR Consumer Rule 4). Flow continues.
     |
     +-- Field is content-bearing (e.g., primary_subject,
         persons.age_range_signals, location.setting_descriptor)?
             |
             +-- Content Profile has a fallback or
             |   optional alternative for this field?
             |       Yes --> System skips the field;
             |               Content Generation Layer
             |               generates output without it.
             |               Flow continues to Step 6.
             |
             +-- Field is required with no fallback?
                     Yes --> System flags the processing
                             run as incomplete.
                             Output: Processing halted.
                             User is notified that the
                             Output Package cannot be
                             generated for this profile
                             without sufficient confidence
                             in the missing field.
                             Recovery: User may re-submit
                             the Asset with a higher-
                             quality source file, or
                             select a different Content
                             Profile whose rules do not
                             require the low-confidence
                             field.
```

**Termination outcome:** Processing halts; no Output Package is produced. The User receives a notification identifying which field(s) fell below threshold and what options are available.

---

### E2 — Asset Submission Fails Input Validation

**Where it occurs:** Step 2 (Input validation).

**Trigger:** System. The submitted Asset file is missing, is an unrecognised file type, or the Profile Identifier is absent.

**Sequence:**

```
Step 2
     |
     |-- System checks: Asset file present?
     |   No  --> Reject submission immediately.
     |
     |-- System checks: Asset Type recognised?
     |   No  --> Reject submission.
     |
     |-- System checks: Profile Identifier present?
         No  --> Reject submission.
         |
         v
     Processing does not begin.
     User is notified with a specific reason:
       - "No asset file received."
       - "File type not supported. Supported types: [list]."
       - "Profile Identifier is required."
     Recovery: User corrects the submission and
               re-submits. No platform state is
               modified by the failed attempt.
```

**Termination outcome:** Submission rejected before any layer processing begins. No CAR is produced, no Content Profile is resolved, no Generated Content is created, and no Output Package is returned.

---

### E3 — Profile Identifier Not Found or Invalid Profile

**Where it occurs:** Step 4 (Content Profile resolution).

**Trigger:** System. The Profile Identifier supplied by the User does not match any registered Content Profile in the platform's profile store, or the retrieved profile is structurally invalid (missing a Required field in the Content Profile Schema).

**Sequence:**

```
Step 4
     |
     |-- System looks up Profile Identifier
     |   in the profile store.
     |
     +-- Profile Identifier not found?
     |       Yes --> Halt processing.
     |               User is notified:
     |               "Profile '<identifier>' not found.
     |               Available profiles: [list]."
     |               Recovery: User re-submits with a
     |               valid Profile Identifier.
     |
     +-- Profile retrieved but structurally invalid?
             Yes --> Halt processing.
                     Platform operator is notified of
                     the invalid profile definition.
                     User is notified that the selected
                     profile is temporarily unavailable.
                     Recovery: Platform operator corrects
                     the Content Profile definition.
                     User re-submits once the profile
                     is restored to a valid state.
```

Note: the CAR produced in Step 3 may already be complete when this error is detected. The CAR is not discarded — it is retained so that if the User re-submits with a valid Profile Identifier the Asset Intelligence Layer does not need to re-process the same Asset (this is a platform optimisation; the re-processing policy is an MVP1 decision).

**Termination outcome:** Processing halts after Step 3; no Generated Content is produced and no Output Package is returned.

---

### E4 — Validation Failure in Channel Adaptation Layer

**Where it occurs:** Step 6 (Channel Adaptation Layer validation pass).

**Trigger:** System. The Generated Content received from Step 5 fails one or more of the Validation Rules specified in the active Content Profile.

**Sequence:**

```
Step 6
     |
     |-- Channel Adaptation Layer runs
     |   Validation Rules against
     |   Generated Content.
     |
     +-- All rules pass?
     |       Yes --> Continue to Output Package
     |               assembly and Step 7.
     |
     +-- One or more rules fail?
             Yes --> System records which rules
                     failed (e.g., keyword count
                     below minimum, required field
                     empty, forbidden term detected).
                     |
                     +-- Failure is recoverable
                     |   by the platform
                     |   (e.g., keyword count is
                     |   slightly below minimum)?
                     |       Yes --> System routes
                     |               the run back
                     |               to Layer 2 for
                     |               a targeted
                     |               regeneration
                     |               of the failing
                     |               field only.
                     |               One retry is
                     |               permitted before
                     |               the run is
                     |               escalated.
                     |
                     +-- Failure is unrecoverable
                         (e.g., required CAR data
                         is absent and cannot yield
                         a valid field)?
                             Yes --> Halt processing.
                                     User is notified
                                     with the specific
                                     validation failure
                                     reason.
                                     Recovery: User
                                     reviews the Asset
                                     and Profile
                                     combination and
                                     re-submits with
                                     a corrected Asset
                                     or a different
                                     Content Profile.
```

**Termination outcome (unrecoverable):** No Output Package is produced. The User receives a validation failure report identifying which rule(s) failed and which field(s) are affected.

---

## Summary: Step Ownership and Artifacts

| Step | Actor | Input Artifacts | Output Artifact |
|---|---|---|---|
| 1. Submit Asset + Profile ID | User | Asset file, Profile Identifier | Submission accepted |
| 2. Input validation | System | Submission | Validated submission (or E2 rejection) |
| 3. Asset Intelligence Layer | System | Raw Asset | Canonical Asset Record (CAR) |
| 4. Resolve Content Profile | System | Profile Identifier | Resolved Content Profile |
| 5. Content Generation Layer | System | CAR + Resolved Content Profile | Generated Content |
| 6. Channel Adaptation Layer | System | Generated Content + Output Format + Validation Rules | Output Package |
| 7. Deliver Output Package | System | Output Package | Output Package at outbound Integration Touch-point |

---

## Error Path Summary

| Error | Detected at Step | Trigger | Outcome |
|---|---|---|---|
| E1: Low-confidence required CAR field | 3 or 5 | System | Halt; user notified of missing confidence; re-submit or switch profile |
| E2: Invalid submission (missing asset or profile ID) | 2 | System | Reject before processing begins; no state modified |
| E3: Profile Identifier not found or invalid | 4 | System | Halt after L1; CAR retained; user notified; operator corrects profile |
| E4: Validation failure in Channel Adaptation Layer | 6 | System | One Layer 2 retry if recoverable; otherwise halt and notify user |

---

## Out of Scope

The following are intentionally excluded from this document:

- Technology and infrastructure choices: queues, databases, containers, or runtime environments — these are MVP1 decisions.
- Non-functional flows: authentication, billing, observability, rate limiting — these are MVP12 concerns.
- Batch processing: applying one or more Content Profiles to multiple Assets in a single run — this is MVP5 scope.
- Human review workflow detail: the human review step triggered by Approval Requirements is noted at Step 5 and Step 7 but its UI and workflow are MVP4 scope.
- Re-processing logic for updated CAR models: the decision on whether to re-process a cached CAR when the Asset Intelligence Layer model version changes is an MVP1 decision.
