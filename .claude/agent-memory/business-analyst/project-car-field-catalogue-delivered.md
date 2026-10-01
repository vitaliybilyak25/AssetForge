---
name: CAR Field Catalogue delivered (story #78)
description: Story #78 complete — CAR field catalogue at docs/car-field-catalogue.md, Epic #1 updated, comment on GH issue #78, awaiting PO approval
type: project
---

Story #78 (Draft Canonical Asset Record field catalogue) delivered on 2026-09-26.

**Why:** MVP0 requires a field-level complement to the CAR concept document (#15) so that MVP1 implementation has named fields, data types, and cardinality to work from.

**How to apply:** Treat docs/car-field-catalogue.md as the authoritative field-level spec for the CAR from this point. Any future story referencing individual CAR field names should align with the dot-notation names defined there (e.g., `objects.detected_subjects`, `persons.count`, `risk.model_release_required`). Confidence score threshold values are deferred to story #84.

Deliverables:
- docs/car-field-catalogue.md — Draft v0.1 with 7 categories, 3–7 fields each, Required/Conditional cardinality, conditions stated for all conditional fields
- Epic #1 body updated — CAR Field Catalogue entry added to Reference section
- GH issue #78 comment posted confirming delivery and requesting PO review
- Issue #78 left open per instruction
