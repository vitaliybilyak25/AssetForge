---
name: Commercial vs Editorial Classification — story #86 delivered
description: Story #86 complete — commercial/editorial classification concept at docs/commercial-editorial-classification.md, glossary updated, Epic #1 updated, comment on GH issue #86, awaiting PO approval
type: project
---

Story #86 delivered on 2026-09-27.

**Why:** Every stock profile needs to reference commercial/editorial classification; the concept must live in the domain model, not inside any single profile.

**Deliverables:**
- `docs/commercial-editorial-classification.md` — domain definitions, CAR field signals (primary: `risk.editorial_only`; supporting: 6 fields), Content Profile override rules, platform mappings for Adobe Stock and Shutterstock, decision sequence
- `docs/glossary.md` — Commercial Use (## C) and Editorial Use (## E) stubs replaced with complete authoritative definitions cross-referencing the new document and named CAR fields
- GitHub issue #86 comment confirming delivery
- Epic #1 body updated with reference to `docs/commercial-editorial-classification.md`

**How to apply:** When authoring the `stock/adobe-stock` or `stock/shutterstock` Content Profile (MVP2, MVP6), reference this document for the classification gate rules that must appear in the Validation Rules and Approval Requirements dimensions.
