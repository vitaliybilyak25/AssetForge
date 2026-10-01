---
name: CAR concept document delivered (story #15)
description: Story #15 complete — CAR concept definition at docs/canonical-asset-record.md, Epic #1 updated, comments on GH issues #15 and #78, awaiting PO approval
type: project
---

Story #15 (Define the Canonical Asset Record concept) is complete as of 2026-09-26.

Deliverable: `/Users/Vitaliy_Bilyak/Projects/AssetForge/docs/canonical-asset-record.md`

Document structure:
1. Purpose — the question the CAR answers (observable facts) and explicitly does NOT answer (channel-specific content)
2. Position in the Architecture — Layer 1 produces it, Layer 2 consumes it, immutability rule: never modified after production
3. Information Categories — seven categories: objects/subjects, people, locations, text/logos, activities, risk flags, confidence scores
4. Consumer Rules — four binding rules covering absent fields, below-threshold fields, prohibition on inference, and mandatory propagation of risk flags
5. Relationship to the Field Catalogue — forward reference to story #78 as the implementation-level complement

Post-delivery actions completed:
- Epic #1 Reference section updated with CAR document link (https://github.com/vitaliybilyak25/AssetForge/issues/1)
- Comment posted on issue #78 (field catalogue cross-reference): https://github.com/vitaliybilyak25/AssetForge/issues/78#issuecomment-5849650347
- Comment posted on issue #15 (delivery notification): https://github.com/vitaliybilyak25/AssetForge/issues/15#issuecomment-5849650494

Issue #15 remains open; PO approval required before closing.

**Why:** MVP0 requires the CAR concept to be formally defined before MVP1 (field catalogue) can begin. The immutability rule and the seven categories are the architectural commitments that story #78 must honour.

**How to apply:** When working on story #78, treat the seven categories in canonical-asset-record.md as the mandatory organising structure. Any field in the Field Catalogue must trace to one of those seven categories.
