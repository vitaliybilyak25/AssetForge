# Scenario C — Expected Output

**CAR input:** `scenario-c-car.json`
**Scenario:** Editorial photo (`risk.editorial_only = true`) — protest march

---

## Expected Title

```
Protesters march during climate rally in city center
```

**Derivation:** `objects.primary_subject` = "crowd of protesters"; `activities.primary_activity` = "protest march"; `location.setting_descriptor` = "city street". Editorial path — brand names would be included if present; none detected. Sentence case; 52 characters.

---

## Expected Keywords

```
protest,rally,crowd,demonstration,march,climate,city,street,banner,sign,outdoor,urban,activism,people,group,movement,political,community,gathering,event,editorial,news,journalism,documentary,public,social issue,democracy,human rights,chanting,placard,police barrier,daytime,color photography,horizontal,stock photo
```

**Derivation:** Primary subject "protest" first; followed by activity keywords from `activities.detected_activities`, scene keywords from `location`, and editorial-specific contextual terms. 35 keywords; all lowercase; comma-separated; relevance-descending.

**Note — editorial path:** `risk.editorial_only = true`. Brand names would be included as subject-identifying keywords on the editorial path; none are present in this scenario (`text.logo_marks_detected` is empty).

---

## Expected Category

```
11
```

**Code:** 11 — People (`docs/adobe-stock-submission-rules.md` §4.2)

**Derivation:** `objects.primary_subject` = "crowd of protesters"; `persons.present = true`; `persons.group_composition` = "large crowd". The primary subject is a large group of people. People category is the most specific match.

---

## Expected Releases State

**State: C — Release not required (editorial exemption)**

**Condition:** `risk.editorial_only = true`. Under the editorial classification path, model and property release requirements do not block Output Package generation. The `Releases` column is left empty under State C semantics for the editorial Output Package.

**`Releases` column value:** `""` (empty string)

**Note:** `risk.model_release_required = true` is also set on this CAR (faces visible). However, the editorial exemption takes precedence for the editorial Output Package. If a human reviewer subsequently overrides `risk.editorial_only` and a commercial Output Package is generated, State B would apply and full release rules would govern.

**Rule reference:** `docs/adobe-stock-release-rules.md` §5.1 (editorial exemption); §3.3 (State C semantics).
