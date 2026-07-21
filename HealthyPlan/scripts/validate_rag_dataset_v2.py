import os
import csv
import json
import hashlib
import sys

# Paths
v2_dir = r"data/rag/v2"
chunks_path = os.path.join(v2_dir, "health_knowledge_chunks_v2.csv")
traceability_path = os.path.join(v2_dir, "chunk_source_traceability_v2.csv")
registry_path = os.path.join(v2_dir, "source_registry_v2.csv")
eval_path = os.path.join(v2_dir, "rag_eval_set_v2.csv")
manifest_path = os.path.join(v2_dir, "dataset_v2_manifest.json")
log_path = r"C:\Users\ACER\.gemini\antigravity\brain\0aa56c2e-6606-490f-9cb3-8d67f2be550e\scratch\validation_run.log"

# Original files & checksums
original_files = {
    "data/rag/rag_chunks_reviewed.csv": "ecb72cadf082666299f411e8fc1310f34db956c565d2f19a855b4b55a1d1f715",
    "data/rag/rag_eval_set_reviewed.csv": "5e26d3a5401b71214375ef465a01414158cc9f1ab550d9778e943d13acaaac58",
    "data/rag/symptom_condition_mapping_reviewed.csv": "4f0eaf450a7cb3221db5a6fa8b3f48b39bdf07dc3cbd3f655467a12736bb7838",
    "data/rag/source_registry.csv": "73741bc70338d4a2d037cdc9c46805d1b92093aff36098f939535a1f39b20f8a"
}

# Valid condition codes
valid_condition_codes = {
    "diabetes_type_1", "diabetes_type_2", "diabetes_type_unknown", "prediabetes",
    "ckd_g1", "ckd_g2", "ckd_g3a", "ckd_g3b", "ckd_g4", "ckd_g5_non_dialysis", "ckd_dialysis", "ckd_stage_unknown",
    "hypertension", "gout", "obesity", "general_safety"
}

def calculate_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def run_validation():
    log_file = open(log_path, "w", encoding="utf-8")
    log_file.write("RUNNING DETERMINISTIC DATASET V2 VALIDATION...\n")
    failures = []
    
    # 1. Verify Original Files Checksums
    original_unchanged = True
    log_file.write("\n[1/5] Checking original files protection...\n")
    for path, expected_hash in original_files.items():
        if not os.path.exists(path):
            failures.append(f"Original file missing: {path}")
            original_unchanged = False
            continue
        curr_hash = calculate_sha256(path)
        if curr_hash != expected_hash:
            failures.append(f"Original file was modified! Path: {path} (Expected: {expected_hash}, Current: {curr_hash})")
            original_unchanged = False
        else:
            log_file.write(f"  Unmodified: {path}\n")
            
    # 2. Check File Existences & Schema
    log_file.write("\n[2/5] Checking V2 dataset schemas...\n")
    for fn in [chunks_path, traceability_path, registry_path, eval_path]:
        if not os.path.exists(fn):
            failures.append(f"V2 file missing: {fn}")
            
    # Chunks Schema & Content Validation
    all_chunk_ids = set()
    all_chunk_contents = set()
    chunk_rows = []
    if os.path.exists(chunks_path):
        with open(chunks_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
            if header != ["chunk_id", "condition_code", "content", "source_id"]:
                failures.append(f"Chunks V2 header is invalid: {header} (must be exactly chunk_id, condition_code, content, source_id)")
            
            for line_idx, row in enumerate(reader, start=2):
                if len(row) != 4:
                    failures.append(f"Row {line_idx} in chunks has {len(row)} columns instead of 4")
                    continue
                cid, cond, content, sid = row
                chunk_rows.append(row)
                
                # Missing fields
                if not cid: failures.append(f"Row {line_idx} has empty chunk_id")
                if not cond: failures.append(f"Row {line_idx} has empty condition_code")
                if not content: failures.append(f"Row {line_idx} has empty content")
                if not sid: failures.append(f"Row {line_idx} has empty source_id")
                
                # Duplicates
                if cid in all_chunk_ids:
                    failures.append(f"Duplicate chunk_id found: {cid}")
                all_chunk_ids.add(cid)
                
                if content in all_chunk_contents:
                    failures.append(f"Duplicate content found in chunk_id: {cid}")
                all_chunk_contents.add(content)
                
                # Invalid condition codes
                if cond not in valid_condition_codes:
                    failures.append(f"Invalid condition_code in chunk {cid}: {cond}")
                    
                # Explicit population check in content
                content_lower = content.lower()
                if cond == "diabetes_type_1":
                    if "type 1" not in content_lower:
                        failures.append(f"Chunk {cid} labeled as diabetes_type_1 but does not explicitly mention 'type 1' in content")
                elif cond == "diabetes_type_2":
                    if "type 2" not in content_lower:
                        failures.append(f"Chunk {cid} labeled as diabetes_type_2 but does not explicitly mention 'type 2' in content")
                elif cond == "prediabetes":
                    if "tiền đái tháo đường" not in content_lower and "tiền tiểu đường" not in content_lower:
                        failures.append(f"Chunk {cid} labeled as prediabetes but does not mention prediabetes keywords in content")
                elif cond == "hypertension":
                    if "huyết áp" not in content_lower:
                        failures.append(f"Chunk {cid} labeled as hypertension but does not mention blood pressure keywords in content")
                elif cond.startswith("ckd_"):
                    # Check that stage is mentioned
                    stage_terms = {
                        "ckd_g1": "giai đoạn g1", "ckd_g2": "giai đoạn g2", 
                        "ckd_g3a": "giai đoạn g3a", "ckd_g3b": "giai đoạn g3b",
                        "ckd_g4": "giai đoạn g4", "ckd_g5_non_dialysis": "giai đoạn g5 chưa chạy thận",
                        "ckd_dialysis": "chạy thận", "ckd_stage_unknown": "chưa rõ giai đoạn"
                    }
                    term = stage_terms[cond]
                    if term not in content_lower:
                        failures.append(f"CKD chunk {cid} labeled as {cond} but does not explicitly mention '{term}' in content")
                        
    # 3. Registry & Traceability Integrity
    log_file.write("\n[3/5] Checking registry and traceability integrity...\n")
    registry_source_ids = set()
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                registry_source_ids.add(row["source_id"])
                # Local file check
                local_file = row["local_snapshot_path"]
                if not os.path.exists(local_file):
                    failures.append(f"Source snapshot file missing for source_id '{row['source_id']}': {local_file}")
                    
    traceability_chunk_ids = set()
    if os.path.exists(traceability_path):
        with open(traceability_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cid = row["chunk_id"]
                sid = row["source_id"]
                traceability_chunk_ids.add(cid)
                if cid not in all_chunk_ids:
                    failures.append(f"Traceability maps to non-existent chunk_id: {cid}")
                if sid not in registry_source_ids:
                    failures.append(f"Traceability maps to non-existent source_id: {sid}")
                    
    # Ensure every chunk has traceability
    missing_traceability = all_chunk_ids - traceability_chunk_ids
    if missing_traceability:
        failures.append(f"Chunks missing from traceability map: {missing_traceability}")
        
    # Ensure every chunk's source exists in registry
    for row in chunk_rows:
        cid, cond, content, sid = row
        if sid not in registry_source_ids:
            failures.append(f"Chunk {cid} references unregistered source_id: {sid}")

    # 4. Evaluation Set V2 Validation
    log_file.write("\n[4/5] Checking evaluation set integrity...\n")
    if os.path.exists(eval_path):
        with open(eval_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for line_idx, row in enumerate(reader, start=2):
                eid = row["eval_id"]
                cond = row["condition_code"]
                supporting_ids_str = row["supporting_chunk_ids"]
                
                if cond not in valid_condition_codes:
                    failures.append(f"Eval query {eid} has invalid condition_code: {cond}")
                
                if supporting_ids_str.strip():
                    supporting_ids = [c.strip() for c in supporting_ids_str.split(";") if c.strip()]
                    for cid in supporting_ids:
                        if cid not in all_chunk_ids:
                            failures.append(f"Eval query {eid} maps to non-existent chunk_id: {cid}")
                else:
                    failures.append(f"Eval query {eid} has empty supporting_chunk_ids")

    # 5. Summary & Verdict
    log_file.write("\n[5/5] Finalizing validation report...\n")
    if failures:
        log_file.write("\nVALIDATION FAILED WITH THE FOLLOWING ERRORS:\n")
        for err in failures:
            log_file.write(f" - {err}\n")
        log_file.close()
        
        # Output failure to stdout using simple ASCII
        print("VALIDATION FAILED! See scratch/validation_run.log for details.")
        write_manifest(False, original_unchanged, len(chunk_rows), len(registry_source_ids))
        sys.exit(1)
    else:
        log_file.write("\nALL DETERMINISTIC CHECKS PASSED SUCCESSFULLY!\n")
        log_file.write("RAG_DATASET_V2_VALIDATION=PASS\n")
        log_file.close()
        
        print("ALL DETERMINISTIC CHECKS PASSED!")
        print("RAG_DATASET_V2_VALIDATION=PASS")
        write_manifest(True, original_unchanged, len(chunk_rows), len(registry_source_ids))
        sys.exit(0)

def write_manifest(is_pass, original_unchanged, chunk_count, source_count):
    # Collect publishers
    publishers = set()
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                publishers.add(row["publisher"])
                
    manifest = {
        "dataset_version": "2.0",
        "created_at": datetime_now_str(),
        "source_dataset": "rag_chunks_reviewed.csv",
        "chunk_count": chunk_count,
        "source_count": source_count,
        "condition_codes": sorted(list(valid_condition_codes)),
        "source_publishers": sorted(list(publishers)),
        "validation_status": "PASS" if is_pass else "FAIL",
        "source_verification_status": "downloaded_verified_tls",
        "medical_review_status": "not_reviewed_by_clinician",
        "original_files_unchanged": original_unchanged,
        "build_scripts": [
            "scripts/collect_rag_sources_v2.py",
            "scripts/extract_rag_sources_v2.py",
            "scripts/build_rag_chunks_v2.py",
            "scripts/build_rag_eval_set_v2.py",
            "scripts/validate_rag_dataset_v2.py"
        ],
        "dataset_checksum": calculate_sha256(chunks_path) if os.path.exists(chunks_path) else ""
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def datetime_now_str():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

if __name__ == "__main__":
    run_validation()
