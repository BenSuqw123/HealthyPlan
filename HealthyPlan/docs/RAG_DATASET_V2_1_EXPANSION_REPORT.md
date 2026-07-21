# HealthyPlan RAG Dataset V2.1 Expansion Report

This report documents the expansion and quality assurance of the HealthyPlan RAG Dataset V2.1 prior to building Vector Database V1.

---

## 1. Dataset Summary
* **Original V2 Chunk Count**: 116
* **V2.1 Expanded Chunk Count**: 205
* **Original V2 Source Count**: 27
* **New Accepted Source Count**: 7
* **Total Accepted Source Count**: 34
* **Rejected Source Count**: 3
* **HTML Source Count**: 33
* **PDF Source Count**: 1 (`kdigo_2024_ckd_guideline.pdf`)
* **Evaluation Question Count**: 75 (25 inherited, 50 newly added)
* **Validation Status**: **PASS**

---

## 2. Condition Code Distribution

| condition_code | V2 chunks | V2.1 chunks | source count | verdict |
| --- | --- | --- | --- | --- |
| `diabetes_type_1` | 9 | 16 | 4 | **PASSED** |
| `diabetes_type_2` | 10 | 20 | 4 | **PASSED** |
| `diabetes_type_unknown` | 4 | 7 | 3 | **PASSED** |
| `prediabetes` | 8 | 15 | 3 | **PASSED** |
| `hypertension` | 9 | 18 | 5 | **PASSED** |
| `ckd_g1` | 5 | 8 | 3 | **PASSED** |
| `ckd_g2` | 5 | 8 | 3 | **PASSED** |
| `ckd_g3a` | 7 | 11 | 3 | **PASSED** |
| `ckd_g3b` | 7 | 11 | 3 | **PASSED** |
| `ckd_g4` | 8 | 13 | 4 | **PASSED** |
| `ckd_g5_non_dialysis`| 8 | 13 | 4 | **PASSED** |
| `ckd_dialysis` | 7 | 13 | 3 | **PASSED** |
| `ckd_stage_unknown` | 4 | 7 | 3 | **PASSED** |
| `gout` | 10 | 18 | 4 | **PASSED** |
| `obesity` | 8 | 16 | 5 | **PASSED** |
| `general_safety` | 7 | 11 | 5 | **PASSED** |
| **Total** | **116** | **205** | **34** | **PASSED** |

---

## 3. Source Quality Gate

The following new sources were added to Dataset V2.1 after passing the Quality Gate:

| source_id | publisher | source type | condition | topics | accepted/rejected |
| --- | --- | --- | --- | --- | --- |
| `ada_alcohol_safety` | American Diabetes Association | HTML | `diabetes` | Alcohol consumption, delayed hypoglycemia | **accepted** (Tier 1) |
| `cdc_prediabetes_monitoring` | CDC | HTML | `prediabetes` | HbA1c tests, screening, lifestyle prevention | **accepted** (Tier 1) |
| `aha_dash_diet` | American Heart Association | HTML | `hypertension` | DASH eating plan, sodium limits | **accepted** (Tier 1) |
| `nkf_gout_ckd` | National Kidney Foundation | HTML | `ckd` | Gout and CKD link, hyperuricemia | **accepted** (Tier 1) |
| `nih_sleep_weight` | NIH | HTML | `obesity` | Sleep and appetite hormones, ghrelin, leptin | **accepted** (Tier 1) |
| `medlineplus_caffeine` | NIH MedlinePlus | HTML | `hypertension` | Caffeine vasoconstriction, blood pressure rise | **accepted** (Tier 1) |
| `who_obesity_guidelines` | WHO | HTML | `obesity` | Obesity criteria, energy balance parameters | **accepted** (Tier 1) |

### Rejected Sources
The following sources were inspected and rejected from the dataset:

* `http://www.goutdiettipsblog.com` (Reason: Personal blog with commercial ads and unverified author).
* `https://www.supplementworld.org/obesity-cure` (Reason: Commercial supplement seller with marketing bias).
* `https://www.healthline-seo-copy.com/hypertension` (Reason: SEO-generated health article lacking peer review or medical authority).

---

## 4. Topic Coverage & Additions

| condition_code | new topics | new chunk IDs |
| --- | --- | --- |
| `diabetes_type_1` | Timezone travel adjustments, sick days management, alcohol delayed hypoglycemia, carb counting measuring tools, bolus meal skip warnings, severe low rescue glucagon, rule of 15 | `diabetes_t1_010` to `diabetes_t1_016` |
| `diabetes_type_2` | Resistance training, dining out tips, label reading, breakfast and snacks guidelines, diabetic nephropathy screening, sulfonylurea hypo risks, 150 minutes weekly aerobic activity, sodium limits | `diabetes_t2_011` to `diabetes_t2_020` |
| `diabetes_type_unknown` | General safe nutrition, type classification differences, medication change warnings | `diabetes_unknown_005` to `diabetes_unknown_007` |
| `prediabetes` | Sugary drinks/milk tea warnings, postprandial walking, sleep hormone impacts, complex carbs, progression risk factors, HbA1c monitoring frequency, prevention programs | `prediabetes_009` to `prediabetes_015` |
| `hypertension` | Soy sauce, instant noodles, processed meat warnings, nutrition facts sodium %DV, DASH eating plan, caffeine vasoconstriction, alcohol limits, aerobic activity, home blood pressure sitting posture | `hypertension_010` to `hypertension_018` |
| `ckd_g1` | Glycemic control targets, fat restrictions, adequate hydration | `ckd_g1_006` to `ckd_g1_008` |
| `ckd_g2` | ACEi/ARB renal protection, herbal supplement caution, aerobic physical activity | `ckd_g2_006` to `ckd_g2_008` |
| `ckd_g3a` | Moderate protein target (0.6-0.8), phosphorus additives, anemia screening, iodinated contrast preparation | `ckd_g3a_008` to `ckd_g3a_011` |
| `ckd_g3b` | Plant protein substitution, potassium restriction (>5.0 mEq/L), calcium-phosphorus tracking, renally cleared drug adjustments | `ckd_g3b_008` to `ckd_g3b_011` |
| `ckd_g4` | Metabolic acidosis bicarbonate therapy, Hepatitis B vaccination, peripheral vein preservation, potassium chloride salt alternatives, MBD bone tracking | `ckd_g4_009` to `ckd_g4_013` |
| `ckd_g5_non_dialysis`| Bicarbonate target level (>22), phosphate binder meal timing, plant-based phosphorus absorption (30-40%), uremic syndrome warning, metformin contraindication | `ckd_g5_nondialysis_009` to `ckd_g5_nondialysis_013` |
| `ckd_dialysis` | Hemodialysis interdialytic weight gain (3-5%), peritoneal dialysis fluid/potassium safety, peritoneal dialysis protein target (1.2), hemodialysis access protection (AVF), water-soluble vitamin loss | `ckd_dialysis_008` to `ckd_dialysis_013` |
| `ckd_stage_unknown` | Stage-unspecified low-sodium diet, staging diagnostics (eGFR/UACR), NSAID contraindication | `ckd_unknown_005` to `ckd_unknown_007` |
| `gout` | Meat broths, vegetable purines safety, low-fat dairy, rapid weight loss risk, Gout-CKD link, uric acid target (<6.0), distilled spirits, diet limitations vs medication | `gout_011` to `gout_018` |
| `obesity` | Emotional eating coping, sleep ghrelin/leptin hormone link, low energy density foods, protein satiety, weight loss rate (0.5-1.0 kg/week), weight maintenance physical activity, visceral fat, blood pressure drop | `obesity_009` to `obesity_016` |
| `general_safety` | Geriatric sarcopenic obesity frailty, eating disorders exception, incomplete test data, complex comorbidities conflict, emergency chest pain / stroke FAST | `safety_008` to `safety_011` |

---

## 5. Numerical Claims Review
* **Verified Count**: 55 (All clinical parameters checked)
* **Rejected Count**: 0
* **Requires Clinical Review**: 0
* **Status**: 100% verified against KDIGO, CDC, ADA, and AHA sources. All claims are stored in `numerical_claims_review_v2_1.csv` with status `verified_against_source`.

---

## 6. Duplication Audit Results
* **Exact Duplicates**: 0
* **Near Duplicates (>0.8 Jaccard)**: 0
* **Medically Necessary Overlaps**: High similarity pairs (e.g. CKD stage protein targets) are verified as medically necessary overlaps where sharing terminology is critical for retrieval.

---

## 7. Protected Files Integrity
* **Protected Checksums Logged**: True (`scratch/protected_checksums.json`)
* **Post-Execution Check**: All 17 protected V1 and V2 source code, data, and report files match their pre-execution checksums exactly.

---

## 8. Pipeline Execution Log

All pipeline scripts were run sequentially:

| Command | Exit Code | Result |
| --- | --- | --- |
| `python scripts/collect_rag_sources_v2_1.py` | 0 | Sources copied and new sources collected. |
| `python scripts/extract_rag_sources_v2_1.py` | 0 | Raw HTML/PDF parsed to clean text. |
| `python scripts/build_rag_chunks_v2_1.py` | 0 | Combined CSVs and numerical claims generated. |
| `python scripts/build_rag_eval_set_v2_1.py` | 0 | Evaluation set expanded to 75 questions. |
| `python scripts/validate_rag_dataset_v2_1.py` | 0 | ALL DETERMINISTIC CHECKS PASSED. |

---

## 9. Limitations & Medical Disclaimers
* **Clinical Review**: `medical_review_status = not_reviewed_by_clinician`
* **Prototype Use Only**: The dataset is intended solely for academic thesis evaluation and RAG demonstration.
* **Calculations**: Personalized nutrient calculations remain outside the RAG retrieval scope.
* **Rule Engine**: The Rule Engine has not yet been implemented.

---

## 10. Final Verdict

# **`READY_FOR_VECTOR_DB_V1`**
All files are correctly structured, referential integrity is complete, 100% of numerical claims are verified, and the validation script reports PASS.
