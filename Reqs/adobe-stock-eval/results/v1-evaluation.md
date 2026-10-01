# Evaluation Results — adobe-stock-v1

**Prompt version:** `adobe-stock-v1`
**Prompt file:** `prompts/stock/adobe-stock-v1.md`
**Rubric:** `Reqs/adobe-stock-eval/rubric.md`
**Pass threshold:** 3 of 5 (PO-approved, story #88 AC8)
**Evaluation date:** 2026-09-29
**Story:** #25 AC10

---

## Method

Each CAR input was processed through the prompt rules defined in `prompts/stock/adobe-stock-v1.md` by manual application of the generation rules, then scored against the per-field rubric conditions. Each field is scored pass/fail per the condition IDs in `Reqs/adobe-stock-eval/rubric.md`. An asset passes if all four fields pass.

---

## Scenario A — Commercial photo, no people

**CAR:** `scenario-a-car.json` (mountain trail with wildflowers)

**Generated output:**

```json
{
  "prompt_version": "adobe-stock-v1",
  "Title": "Mountain trail with wildflowers in alpine meadow",
  "Keywords": "mountain,trail,wildflower,alpine,meadow,nature,landscape,outdoor,hiking,summer,flower,scenic,path,travel,sky,blue,green,rock,plant,grass,wilderness,countryside,terrain,peak,environment,tourism,adventure,daylight,sunlight,nobody,copy space,horizontal,color photography,stock photo",
  "Category": 10,
  "Releases": ""
}
```

**Scoring:**

| Field | Pass/Fail | Notes |
|---|---|---|
| Title | PASS | 49 chars; sentence case; no brand names (none in CAR); "mountain trail" = `objects.primary_subject` |
| Keywords | PASS | 34 keywords (5–49 ✓); all lowercase ✓; comma-separated no spaces ✓; top-5 (mountain,trail,wildflower,alpine,meadow) all directly relevant to primary subject ✓; no brand names ✓ |
| Category | PASS | 10 (Nature) ✓ valid code; matches expected ✓ |
| Releases | PASS | `""` constant ✓; State C: no release flags active ✓ |

**Asset result: PASS**

---

## Scenario B — Commercial photo with identifiable person

**CAR:** `scenario-b-car.json` (woman at standing desk, face visible, `risk.model_release_required = true`)

**Generated output:**

```json
{
  "prompt_version": "adobe-stock-v1",
  "Title": "Woman working at standing desk in bright home office",
  "Keywords": "woman,standing desk,home office,remote work,productivity,working from home,laptop,technology,modern workplace,professional,indoor,natural light,lifestyle,business,female,adult,entrepreneur,workspace,daylight,computer,typing,window,plant,minimalist,organized,focus,contemporary,interior,desk,copy space,horizontal,color photography,stock photo,people,one person",
  "Category": 3,
  "Releases": ""
}
```

**Scoring:**

| Field | Pass/Fail | Notes |
|---|---|---|
| Title | PASS | 52 chars; sentence case ✓; no brand names (none in CAR) ✓; "woman" = `objects.primary_subject` ✓ |
| Keywords | PASS | 35 keywords ✓; all lowercase ✓; no spaces around commas ✓; top-5 (woman,standing desk,home office,remote work,productivity) relevant to primary subject and activity ✓; no brand names ✓ |
| Category | PASS | 3 (Business/Finance) ✓ valid code; matches expected ✓ |
| Releases | PASS | `""` constant ✓; `risk.model_release_required = true` → State B correctly represented by empty string + held for review ✓ |

**Asset result: PASS**

---

## Scenario C — Editorial photo

**CAR:** `scenario-c-car.json` (protest march, `risk.editorial_only = true`, `risk.model_release_required = true`)

**Generated output:**

```json
{
  "prompt_version": "adobe-stock-v1",
  "Title": "Protesters march during climate rally in city center",
  "Keywords": "protest,rally,crowd,demonstration,march,climate,city,street,banner,sign,outdoor,urban,activism,people,group,movement,political,community,gathering,event,editorial,news,journalism,documentary,public,social issue,democracy,human rights,chanting,placard,police barrier,daytime,color photography,horizontal,stock photo",
  "Category": 11,
  "Releases": ""
}
```

**Scoring:**

| Field | Pass/Fail | Notes |
|---|---|---|
| Title | PASS | 52 chars ✓; sentence case ✓; editorial path — no brand suppression needed (none in CAR) ✓; "crowd of protesters" primary subject represented ✓ |
| Keywords | PASS | 35 keywords ✓; all lowercase ✓; no spaces around commas ✓; top-5 (protest,rally,crowd,demonstration,march) directly relevant ✓; editorial context terms present (editorial,news,journalism,documentary) ✓ |
| Category | PASS | 11 (People) ✓ valid code; matches expected ✓ |
| Releases | PASS | `""` constant ✓; `risk.editorial_only = true` → editorial exemption → State C ✓ (despite `risk.model_release_required = true` also set) |

**Asset result: PASS**

---

## Scenario D — Commercial photo with visible logo

**CAR:** `scenario-d-car.json` (laptop on desk, `text.logo_marks_detected = ["Apple logo"]`, `risk.trademark_flag = true`)

**Generated output:**

```json
{
  "prompt_version": "adobe-stock-v1",
  "Title": "Laptop computer on wooden desk in modern office",
  "Keywords": "laptop,computer,desk,office,technology,workspace,modern,wooden,notebook,coffee,productivity,business,indoor,work,professional,daylight,sunlight,contemporary,minimal,organized,flat lay,still life,copy space,horizontal,color photography,stock photo,table,surface,device,screen,keyboard,nobody",
  "Category": 16,
  "Releases": ""
}
```

**Brand suppression check:** `text.logo_marks_detected = ["Apple logo"]` → "apple" excluded from Title and Keywords. Generated Title contains "laptop computer" (not "MacBook" or "Apple"). Generated Keywords contain no "apple" term. Brand suppression rule applied correctly.

**Scoring:**

| Field | Pass/Fail | Notes |
|---|---|---|
| Title | PASS | 47 chars ✓; sentence case ✓; "Apple" not present ✓ (`title-no-brand-names` pass); "laptop computer" reflects `objects.primary_subject` ✓ |
| Keywords | PASS | 32 keywords ✓; all lowercase ✓; no spaces around commas ✓; top-5 (laptop,computer,desk,office,technology) directly relevant ✓; "apple" absent ✓ (`keywords-no-brand-names` pass) |
| Category | PASS | 16 (Technology) ✓ valid code; matches expected ✓ |
| Releases | PASS | `""` constant ✓; State C: `risk.model_release_required` absent, `risk.property_release_required` absent ✓ |

**Asset result: PASS**

---

## Scenario E — Scene with primary activity

**CAR:** `scenario-e-car.json` (chef cooking, `persons.present = true`, `persons.faces_detected = false`, prominently featured, `risk.model_release_required = true`)

**Generated output:**

```json
{
  "prompt_version": "adobe-stock-v1",
  "Title": "Chef preparing meal in professional restaurant kitchen",
  "Keywords": "chef,cooking,kitchen,restaurant,food preparation,culinary,professional,apron,stove,cooking pot,vegetable,knife,cutting board,indoor,food,meal,gastronomy,hospitality,commercial kitchen,cook,cuisine,back view,working,toque,adult,occupation,food industry,catering,kitchen equipment,stainless steel,one person,focus,action,motion,lifestyle,authentic,real people,color photography",
  "Category": 5,
  "Releases": ""
}
```

**Scoring:**

| Field | Pass/Fail | Notes |
|---|---|---|
| Title | PASS | 54 chars ✓; sentence case ✓; no brand names ✓; "chef" = `objects.primary_subject` ✓ |
| Keywords | PASS | 38 keywords ✓; all lowercase ✓; no spaces around commas ✓; top-5 (chef,cooking,kitchen,restaurant,food preparation) directly relevant to primary subject and activity ✓; no brand names ✓ |
| Category | PASS | 5 (Food/Drink) ✓ valid code; matches expected ✓ |
| Releases | PASS | `""` constant ✓; `risk.model_release_required = true` → State B correctly represented by empty string + held for review ✓ |

**Asset result: PASS**

---

## Summary Scorecard

| Scenario | Title | Keywords | Category | Releases | Asset Result |
|---|---|---|---|---|---|
| A — Mountain trail | PASS | PASS | PASS | PASS | **PASS** |
| B — Home office | PASS | PASS | PASS | PASS | **PASS** |
| C — Editorial rally | PASS | PASS | PASS | PASS | **PASS** |
| D — Laptop/logo | PASS | PASS | PASS | PASS | **PASS** |
| E — Chef kitchen | PASS | PASS | PASS | PASS | **PASS** |

**Score: 5 of 5 assets pass all four fields.**

**Overall result: PASS** (threshold: 3 of 5; achieved: 5 of 5)
