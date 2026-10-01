---
name: Short description profile refined
description: Story #29 refined 2026-09-28 — general/short-description Content Profile, 9 ACs, ready label + board Status Ready
type: project
---

Story #29 ("Define generic short description profile") refined on 2026-09-28 for Sprint 5. Issue body replaced with full user story, in/out scope, 9 testable ACs, dependency table, and risks section. Ready label added. Board Status set to Ready.

**Key decisions recorded in the story:**
- Profile ID is `general/short-description`; `general` category is not currently in the content-profile-schema.md enum — risk flagged for implementing developer to raise with PO before closing
- `output_format.type` set to `json` (channel-agnostic; no CSV/IPTC needed for a general profile)
- Keyword Rules dimension explicitly marked not applicable (no keyword generation in this profile)
- Six CAR source fields named: `objects.primary_subject`, `objects.scene_type`, `location.environment_type`, `location.setting_descriptor`, `persons.present`, `activities.primary_activity`
- Three mandatory validation rule IDs: `short-desc-required`, `short-desc-max-length`, `short-desc-no-promotional`
- Fallback generation behaviour when conditional CAR fields are absent is deferred to the Layer 2 implementation story

**Why:** This is the first MVP3 general profile — establishes the pattern for subsequent general profiles in Epic #4.

**How to apply:** When refining other general profile stories in Epic #4, use this story as the template. The `general` category schema enum risk applies to all of them.
