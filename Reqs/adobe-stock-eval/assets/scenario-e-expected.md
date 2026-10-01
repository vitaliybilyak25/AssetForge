# Scenario E — Expected Output

**CAR input:** `scenario-e-car.json`
**Scenario:** Commercial photo with recognisable scene and primary activity — chef cooking in professional kitchen (tests category resolution and keyword depth)

---

## Expected Title

```
Chef preparing meal in professional restaurant kitchen
```

**Derivation:** `objects.primary_subject` = "chef"; `activities.primary_activity` = "cooking" → rendered as "preparing meal"; `location.setting_descriptor` = "professional restaurant kitchen". Sentence case; 54 characters; no brand names.

---

## Expected Keywords

```
chef,cooking,kitchen,restaurant,food preparation,culinary,professional,apron,stove,cooking pot,vegetable,knife,cutting board,indoor,food,meal,gastronomy,hospitality,commercial kitchen,cook,cuisine,back view,working,toque,adult,male,occupation,food industry,catering,kitchen equipment,stainless steel,one person,focus,action,motion,lifestyle,authentic,real people,contemporary,color photography
```

**Derivation:** Primary subject "chef" first; "cooking" as primary activity second; scene-specific terms from `objects.detected_subjects`, `activities.detected_activities`, and `location.setting_descriptor`. 40 keywords; all lowercase; comma-separated; relevance-descending. No brand names detected.

---

## Expected Category

```
5
```

**Code:** 5 — Food/Drink (`docs/adobe-stock-submission-rules.md` §4.2)

**Derivation:** `activities.primary_activity` = "cooking"; `objects.primary_subject` = "chef"; `location.setting_descriptor` = "professional restaurant kitchen". Food/Drink is the most specific match for a culinary scene with an active cooking activity, more specific than People (11) for this context.

---

## Expected Releases State

**State: B — Release required, absent or unconfirmed**

**Condition:** `risk.model_release_required = true` (person is prominently featured as the primary subject; back-to-camera pose with `persons.activity_posture` = "standing, back to camera, actively working" and `objects.primary_subject` = "chef" confirming prominent feature status); `persons.faces_detected = false` but person is prominently featured. No confirmed release in the CAR input.

**`Releases` column value:** `""` (empty string — held pending human review)

**Export behaviour:** Output Package must not be delivered until a human reviewer confirms a valid model release is on file.

**Rule reference:** `docs/adobe-stock-release-rules.md` §3.2 (State B); §4.1 (require human review policy); `docs/car-risk-flags-spec.md` §risk.model_release_required (prominently featured trigger condition).
