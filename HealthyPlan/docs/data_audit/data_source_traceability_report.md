# HealthyPlan data source traceability report

Audit date: 2026-07-14

## Executive result

No final dataset has complete academic traceability because no collection, extraction, transformation, translation, merge, chunking, review, or export script is present. Source evidence is nevertheless strong for the activity dataset and the USDA portion of the single-food dataset.

| Final file | Original source | Preserved raw file/evidence | Transformation scripts | Traceability status | Principal missing evidence |
|---|---|---|---|---|---|
| `single_food_items.csv` | Vietnam Food Composition Table 2007; USDA Foundation Foods 04/2026; USDA SR Legacy 04/2018 | VTN PDF and 13 USDA CSV files | None found | Partial/strong row evidence | PDF extractor, USDA selection rules, translation method, fallback logic, checksums, manifest |
| `exercise_activities.csv` | 2024 Adult Compendium; Older Adult Compendium; Wheelchair Compendium | 25 HTML snapshots | None found | Strong row evidence, not reproducible | Parser, translation rules, suitability derivation, hash method |
| `health_condition_nutrient_rules.csv` | 42 distinct guideline/web URLs | Only one exact URL is also preserved as a local RAG snapshot | None found | Incomplete/high risk | 41 source snapshots, title/year/version/page locator, rule-extraction method, medical approval |
| `composite_dishes.csv` | Claimed `ingredient_estimate` | None | None found | Missing | Dish recipes, ingredient IDs, gram amounts, yield factors, citations, calculation script |
| `source_registry.csv` | 19 public-health webpages | 19 HTML plus 19 extracted-text files | None found | Partial/strong source evidence | Download timestamp, HTTP/TLS evidence, checksum, publication date/version, actual reuse license |
| `rag_chunks_reviewed.csv` | 19 registered webpages | All registered HTML/text pairs | None found | Partial | Passage/page offsets, chunking/paraphrase method, version history, human review sign-off |
| `symptom_condition_mapping_reviewed.csv` | Synthetic LLM-assisted utterances | No prompt/model/run artifact | None found | Incomplete | Model/version, prompt, seed, author, generation date, acceptance protocol |
| `rag_eval_set_reviewed.csv` | Synthetic/manual evaluation questions linked to chunks | No generation artifact; partial downstream chunk links | None found | Incomplete | Design protocol, annotator, leakage controls, acceptance criteria, one missing chunk link |

## 1. Single-food nutrition data

### Preserved sources

- `data/raw/VTN_FCT_2007.pdf`: 567-page *Bảng thành phần thực phẩm Việt Nam / Vietnamese Food Composition Table*, Ministry of Health, National Institute of Nutrition, Medical Publishing House, 2007. The PDF records editor/author information, year, food codes, per-100-g edible-portion values, units, and per-value source-number notation. It contains 527 foods used in the final file.
- `data/raw/FoodData_Central_foundation_food_csv_2026-04-30/`: USDA FoodData Central Foundation Foods April 2026 release. The official download listing confirms Foundation Foods 04/2026 and the update log identifies FoodData Central Version 15.0 dated 2026-04-30: [USDA downloadable data](https://fdc.nal.usda.gov/download-datasets/), [USDA update log](https://fdc.nal.usda.gov/log/).
- `data/raw/FoodData_Central_sr_legacy_food_csv_2018-04/`: USDA FoodData Central SR Legacy final April 2018 release, confirmed by the [USDA download listing](https://fdc.nal.usda.gov/download-datasets/).

### Verified row-level linkage

| Final source label | Final rows | Source key check | Nutrient-value check |
|---|---:|---|---|
| `VTN_FCT_2007` | 527 | `source_food_id` stores the book food code; representative pages visually verified | Source can be checked by code, but no extraction mapping or page number is stored |
| `Foundation Foods` | 380 | All 380 `source_food_id` values exist as `foundation_food` records in raw `food.csv` | Directly stored core nutrients match raw rows except 7 raw negative carbohydrate-by-difference values changed to `0.0`; change is undocumented |
| `SR Legacy` | 3,745 | All 3,745 source IDs exist in raw `food.csv` | Directly stored core nutrients checked in the audit match raw nutrient rows |

The file also contains 85 fallback-source rows, but the algorithm deciding when and how to use a fallback is absent. Source names and IDs make many rows auditable, but translation, food selection, normalization, canonical-ID generation, and fallback selection are not reproducible.

The three negative VTN values in the final file (`sugar_g=-3`, `iron_mg=-3`, `zinc_mg=-4`) strongly match the PDF’s notation pattern “missing dash + source-number 3/4” and therefore appear to be extraction artifacts, not real negative nutrient measurements. This is an inference from the source layout and must be confirmed on the three affected PDF food pages before correction.

### Missing metadata

- No repository source manifest lists official URLs, archive filenames, hashes, license/terms, or download dates.
- The USDA release folders encode versions, but the official download URL is not recorded locally.
- The VTN PDF has organization/title/year internally, but no repository citation record or stable acquisition URL.
- No record explains why 380 of 469 Foundation foods and 3,745 of 7,793 SR foods were selected.
- No record identifies the translation model, dictionary, human reviewer, or review date.

## 2. Vietnamese dishes

`composite_dishes.csv` has 60 serving-level rows, and every row declares `source=ingredient_estimate`. No dish-definition source, recipe, ingredient mapping, quantity, edible yield, cooking-retention factor, or calculation input exists.

The required formula cannot be reproduced:

`dish nutrient = sum(food nutrient per 100 g × ingredient grams / 100)`

There is no `dish_ingredients` dataset and therefore no `dish_id -> food_id` or gram-quantity lineage. The output is not traceable to `single_food_items.csv`, even though its energy values are internally close to `4×protein + 9×fat + 4×carbohydrate`. This arithmetic consistency does not prove the ingredient estimates are correct.

Traceability status: **missing; blocks reproducible dish nutrition**.

## 3. Exercise and MET data

The final file contains 1,110 adult, 99 older-adult, and 124 wheelchair activities. The raw sources are preserved in `data/raw/compendium/`.

Audit parsing found exactly 1,333 raw activity rows after removing HTML table headers/blank rows. Joining on `(source_compendium, source_activity_code)` produced:

- 1,333 matched rows;
- 0 final-only or raw-only rows;
- 0 MET mismatches;
- 0 normalized English-description mismatches;
- 0 duplicate source keys.

This is the strongest row-level source relationship in the repository. The final file also stores source URLs and `source_accessed_at=2026-07-04T07:32:45Z`.

What remains missing is the parser, the Vietnamese translation method, the rules that assign intensity/beginner/elderly/wheelchair flags, and the row-hash algorithm. Source pages include the 2024 Adult Compendium label; the repository does not include a formal citation entry or source version for the older-adult and wheelchair tables.

Traceability status: **strong raw-to-final evidence but non-reproducible transformation**.

## 4. Nutrient and health-risk rules

The rules file has 89 rows and 42 distinct URLs, all with a single access time (`2026-07-04T09:28:54Z`). Only the AHA “Shaking the Salt Habit” URL is also preserved locally among RAG snapshots. Thus, 41 distinct rule sources lack a source snapshot or downloaded guideline/PDF.

Metadata weaknesses:

- No source publication year, guideline version, section/table/page locator, quotation, or source snapshot is stored per rule.
- 42 URLs are represented by 78 different `(source_name, source_url)` pairs; the same URL has as many as five different source labels.
- Generic landing pages such as AASLD practice guidelines and DietaryGuidelines.gov do not identify the exact document that supports a row.
- Two obesity rules use `https://www.cdc.gov/healthyweight/healthy_eating/index.html`, confirmed as 404 during the audit. The current CDC page is [Tips for Healthy Eating for a Healthy Weight](https://www.cdc.gov/healthy-weight-growth/healthy-eating/index.html).
- NKF phosphorus/potassium and NHLBI DASH links redirect to newer paths. Redirects are not necessarily broken, but they show why version/date snapshots are required.
- WHO’s Healthy Diet page was updated in 2026; because the file has no publication/version field, it cannot prove which page version supported the stored rules. See [WHO Healthy Diet](https://www.who.int/news-room/fact-sheets/detail/healthy-diet).

Traceability status: **incomplete and unsuitable as thesis evidence until exact source versions are preserved**.

## 5. RAG source registry and source documents

All 19 source IDs have both `html/<source_id>.html` and `extracted_text/<source_id>.txt`. All text files contain non-empty content with no Unicode replacement characters. Token coverage of extracted text in visible HTML is 89.4%-100%, with the lowest match for `nkf_potassium_ckd_diet`; that source needs an extraction-rule review.

| Condition | Registered sources | Organizations |
|---|---:|---|
| diabetes | 4 | ADA, CDC |
| prediabetes | 2 | CDC |
| hypertension | 3 | AHA, CDC |
| chronic_kidney_disease | 4 | NKF, NIH MedlinePlus |
| gout | 3 | NIH MedlinePlus |
| obesity | 3 | CDC, NIH MedlinePlus |

The registry records organization, title, URL, type, priority, and status, but all 19 rows say `downloaded_unverified_tls` and `draft`. It lacks download timestamp, content hash, publication/update date, webpage version, retrieval tool, and genuine license/terms. The generic chunk `license_note` is a project-use statement, not proof that the source permits a particular reuse.

## 6. Reviewed RAG chunks

All 70 chunks reference existing registry source IDs; source titles, URLs, and organizations match the registry. One cross-condition linkage exists: `expanded_prediabetes_004` uses source `cdc_diabetes_meal_planning`, whose registry condition is `diabetes`. The reuse may be substantively reasonable, but the registry schema needs multi-condition support or an explicit cross-domain mapping.

The reviewed file is a superset, not simply a reviewed copy: it adds 44 chunk IDs to the 26-row base. Review notes explicitly say those 44 were script-generated, but the script, prompt, model, and run log are absent. There are no passage offsets or supporting excerpts linking a paraphrased chunk to exact source text.

Traceability status: **source-level traceable; passage-level and generation traceability incomplete**.

## 7. Routing and evaluation data

`symptom_condition_mapping_reviewed.csv` adds 60 examples to the 120-row base. All 180 are labeled `synthetic_llm_assisted` and `needs_review`; no model, prompt, seed, author, or generation run is retained. Fourteen rows are already flagged `ambiguous_mapping`.

`rag_eval_set_reviewed.csv` adds 12 examples to the 48-row base. All 60 remain `needs_review`. `eval_0011` has no `supporting_chunk_ids`; every other listed support ID exists in `rag_chunks_reviewed.csv`. No evaluation-design protocol, annotator agreement, difficulty stratification, or leakage-control record exists.

Traceability status: **incomplete; acceptable only as provisional synthetic prototype material**.

## Final traceability conclusion

- Fully traceable final datasets under the strict academic definition: **0/8**.
- Strong raw-to-row evidence: **2/8** (`exercise_activities.csv`; USDA portion of `single_food_items.csv`).
- Final datasets missing original raw/generation evidence: **4/8** (`composite_dishes.csv`, `health_condition_nutrient_rules.csv`, reviewed routing, reviewed evaluation).
- Final datasets lacking adequate source/generation documentation: **3/8** (dishes, reviewed routing, reviewed evaluation); the other five still have material metadata or processing gaps.
