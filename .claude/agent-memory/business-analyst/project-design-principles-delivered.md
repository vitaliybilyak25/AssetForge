---
name: Design Principles and Naming Conventions — Story #80
description: Story #80 complete — design principles at docs/design-principles.md, CLAUDE.md Reference section updated, comment on GH issue #80, awaiting PO approval
type: project
---

Story #80 delivered on 2026-09-26.

Artifact: `docs/design-principles.md`

Document covers:
- Three design principles: Profile-Driven Not Hardcoded Per-Site; Stock Marketplaces Are the First Use Case Not the Scope; Strict Layer Separation
- Naming conventions for: Profile Identifiers (category/profile-name), Layer Names (canonical Title Case with "Layer"), Artifact Names (Title Case, fixed per glossary), Module Names (PascalCase XxxForge), MVP Milestone Labels
- Governance section naming Product Owner as sole approver; proposal process via GitHub issue with labels `documentation` and `design-principles-proposal`

CLAUDE.md Reference section updated to include link to `docs/design-principles.md`.

GitHub comment posted at https://github.com/vitaliybilyak25/AssetForge/issues/80#issuecomment-5849724467

**Why:** Story #80 was part of MVP0 domain model work to establish a shared conventions baseline for all contributors before MVP1 specification begins.

**How to apply:** When authoring new principles proposals or naming new artifacts, verify against `docs/design-principles.md` Naming Conventions sections before raising a PR or story.
