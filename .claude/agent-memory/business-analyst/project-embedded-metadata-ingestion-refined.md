---
name: Embedded metadata ingestion story #87 delivered
description: Story #87 specification delivered at docs/embedded-metadata-ingestion.md — awaiting PO approval (AC6)
type: project
---

Story #87 "Ingest existing embedded metadata (EXIF, IPTC, XMP) into the Canonical Asset Record" specification was delivered on 2026-09-27.

**Deliverable:** `docs/embedded-metadata-ingestion.md` — EXIF/IPTC/XMP ingestion mapping, precedence rules, exclusions, absent metadata handling, conflict logging rule, and 8 new field placeholders.

**PO decisions applied:**
1. Rights fields (`rights.creator`, `rights.copyright_notice`, `rights.credit_line`, `rights.rights_metadata_present`): deferred — recorded as placeholders in Section 5, no story #78 update required now.
2. Conflict resolution: log only — no `conflict_flag` CAR field; conflicts recorded in processing logs, with log entry structure specified in Section 7.
3. `DateTimeOriginal`: provenance metadata outside the seven categories — recorded as `provenance.capture_date` placeholder.

**Current state:** All 5 pre-PO ACs met. Story awaits PO approval to close AC6 and mark done. Comment posted on issue #87. Epic #2 body updated with specification document table.

**Why:** Many assets carry trusted embedded GPS, rights, and subject data that the Asset Intelligence Layer would otherwise ignore or re-infer at unnecessary cost.

**How to apply:** When PO approves, add the `ready` label (it already has `ready`; confirm PO has ticked AC6). The placeholder fields in Section 5 of the spec are inputs for the MVP1 implementation team's field catalogue update — flag when that work is scheduled.
