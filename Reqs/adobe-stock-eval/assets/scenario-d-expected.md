# Scenario D — Expected Output

**CAR input:** `scenario-d-car.json`
**Scenario:** Commercial photo with visible logo (`risk.trademark_flag = true`, `text.logo_marks_detected = ["Apple logo"]`)

---

## Expected Title

```
Laptop computer on wooden desk in modern office
```

**Derivation:** `objects.primary_subject` = "laptop computer"; `location.setting_descriptor` = "office desk"; enriched with "wooden" from `objects.detected_subjects` colour/material context. Brand name "Apple" is suppressed on the commercial path (`risk.trademark_flag = true`). Sentence case; 47 characters.

---

## Expected Keywords

```
laptop,computer,desk,office,technology,workspace,modern,wooden,notebook,coffee,productivity,business,indoor,work,professional,daylight,sunlight,contemporary,minimal,organized,flat lay,overhead,still life,copy space,horizontal,color photography,stock photo,table,surface,device,screen,keyboard,cable,peripheral,equipment,digital,electronic,gadget,nobody
```

**Derivation:** Primary subject "laptop" first; followed by workspace and technology terms from `objects.detected_subjects` and `location`. Brand name "Apple" excluded (`risk.trademark_flag = true`; commercial path). 39 keywords; all lowercase; comma-separated; no brand names.

---

## Expected Category

```
16
```

**Code:** 16 — Technology (`docs/adobe-stock-submission-rules.md` §4.2)

**Derivation:** `objects.primary_subject` = "laptop computer"; `objects.scene_type` = "workspace still life". Technology is the most specific matching category for a laptop/device composition.

---

## Expected Releases State

**State: C — Release not required**

**Condition:** `risk.model_release_required` is absent (`persons.present = false`); `risk.property_release_required` is absent; `risk.trademark_flag = true` is active but does not trigger a release requirement — it triggers brand-name suppression in generated content, not a release gate.

**`Releases` column value:** `""` (empty string)

**Note:** `risk.trademark_flag = true` governs content generation (brand name suppression in title and keywords) but does not affect the `Releases` column. Release rules are triggered by `risk.model_release_required` and `risk.property_release_required` only.

**Rule reference:** `docs/adobe-stock-release-rules.md` §3.3 (State C).
