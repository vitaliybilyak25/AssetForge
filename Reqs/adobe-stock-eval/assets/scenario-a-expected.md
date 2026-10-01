# Scenario A — Expected Output

**CAR input:** `scenario-a-car.json`
**Scenario:** Commercial photo, no people present

---

## Expected Title

```
Mountain trail with wildflowers in alpine meadow
```

**Derivation:** `objects.primary_subject` = "mountain trail"; scene enriched with "wildflowers" from `objects.detected_subjects` and "alpine meadow" from `location.setting_descriptor`. Sentence case; 49 characters; no brand names.

---

## Expected Keywords

```
mountain,trail,wildflower,alpine,meadow,nature,landscape,outdoor,hiking,summer,flower,scenic,path,travel,sky,blue,green,rock,plant,grass,wilderness,countryside,terrain,peak,environment,tourism,adventure,fresh air,tranquil,rural,footpath,yellow flower,daylight,sunlight,nobody,copy space,horizontal,color photography,stock photo
```

**Derivation:** Primary subject anchor "mountain" first; followed by scene-specific terms from `objects.detected_subjects`, `location.setting_descriptor`, and `location.environment_type`; padded with contextual commercial keywords. 39 keywords; all lowercase; comma-separated; relevance-descending.

---

## Expected Category

```
10
```

**Code:** 10 — Nature (`docs/adobe-stock-submission-rules.md` §4.2)

**Derivation:** `objects.primary_subject` = "mountain trail"; `objects.scene_type` = "wide landscape"; `location.environment_type` = "outdoor". Primary subject maps directly to Nature category.

---

## Expected Releases State

**State: C — Release not required**

**Condition:** `risk.model_release_required` is absent (no persons detected); `risk.property_release_required` is absent; no active release flags on the CAR.

**`Releases` column value:** `""` (empty string)

**Rule reference:** `docs/adobe-stock-release-rules.md` §3.3 (State C).
