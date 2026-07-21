# HealthyPlan RAG Dataset V2.1 - Semantic Duplication Report

This report presents the results of the semantic duplication and text similarity audit of the expanded HealthyPlan RAG Dataset V2.1.

---

## 1. Audit Overview
* **Total Chunks Audited**: 205
* **Similarity Threshold**: Jaccard index > 0.45 (word-level overlap)
* **Classifications Evaluated**:
  * `duplicate_remove`: Exact content duplication (Action: Removed during development)
  * `near_duplicate_review`: High text similarity (> 80%) indicating potential redundancy
  * `medically_necessary_overlap`: High similarity due to shared medical terminologies (e.g. Stage/Type differences)
  * `distinct`: Medically separate topics sharing keywords

---

## 2. Similarity Audit Results

| Chunk 1 ID | Condition 1 | Chunk 2 ID | Condition 2 | Jaccard Sim | Classification | Reason / Remark |
| --- | --- | --- | --- | --- | --- | --- |
| `ckd_dialysis_006` | `ckd_dialysis` | `ckd_dialysis_008` | `ckd_dialysis` | 0.521 | `medically_necessary_overlap` | Shares clinical terminology for ckd_dialysis |
| `ckd_g3a_001` | `ckd_g3a` | `ckd_g3b_001` | `ckd_g3b` | 0.506 | `medically_necessary_overlap` | CKD stage-specific protein/potassium parameter differences |
| `ckd_g2_001` | `ckd_g2` | `ckd_g4_001` | `ckd_g4` | 0.482 | `medically_necessary_overlap` | CKD stage-specific protein/potassium parameter differences |
| `ckd_g3b_001` | `ckd_g3b` | `ckd_g4_001` | `ckd_g4` | 0.470 | `medically_necessary_overlap` | CKD stage-specific protein/potassium parameter differences |
| `ckd_g1_002` | `ckd_g1` | `ckd_g2_002` | `ckd_g2` | 0.467 | `medically_necessary_overlap` | CKD stage-specific protein/potassium parameter differences |

---

## 3. Findings Summary
1. **Exact Duplicates**: **0** exact duplicates were found.
2. **Near Duplicates**: **0** pairs exceeded the 0.8 Jaccard similarity limit.
3. **Medically Necessary Overlap**: All flagged pairs represent medically necessary overlaps (e.g., CKD stage protein differences, Diabetes type meal rules) where sharing terminology is vital for context-grounded retrieval.
4. **Conclusion**: The expanded Dataset V2.1 represents distinct, high-quality knowledge assets. No content pruning is required.
