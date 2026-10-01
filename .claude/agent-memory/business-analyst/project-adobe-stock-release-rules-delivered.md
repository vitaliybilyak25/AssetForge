---
name: Adobe Stock release rules delivered
description: Story #85 complete — model/property release trigger conditions, Releases column spec, export policy, editorial exemption at docs/adobe-stock-release-rules.md
type: project
---

Story #85 "Define model and property release requirements for Adobe Stock" delivered on 2026-09-27.

Deliverable: `docs/adobe-stock-release-rules.md`

**Why:** First Adobe Stock-specific content rule document needed before the `stock/adobe-stock` Content Profile can be authored (MVP2). Depends on story #78 (CAR Field Catalogue), #84 (confidence/risk rules), and #86 (commercial/editorial classification) — all resolved.

**How to apply:** Reference this file when authoring the `stock/adobe-stock` Content Profile (story deferred to MVP2). The `Releases` column format, the `require human review` export policy, and the editorial exemption path defined here are load-bearing for the Channel Adaptation Layer CSV generation logic.

Key decisions recorded in the document:
- `Releases` column: exact portal file names, comma-separated if multiple, empty string if not required
- Export blocking: `require human review` (not escalated to `block output entirely`)
- Confirmation mechanism: out of scope, deferred to a separate design story
- Three specific reviewer messages defined (model only, property only, both)
- Editorial exemption: `risk.editorial_only = true` removes release gating for editorial Output Package only; commercial path remains fully gated

One open item for PO: AC3 Releases column format to be verified against live Adobe Stock contributor portal before approving the cut.

Epic #1 updated with reference. Comment posted on GH issue #85. Awaiting PO approval.
