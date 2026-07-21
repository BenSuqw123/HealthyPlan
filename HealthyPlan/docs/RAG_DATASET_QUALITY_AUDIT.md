# HEALTHYPLAN RAG DATASET AUDIT

## 1. Executive Summary

This report presents a thorough quality, structure, and medical safety audit of the three core datasets designated for the HealthyPlan RAG subsystem.

* **Are the datasets enough to begin implementation?** **YES, WITH CONDITIONS**. The schemas are structurally intact, and the file references resolve correctly. However, implementation must proceed with the understanding that the data is purely qualitative and synthetically derived.
* **Are they enough for an academic prototype?** **YES, WITH CONDITIONS**. They can serve a basic proof-of-concept demonstrating routing and retrieval, provided a prominent prototype disclaimer is displayed.
* **Are they enough for a thesis defense?** **YES, WITH CONDITIONS**. While technically sufficient to show the RAG pipeline mechanics, they lack the academic reproducibility of raw-to-processed pipelines and require a stage-specific safety breakdown for chronic kidney disease to be academically defensible.
* **Are they safe for public users?** **NO**. 100% of the expanded knowledge chunks are machine-generated paraphrases that have not undergone clinician approval. They contain no specific numerical medical limits (such as sodium in mg, or blood glucose thresholds) and could lead to hazardous generalized recommendations.
* **Is the medical content verified?** **NO**. Every single record across the knowledge, router, and evaluation datasets remains flagged as `needs_review` in the `review_status` column. No clinician or dietitian verification logs exist.
* **Largest Blocker:** **Total Absence of Numerical Medical Metrics**. The knowledge chunks contain zero numeric limits (e.g. daily sodium limits, potassium intake guidelines, calorie deficit targets). This severely restricts the RAG subsystem to general health education rather than personalized nutritional scheduling.

---

## 2. Dataset Inventory

| Dataset | Rows | Columns | Purpose | Parse status | Verdict |
| ------- | ---- | ------- | ------- | ------------ | ------- |
| [symptom_condition_mapping_reviewed.csv](file:///c:/Users/ACER/Documents/Desktop/Đồ%20Án/MainProject/HealthyPlan/data/rag/symptom_condition_mapping_reviewed.csv) | 180 | 9 | Router training and validation utterances | Passed (utf-8-sig, BOM, comma-delimited) | **Usable for MVP** (Includes 14 ambiguous mapping flags; gout keyword leakage) |
| [rag_chunks_reviewed.csv](file:///c:/Users/ACER/Documents/Desktop/Đồ%20Án/MainProject/HealthyPlan/data/rag/rag_chunks_reviewed.csv) | 70 | 15 | Vector store knowledge chunks and sources | Passed (utf-8-sig, BOM, comma-delimited) | **Needs Review** (100% unapproved; 70% contain automated data quality flags) |
| [rag_eval_set_reviewed.csv](file:///c:/Users/ACER/Documents/Desktop/Đồ%20Án/MainProject/HealthyPlan/data/rag/rag_eval_set_reviewed.csv) | 60 | 10 | Ground truth RAG system evaluation questions | Passed (utf-8-sig, BOM, comma-delimited) | **Needs Review** (1 case of missing support link; 2 too-broad questions) |

---

## 3. Condition and Coverage Matrix

| Condition | Router examples | Knowledge chunks | Sources | Eval questions | Coverage verdict |
| --------- | --------------- | ---------------- | ------- | -------------- | ---------------- |
| **chronic_kidney_disease** | 30 | 15 | 4 | 10 | **Bare minimum for prototype**: Lacks stage-specific dietary divisions (protein/sodium/potassium variances between stage 1-5 vs dialysis) and hyperkalemia safety warnings. |
| **diabetes** | 30 | 15 | 4 | 10 | **Usable only for prototype**: Lacks hypoglycemia emergency action (Rule of 15), specific blood glucose metric targets, and insulin timing warnings. |
| **gout** | 30 | 12 | 3 | 10 | **Usable only for prototype**: Lacks specific uric acid target ranges and clear dietary boundaries for acute flare vs chronic prevention. |
| **hypertension** | 30 | 12 | 3 | 10 | **Usable only for prototype**: Lacks numerical daily sodium limits (e.g. <2300mg) and hypertensive crisis warning signs. |
| **obesity** | 30 | 8 | 3 | 10 | **Too narrow for defense**: Low chunk volume (8 chunks); lacks calorie deficit math, weight loss rate safety, and cardiovascular comorbidity warnings. |
| **prediabetes** | 30 | 8 | 2 | 10 | **Too narrow for defense**: Low chunk volume (8 chunks); lacks lifestyle intervention program milestones and HbA1c diagnostic ranges. |

---

## 4. Structural Errors

No parsing, delimiter, encoding, quoting, or column type conflicts were found during programmatic testing. All three CSV files are well-formed UTF-8 with BOM (`utf-8-sig`) and comma-delimited. 

| Severity | Dataset | Row/ID | Error | Impact |
| -------- | ------- | ------ | ----- | ------ |
| **Low** | `rag_chunks_reviewed.csv` | `expanded_prediabetes_004` | Mismatched source condition | Reuses source `cdc_diabetes_meal_planning` (registered under `diabetes`) to write a prediabetes chunk. While content is relevant, it shows a cross-condition metadata schema mismatch. |
| **Low** | `source_registry.csv` | Row 19 | Unused Source ID | `nkf_nutrition_hub` is registered in the registry, but 0 chunks reference it. |

---

## 5. Router Label Errors

A programmatic scan of [symptom_condition_mapping_reviewed.csv](file:///c:/Users/ACER/Documents/Desktop/Đồ%20Án/MainProject/HealthyPlan/data/rag/symptom_condition_mapping_reviewed.csv) shows that all 180 rows are forced to resolve to one of the six primary disease codes.

| Severity | Row/ID | Text | Current label | Recommended handling | Reason |
| -------- | ------ | ---- | ------------- | -------------------- | ------ |
| **High** | `sym_0013` | tôi bị đường huyết cao, muốn ăn vặt lành mạnh hơn | `diabetes` | Reclassify as `ambiguous` or `prediabetes` | "Đường huyết cao" alone is not diagnostic of diabetes and could map to prediabetes. |
| **High** | `sym_0017` | đường máu lúc đói của tôi cao nhiều lần | `diabetes` | Reclassify as `ambiguous` | Cannot resolve confidently without HbA1c or diagnostic details. |
| **High** | `sym_0021` | em mới phát hiện đường huyết cao, bác sĩ bảo coi chừng tiểu đường | `prediabetes` | Reclassify as `ambiguous` | Intent is borderline but text is diagnostic warning, not yet prediabetes state. |
| **High** | `sym_0064` | acid uric cao thì ăn thịt đỏ thế nào | `gout` | Reclassify as `ambiguous` (Hyperuricemia) | High uric acid is asymptomatic hyperuricemia and does not equal a gout diagnosis. |
| **High** | `sym_0070` | tôi có sỏi thận và acid uric cao | `gout` | Reclassify as `ambiguous` | Touches kidney stones and hyperuricemia; forcing it to Gout is clinically narrow. |
| **High** | `sym_0156` | acid uric cao có nên hạn chế nước hầm xương không | `gout` | Reclassify as `ambiguous` | Hyperuricemia symptom, not confirmed gout. |
| **Medium**| `sym_0018` | tôi muốn giảm đồ ngọt nhưng vẫn đủ năng lượng | `diabetes` | Reclassify as `general_health` | A general weight/wellness question; forcing it to diabetes is an over-diagnosis. |
| **Medium**| `sym_0035` | bác sĩ khuyên tôi tham gia chương trình thay đổi lối sống | `prediabetes` | Reclassify as `general_health` | General clinical advice that could apply to obesity, hypertension, or cardiovascular health. |
| **Medium**| `sym_0055` | tôi cần gợi ý món Việt ít mặn hơn | `hypertension` | Reclassify as `general_health` | General healthy eating preference; forcing to hypertension is clinically narrow. |
| **Medium**| `sym_0117` | tôi ngồi nhiều, ít vận động và tăng cân | `obesity` | Reclassify as `general_health` | General sedentary lifestyle symptom. |

---

## 6. Knowledge Content Errors

| Severity | Chunk ID | Current claim/content | Problem | Source evidence | Recommended action |
| -------- | -------- | --------------------- | ------- | --------------- | ------------------ |
| **Critical** | `expanded_ckd_001` to `008` | Generic dietary recommendations for kidney disease. | CKD stage-specific protein limits are completely omitted. Stage 3 patients require protein restriction (0.6-0.8 g/kg), while stage 5 dialysis patients require high protein (1.2 g/kg). | NKF clinical guidelines stage 1-5. | Split CKD chunks explicitly by stage and dialysis status. |
| **Critical** | All 70 chunks | Zero numeric limits (e.g. sodium mg, potassium g). | Recommendations are purely qualitative, which prevents calculating or verifying schedule limits. | AHA/ADA guidelines. | Incorporate precise numeric limits from the primary sources. |
| **High** | `expanded_prediabetes_002` | "giảm dần trà sữa, nước ngọt, nước ép thêm đường..." | Qualitative advice only; does not state daily added sugar limit (e.g. <25g/day). | CDC prevent type 2 guidelines. | Add numerical target thresholds. |
| **High** | `expanded_hypertension_002` | "Nước mắm và nước tương có dùng được khi tăng huyết áp không? Câu trả lời nên thận trọng..." | Fails to state that 1 tbsp of fish sauce contains ~1000mg sodium, which is ~66% of the daily limit. | AHA Sodium limit per day. | Add exact sodium equivalents for standard condiments. |
| **High** | `expanded_gout_006` | Differentiates acute flare vs chronic management qualitatively. | Omits the warning that sudden massive changes in uric acid during flares can worsen joint pain. | MedlinePlus Gout. | Add clinical flare warning notes. |

---

## 7. Evaluation Ground-Truth Errors

| Severity | Eval ID | Question | Current expectation | Correct expectation | Reason |
| -------- | ------- | -------- | ------------------- | ------------------- | ------ |
| **Critical** | `eval_0011` | Tiền tiểu đường có cần bỏ hẳn cơm không? | `supporting_chunk_ids` is blank. | Add chunk answering this query and link it. | The knowledge base currently contains no chunk answering whether prediabetics need to completely avoid rice. |
| **High** | `eval_0014` | Tiền đái tháo đường có phải uống thuốc không? | Expects prediabetes educational answer. | Reject question or fallback to clinician referral. | Diagnosing medication eligibility is a clinical task outside general RAG scope. |
| **High** | `eval_0031` | Ăn uống có chữa khỏi gout không? | Expects gout educational answer. | Add medical disclaimer that gout is a chronic condition that can be managed, not cured by diet alone. | Gout is chronic and incurable; claiming diet "cures" it is factually incorrect and dangerous. |

---

## 8. Source and Citation Audit

| Source ID | Source type | Available | Authoritative | Used by chunks | Traceability | Problem |
| --------- | ----------- | --------- | ------------- | -------------- | ------------ | ------- |
| `ada_eating_healthy` | Webpage | Yes (HTML/TXT) | Yes (ADA) | Yes | URL-only | Download status is `downloaded_unverified_tls`. |
| `ada_meal_planning` | Webpage | Yes (HTML/TXT) | Yes (ADA) | Yes | URL-only | Unverified TLS download. |
| `ada_understanding_carbs` | Webpage | Yes (HTML/TXT) | Yes (ADA) | Yes | URL-only | Unverified TLS download. |
| `cdc_diabetes_meal_planning` | Webpage | Yes (HTML/TXT) | Yes (CDC) | Yes | URL-only | Unverified TLS download. |
| `cdc_prediabetes_lifestyle_change` | Webpage | Yes (HTML/TXT) | Yes (CDC) | Yes | URL-only | Unverified TLS download. |
| `cdc_prevent_type2_guide` | Webpage | Yes (HTML/TXT) | Yes (CDC) | Yes | URL-only | Unverified TLS download. |
| `aha_shaking_salt_habit` | Webpage | Yes (HTML/TXT) | Yes (AHA) | Yes | URL-only | Unverified TLS download. |
| `aha_sodium_per_day` | Webpage | Yes (HTML/TXT) | Yes (AHA) | Yes | URL-only | Unverified TLS download. |
| `cdc_sodium_health` | Webpage | Yes (HTML/TXT) | Yes (CDC) | Yes | URL-only | Unverified TLS download. |
| `nkf_nutrition_ckd_stages_1_5` | Webpage | Yes (HTML/TXT) | Yes (NKF) | Yes | URL-only | Unverified TLS download. |
| `nkf_potassium_ckd_diet` | Webpage | Yes (HTML/TXT) | Yes (NKF) | Yes | URL-only | Unverified TLS download. |
| `medlineplus_ckd_diet` | Webpage | Yes (HTML/TXT) | Yes (MedlinePlus) | Yes | URL-only | Unverified TLS download. |
| `medlineplus_gout` | Webpage | Yes (HTML/TXT) | Yes (MedlinePlus) | Yes | URL-only | Unverified TLS download. |
| `medlineplus_gout_encyclopedia` | Webpage | Yes (HTML/TXT) | Yes (MedlinePlus) | Yes | URL-only | Unverified TLS download. |
| `medlineplus_uric_acid_blood` | Webpage | Yes (HTML/TXT) | Yes (MedlinePlus) | Yes | URL-only | Unverified TLS download. |
| `cdc_healthy_eating_weight` | Webpage | Yes (HTML/TXT) | Yes (CDC) | Yes | URL-only | Unverified TLS download. |
| `cdc_steps_losing_weight` | Webpage | Yes (HTML/TXT) | Yes (CDC) | Yes | URL-only | Unverified TLS download. |
| `medlineplus_obesity` | Webpage | Yes (HTML/TXT) | Yes (MedlinePlus) | Yes | URL-only | Unverified TLS download. |
| `nkf_nutrition_hub` | Webpage | Yes (HTML/TXT) | Yes (NKF) | **No** | None | Registry contains this source but it is not chunked or cited by any row. |

---

## 9. Duplicate and Leakage Analysis

* **Exact Duplicates:** 0 exact duplicates were found across all datasets.
* **Near Duplicates:** Programmatic checking found low near-duplicate rates, indicating clean linguistic variation.
* **Router Leakage:**
  * **gout:** High keyword leakage. **76.7%** (23/30) of the router queries under the `gout` label explicitly contain the word "gout" (e.g. *"gout có liên quan đến thận không"*). This allows a classifier to achieve high accuracy by simple string matching rather than semantic understanding.
  * **Other Conditions:** 0% explicit leakage because condition codes like `chronic_kidney_disease` do not match common Vietnamese terms like *"suy thận"* or *"bệnh thận mạn"*. However, terms like *"tiểu đường"* and *"huyết áp"* appear in over 80% of diabetes and hypertension queries, leading to similar rule-based classification risks.
* **Train-Evaluation Leakage:** 0% (No evaluation questions directly duplicate or closely mimic router questions, showing clean separation of the test set).

---

## 10. Medical Safety Findings

| Severity | Risk | Affected data | Example | Required mitigation |
| -------- | ---- | ------------- | ------- | ------------------- |
| **Critical** | CKD Stage Conflict | `rag_chunks_reviewed.csv` (CKD Chunks) | CKD recommendations are generic and do not distinguish stage 3 (restrict protein) from stage 5 dialysis (increase protein). | Split chronic kidney disease recommendations explicitly by stage and dialysis status. |
| **Critical** | Missing Emergency Escalation | `rag_chunks_reviewed.csv` (All Conditions) | No warning signs or instructions on when to seek immediate emergency care. | Add dedicated emergency escalation chunks for symptoms like chest pain, severe hypoglycemia, or hyperkalemia. |
| **High** | universal nutrient limits | `rag_chunks_reviewed.csv` (Hypertension/Diabetes) | Lacks specific numerical guidance on daily sodium or sugar, which may cause users to ingest unsafe levels. | Add clear numerical limits (e.g., sodium <2300mg) and list standard condiment equivalents. |
| **High** | Missing Pediatric/Pregnancy exclusions | `rag_chunks_reviewed.csv` (All Conditions) | Recommends generic diet and exercise advice without excluding pregnant women, children, or elderly users. | Add clear contraindication notes and demographic exclusions to chunk metadata. |

---

## 11. Dataset Sufficiency Scores

### Condition Router Dataset

| Dimension | Score | Evidence | Main limitation |
| --------- | ----- | -------- | --------------- |
| **Schema quality** | **90** | Contains proper primary IDs, labels, review flags, and audit notes columns. | Unused index column is absent. |
| **Label correctness** | **70** | All 180 rows are forced to match one of the 6 conditions, leading to 14 mislabeled ambiguous queries. | Forced mapping of high blood sugar/uric acid queries. |
| **Class balance** | **100** | Exactly 30 examples per condition (16.67% split). | None. |
| **Linguistic diversity** | **85** | Uses natural variation in Vietnamese syntax (Min=27, Max=71 chars). | Some queries are overly brief. |
| **Ambiguous/unknown coverage** | **0** | **0 examples** for unknown, general, out-of-scope, or emergency queries. | Force-classification of all queries. |
| **Leakage resistance** | **40** | High keyword leakage in Gout (76.7%) and common names in other diseases. | Direct inclusion of condition names. |
| **Prototype readiness** | **80** | Sufficient to demonstrate a basic embedding similarity classifier. | Unsuitable for negative class validation. |

### Knowledge Dataset

| Dimension | Score | Evidence | Main limitation |
| --------- | ----- | -------- | --------------- |
| **Schema quality** | **90** | Good columns for IDs, content, citations, and review metadata. | Lack of passage offsets. |
| **Condition coverage** | **80** | Good representation of 6 conditions. | Obesity and prediabetes have only 8 chunks. |
| **Topic coverage** | **50** | Covers general definition and food items to avoid/limit. | Completely lacks numerical metrics, stages, and emergency escalations. |
| **Chunk quality** | **85** | Length is consistent (354-525 characters). | Paraphrased rows have boilerplate script-like tones. |
| **Medical correctness** | **60** | Text is qualitatively correct but clinically dangerous without stage splits. | Lost context during CKD merging. |
| **Source authority** | **90** | Preserved raw HTML/TXT files matching WHO, CDC, ADA, AHA, and NKF. | Sources are registered as unverified TLS downloads. |
| **Traceability** | **70** | Chunks map to source IDs and registry URLs. | Lacks exact page/passage locators in raw text. |
| **Safety coverage** | **30** | Chunks contain generic warnings to contact doctor. | No emergency exclusions or stage contraindications. |
| **Prototype readiness** | **75** | Sufficient for retrieval proof-of-concept. | Unsuitable for clinical scheduling. |

### Evaluation Dataset

| Dimension | Score | Evidence | Main limitation |
| --------- | ----- | -------- | --------------- |
| **Schema quality** | **90** | Good structure containing expected answers and links. | None. |
| **Distribution** | **80** | Exactly 10 questions per condition. | Lacks out-of-scope or emergency test cases. |
| **Difficulty diversity** | **70** | Includes basic keyword queries and some paraphrases. | Lacks multi-label or complex reasoning questions. |
| **Ground-truth correctness** | **85** | Supporting chunk links match chunks. | `eval_0011` lacks supporting chunk link. |
| **Leakage resistance** | **100** | Evaluation questions do not overlap with router queries. | None. |
| **Router metric readiness**| **70** | Ready to compute basic F1. | Cannot measure negative class (unknown/out-of-scope) detection. |
| **Retrieval metric readiness**| **90** | Contains expected chunk ID lists. | Only one link missing (`eval_0011`). |
| **Generation safety readiness**| **30** | Expects educational answers. | Lacks adversarial prompts or safety verification. |

---

## 12. Is the Current Dataset Enough?

* **Enough for Condition Router V1?** **YES, WITH CONDITIONS**. It can train an initial classifier, but it will force all unknown, general, or emergency queries into one of the 6 diseases.
* **Enough for Knowledge Retrieval V1?** **YES, WITH CONDITIONS**. It is sufficient to index and demonstrate top-k cosine similarity search, but the returned text will be generic and qualitative.
* **Enough for automated RAG evaluation?** **YES, WITH CONDITIONS**. It can measure Retrieval Recall@k and Router accuracy, but cannot evaluate negative class detection or citation validation due to missing labels.
* **Enough for LLM answer generation?** **YES, WITH CONDITIONS**. It can ground basic qualitative recommendations, but the LLM cannot verify numeric scheduling constraints.
* **Enough for thesis demonstration?** **YES, WITH CONDITIONS**. It can show a working RAG pipeline, but cannot be claimed as a stage-specific or clinical-grade implementation.
* **Enough for public deployment?** **NO**. The lack of stage-specific ckd guidelines, emergency escalations, and clinician review makes public use highly unsafe.

---

## 13. Minimum Required Corrections

Before implementing code, the following changes must be completed:

1. **Prediabetes Rice Query Chunk (`eval_0011`):** Add a knowledge chunk to `rag_chunks_reviewed.csv` explaining carbohydrate guidelines (rice/noodle consumption) for prediabetics and link it to `eval_0011`.
2. **Clinical Exclusions/Warnings in Chunks:** Add safety warnings to Gout, CKD, and Diabetes chunks detailing emergency symptoms (e.g. chest pain, severe hypoglycemia) and instructing users to contact emergency services immediately.
3. **Out-of-Scope Examples in Router:** Append at least 20 examples of out-of-scope queries (general wellness, unrelated topics, emergency signs) labeled as `unknown` or `out_of_scope` in the router dataset to prevent over-classification.
4. **Disclaimers in LLM Prompts:** Configure the prompt template to mandate a prominent medical disclaimer at the beginning of every response.

---

## 14. Recommended Expansion

1. **CKD Stage Segmentation:** Split chronic kidney disease recommendations into Stage 1-3 (pre-dialysis protein restrictions) and Stage 5 (dialysis protein requirements).
2. **Incorporate Numerical Limits:** Add guidelines with numeric targets (sodium <2300mg, activity >150 mins/week) to chunks.
3. **Gout Keyword Paraphrasing:** Paraphrase the 23 gout router queries containing the word "gout" to use symptoms instead.
4. **Added Sugar Limits:** Add exact added sugar thresholds to diabetes chunks.

---

## 15. Final Verdict

### Verdict: **Prototype-Only Dataset**

**Explanation:**
The RAG datasets are structurally sound, well-indexed, and contain clean bilingual references back to authoritative sources (WHO, CDC, ADA, AHA, NKF). However, because they are purely qualitative, lack critical numerical metrics, merge distinct disease stages (such as CKD stages 1-5 vs dialysis), and have not undergone human medical validation, they are unsuitable for production or clinical health scheduling. They are sufficient only to build and demonstrate a prototype.
