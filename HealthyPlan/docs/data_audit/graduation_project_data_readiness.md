# HealthyPlan graduation-project data readiness

Audit date: 2026-07-14

## Feature readiness matrix

| Feature | Required data | Available files | Status | Main limitation | Required next action |
|---|---|---|---|---|---|
| User nutrition profile calculation | Age/sex/body measurements/activity state, equations, units, clinical exclusions | No profile/equation dataset or code; food and exercise tables only | Insufficient data | Repository contains no calculation specification or consumer code | Recover the intended BMR/TDEE/profile algorithm and authoritative citations |
| Daily calorie and macronutrient targets | Energy equations, goal adjustments, macro allocation rules, age/pregnancy/condition constraints | `single_food_items.csv`; partial health rules | Insufficient data | Food composition is not a target-setting model; several rule thresholds are individualized/missing | Document and test target algorithms separately from food data |
| Single-food recommendation | Broad foods, per-100-g nutrients, searchable names, quality flags | `single_food_items.csv` (4,652 foods) plus VTN/USDA raw sources | Usable with limitations | 4,059 rows need review; 3 negative values; translation corruption; important nutrient gaps | Exclude invalid rows, prioritize 593 currently unflagged rows, complete review of a curated Vietnamese subset |
| Vietnamese dish recommendation | Dish names, categories, regions, meals, servings, reliable nutrition | `composite_dishes.csv` (60 dishes) | Usable with limitations | Enough variety for a static demo, but totals are source-free and some are implausible | Use only as an explicitly provisional catalog until recipes are recovered |
| Dish nutrition calculation | Dish-to-ingredient mapping, grams, food IDs, yields, calculation script | No ingredient dataset | Missing | Required formula cannot be executed or verified | Recover `dish_ingredients`-equivalent data and transformation script |
| Rule-based nutrient filtering | Executable thresholds, units/basis, nutrient dictionary, complete food fields | `health_condition_nutrient_rules.csv`; `single_food_items.csv` | Insufficient data | 11 operand codes/28 rules have no food field; 28 thresholds blank; missing source versions | Restrict MVP to well-supported numeric rules such as sodium/fiber/fat after review; add schema/codebook |
| Health-condition-aware food filtering | Condition map, food nutrients, reviewed medical rules | Rules + single foods | Insufficient data | `diabetes` code mismatch; purine exists for only 82 foods; medical source snapshots incomplete | Create governed condition mapping and condition-specific coverage tests |
| Exercise recommendation by user group | Activity IDs, MET, group suitability, translations, contraindications | `exercise_activities.csv` (1,333 exact-source activities) and raw Compendium HTML | Usable with limitations | Excellent MET coverage; all contraindications blank and 166+ Vietnamese descriptions partly English | Curate a smaller reviewed activity subset for each group and add safety exclusions |
| Meal schedule generation | Reliable foods/dishes, meal tags, servings, targets, variety/allergy/condition constraints | 4,652 foods; 60 dishes with meal tags | Insufficient data | Can assemble a superficial schedule but cannot reliably calculate dish nutrients or meet health rules | Recover dish recipes and implement validated target/constraint logic |
| Exercise schedule generation | MET, duration, frequency, progression, recovery, limitations | 1,333 MET activities | Insufficient data | No duration/frequency/progression or condition contraindication data | Add evidence-backed scheduling rules and reviewed beginner/elderly/wheelchair plans |
| RAG health consultation | Authoritative sources, grounded chunks, safety language, human review | 19 source snapshots; 70 reviewed-file chunks | Usable with limitations | Six conditions and reasonable chunk lengths, but all 70 remain `needs_review`; no passage offsets | Complete medical/localization review and store exact supporting passages |
| Symptom/question routing | Representative utterances, supported labels, split/evaluation | 180 reviewed-file examples, balanced 30 per six conditions | Usable with limitations | All synthetic/unreviewed; 14 ambiguous; no train/dev/test split | Human-review labels and freeze stratified splits |
| Retrieval of relevant health knowledge | Searchable chunks, valid source links, query set | 70 chunks; 60 eval questions; all nonblank support IDs valid | Usable with limitations | Small domain coverage, one missing support link, no retrieval metrics | Fix `eval_0011`, freeze corpus, report Recall@k/MRR/nDCG and qualitative errors |
| Health advice for rules-only conditions outside RAG | RAG sources/chunks/routes per condition | Rules cover 24 conditions; RAG covers 6 | Missing | Eighteen rule domains have no RAG coverage | For the demo, clearly scope to six RAG conditions; do not imply 24-condition consultation |
| Complete graduation-project demo | Minimum viable data across food, dish, exercise, rules, RAG | All final candidate files | Usable with limitations | Static food/exercise/RAG demonstrations are feasible; reproducible dish calculation and defensible medical review are not | Narrow demo claims and finish the two critical recovery items |
| Realistic thesis evaluation section | Frozen datasets, provenance, splits, metrics, baselines, reviewer protocol, results | 60 RAG questions; data statistics in this audit | Insufficient data | No evaluation methodology/results, no routing split, all examples unreviewed, possible leakage cannot be ruled out | Define baselines/metrics, review annotations, freeze versions/hashes, run reproducible experiments |
| Medical diagnosis or treatment recommendation | Clinical validation, regulatory controls, clinician oversight, monitoring | Not provided and not an appropriate graduation-project expectation | Out of scope | HealthyPlan data supports education/recommendation prototypes only | State a non-diagnostic disclaimer and referral/escalation boundaries |

## Academic sufficiency

| Requirement | Assessment | Evidence |
|---|---|---|
| Clear dataset provenance | Partial | VTN PDF, USDA releases, Compendium and RAG HTML are preserved; dishes/rules/synthetic data are incomplete |
| Reproducible preprocessing | Missing | No scripts, notebooks, package lockfiles, commands, or run logs |
| Reliable source organizations | Mostly adequate where present | Ministry of Health/National Institute of Nutrition, USDA, CDC, NIH, AHA, ADA, NKF, WHO, professional guidelines |
| Preserved raw evidence | Mixed | Excellent for food/exercise/RAG sources; missing for dishes and most health rules |
| Validation results | Missing | No validation program or result artifact existed before this audit |
| Data statistics | Now available in audit reports | Counts, nulls, duplicates, ranges, relationships, and provenance were measured |
| Limitations | Major and now documented | Translation backlog, medical review, missing recipes, missing scripts, sparse condition nutrients |
| Ethical/medical disclaimers | Partial | Chunk/rule text includes cautions, but no project-wide policy or escalation design exists |
| Evaluation methodology | Insufficient | Evaluation examples exist, but no split, baseline, metric definition, annotator protocol, or results |

For the written thesis, the essential remaining work is not production-scale medical coverage. It is a reproducible and honest evidence package: recover scripts, preserve source versions, narrow claims, document limitations, freeze dataset hashes, and run a transparent evaluation.

## Functional demo sufficiency

The current data is enough to demonstrate:

- browsing/searching thousands of foods with per-100-g nutrients;
- recommending from a curated, reviewed subset of foods;
- browsing 60 Vietnamese dishes as provisional catalog items;
- recommending MET activities for adults, older adults, and wheelchair users;
- routing questions among six domains;
- retrieving short Vietnamese knowledge chunks for those six domains;
- showing static condition-rule examples with prominent prototype disclaimers.

The current data is not enough to credibly demonstrate:

- ingredient-derived dish nutrition;
- reliable condition-aware filtering across all 24 rule conditions;
- medically reviewed RAG answers;
- evidence-backed exercise prescriptions or condition-specific contraindications;
- a reproducible thesis pipeline and defensible final evaluation.

## What is required at each ambition level

### Functional graduation demo

Required now:

1. Recover dish recipes/ingredients or remove the dish-calculation claim.
2. Use only validated food rows and a narrow set of executable health rules.
3. Human-review the six-condition RAG corpus, routes, and evaluation examples.
4. Curate safe exercise subsets and clearly label MET as an energy-cost reference, not a prescription.
5. Add a prominent educational/non-diagnostic disclaimer.

### Written graduation thesis

Additionally required:

1. Recover and document the full processing pipeline.
2. Add source manifest, hashes, dates, versions, licenses/terms, and exact citations.
3. Freeze authoritative dataset versions and database schema/codebook.
4. Define experiment splits, baselines, metrics, error analysis, and limitations.
5. Record human reviewer roles and decisions.

### Production-grade medical application

This is beyond the graduation scope. It would additionally require clinical governance, validated contraindication/interaction logic, continuous guideline/version monitoring, privacy/security controls, audit logging, professional oversight, regulatory analysis, adverse-event handling, and post-deployment monitoring. The graduation project should not claim this level.

## Final conclusion

The repository has enough breadth for a constrained prototype: 4,652 foods, 1,333 exactly sourced activities, 60 provisional dishes, 89 rules, 19 preserved RAG sources, 70 chunks, 180 routing examples, and 60 evaluation questions. However, two critical gaps remain: the dish ingredient layer is absent, and none of the final datasets is reproducible from scripts. High-risk medical review, rule compatibility, translation quality, and evaluation provenance gaps mean the project can be demonstrated only with tightly scoped claims and prominent limitations.

READY WITH MAJOR LIMITATIONS
