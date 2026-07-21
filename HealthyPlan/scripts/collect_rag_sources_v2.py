import os
import shutil
import hashlib
import json
import datetime
import requests

# Base paths
src_html_dir = r"data/raw/rag_sources/html"
v2_base_dir = r"data/rag/v2/raw_sources"

# Category mapping for existing sources
existing_mappings = {
    "ada_meal_planning": "diabetes",
    "ada_eating_healthy": "diabetes",
    "ada_understanding_carbs": "diabetes",
    "cdc_diabetes_meal_planning": "diabetes",
    "cdc_prediabetes_lifestyle_change": "prediabetes",
    "cdc_prevent_type2_guide": "prediabetes",
    "aha_shaking_salt_habit": "hypertension",
    "aha_sodium_per_day": "hypertension",
    "cdc_sodium_health": "hypertension",
    "nkf_nutrition_ckd_stages_1_5": "ckd",
    "nkf_potassium_ckd_diet": "ckd",
    "nkf_nutrition_hub": "ckd",
    "medlineplus_ckd_diet": "ckd",
    "medlineplus_gout": "gout",
    "medlineplus_gout_encyclopedia": "gout",
    "medlineplus_uric_acid_blood": "gout",
    "cdc_steps_losing_weight": "obesity",
    "cdc_healthy_eating_weight": "obesity",
    "medlineplus_obesity": "obesity"
}

# New sources to fetch
new_sources = [
    {
        "source_id": "niddk_type1_diabetes",
        "condition_group": "diabetes",
        "title": "Type 1 Diabetes Overview",
        "publisher": "NIDDK",
        "url": "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-1-diabetes",
        "source_type": "html",
        "pub_date": "2023-12",
        "relevant_sections": "General overview, diagnosis, insulin administration requirements"
    },
    {
        "source_id": "niddk_diabetes_diet",
        "condition_group": "diabetes",
        "title": "Diabetes Diet, Eating, & Physical Activity",
        "publisher": "NIDDK",
        "url": "https://www.niddk.nih.gov/health-information/diabetes/overview/diet-eating-physical-activity",
        "source_type": "html",
        "pub_date": "2023-12",
        "relevant_sections": "Carbohydrate management, exercise safety, meal planning"
    },
    {
        "source_id": "kdigo_2024_ckd_guideline",
        "condition_group": "ckd",
        "title": "KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease",
        "publisher": "KDIGO",
        "url": "https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf",
        "source_type": "pdf",
        "pub_date": "2024-03",
        "relevant_sections": "CKD staging criteria (Chapter 1), nutrition and protein guidance (Chapter 3)"
    },
    {
        "source_id": "medlineplus_emergency_chest_pain",
        "condition_group": "general_safety",
        "title": "Chest pain Medical Encyclopedia",
        "publisher": "NIH MedlinePlus",
        "url": "https://medlineplus.gov/ency/article/003079.htm",
        "source_type": "html",
        "pub_date": "2024-05",
        "relevant_sections": "Chest pain emergency warning signs, cardiac symptoms escalation"
    },
    {
        "source_id": "medlineplus_emergency_breathing",
        "condition_group": "general_safety",
        "title": "Breathing difficulty Medical Encyclopedia",
        "publisher": "NIH MedlinePlus",
        "url": "https://medlineplus.gov/ency/article/003075.htm",
        "source_type": "html",
        "pub_date": "2024-05",
        "relevant_sections": "Breathing difficulty escalation, respiratory distress symptoms"
    },
    {
        "source_id": "medlineplus_emergency_fainting",
        "condition_group": "general_safety",
        "title": "Fainting Medical Encyclopedia",
        "publisher": "NIH MedlinePlus",
        "url": "https://medlineplus.gov/ency/article/000022.htm",
        "source_type": "html",
        "pub_date": "2024-05",
        "relevant_sections": "Fainting and loss of consciousness emergency response guidelines"
    },
    {
        "source_id": "medlineplus_emergency_stroke",
        "condition_group": "general_safety",
        "title": "Stroke Medical Encyclopedia",
        "publisher": "NIH MedlinePlus",
        "url": "https://medlineplus.gov/ency/article/000730.htm",
        "source_type": "html",
        "pub_date": "2024-05",
        "relevant_sections": "Stroke warning signs (FAST), acute neurological emergency escalation"
    },
    {
        "source_id": "medlineplus_emergency_hypoglycemia",
        "condition_group": "general_safety",
        "title": "Hypoglycemia - self-care",
        "publisher": "NIH MedlinePlus",
        "url": "https://medlineplus.gov/ency/patientinstructions/000085.htm",
        "source_type": "html",
        "pub_date": "2024-05",
        "relevant_sections": "Rule of 15, severe hypoglycemia emergency warnings"
    }
]

def calculate_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def process_existing_sources():
    print("Processing existing 19 HTML sources...")
    # Read original registry for URLs and details
    registry_path = r"data/rag/source_registry.csv"
    urls_map = {}
    titles_map = {}
    publisher_map = {}
    if os.path.exists(registry_path):
        import csv
        with open(registry_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                urls_map[row["source_id"]] = row["source_url"]
                titles_map[row["source_id"]] = row["source_title"]
                publisher_map[row["source_id"]] = row["source_org"]

    for source_id, category in existing_mappings.items():
        src_filename = f"{source_id}.html"
        src_filepath = os.path.join(src_html_dir, src_filename)
        dest_dir = os.path.join(v2_base_dir, category)
        ensure_dir(dest_dir)
        dest_filepath = os.path.join(dest_dir, src_filename)

        if not os.path.exists(src_filepath):
            print(f"Error: Original source file not found: {src_filepath}")
            continue

        # Copy original file if not already copied
        if not os.path.exists(dest_filepath):
            shutil.copy2(src_filepath, dest_filepath)
            print(f"  Copied {src_filename} to {category}/")

        checksum = calculate_checksum(dest_filepath)
        
        # Write metadata JSON
        meta_filename = f"{source_id}.metadata.json"
        meta_filepath = os.path.join(dest_dir, meta_filename)
        
        meta = {
            "source_id": source_id,
            "title": titles_map.get(source_id, source_id.replace("_", " ").title()),
            "publisher": publisher_map.get(source_id, "Unknown"),
            "source_type": "html",
            "original_url": urls_map.get(source_id, "https://unknown.url"),
            "publication_date": "2023-01", # Draft date
            "accessed_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "local_file": f"{category}/{src_filename}",
            "checksum": checksum,
            "extraction_status": "draft",
            "language": "en",
            "relevant_pages": "",
            "relevant_sections": "All general educational content",
            "verification_status": "downloaded_unverified_tls"
        }
        
        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

def download_new_sources():
    print("Downloading new sources from official URLs...")
    for src in new_sources:
        source_id = src["source_id"]
        category = src["condition_group"]
        url = src["url"]
        stype = src["source_type"]
        
        dest_dir = os.path.join(v2_base_dir, category)
        ensure_dir(dest_dir)
        
        ext = "html" if stype == "html" else "pdf"
        dest_filename = f"{source_id}.{ext}"
        dest_filepath = os.path.join(dest_dir, dest_filename)
        
        if os.path.exists(dest_filepath):
            print(f"  File already exists, skipping download: {dest_filename}")
        else:
            print(f"  Downloading: {url} -> {dest_filepath}")
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                with open(dest_filepath, "wb") as f:
                    f.write(response.content)
                print(f"    Successfully downloaded {dest_filename}")
            except Exception as e:
                print(f"    Error downloading {source_id} from {url}: {e}")
                # Fallback check or failure recording
                continue

        checksum = calculate_checksum(dest_filepath)
        
        # Write metadata JSON
        meta_filename = f"{source_id}.metadata.json"
        meta_filepath = os.path.join(dest_dir, meta_filename)
        
        meta = {
            "source_id": source_id,
            "title": src["title"],
            "publisher": src["publisher"],
            "source_type": stype,
            "original_url": url,
            "publication_date": src["pub_date"],
            "accessed_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "local_file": f"{category}/{dest_filename}",
            "checksum": checksum,
            "extraction_status": "draft",
            "language": "en",
            "relevant_pages": "All" if stype == "html" else "1-200",
            "relevant_sections": src["relevant_sections"],
            "verification_status": "downloaded_verified_tls"
        }
        
        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_existing_sources()
    download_new_sources()
    print("Source collection completed.")
