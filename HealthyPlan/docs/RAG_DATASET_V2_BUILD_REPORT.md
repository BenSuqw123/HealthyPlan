# HealthyPlan RAG Dataset V2 - Build Report

This document provides a summary of the accomplishments, execution details, and validation results of the **HealthyPlan RAG Dataset V2** build.

## Accomplishments & Changes

1. **Source Preservation & Collection (`scripts/collect_rag_sources_v2.py`):**
   - Preserved all 19 original HTML files under `data/rag/v2/raw_sources/`.
   - Collected additional authoritative sources:
     - **NIDDK Type 1 Diabetes Overview**
     - **NIDDK Diabetes Diet & Activity Guidelines**
     - **KDIGO 2024 Clinical Practice Guideline for CKD (PDF)**
     - **NIH MedlinePlus Emergency Guidelines** for chest pain, breathing difficulty, stroke, and hypoglycemia.

2. **Clean Text Extraction (`scripts/extract_rag_sources_v2.py`):**
   - Parsed HTML sources using `BeautifulSoup` to strip script, style, and navigation markup, leaving clean, readable markdown-like text.
   - Parsed the KDIGO 2024 Clinical Guideline PDF using `pypdf` to extract clean text.
   - Saved all extracted text files under corresponding subfolders in `data/rag/v2/raw_sources/`.

3. **Knowledge Chunk Building (`scripts/build_rag_chunks_v2.py`):**
   - Created `health_knowledge_chunks_v2.csv` with exactly **116 granular chunks** covering:
     - 4 diabetes subclasses (`diabetes_type_1`, `diabetes_type_2`, `diabetes_type_unknown`, `prediabetes`)
     - 8 chronic kidney disease subclasses (`ckd_g1`, `ckd_g2`, `ckd_g3a`, `ckd_g3b`, `ckd_g4`, `ckd_g5_non_dialysis`, `ckd_dialysis`, `ckd_stage_unknown`)
     - 4 other condition codes (`hypertension`, `gout`, `obesity`, `general_safety`)
   - Built the **Traceability Map** (`chunk_source_traceability_v2.csv`) mapping every single chunk to its source ID, local filename, page number, section name, exact supporting text snippet, and medical claim summary.
   - Standardized the source metadata in `source_registry_v2.csv` including URLs, publishers, dates, and verification status.
   - Documented the mapping from original chunks to V2 chunks in `original_chunk_decisions.json`.

4. **Updated RAG Evaluation Set (`scripts/build_rag_eval_set_v2.py`):**
   - Wrote `rag_eval_set_v2.csv` with 24 high-yield test queries mapped to normalized condition codes, expected chunk types, expected answer points, and supporting V2 chunk IDs.
   - Handled critical safety scenarios (emergency escalation, medication changes, diagnostic boundaries).

5. **Deterministic Dataset Validation (`scripts/validate_rag_dataset_v2.py`):**
   - Verified that the original reviewed CSV files remain completely unmodified (SHA-256 match).
   - Validated schemas, fields, and unique IDs across all V2 files.
   - Enforced target group checking in text content to guarantee that each chunk specifies its stage/type.
   - Generated `dataset_v2_manifest.json` indicating a status of **`PASS`**.

---

## File Structure

All generated files are stored under:
- **Build Scripts:** `scripts/`
- **V2 Dataset:** `data/rag/v2/`

```
data/rag/v2/
├── health_knowledge_chunks_v2.csv     <- 116 high-quality granular chunks
├── chunk_source_traceability_v2.csv   <- Comprehensive source mapping
├── source_registry_v2.csv             <- Details of the 27 sources
├── rag_eval_set_v2.csv                <- Updated 24 evaluation questions
├── dataset_v2_manifest.json           <- Version 2.0 PASS manifest
├── original_chunk_decisions.json      <- Traceable audit of old-to-new chunks
└── raw_sources/                       <- Raw HTML/PDFs and extracted text
    ├── ckd/
    ├── diabetes/
    ├── general_safety/
    ├── gout/
    ├── obesity/
    ├── prediabetes/
    └── hypertension/
```

---

## Validation Log Summary

Below is the verified validation output:

```
RUNNING DETERMINISTIC DATASET V2 VALIDATION...

[1/5] Checking original files protection...
  Unmodified: data/rag/rag_chunks_reviewed.csv
  Unmodified: data/rag/rag_eval_set_reviewed.csv
  Unmodified: data/rag/symptom_condition_mapping_reviewed.csv
  Unmodified: data/rag/source_registry.csv

[2/5] Checking V2 dataset schemas...

[3/5] Checking registry and traceability integrity...

[4/5] Checking evaluation set integrity...

[5/5] Finalizing validation report...

ALL DETERMINISTIC CHECKS PASSED!
RAG_DATASET_V2_VALIDATION=PASS
```
