# Adobe Stock Metadata Generation Prompt

**Version:** `adobe-stock-v1`
**Story:** #25
**Layer:** Content Generation Layer (Layer 2)
**Profile:** `stock/adobe-stock`

---

## Purpose

This prompt instructs the AI model to generate Adobe Stock-compliant metadata — Title, Keywords, and Category — from a Canonical Asset Record (CAR). The output is used by the Channel Adaptation Layer (Layer 3) to produce the Adobe Stock bulk upload CSV row.

This prompt does **not** generate a Description field (the Adobe Stock CSV has no Description column) and does **not** evaluate release state (Releases is always an empty string constant — release determination belongs to the Approval Requirements review step).

---

## Input Schema

The prompt receives a single Canonical Asset Record as a JSON object. The CAR contains up to seven top-level categories. All seven categories are listed below; categories absent from the CAR (null or missing) are handled per the Partial CAR Fallback Rules section.

```
{
  "objects":     { ... },   // Objects and Subjects — primary source for Title, Keywords, Category
  "persons":     { ... },   // People — supplements Keywords with lifestyle/demographic terms
  "location":    { ... },   // Locations — supplements Title and Keywords with setting context
  "text":        { ... },   // Text and Logos — drives brand suppression (see Brand Suppression)
  "activities":  { ... },   // Activities — drives editorial path and activity keywords
  "risk":        { ... },   // Risk Flags — drives editorial handling conditional
  "confidence":  { ... }    // Confidence Scores — provides model version context; not used in generation
}
```

### Key CAR fields used by this prompt

| CAR Field | Used For |
|---|---|
| `objects.primary_subject` | Title anchor; first keyword; Category primary signal |
| `objects.detected_subjects` | Keywords; Title enrichment |
| `objects.scene_type` | Category disambiguation |
| `objects.colour_palette` | Supplementary keywords |
| `persons.present` | Triggers people/lifestyle keywords |
| `persons.count` | Group composition keywords |
| `persons.age_range_signals` | Demographic keywords |
| `persons.group_composition` | Group keywords |
| `persons.activity_posture` | Activity/posture keywords |
| `activities.primary_activity` | Title enrichment; Category signal; first activity keyword |
| `activities.detected_activities` | Activity keywords |
| `activities.editorial_event_signal` | Editorial path trigger |
| `location.environment_type` | Indoor/outdoor keywords |
| `location.setting_descriptor` | Title setting phrase; setting keywords |
| `location.visual_landmark` | Landmark keyword (editorial path: include as subject identifier) |
| `text.logo_marks_detected` | Brand suppression exclusion list |
| `objects.brand_objects_detected` | Brand suppression exclusion list |
| `risk.editorial_only` | Editorial handling conditional |
| `risk.trademark_flag` | Confirms brand suppression is active |

---

## Output Schema

The prompt returns exactly four fields. Three are generated; one is a fixed constant.

```json
{
  "prompt_version": "adobe-stock-v1",
  "Title": "<generated string>",
  "Keywords": "<generated comma-separated string>",
  "Category": <generated integer>,
  "Releases": ""
}
```

| Field | Type | Generated or Constant | Rule |
|---|---|---|---|
| `prompt_version` | string | Constant | Always `"adobe-stock-v1"` — records the prompt version alongside the output for audit purposes |
| `Title` | string | Generated | See Title Generation Rules |
| `Keywords` | string | Generated | See Keywords Generation Rules |
| `Category` | integer | Generated | See Category Resolution Rules |
| `Releases` | string | Constant `""` | Always an empty string — release state is determined by the Approval Requirements review step, not by this prompt |

**No other fields may appear in the output.** Do not generate a `Description`, `Filename`, or any field not listed above.

---

## Partial CAR Fallback Rules

If any top-level CAR category is null or absent, apply the following fallbacks. Never fail silently or return an error for a missing category — always produce a best-effort output using available fields.

| Missing Category | Fallback Behaviour |
|---|---|
| `objects` absent or null | Use `activities.primary_activity` as the Title anchor if available; use `location.setting_descriptor` as the primary subject. If both are absent, Title = `"Untitled scene"` and Keywords = `"photograph,image,stock photo"`. Set Category = 9 (Miscellaneous) and flag with a comment in `prompt_version` field as `"adobe-stock-v1-partial"`. |
| `persons` absent or null | Skip all People-category keywords; do not infer person presence. |
| `location` absent or null | Skip setting and environment keywords; do not include location context in Title. |
| `text` absent or null | Treat `text.logo_marks_detected` as an empty array; no brand suppression needed. |
| `activities` absent or null | Skip activity keywords; `activities.editorial_event_signal` is treated as `false`. |
| `risk` absent or null | Treat `risk.editorial_only` as `false`; apply the commercial path. |
| `confidence` absent or null | Skip — `confidence` fields are not used in content generation. |

---

## Title Generation Rules

Generate a factual, scene-describing sentence or noun phrase in English (US).

**Mandatory constraints (all must be satisfied):**

1. **Length:** ≤ 200 characters.
2. **Case:** Sentence case — first word capitalised; all subsequent words lowercase unless they are proper nouns (person names, place names, brand names that must be included on the editorial path).
3. **Language:** English (US) spelling and grammar.
4. **Subject accuracy:** The title must name or clearly describe the primary subject identified in `objects.primary_subject`. If `objects.primary_subject` is null, use `activities.primary_activity` or `location.setting_descriptor` as the anchor.
5. **Brand suppression (commercial path):** When `risk.editorial_only` is absent or `false`, exclude any term present in `text.logo_marks_detected` or `objects.brand_objects_detected`. Do not replace excluded brand names with generic equivalents that still identify the brand (e.g., do not write "the fruit logo laptop" to avoid writing "MacBook").

**Construction guidance:**

- Start with the primary subject (`objects.primary_subject`).
- Add the primary activity (`activities.primary_activity`) if it enriches the scene description.
- Add the setting (`location.setting_descriptor`) to complete the context.
- Keep the title to one clause; avoid compound sentences.
- Avoid aspirational, promotional, or evaluative language ("stunning", "beautiful", "perfect").
- Do not include keyword lists, comma-separated terms, or hashtags in the Title.

**Editorial path override (when `risk.editorial_only = true`):**
- Brand names present in `text.logo_marks_detected` or `objects.brand_objects_detected` **must** be included in the Title when they identify the documented subject (e.g., a photo of a Heineken bottle at a news event should include "Heineken" in the Title).
- Use factual, descriptive phrasing that records the event, person, or place being documented.
- Do not use promotional or stock-centric phrasing on the editorial path.

---

## Keywords Generation Rules

Generate a single comma-separated keyword list in English (US).

**Mandatory constraints (all must be satisfied):**

1. **Count:** Between 5 and 49 keywords inclusive. Never fewer than 5, never more than 49.
2. **Case:** All keywords must be lowercase. No capitalisation, even for proper nouns.
3. **Separator:** Comma with no surrounding whitespace. Format: `keyword1,keyword2,keyword3`.
4. **Ordering:** Most important keyword first (relevance-descending). The most specific descriptor of the primary subject should be keyword 1.
5. **Language:** English (US) terms only.
6. **Brand suppression (commercial path):** When `risk.editorial_only` is absent or `false`, exclude any term from `text.logo_marks_detected` or `objects.brand_objects_detected`. Do not include brand names, product names, or model names associated with detected brand marks.
7. **No duplicates:** Each keyword or phrase must appear at most once in the list.

**Source fields and keyword categories to include (relevance order):**

1. Primary subject keyword — `objects.primary_subject` (always first)
2. Key secondary objects — top entries from `objects.detected_subjects`
3. Primary activity — `activities.primary_activity` if present
4. Secondary activities — `activities.detected_activities`
5. People keywords (when `persons.present = true`): count, age, gender signals from `persons.age_range_signals`, `persons.group_composition`, lifestyle terms
6. Setting keywords — `location.setting_descriptor`, `location.environment_type`, `location.urban_rural_signal`
7. Compositional keywords — `objects.scene_type`, format (horizontal/vertical), copy space
8. Colour keywords — `objects.colour_palette` entries when commercially relevant
9. Generic commercial stock keywords — e.g., `"stock photo"`, `"color photography"`, `"nobody"` (when `persons.present = false`)

**Editorial path override (when `risk.editorial_only = true`):**
- Brand names from `text.logo_marks_detected` are included as subject-identifying keywords.
- Replace generic commercial stock terms with editorial-context terms: `"editorial"`, `"news"`, `"journalism"`, `"documentary"`.
- Include `location.visual_landmark` as a keyword when present.

---

## Category Resolution Rules

Resolve a single Adobe Stock numeric category code from the 20-category taxonomy below. The output must be an integer — not a string, not the category name.

**Adobe Stock category taxonomy** (from `docs/adobe-stock-submission-rules.md` §4.2):

| Code | Name | Code | Name |
|---|---|---|---|
| 1 | Animals | 11 | People |
| 2 | Buildings/Architecture | 12 | Religion |
| 3 | Business/Finance | 13 | Science |
| 4 | Education | 14 | Signs/Symbols |
| 5 | Food/Drink | 15 | Sports/Recreation |
| 6 | Holidays | 16 | Technology |
| 7 | Industrial | 17 | Transportation/Vehicles |
| 8 | Interiors | 18 | Travel/Locations |
| 9 | Miscellaneous | 19 | Vintage/Retro |
| 10 | Nature | 20 | Celebrities |

**Resolution rules (apply in priority order):**

1. **Primary subject match:** Map `objects.primary_subject` to the most specific matching category. A professional person at a desk maps to 3 (Business/Finance) before 11 (People).
2. **Activity refinement:** Use `activities.primary_activity` to disambiguate when multiple categories are plausible. A scene with a chef cooking maps to 5 (Food/Drink) rather than 11 (People).
3. **Scene type confirmation:** Use `objects.scene_type` and `location.setting_descriptor` to confirm or override the primary subject match. A "professional kitchen" setting confirms 5 (Food/Drink) for a chef scene.
4. **Disambiguation rule — most specific wins:** When multiple categories are equally plausible, choose the most specific category for the dominant subject rather than the broader one.
5. **Fallback rule:** When no category unambiguously matches the primary subject and scene, use category **9 (Miscellaneous)** and set `prompt_version` to `"adobe-stock-v1-fallback-category"` to flag the unresolved case for human review.

**Do not output a string or category name.** The output must be a bare integer (e.g., `5`, not `"Food/Drink"` or `"5"`).

---

## Brand Suppression

Brand suppression applies on the **commercial path** (when `risk.editorial_only` is absent or `false`).

**Exclusion lists:**
- `text.logo_marks_detected` — array of detected logo/brand names
- `objects.brand_objects_detected` — array of detected branded objects

**Rules:**
1. Before finalising Title and Keywords, check every generated term against both exclusion lists.
2. Remove any term that matches an entry in either list, whether as an exact match or as the primary identifying word (e.g., if `"Apple logo"` is in `text.logo_marks_detected`, remove both `"Apple"` and `"apple"` from Keywords).
3. Do not replace the removed term with a circumlocution that still identifies the brand.
4. If removing brand terms brings the keyword count below 5, replace them with generic equivalent terms (e.g., replace `"macbook"` with `"laptop"`, `"computer"`).

**Editorial path:** Brand suppression does not apply when `risk.editorial_only = true`. Brand names identifying the documented subject must be included.

---

## Editorial Handling

When `risk.editorial_only = true`:

1. **Generate, do not block.** Always return Title, Keywords, and Category. Do not return an error or empty values. Routing of editorial assets to the editorial submission path is a Channel Adaptation Layer concern — not a prompt concern.
2. **Title:** Use factual, event-descriptive phrasing. Include the documented subject (person, place, event) by name when identifiable. Do not use promotional or commercially aspirational language.
3. **Keywords:** Include editorial context keywords (`"editorial"`, `"news"`, `"documentary"`, `"journalism"`). Include brand names when they identify the subject. Include `location.visual_landmark` when present. Treat `activities.primary_activity` and `location.setting_descriptor` as required inputs.
4. **Category:** Resolve using the same taxonomy rules as the commercial path. Editorial classification does not change the category assignment.
5. **Releases:** Always `""` — the editorial exemption to release requirements is applied by the Channel Adaptation Layer, not by this prompt.

---

## Prompt Instructions (for AI model execution)

```
You are the Content Generation Layer for the AssetForge Adobe Stock profile.

You receive a Canonical Asset Record (CAR) as a JSON object. Your task is to generate Adobe Stock-compliant metadata for the asset.

Follow all rules exactly as stated. Do not improvise, add fields, or omit fields.

OUTPUT exactly this JSON structure — nothing before it, nothing after it:
{
  "prompt_version": "adobe-stock-v1",
  "Title": "<your generated title>",
  "Keywords": "<your generated comma-separated keyword list>",
  "Category": <your resolved integer category code>,
  "Releases": ""
}

TITLE RULES:
- Maximum 200 characters
- Sentence case (first word capitalised, rest lowercase unless proper noun)
- Factual description of the primary subject and its setting
- English (US)
- EXCLUDE any term from text.logo_marks_detected or objects.brand_objects_detected (commercial path only — not when risk.editorial_only is true)

KEYWORD RULES:
- Between 5 and 49 keywords inclusive
- All lowercase
- Comma-separated, no spaces around commas
- Most important keyword first
- English (US)
- EXCLUDE any term from text.logo_marks_detected or objects.brand_objects_detected (commercial path only)
- No duplicates

CATEGORY RULES:
- Output a single integer from this list only: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
- Map the primary subject and activity to the most specific matching category
- If no category clearly matches, use 9 and set prompt_version to "adobe-stock-v1-fallback-category"

RELEASES RULE:
- Always output "" (empty string) — never evaluate release state

EDITORIAL OVERRIDE (applies when risk.editorial_only = true):
- Do NOT suppress brand names — include them when they identify the subject
- Use factual, event-descriptive language
- Add editorial context keywords: editorial, news, documentary, journalism

PARTIAL CAR:
- If a CAR category is null or missing, apply best-effort generation using available fields
- If objects is null, use activities.primary_activity or location.setting_descriptor as the title anchor
- If both are null, output Title = "Untitled scene", Keywords = "photograph,image,stock photo", Category = 9, and set prompt_version to "adobe-stock-v1-partial"

INPUT CAR:
```json
{CAR_JSON}
```
```

---

## Version History

| Version | Change |
|---|---|
| `adobe-stock-v1` | Initial version — covers full commercial and editorial paths for Photo assets |

---

## References

- `docs/adobe-stock-output-spec.md` — column specs, generation rules, validation rule IDs
- `docs/adobe-stock-submission-rules.md` §4.2 — category taxonomy
- `docs/adobe-stock-release-rules.md` §3, §5.1 — Releases column behaviour; editorial exemption
- `docs/car-field-catalogue.md` — authoritative CAR field names and types
- `docs/commercial-editorial-classification.md` — editorial classification decision sequence
- `Reqs/adobe-stock-eval/` — 5-asset evaluation set and scoring rubric (story #88)
