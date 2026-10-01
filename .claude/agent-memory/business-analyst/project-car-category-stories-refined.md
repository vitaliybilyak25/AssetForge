---
name: CAR category stories #17–#21 and #100 refined
description: MVP1 CAR schema stories for five categories refined 2026-09-27; PO decisions for #17, #18, #19 and new story #100 incorporated 2026-09-27
type: project
---

Stories #17–#21 (CAR field-level specifications for five of the seven CAR categories) were initially refined 2026-09-27. PO decisions for #17, #18, #19 were subsequently incorporated and issue bodies updated 2026-09-27. Story #100 (Locations, split from #19) was raised as a stub and fully refined to ready state 2026-09-27.

**Why:** These are the MVP1 implementation-level field specifications. The CAR Field Catalogue (story #78) exists; these stories translate each category's fields into testable ACs a Layer 1 developer can implement against.

**Story coverage:**
- #17 — Activities category (6 fields: detected_activities, primary_activity, social_context, physical_intensity, editorial_event_signal, confidence_score) — PO decisions applied: social_context conditional on persons.count >= 2 (cross-category dep on People); physical_intensity applies to non-person activities. AC count 10. Awaiting PO approval.
- #18 — Objects and Subjects category (6 fields: detected_subjects, primary_subject, scene_type, colour_palette, brand_objects_detected, confidence_score) — PO decisions applied: colour_palette = plain colour names only (no hex); foreground/background is a catalogue gap (AC7 notes gap, AC8 gates closure on catalogue revision). AC count 11. Awaiting PO approval.
- #19 — People category only (7 fields) — PO decisions applied: gender field out of scope (final, documented in AC6); age_range_signals closed enum child/adult/senior/other; Locations split to #100. AC count 11. Awaiting PO approval.
- #20 — Text and Logos category (6 fields: strings_present, detected_strings, logo_marks_detected, watermark_present, dominant_language, confidence_score) — PO decisions still outstanding (see below).
- #21 — Confidence Scores category (5 fields: overall_score, analysis_model_version, low_confidence_categories, analysis_timestamp, asset_quality_signal) — PO decisions still outstanding (see below).
- #100 — Locations category (7 fields: environment_type, setting_descriptor, gps_coordinates, gps_derived_region, visual_landmark, urban_rural_signal, confidence_score) — fully refined from stub; GPS-from-EXIF-only constraint; absent GPS = unknown per CAR Consumer Rule 1; cross-reference to docs/embedded-metadata-ingestion.md (story #87). AC count 10. Awaiting PO approval.

**PO decisions still outstanding:**

| Story | Decisions needed |
|---|---|
| #20 | (1) position/bounding-box field decision (add to Field Catalogue or formally descope); (2) logo_marks_detected conditioning when strings_present = false confirmation |
| #21 | (1) confidence.overall_score weighting formula — implementation decision vs PO-specified weights; (2) asset_quality_signal `none` value — present-with-none vs absent-when-no-issues (possible Field Catalogue inconsistency) |

**How to apply:** When PO provides decisions for any of the above, update the relevant issue body to close the open decisions, then apply the `ready` label and set board Status to Ready.

**Recurring pattern observed:** Original issues contained fields (gender, position/bounding-box, foreground/background, per-item confidence scores) not present in the Field Catalogue. Always cross-check issue scope against `docs/car-field-catalogue.md` before refining; descope any field not in the catalogue and flag as a PO decision.
