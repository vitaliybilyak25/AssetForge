---
name: Adobe Stock output fields story refined and PO decisions incorporated
description: Story #24 body updated 2026-09-27 — confirmed 5 columns only (not 9), parallel authoring permitted, AI generated column removed, ready checklist 7/8 checked
type: project
---

Story #24 refined on 2026-09-27 and issue body updated with PO decisions on the same date.

**Confirmed column set (5 columns only):** Filename, Title, Keywords, Category, Releases. This was verified against Reqs/Sample_Adobe_Stock_CSV_upload.csv. The original refinement assumed 9 columns (including Description, Editorial, Mature content, AI generated) — all four removed. PO confirmed from sample CSV that these columns do not exist in the Adobe Stock bulk upload template.

Persona: Content Profile author (dual audience: profile author and Channel Adaptation Layer developer). Six testable ACs. Parallel authoring with #23 is permitted (PO decision); AC5 rewritten to reflect this. #25 and #26 remain blocked until both #23 and #24 are accepted by the PO.

**Why:** The 9-column assumption in the original refinement was wrong. Adobe Stock's bulk upload CSV has only 5 columns. The hard dependency gate on #23 was also relaxed by PO to allow parallel drafting.

**How to apply:** When #24 author asks what to document, direct them to the 5-column table: Filename, Title, Keywords, Category, Releases. Releases column maps to docs/adobe-stock-release-rules.md Section 3. Category maps to numeric code via rule in #23. Do NOT add Description, Editorial, Mature content, or AI generated columns.

### PO decisions resolved

1. Authoring order: #23 and #24 can be drafted in parallel — hard sequencing gate removed.
2. AI generated column: OUT OF SCOPE — no such column exists in the Adobe Stock CSV template (confirmed from Reqs/Sample_Adobe_Stock_CSV_upload.csv).
3. Column completeness: exactly 5 columns from sample CSV — Filename, Title, Keywords, Category, Releases.

### Status

Issue body updated and confirmation comment posted. Ready checklist: 7/8 checked. Awaiting PO approval to apply `ready` label and set board Status to Ready.
