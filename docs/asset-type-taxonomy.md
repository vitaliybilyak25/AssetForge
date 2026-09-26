# AssetForge Asset Type Taxonomy

## Purpose

This document classifies the three primary Asset Types supported by the AssetForge platform — Photo, Video, and Vector — and the Sub-types within each. For each primary type it records: the MVP milestone that brings the type into processing scope, the Canonical Asset Record (CAR) fields that are unique or particularly significant for that type, and the compliance implications (editorial vs. commercial classification, release requirements) that the Asset Intelligence Layer must capture as Risk Flags. The taxonomy determines which processing Pipeline path is activated when an Asset is ingested and is the authoritative reference for scoping decisions across MVP1 through MVP10. All terms used in this document are defined in the [AssetForge Domain Glossary](glossary.md). The full field-level specification of the CAR is the subject of story #78 (CAR Field Catalogue); the CAR field references below are indicative and must be confirmed against that catalogue once it is complete.

---

## Photo

### Definition

A Photo is a primary Asset Type representing a raster photographic image captured by a camera or similar imaging device. Photos are pixel-based; resolution and quality are functions of the sensor or scanning source. This definition follows the glossary entry: a Photo is not a vector or illustration. Supported file formats include, but are not limited to, JPEG, TIFF, PNG, and RAW variants.

### Sub-types

| Sub-type | Description | Notes |
|---|---|---|
| Lifestyle | Depicts people in naturalistic, staged, or candid everyday scenarios intended for commercial advertising and marketing use | High probability of identifiable persons; model release tracking is mandatory in the CAR |
| Editorial | Depicts real-world events, public figures, recognisable locations, or news situations; intended for informational, educational, or journalistic use only | Cannot be used commercially; editorial classification must be recorded as a CAR flag and propagated to all Output Packages |
| Nature and Wildlife | Depicts natural environments, flora, fauna, landscapes, and ecosystems with no human subjects | Lower release risk; location metadata (GPS, region) is a high-value CAR field |
| Architecture and Real Estate | Depicts buildings, interiors, urban environments, and constructed structures | Private property depicted in commercial contexts may require a Property Release; this must be flagged in the CAR |
| Food and Product | Depicts food, beverages, consumer goods, or product arrangements against controlled backgrounds | Frequently used in commerce contexts; accurate object identification in the CAR is critical for downstream keyword generation |
| Abstract and Texture | Depicts patterns, textures, gradients, and visual abstractions without identifiable subjects | Minimal compliance risk; low likelihood of release requirements |
| Aerial and Drone | Captured from elevated or unmanned aerial platforms; may depict private property, public gatherings, or restricted airspace | Regulatory compliance (airspace, privacy) may vary by jurisdiction; Risk Flags for identifiable property and persons must be applied where detectable |

### MVP Introduction

**MVP1.** Photo is the first and only Asset Type in scope for MVP1 (Canonical Asset Record specification) and remains the sole supported type through MVP6 (additional stock profiles). All CAR field design, Content Profile work, and channel adaptation from MVP1 through MVP6 targets Photo assets exclusively. Video and Vector are documented here for planning continuity but are not in scope until MVP10.

### CAR Fields Unique or Significant to Photo

The following fields are either unique to Photo or carry heightened importance relative to Video and Vector assets. These are indicative; story #78 (CAR Field Catalogue) holds the authoritative field-level specification.

| Field (indicative name) | Description | Rationale |
|---|---|---|
| `image.resolution_px` | Width and height of the raster image in pixels | Determines print and web usability; stock marketplaces impose minimum resolution thresholds |
| `image.color_profile` | Embedded colour space (e.g., sRGB, Adobe RGB, CMYK) | Affects downstream reproduction accuracy; relevant to print-oriented stock channels |
| `image.exif_capture_datetime` | Date and time of capture from EXIF metadata | Supports editorial classification by establishing when a depicted event occurred |
| `image.exif_camera_make_model` | Camera manufacturer and model from EXIF | Supporting metadata for editorial provenance; may be required by some stock channels |
| `persons.count` | Number of identifiable persons detected | Drives model release requirement logic; a count above zero triggers release Risk Flags |
| `persons.faces_detected` | Boolean or array indicating whether faces are detectable | Refines model release risk assessment; face detection elevates release requirement probability |
| `risk.model_release_required` | Risk Flag indicating that one or more identifiable persons are present and a model release may be required for commercial use | Core compliance signal for stock channel profiles; propagated to all Output Packages |
| `risk.property_release_required` | Risk Flag indicating that recognisable private property is present and a property release may be required for commercial use | Required for architecture sub-type and any asset depicting branded or privately owned structures |
| `risk.editorial_only` | Risk Flag indicating the asset depicts a real-world event or public figure and is classified as Editorial Use only | Must block commercial channel profiles from generating Output Packages without human review |

### Compliance Implications

- **Commercial vs. Editorial classification.** The Asset Intelligence Layer must determine, to the extent possible from visual analysis, whether the asset depicts real-world events, identifiable public figures, or news situations that restrict it to Editorial Use. The `risk.editorial_only` flag must be set when this is detected. No commercial Output Package should be generated for a flagged editorial asset without human review.
- **Model Release.** Any photo depicting an identifiable person — whether in a Lifestyle, Aerial, or other sub-type — requires a model release for commercial distribution. The CAR records the presence or absence of this release as a Risk Flag. AssetForge does not collect or verify the release document itself; this is explicitly out of scope per the system boundaries.
- **Property Release.** Photos depicting recognisable private property (buildings, artworks, branded objects) in a commercial context require a property release. Architecture and Real Estate sub-types have the highest exposure. The CAR records the risk signal; resolution is the operator's responsibility.
- **Minimum resolution requirements.** Stock marketplace channels (Adobe Stock, Shutterstock, iStock) impose minimum pixel dimension thresholds. The CAR must capture resolution so that the Channel Adaptation Layer can validate compliance and flag assets that are below threshold.

---

## Video

### Definition

A Video is a primary Asset Type representing a time-based moving image file composed of sequential frames, captured by a camera or generated digitally. Videos have duration, frame rate, and audio tracks as intrinsic properties that have no equivalent in Photo or Vector assets. This definition follows the glossary entry: Video is not an animated GIF or motion graphic vector. Supported file formats include, but are not limited to, MP4, MOV, MXF, and AVI.

### Sub-types

| Sub-type | Description | Notes |
|---|---|---|
| Live Action Footage | Real-world footage captured by a camera; depicts people, places, events, or objects in motion | Highest compliance complexity: editorial classification, model release, and property release all apply; temporal event detection adds complexity beyond still photo analysis |
| Time-lapse | A sequence of still frames captured at extended intervals and played back at normal or elevated speed to compress time | Environmental or architectural subjects common; release requirements follow the same logic as the equivalent photo sub-types |
| Slow Motion | Footage captured at a high frame rate and played back at normal speed to reveal detail in fast-moving subjects | Typically nature, sport, or product-focused; release requirements consistent with live action |
| Aerial and Drone Video | Moving image footage captured from elevated or unmanned aerial platforms | Regulatory and privacy considerations equivalent to Aerial and Drone Photo sub-type; duration and location-over-time add complexity |
| Motion Graphic (Camera-Captured) | Video footage of physical motion graphic displays or broadcast outputs; distinct from vector-based animation | Distinct from Vector motion graphic (which is path-defined); this sub-type is camera-captured raster footage |
| Screen Recording | Footage captured from a digital screen or display | Low release risk for proprietary content; high risk for third-party software UI copyright; flagged for review |

### MVP Introduction

**MVP10.** Video is not in processing scope until MVP10 (Video and Vector workflows). No CAR fields, Content Profiles, or Channel Adaptation work for Video should be designed or implemented before MVP10. The sub-types and CAR field notes below are recorded here for planning and architecture continuity only.

### CAR Fields Unique or Significant to Video

| Field (indicative name) | Description | Rationale |
|---|---|---|
| `video.duration_seconds` | Total duration of the clip in seconds | Stock marketplaces and social channels impose minimum and maximum duration limits; required for validation |
| `video.frame_rate` | Frames per second (e.g., 24, 30, 60 fps) | Affects output suitability for broadcast vs. web channels; slow-motion and time-lapse sub-types require frame rate context |
| `video.resolution_px` | Frame width and height in pixels | Equivalent function to `image.resolution_px` for photos; HD/4K thresholds apply on stock channels |
| `video.audio_present` | Boolean indicating whether an audio track is present | Audio may introduce separate licensing and rights considerations; must be recorded in the CAR |
| `video.key_frame_objects` | Aggregated object, person, and location observations extracted from representative key frames across the clip | Frame-level analysis is architecturally more complex than single-image analysis; this field aggregates findings across time |
| `video.temporal_event_flags` | Flags indicating detected events that change compliance or classification status over the duration of the clip (e.g., a person enters frame at 00:12) | Temporal complexity unique to video; a person appearing in only one segment of a clip still triggers model release logic |
| `risk.audio_rights_flag` | Risk Flag indicating that the audio track may contain third-party copyrighted material | Unique to Video; has no equivalent in Photo or Vector types |

### Compliance Implications

- **Frame-level analysis complexity.** Unlike a Photo, a Video may contain identifiable persons, brand logos, or editorial events in only a subset of frames. The Asset Intelligence Layer must perform key-frame analysis across the full duration and aggregate Risk Flags accordingly. A model release requirement triggered by one frame applies to the entire clip.
- **Audio rights.** The presence of a music or voice audio track introduces copyright risk that does not exist for Photo or Vector assets. The `risk.audio_rights_flag` signals that downstream human review or rights clearance may be required before commercial distribution.
- **Duration and resolution thresholds.** Stock video channels impose minimum clip duration (commonly 5 seconds) and minimum resolution (commonly HD 1920x1080). These must be validated at the Channel Adaptation Layer using CAR-supplied duration and resolution fields.
- **Editorial classification.** The same editorial vs. commercial distinction that applies to Photos applies to Video. Live Action Footage of news events, public figures, or real-world situations must be flagged `risk.editorial_only`.

---

## Vector

### Definition

A Vector is a primary Asset Type representing a resolution-independent graphic defined by mathematical paths rather than pixels. Vectors can be scaled to any size without loss of quality. This definition follows the glossary entry: a Vector is not a photo or video; vectors have distinct analysis and processing requirements. Supported file formats include, but are not limited to, SVG, EPS, and AI (Adobe Illustrator).

### Sub-types

| Sub-type | Description | Notes |
|---|---|---|
| Illustration | An original hand-drawn or digitally painted artwork rendered as a vector; may depict characters, scenes, objects, or conceptual imagery | Depicts artistic interpretations rather than real-world captures; editorial classification is less common but possible for caricatures or news-editorial illustrations |
| Icon and UI Element | A flat or outlined symbol, icon, glyph, or user interface component; typically simple geometry at small display sizes | High commercial volume on stock marketplaces; minimal release requirements; keyword precision is critical |
| Infographic | A data visualisation, diagram, or information design combining text, shapes, and visual elements into a single vector composition | Text extraction from the CAR is a high-priority field; the `text_elements` field must capture labels and data captions embedded in the graphic |
| Logo and Brand Mark | A distinctive symbol or wordmark representing an organisation or product identity | Frequently contains third-party trademark elements; requires a `risk.trademark_flag` in the CAR when third-party brand marks are detected |
| Pattern and Background | A repeating decorative or abstract design intended for use as a background, textile print, or surface treatment | Minimal compliance risk; no release requirements in typical cases |
| Motion Graphic (Vector-Based) | An animated vector composition (e.g., animated SVG or After Effects export as a vector format) | Distinct from Camera-Captured Motion Graphic; file format detection must differentiate static from animated vectors |
| Map and Cartographic | A vector representation of geographic areas, regions, borders, or route diagrams | Geopolitical accuracy is a compliance concern; depiction of disputed territories may require editorial review flags |

### MVP Introduction

**MVP10.** Vector is not in processing scope until MVP10 (Video and Vector workflows), the same milestone as Video. No CAR fields, Content Profiles, or Channel Adaptation work for Vector should be designed or implemented before MVP10. The sub-types and CAR field notes below are recorded here for planning and architecture continuity only.

### CAR Fields Unique or Significant to Vector

| Field (indicative name) | Description | Rationale |
|---|---|---|
| `vector.text_elements` | Array of text strings extracted from the vector file (labels, titles, captions, data values, embedded copy) | Text is a structural component of many vector types (infographics, maps, icons with labels); extraction is required for keyword and description generation |
| `vector.path_complexity` | A measure of the number of distinct paths, nodes, or layers in the file | Relevant for technical validation; some stock channels impose path count limits or file size constraints related to path complexity |
| `vector.color_mode` | The colour mode of the file (e.g., RGB, CMYK, spot colours) | CMYK and spot colour vectors are print-oriented; RGB is screen-oriented; the Content Generation Layer needs this to shape description tone for appropriate channels |
| `vector.artboard_dimensions` | The canvas or artboard dimensions defined in the file | Unlike a Photo, vector dimensions are defined by artboard, not pixel count; relevant for layout and composition context |
| `vector.contains_raster_embeds` | Boolean indicating whether the vector file embeds raster image elements | A vector file with embedded rasters inherits the compliance considerations of Photo assets (e.g., identifiable persons in an embedded photo within an illustration) |
| `risk.trademark_flag` | Risk Flag indicating that the vector contains a detectable third-party brand mark or logo element | Unique to Vector; Logo and Brand Mark sub-type has the highest exposure; also applicable to illustrations or patterns that incorporate brand imagery |

### Compliance Implications

- **Trademark and brand mark risk.** Unlike Photos, Vectors frequently contain explicit brand logos, wordmarks, and proprietary symbols that are protected as trademarks. The `risk.trademark_flag` must be set when third-party brand marks are detected. Commercial distribution of such assets requires rights clearance outside AssetForge's scope.
- **Embedded raster content.** A Vector file that embeds raster image elements (a common practice in complex illustrations) inherits the full Photo compliance logic for those embedded elements. The `vector.contains_raster_embeds` flag triggers a secondary compliance pass using Photo-equivalent Risk Flag logic.
- **Editorial illustration.** While less common than editorial photography, editorial illustrations — such as political caricatures or news commentary graphics — carry the same Editorial Use restrictions. The Asset Intelligence Layer must detect and flag these cases.
- **Geopolitical content.** Map and Cartographic vectors depicting disputed political borders or territories may require editorial review before distribution on certain channels. This is recorded as a Risk Flag; resolution is the operator's responsibility.
- **Text accuracy.** Infographic and map vectors contain embedded text that forms part of the asset's meaning. Inaccurate text extraction in the CAR could lead to incorrect keyword and description generation. Text element extraction must be treated as a high-confidence requirement for these sub-types.

---

## Cross-Reference Note

The CAR field names used in this taxonomy (e.g., `persons.count`, `video.duration_seconds`, `risk.model_release_required`) are indicative labels introduced here for planning and scoping purposes. They are not yet authoritative field specifications. The complete Canonical Asset Record field catalogue — including field names, data types, cardinality, validation rules, and confidence score applicability — is the subject of **story #78 (CAR Field Catalogue)**. All implementers and profile authors must treat story #78 as the authoritative source for CAR field definitions once that work is complete. Any conflicts between field names used here and the field names defined in story #78 must be resolved in favour of story #78.
