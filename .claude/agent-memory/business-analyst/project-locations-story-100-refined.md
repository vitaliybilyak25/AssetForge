---
name: Locations story #100 refined
description: Story #100 (Locations category, split from #19) elevated from stub to full ready state 2026-09-27
type: project
---

Story #100 was raised as a stub with incomplete ACs and was fully refined to ready state 2026-09-27. It covers all seven Locations fields from docs/car-field-catalogue.md.

**Why:** PO decision split Locations from People story #19 into a separate story. The stub body referenced some fields not exactly matching the catalogue and lacked full ACs.

**Key decisions recorded in the story:**
- GPS-from-EXIF-only constraint: `location.gps_coordinates` populated from EXIF `GPSLatitude` + `GPSLongitude` only; visual inference prohibited; sourced from docs/embedded-metadata-ingestion.md (story #87), Sections 2.1 and 3.1.
- Absent GPS = unknown per CAR Consumer Rule 1 (docs/canonical-asset-record.md, Section 4, Rule 1) — not "no location".
- `location.gps_derived_region` source hierarchy: GPS-derived primary; IPTC IIM city/state/country as lower-authority supplement when GPS absent — per story #87 Section 2.2.
- All seven catalogue fields included: environment_type (Required, enum: indoor/outdoor/mixed), setting_descriptor (Conditional), gps_coordinates (Conditional, object {lat, lon}), gps_derived_region (Conditional), visual_landmark (Conditional), urban_rural_signal (Conditional, enum: urban/suburban/rural/wilderness), confidence_score (Required).
- Reverse-geocoding service selection is an MVP1 implementation decision — out of scope.

**How to apply:** When the PO approves this story, apply the `ready` label and set board Status to Ready. The story has 10 ACs. Confirm with the PO that the `parent` field on issue #100 is set to #2 (Epic).
