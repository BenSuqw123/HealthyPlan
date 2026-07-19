# HealthyPlan data quality audit report

Audit date: 2026-07-14

## Severity summary

| Severity | Count | Meaning in this audit |
|---|---:|---|
| Critical | 2 | Blocks a required graduation-project capability or academic reproducibility |
| High | 7 | Materially risks incorrect recommendations, medical evidence, or defensible evaluation |
| Medium | 8 | Important cleanup/metadata/versioning weakness that does not alone block a demo |
| Low | 3 | Hygiene or clarity improvement |

## Critical and high-priority findings

| ID | Severity | Affected data | Finding | Evidence | Required action |
|---|---|---|---|---|---|
| C1 | Critical | All final datasets | No preprocessing/validation/export scripts or execution documentation exist | Repository contains only 88 data files under `data/` | Recover the actual scripts and environment lockfile; document deterministic order and manual steps |
| C2 | Critical | `composite_dishes.csv` | Dish ingredients, `food_id` mappings, and gram quantities are entirely absent | No `dish_ingredients`-like file exists; all 60 rows only say `ingredient_estimate` | Recover recipes, quantities, yield factors, source citations, and calculation script |
| H1 | High | `composite_dishes.csv` | Several nutrition values are implausible or unsupported | Sugarcane juice is 2.6 kcal/250 g; braised fish has 0 mg sodium; boiled chicken breast has 34.2 g fat and 723 mg sodium; bánh chưng/bánh tét share an identical nutrient vector | Revalidate every dish against preserved recipes; do not hand-edit the current file |
| H2 | High | `health_condition_nutrient_rules.csv` | Medical-rule provenance is incomplete | 41 of 42 URLs lack a local source snapshot; no exact edition/section/page; two rows use a confirmed 404 CDC URL | Preserve exact guideline/page versions and page locators; obtain medical reviewer sign-off |
| H3 | High | Health rules + foods + RAG | Rules are not consistently executable or joinable | 11 nutrient codes/28 rows have no food-schema field; `diabetes` in RAG does not equal `diabetes_type_1/2` in rules; GERD caffeine has duplicate `limit` and `monitor` rules | Add a governed nutrient dictionary and condition-code mapping; resolve duplicate semantics |
| H4 | High | `single_food_items.csv` | Invalid values, corrupted names, and very large review backlog | 3 negative VTN nutrients; 20 English names contain OCR nutrient-table text; 9 English names missing; 8 Vietnamese names contain legacy encoding corruption; 4,059/4,652 rows require manual review | Validate affected source pages and complete prioritized human translation/nutrition review |
| H5 | High | `rag_chunks_reviewed.csv`, registry | No human medical approval or passage-level traceability | All 70 rows are `needs_review`; 49 have quality flags; one diagnosis-risk flag; 44 added rows cite a missing script; no passage offsets | Human-review every chunk, store reviewer/date/status, and add exact supporting passage locators |
| H6 | High | Reviewed routing and evaluation | Synthetic generation and evaluation methodology are missing | 180/180 routing and 60/60 evaluation rows remain `needs_review`; 14 routing rows are ambiguous; `eval_0011` has no supporting chunk; no model/prompt/seed | Recover generation artifacts, review labels, define train/dev/test splits and leakage controls |
| H7 | High | `exercise_activities.csv` | Exercise safety/localization enrichment is not sufficient for personalized health advice | All 1,333 contraindication notes are blank; at least 166 Vietnamese descriptions retain obvious English fragments; suitability flags mirror source group rather than individual contraindications | Add reviewed translations and condition/limitation-specific safety rules; retain original MET values |

## Schema and missing-value findings

### `single_food_items.csv`

The file has unique `food_id`, `canonical_food_id`, and `(source_name, source_food_id)` keys. Numeric columns parse, but completeness varies materially.

| Field | Missing | Impact |
|---|---:|---|
| `purine_mg` | 4,570 | Only 82 foods can support purine-based gout filtering |
| `trans_fat_g` | 2,173 | Trans-fat rules cannot be applied consistently |
| `sugar_g` | 1,541 | Sugar filtering is incomplete; also not equivalent to added sugar |
| `saturated_fat_g` | 843 | Saturated-fat filtering has partial coverage |
| `cholesterol_mg` | 440 | Cholesterol filtering incomplete |
| `fiber_g` | 402 | Fiber prioritization incomplete |
| `zinc_mg` | 386 | Micronutrient filtering incomplete |
| `magnesium_mg` | 370 | Micronutrient filtering incomplete |
| `potassium_mg` | 341 | CKD/potassium filtering incomplete |
| `sodium_mg` | 300 | Hypertension/sodium filtering incomplete |
| `phosphorus_mg` | 167 | CKD/phosphorus filtering incomplete |
| `iron_mg` | 101 | Iron-anemia filtering incomplete |
| `fat_g` | 96 | Macro totals incomplete |
| `kcal_per_100g`, `carb_g` | 61 each | Calorie/macronutrient recommendations incomplete |
| `calcium_mg` | 52 | Bone-health filtering incomplete |
| `protein_g` | 16 | Macro recommendations incomplete |
| `name_en` | 9 | Search/display gap |

`brand_name` is blank for every row, but every row is also marked `is_branded=False`; this is consistent rather than a defect.

### `composite_dishes.csv`

No required field is blank, and IDs/names are unique. The schema itself is insufficient: it stores only totals, not the ingredients needed to generate them. Seven dishes have zero fiber and four have zero sodium; some zeros are plausible (e.g., plain ingredients), but zero sodium for a braised fish dish is not credible without a recipe.

### `exercise_activities.csv`

Every activity has IDs, descriptions, MET, source URL, access time, and hash. The only universally blank field is `contraindication_note` (1,333/1,333). MET values range 0.8-23.0 with no missing, nonpositive, or out-of-range values detected.

### `health_condition_nutrient_rules.csv`

Twenty-eight thresholds are blank. Many are intentionally marked `individualized`, but seven are `limit` rules and therefore cannot implement a numeric filter. Blank individualized thresholds are not inherently medically wrong; they are non-executable as machine thresholds and require a separate rule strategy.

## Invalid and suspicious numeric values

| File/record | Field/value | Assessment |
|---|---|---|
| `FOOD000096` / fish sauce grade I | `sugar_g=-3.0` | Invalid; likely missing-dash plus source-number OCR artifact |
| `FOOD000366` / vegetable butter | `iron_mg=-3.0` | Invalid; likely OCR/source-number artifact |
| `FOOD000472` / sardine | `zinc_mg=-4.0` | Invalid; likely OCR/source-number artifact |
| `FOOD000286` / Xương sông | 15 kcal but 9.469 g fat/100 g | Internally impossible under ordinary energy calculation; likely column extraction error |
| Seven Foundation food rows | Raw negative carbohydrate was converted to final `0.0` | Sensible normalization may be intended, but undocumented transformation is not reproducible |
| `DISH000056` / sugarcane juice | 2.6 kcal, 0.55 g carbohydrate per 250 g | Implausibly low and source-free; high likelihood of wrong ingredient/value |
| `DISH000033` / braised fish | 0 mg sodium per serving | Implausible for a dish normally prepared with salty seasoning; no recipe to verify |
| `DISH000060` / boiled chicken breast | 409.5 kcal, 34.2 g fat, 723 mg sodium per 150 g | Suspicious for the stated dish; resembles a copied/incorrect ingredient profile |

Atwater screening found 25 foods with an absolute difference over 50 kcal between stored energy and `4P+9F+4C`. Many high-fiber USDA foods legitimately diverge because carbohydrate-by-difference includes fiber and energy uses source-specific factors. These are review candidates, not automatically errors. The Xương sông row remains clearly inconsistent.

## Duplicates and naming quality

- No exact duplicate rows were found in any project CSV.
- No duplicate primary IDs were found in final CSVs.
- `single_food_items.csv` has 106 normalized Vietnamese-name duplicate groups. Most represent the same USDA food appearing in Foundation and SR versions; canonical IDs do not unify them, so recommendation deduplication is needed.
- Bánh chưng and bánh tét have exactly the same six nutrient totals. This may be a deliberate shared recipe estimate, but no evidence exists.
- Twenty VTN `name_en` values begin with OCR content such as “Magiê (Magnesium) ...” rather than a food name.
- Eight Vietnamese names retain corrupted legacy characters such as `đÆc`, `ViÖt`, and `NghÖ`.
- USDA-derived Vietnamese translations are frequently mixed-language. The file itself marks 4,059 rows for manual review, including 2,295 `low_confidence_translation` rows and 1,046 `low_confidence_translation; technical_cut_name` rows.
- At least 166 exercise `description_vi` fields contain obvious English fragments; this count is conservative.

## Relationship checks

| Relationship | Result |
|---|---|
| `dish_ingredients.dish_id -> dishes` | Cannot test; ingredient table missing |
| `dish_ingredients.food_id -> foods` | Cannot test; ingredient table missing |
| USDA final source IDs -> raw `food.csv` | 380/380 Foundation and 3,745/3,745 SR IDs matched |
| Exercise `(source, code)` -> raw HTML | 1,333/1,333 matched; MET and English description exact |
| RAG chunk `source_id -> source_registry` | 70/70 valid |
| RAG source metadata -> registry | Titles, URLs, and organizations all match |
| RAG chunk condition -> registry condition | 69/70 match; `expanded_prediabetes_004` reuses a diabetes source |
| Eval `supporting_chunk_ids -> reviewed chunks` | All nonblank IDs valid; `eval_0011` has no support ID |
| Router condition -> reviewed chunk conditions | Complete for six RAG domains |
| Rule condition -> RAG condition | Broken for diabetes (`diabetes` vs `diabetes_type_1/2`); rules also contain 18 domains absent from RAG |
| Rule nutrient -> food field | 11 codes/28 rule rows lack a corresponding field |

The 11 unsupported rule codes are `added_sugar`, `alcohol`, `caffeine`, `folate`, `omega_3`, `refined_grain`, `sugar_sweetened_beverage`, `ultra_processed_food`, `vitamin_b12`, `vitamin_d`, and `vitamins`. Some are food attributes rather than numeric nutrients; the schema needs explicit typed rule operands rather than pretending every rule maps to a nutrient column.

## RAG quality findings

Positive structural results:

- No duplicate chunk IDs, exact/normalized duplicate chunk texts, orphan source IDs, heading-only chunks, or empty chunks.
- Chunk length is consistent: 354-525 characters, median 404.5.
- Router data is balanced at 30 examples for each of six conditions; only one high-similarity pair (similarity >= 0.82) was found, within obesity.
- The RAG evaluation set is balanced at 10 examples per condition.

Material limitations:

- All chunks, routes, and evaluation examples remain `needs_review`; filenames containing `reviewed` do not mean human-approved.
- Forty-four of 70 chunks, 60 of 180 routing examples, and 12 of 60 evaluation examples were added relative to base files without generation artifacts.
- Review notes are highly templated/repeated and explicitly describe automated review. They are not evidence of medical review.
- `nkf_nutrition_hub` is registered and preserved but unused by any reviewed chunk.
- No chunk stores source passage offsets, section headings, page anchors, extraction hash, or source snapshot hash.
- No router train/dev/test split exists. Because generation and evaluation methodology is missing, data leakage or prompt-template contamination cannot be ruled out.
- No semantic contradiction test or clinician adjudication exists. Structural scanning did not find explicit duplicate contradictions, but that is not a medical validation.

## Raw-source quality observations

- USDA SR raw foreign-key-like relationships are complete for the inspected files.
- Foundation `food_nutrient.csv` has 33 blank-amount rows for nutrient ID 2066, which is absent from the included nutrient lookup, and 10 negative carbohydrate-by-difference values. These are raw-release anomalies; seven negatives were selected and clamped to zero in the final file.
- Foundation `food_portion.csv` has 273 rows with blank `fdc_id` and `measure_unit_id`; nonblank keys join successfully.
- RAG extracted text has no replacement characters and very high token overlap with HTML; `nkf_potassium_ckd_diet` is the only notable lower-overlap case at 89.4%.

## Lower-priority findings

| Severity | Finding | Action |
|---|---|---|
| Medium | “Reviewed” filenames are supersets but authority is undocumented | Add dataset manifest with authoritative filename/version/hash |
| Medium | Registry has no download date/hash/publication date/license | Add immutable source metadata |
| Medium | All RAG downloads say `downloaded_unverified_tls` | Reacquire/verify with standard TLS and record method without deleting old evidence |
| Medium | Same health-rule URL uses multiple source labels | Normalize source registry and reference source IDs |
| Medium | Exercise suitability flags equal source group rather than reviewed capability | Add eligibility rationale and exceptions |
| Medium | Purine coverage is only 82 foods | Restrict gout demo scope or acquire cited purine data |
| Medium | Per-100-g basis is explicit only in `kcal_per_100g`, not every nutrient field | Add schema/data dictionary that states basis and unit |
| Medium | No database schema or constraints exist | Add schema with primary/foreign keys and enums |
| Low | Folder name `dished_excercises` is misspelled | Document current path; rename only in a controlled migration after consumers exist |
| Low | Source registry leaves one source unused | Document intentional reserve or remove only after owner review |
| Low | USDA support files duplicate across releases | Retain as release evidence; optionally archive whole release packages together |

## Overall data-quality judgment

The exercise MET data is technically strong and exactly traceable. Food data is broad but needs targeted invalid-value correction and substantial translation review. RAG structure is clean but medically unapproved. Health rules and dish nutrition are the highest-risk functional datasets: the former lacks preserved source versions and schema compatibility, while the latter lacks the source recipe layer entirely.
