---
name: Story #27 — Human Review Workflow Refined
description: Issue #27 refined 2026-09-28 — 6 workflow states, 3 triggers, 10 ACs, CAR immutability constraint, validator gate; ready label + board Status Ready
type: project
---

Story #27 ("Define human review and approval workflow for Adobe Stock metadata") refined on 2026-09-28 for Sprint 5.

**What changed:** Replaced 4 skeleton ACs with 10 concrete ACs grounded in existing spec documents. Replaced invented states (Draft, Pending Review, Approved, Rejected, Exported) with the 6 correct states (Generated, Pending Review, Approved — Editorial, Approved — Commercial, Rejected, Exported) derived from CAR risk flags and release rules. Added full trigger condition table (3 triggers: release absent, editorial_only, adult/violence). Defined reviewer action scope (release confirmation, editorial override, content edit, rejection). Documented CAR immutability constraint and validator gate as hard requirements. Added audit log field spec.

**Why:** Skeleton states were not aligned with the three-state Releases column behaviour (docs/adobe-stock-output-spec.md Section 5), the export handling policy (docs/adobe-stock-release-rules.md Section 4), or the editorial exemption path (docs/adobe-stock-release-rules.md Section 5). All 10 ACs now reference specific rule IDs or document sections.

**Status:** ready label applied; board Status set to Ready; awaiting PO approval (AC8 on the ready checklist).

**Dependencies confirmed:** stories #15, #24, #26, #85, #86.

**Story points:** 5 (medium — multiple cross-referenced specs, conditional state logic, audit requirements).
