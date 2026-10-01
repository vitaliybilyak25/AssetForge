# Scenario B — Expected Output

**CAR input:** `scenario-b-car.json`
**Scenario:** Commercial photo with identifiable person (face visible — `risk.model_release_required = true`)

---

## Expected Title

```
Woman working at standing desk in bright home office
```

**Derivation:** `objects.primary_subject` = "woman"; `activities.primary_activity` = "working at computer"; `location.setting_descriptor` = "home office"; enriched with "standing desk" from `objects.detected_subjects` and "bright" from `objects.colour_palette`. Sentence case; 52 characters; no brand names.

---

## Expected Keywords

```
woman,standing desk,home office,remote work,productivity,working from home,laptop,technology,modern workplace,professional,indoor,natural light,lifestyle,business,female,adult,entrepreneur,workspace,daylight,computer,typing,window,plant,minimalist,organized,focus,contemporary,interior,desk,white background,copy space,horizontal,color photography,stock photo,people,one person,casual,confident,millennial
```

**Derivation:** Primary subject anchor "woman" first; "standing desk" as the key scene differentiator second; lifestyle and business keywords drawn from `activities`, `location`, and `persons` fields. 39 keywords; all lowercase; comma-separated; relevance-descending; no brand names (none in `text.logo_marks_detected`).

---

## Expected Category

```
3
```

**Code:** 3 — Business/Finance (`docs/adobe-stock-submission-rules.md` §4.2)

**Derivation:** `activities.primary_activity` = "working at computer"; `location.setting_descriptor` = "home office"; `objects.primary_subject` = "woman" in a professional context. Business/Finance is more specific than People for this scene type.

---

## Expected Releases State

**State: B — Release required, absent or unconfirmed**

**Condition:** `risk.model_release_required = true` (face visible; `persons.faces_detected = true`); no confirmed release record is available in the CAR input (no reviewer confirmation provided).

**`Releases` column value:** `""` (empty string — held pending human review)

**Export behaviour:** Output Package must not be delivered until a human reviewer confirms a valid model release is on file.

**Rule reference:** `docs/adobe-stock-release-rules.md` §3.2 (State B); §4.1 (require human review policy).
