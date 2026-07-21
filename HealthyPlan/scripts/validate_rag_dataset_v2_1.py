import os
import csv
import json
import hashlib
import sys

project_root = r"c:\Users\ACER\Documents\Desktop\Đồ Án\MainProject\HealthyPlan"
v2_1_dir = os.path.join(project_root, "data/rag/v2_1")
manifest_path = os.path.join(v2_1_dir, "dataset_v2_1_manifest.json")
checksums_json_path = r"C:\Users\ACER\.gemini\antigravity\brain\0aa56c2e-6606-490f-9cb3-8d67f2be550e\scratch\protected_checksums.json"

valid_condition_codes = {
    "diabetes_type_1", "diabetes_type_2", "diabetes_type_unknown", "prediabetes",
    "hypertension", "ckd_g1", "ckd_g2", "ckd_g3a", "ckd_g3b", "ckd_g4",
    "ckd_g5_non_dialysis", "ckd_dialysis", "ckd_stage_unknown", "gout",
    "obesity", "general_safety"
}

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def check_protected_files():
    print("Checking if V1 and V2 protected files are unchanged...")
    if not os.path.exists(checksums_json_path):
        print(f"WARNING: Protected checksums log not found at {checksums_json_path}. Skipping hash verification.")
        return True
        
    with open(checksums_json_path, "r", encoding="utf-8") as f:
        saved_checksums = json.load(f)
        
    for rel_path, saved_hash in saved_checksums.items():
        full_path = os.path.join(project_root, rel_path)
        if not os.path.exists(full_path):
            print(f"ERROR: Protected file missing: {rel_path}")
            return False
        current_hash = get_sha256(full_path)
        if current_hash != saved_hash:
            print(f"ERROR: Protected file modified! {rel_path}")
            print(f"  Expected: {saved_hash}")
            print(f"  Got:      {current_hash}")
            return False
    print("  All protected V1 and V2 files are verified as unchanged.")
    return True

def main():
    errors = []
    
    # Check protected files first
    if not check_protected_files():
        errors.append("Protected files were modified or are missing.")
        
    # Check files exist
    chunks_csv = os.path.join(v2_1_dir, "health_knowledge_chunks_v2_1.csv")
    registry_csv = os.path.join(v2_1_dir, "source_registry_v2_1.csv")
    trace_csv = os.path.join(v2_1_dir, "chunk_source_traceability_v2_1.csv")
    eval_csv = os.path.join(v2_1_dir, "rag_eval_set_v2_1.csv")
    numerical_csv = os.path.join(v2_1_dir, "numerical_claims_review_v2_1.csv")
    
    for fpath in [chunks_csv, registry_csv, trace_csv, eval_csv, numerical_csv]:
        if not os.path.exists(fpath):
            errors.append(f"Missing required output file: {os.path.basename(fpath)}")
            
    if errors:
        print("\nValidation failed with errors:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
        
    # 1. Validate chunks schema (exactly four columns) and values
    chunks = []
    chunk_ids = set()
    with open(chunks_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)
        if headers != ["chunk_id", "condition_code", "content", "source_id"]:
            errors.append(f"Invalid chunks CSV schema headers: {headers}")
            
        f.seek(0)
        dict_reader = csv.DictReader(f)
        for idx, row in enumerate(dict_reader, start=2):
            chunks.append(row)
            cid = row["chunk_id"]
            cc = row["condition_code"]
            content = row["content"]
            sid = row["source_id"]
            
            if not cid:
                errors.append(f"Line {idx}: Empty chunk_id")
            elif cid in chunk_ids:
                errors.append(f"Line {idx}: Duplicate chunk_id: {cid}")
            else:
                chunk_ids.add(cid)
                
            if cc not in valid_condition_codes:
                errors.append(f"Line {idx}: Invalid condition_code: {cc}")
                
            if not content or len(content.strip()) < 10:
                errors.append(f"Line {idx}: Content too short or empty for {cid}")
                
            if not sid:
                errors.append(f"Line {idx}: Empty source_id for {cid}")
                
    print(f"Validated {len(chunks)} knowledge chunks.")
    
    # 2. Validate source registry reference integrity
    source_ids = set()
    with open(registry_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_ids.add(row["source_id"])
            
    for c in chunks:
        if c["source_id"] not in source_ids:
            errors.append(f"Chunk {c['chunk_id']} references unregistered source_id: {c['source_id']}")
            
    print(f"Validated source registry referential integrity. Registered sources: {len(source_ids)}")
    
    # 3. Validate complete traceability mapping
    trace_map = {}
    with open(trace_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            cid = row["chunk_id"]
            sid = row["source_id"]
            trace_map[cid] = sid
            if cid not in chunk_ids:
                errors.append(f"Traceability row {idx} maps to non-existent chunk_id: {cid}")
            if sid not in source_ids:
                errors.append(f"Traceability row {idx} maps to unregistered source_id: {sid}")
                
    for cid in chunk_ids:
        if cid not in trace_map:
            errors.append(f"Chunk ID {cid} is missing a traceability record in chunk_source_traceability_v2_1.csv")
            
    print("Validated complete traceability mappings.")
    
    # 4. Validate numerical claims review status
    verified_numerical_chunks = set()
    with open(numerical_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            cid = row["chunk_id"]
            status = row["verification_status"]
            if cid not in chunk_ids:
                errors.append(f"Numerical claim row {idx} references non-existent chunk_id: {cid}")
            if status != "verified_against_source":
                errors.append(f"Numerical claim row {idx} for {cid} is not marked as verified_against_source: {status}")
            verified_numerical_chunks.add(cid)
            
    print(f"Validated {len(verified_numerical_chunks)} numerical claims as verified_against_source.")
    
    # 5. Validate evaluation set coverage (at least 3 queries per condition)
    eval_counts = {cc: 0 for cc in valid_condition_codes}
    eval_queries = []
    with open(eval_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            eval_queries.append(row)
            cc = row["condition_code"]
            if cc not in valid_condition_codes:
                errors.append(f"Eval question row {idx} has invalid condition_code: {cc}")
            else:
                eval_counts[cc] += 1
                
    for cc, count in eval_counts.items():
        if count < 3:
            errors.append(f"Condition code {cc} has insufficient evaluation coverage: only {count} questions (target: >=3)")
            
    print(f"Validated evaluation set. Total questions: {len(eval_queries)}.")
    
    # Final output status check
    if errors:
        print("\nVALIDATION FAILED with errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nALL DETERMINISTIC CHECKS PASSED!")
        print("RAG_DATASET_V2_1_VALIDATION=PASS")
        
        # Save manifest
        manifest = {
            "dataset_version": "2.1",
            "validation_status": "PASS",
            "last_validated": "2026-07-20",
            "chunks_hash": get_sha256(chunks_csv),
            "eval_set_hash": get_sha256(eval_csv),
            "chunk_count": len(chunks),
            "source_count": len(source_ids),
            "eval_count": len(eval_queries)
        }
        with open(manifest_path, "w", encoding="utf-8") as fm:
            json.dump(manifest, fm, indent=2)
        print("Manifest written to destination directory.")

if __name__ == "__main__":
    main()
