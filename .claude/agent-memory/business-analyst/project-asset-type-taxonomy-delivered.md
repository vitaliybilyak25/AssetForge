---
name: Asset Type Taxonomy Delivered
description: Story #82 complete — asset type taxonomy at docs/asset-type-taxonomy.md, Epic #1 updated, comment on GH issue #82, awaiting PO approval
type: project
---

Story #82 (Define asset type taxonomy) delivered on 2026-09-26.

Artifact: `docs/asset-type-taxonomy.md`

**Why:** MVP0 requires a classification of all three primary Asset Types (Photo, Video, Vector) with sub-types, MVP scope annotations, indicative CAR fields, and compliance implications to support pipeline routing design and MVP1 scoping.

**How to apply:** Photo is MVP1 scope; Video and Vector are MVP10 scope. All CAR field names in the taxonomy are indicative — story #78 (CAR Field Catalogue) is the authoritative source. Epic #1 Reference section updated. Comment posted on issue #82. Issue left open for PO approval.

Key decisions recorded in the taxonomy:
- 7 Photo sub-types, 6 Video sub-types, 7 Vector sub-types
- Photo CAR fields include: resolution, colour profile, EXIF datetime/camera, person count, faces detected, model release flag, property release flag, editorial-only flag
- Video-unique fields include: duration, frame rate, audio_present, key_frame_objects, temporal_event_flags, audio rights flag
- Vector-unique fields include: text_elements, path_complexity, color_mode, artboard_dimensions, contains_raster_embeds, trademark flag
- All CAR field names cross-referenced to story #78 as the authoritative catalogue
