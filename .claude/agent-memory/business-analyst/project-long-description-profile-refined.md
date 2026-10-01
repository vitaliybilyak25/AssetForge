---
name: Generic long description profile refined
description: Story #30 refined 2026-09-28 — general/long-description Content Profile, 11 ACs, ready label + board Status Ready
type: project
---

Story #30 ("Define generic long description profile") was refined on 2026-09-28.

Profile target: `profiles/general/long-description.yaml`
MVP: MVP3

Key decisions recorded in AC:
- `tone.register = descriptive`; `language.primary = en-US`; `output_format.type = filesystem_export`
- Length constraint: 2–5 sentences; 150–500 chars documented as guidance only (not a hard limit)
- Four ordered sentence slots: (1) primary subject + action, (2) setting/environment, (3) supporting elements, (4) mood/atmosphere (conditional)
- Absent CAR fields: sentence slot omitted entirely; no fabrication
- Forbidden: promotional adjectives, subjective quality claims, calls to action, brand names
- 4 validation rules: `long-desc-required`, `long-desc-min-sentences`, `long-desc-max-sentences`, `long-desc-no-promotional`
- 11 ACs covering all ten Content Profile schema dimensions plus examples and validation
- Open item: `module` field placeholder — PO to confirm which module owns general-purpose profiles

**Why:** Sprint 5 story; needed to establish the first generic Layer 2 description profile independent of any stock or social channel.

**How to apply:** When any future general-purpose description story references this profile, the sentence-slot ordering and CAR source mapping in AC3/AC5 are the authoritative generation rules.

Label `ready` added; board Status set to Ready (Project #3, item PVTI_lAHODHI90s4BklMlzg8m8fg).
Awaiting PO approval (ready checklist item 8).
