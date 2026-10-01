---
name: Worked example accuracy check
description: Specification stories with worked examples against named external schemas must be verified before PO review
type: feedback
---

Worked examples in specification stories that reference a named external schema or API (e.g., Adobe Stock CSV format, Shutterstock metadata fields) must be verified against the source before the story is labelled ready.

**Why:** Sprint 2 story #77 contained a worked example with incorrect Adobe Stock fields (missing Description column, wrong keyword minimum). The PO caught it and a correction pass was required before acceptance. This added rework that could have been caught at the ready checklist stage.

**How to apply:** When reviewing a story for ready status, check whether the story body contains a worked example referencing a named external schema or API. If yes, confirm the example has been spot-checked against that source before approving. This is now a line item in the AGILE_BOARD.md Ready checklist.
