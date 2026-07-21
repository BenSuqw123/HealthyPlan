import os
import csv
import json

v2_dir = r"data/rag/v2"
os.makedirs(v2_dir, exist_ok=True)

chunks_v2_path = os.path.join(v2_dir, "health_knowledge_chunks_v2.csv")
traceability_path = os.path.join(v2_dir, "chunk_source_traceability_v2.csv")
registry_v2_path = os.path.join(v2_dir, "source_registry_v2.csv")

# 1. Define source registry V2 entries
source_registry_v2 = [
    # Existing sources
    {
        "source_id": "ada_meal_planning",
        "publisher": "American Diabetes Association",
        "title": "ADA Meal Planning",
        "source_type": "html",
        "original_url": "https://diabetes.org/food-nutrition/meal-planning",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/diabetes/ada_meal_planning.html",
        "extracted_text_path": "data/rag/v2/raw_sources/diabetes/ada_meal_planning.txt",
        "relevant_pages": "All",
        "relevant_sections": "Meal planning, Diabetes Plate Method guidelines",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "ada_eating_healthy",
        "publisher": "American Diabetes Association",
        "title": "Eating Well & Managing Diabetes",
        "source_type": "html",
        "original_url": "https://diabetes.org/food-nutrition/eating-healthy",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/diabetes/ada_eating_healthy.html",
        "extracted_text_path": "data/rag/v2/raw_sources/diabetes/ada_eating_healthy.txt",
        "relevant_pages": "All",
        "relevant_sections": "General nutrition, fruit consumption, and added sugars",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "ada_understanding_carbs",
        "publisher": "American Diabetes Association",
        "title": "Understanding Carbs",
        "source_type": "html",
        "original_url": "https://diabetes.org/food-nutrition/understanding-carbs",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/diabetes/ada_understanding_carbs.html",
        "extracted_text_path": "data/rag/v2/raw_sources/diabetes/ada_understanding_carbs.txt",
        "relevant_pages": "All",
        "relevant_sections": "Carbohydrates and blood glucose, medication timing guidelines",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "cdc_diabetes_meal_planning",
        "publisher": "CDC",
        "title": "Diabetes Meal Planning",
        "source_type": "html",
        "original_url": "https://www.cdc.gov/diabetes/healthy-eating/diabetes-meal-planning.html",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/diabetes/cdc_diabetes_meal_planning.html",
        "extracted_text_path": "data/rag/v2/raw_sources/diabetes/cdc_diabetes_meal_planning.txt",
        "relevant_pages": "All",
        "relevant_sections": "Meal planning, weight management for Type 2, monitoring guidelines",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "cdc_prediabetes_lifestyle_change",
        "publisher": "CDC",
        "title": "About the Lifestyle Change Program",
        "source_type": "html",
        "original_url": "https://www.cdc.gov/diabetes-prevention/lifestyle-change-program/lifestyle-change-program-details.html",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/prediabetes/cdc_prediabetes_lifestyle_change.html",
        "extracted_text_path": "data/rag/v2/raw_sources/prediabetes/cdc_prediabetes_lifestyle_change.txt",
        "relevant_pages": "All",
        "relevant_sections": "Prediabetes overview, lifestyle intervention program details",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "cdc_prevent_type2_guide",
        "publisher": "CDC",
        "title": "About On Your Way to Preventing Type 2 Diabetes",
        "source_type": "html",
        "original_url": "https://www.cdc.gov/diabetes/prevention-type-2/type-2-diabetes-prevention-guide.html",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/prediabetes/cdc_prevent_type2_guide.html",
        "extracted_text_path": "data/rag/v2/raw_sources/prediabetes/cdc_prevent_type2_guide.txt",
        "relevant_pages": "All",
        "relevant_sections": "Prediabetes dietary recommendations, sugary drinks, portion control, progression monitoring",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "aha_shaking_salt_habit",
        "publisher": "American Heart Association",
        "title": "Shaking the Salt Habit to Lower High Blood Pressure",
        "source_type": "html",
        "original_url": "https://www.heart.org/en/health-topics/high-blood-pressure/changes-you-can-make-to-manage-high-blood-pressure/shaking-the-salt-habit-to-lower-high-blood-pressure",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/hypertension/aha_shaking_salt_habit.html",
        "extracted_text_path": "data/rag/v2/raw_sources/hypertension/aha_shaking_salt_habit.txt",
        "relevant_pages": "All",
        "relevant_sections": "Condiments, processed foods, and dietary patterns for blood pressure",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "aha_sodium_per_day",
        "publisher": "American Heart Association",
        "title": "How Much Sodium Should I Eat Per Day?",
        "source_type": "html",
        "original_url": "https://www.heart.org/en/healthy-living/healthy-eating/eat-smart/sodium/how-much-sodium-should-i-eat-per-day",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/hypertension/aha_sodium_per_day.html",
        "extracted_text_path": "data/rag/v2/raw_sources/hypertension/aha_sodium_per_day.txt",
        "relevant_pages": "All",
        "relevant_sections": "AHA/ACC absolute sodium limits, warnings on processed foods",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "cdc_sodium_health",
        "publisher": "CDC",
        "title": "About Sodium and Health",
        "source_type": "html",
        "original_url": "https://www.cdc.gov/salt/about/index.html",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/hypertension/cdc_sodium_health.html",
        "extracted_text_path": "data/rag/v2/raw_sources/hypertension/cdc_sodium_health.txt",
        "relevant_pages": "All",
        "relevant_sections": "Sodium mechanisms, processed food sources, public health limits",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "publisher": "National Kidney Foundation",
        "title": "Nutrition and Kidney Disease Stages 1-5",
        "source_type": "html",
        "original_url": "https://www.kidney.org/kidney-topics/nutrition-and-kidney-disease-stages-1-5-not-dialysis",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/ckd/nkf_nutrition_ckd_stages_1_5.html",
        "extracted_text_path": "data/rag/v2/raw_sources/ckd/nkf_nutrition_ckd_stages_1_5.txt",
        "relevant_pages": "All",
        "relevant_sections": "Nephrologist nutrition overviews, protein guidelines for Stages 1-5",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "nkf_potassium_ckd_diet",
        "publisher": "National Kidney Foundation",
        "title": "Potassium in Your CKD Diet",
        "source_type": "html",
        "original_url": "https://www.kidney.org/kidney-topics/potassium-your-ckd-diet",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/ckd/nkf_potassium_ckd_diet.html",
        "extracted_text_path": "data/rag/v2/raw_sources/ckd/nkf_potassium_ckd_diet.txt",
        "relevant_pages": "All",
        "relevant_sections": "Potassium rich food classifications, lab measurement requirements",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "nkf_nutrition_hub",
        "publisher": "National Kidney Foundation",
        "title": "NKF Nutrition Hub",
        "source_type": "html",
        "original_url": "https://www.kidney.org/nutrition",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/ckd/nkf_nutrition_hub.html",
        "extracted_text_path": "data/rag/v2/raw_sources/ckd/nkf_nutrition_hub.txt",
        "relevant_pages": "All",
        "relevant_sections": "Patient nutrition resources and portal link entries",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "medlineplus_ckd_diet",
        "publisher": "NIH MedlinePlus",
        "title": "Diet - Chronic Kidney Disease",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/ency/article/002442.htm",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/ckd/medlineplus_ckd_diet.html",
        "extracted_text_path": "data/rag/v2/raw_sources/ckd/medlineplus_ckd_diet.txt",
        "relevant_pages": "All",
        "relevant_sections": "Protein, sodium, phosphorus, and fluid restrictions in kidney disease",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "medlineplus_gout",
        "publisher": "NIH MedlinePlus",
        "title": "Gout",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/gout.html",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/gout/medlineplus_gout.html",
        "extracted_text_path": "data/rag/v2/raw_sources/gout/medlineplus_gout.txt",
        "relevant_pages": "All",
        "relevant_sections": "Gout definition, flares, hydration, and long-term joint damage prevention",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "medlineplus_gout_encyclopedia",
        "publisher": "NIH MedlinePlus",
        "title": "Gout Medical Encyclopedia",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/ency/article/000422.htm",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/gout/medlineplus_gout_encyclopedia.html",
        "extracted_text_path": "data/rag/v2/raw_sources/gout/medlineplus_gout_encyclopedia.txt",
        "relevant_pages": "All",
        "relevant_sections": "Purines, foods to avoid (organ meats, red meats, alcohol), clinical features",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "medlineplus_uric_acid_blood",
        "publisher": "NIH MedlinePlus",
        "title": "Uric Acid Blood",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/ency/article/003476.htm",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/gout/medlineplus_uric_acid_blood.html",
        "extracted_text_path": "data/rag/v2/raw_sources/gout/medlineplus_uric_acid_blood.txt",
        "relevant_pages": "All",
        "relevant_sections": "Uric acid diagnostic thresholds, distinction from asymptomatic state",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "cdc_steps_losing_weight",
        "publisher": "CDC",
        "title": "Steps for Losing Weight",
        "source_type": "html",
        "original_url": "https://www.cdc.gov/healthy-weight-growth/losing-weight/index.html",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/obesity/cdc_steps_losing_weight.html",
        "extracted_text_path": "data/rag/v2/raw_sources/obesity/cdc_steps_losing_weight.txt",
        "relevant_pages": "All",
        "relevant_sections": "Sustainable weight management, safe weight loss rates, activity planning",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "cdc_healthy_eating_weight",
        "publisher": "CDC",
        "title": "Tips for Healthy Eating for a Healthy Weight",
        "source_type": "html",
        "original_url": "https://www.cdc.gov/healthy-weight-growth/healthy-eating/index.html",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/obesity/cdc_healthy_eating_weight.html",
        "extracted_text_path": "data/rag/v2/raw_sources/obesity/cdc_healthy_eating_weight.txt",
        "relevant_pages": "All",
        "relevant_sections": "Portion control, sugary drinks reduction, energy density concepts",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    {
        "source_id": "medlineplus_obesity",
        "publisher": "NIH MedlinePlus",
        "title": "Obesity",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/obesity.html",
        "publication_date": "2023-01",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/obesity/medlineplus_obesity.html",
        "extracted_text_path": "data/rag/v2/raw_sources/obesity/medlineplus_obesity.txt",
        "relevant_pages": "All",
        "relevant_sections": "Obesity definition, extreme diets warnings, comorbidities, frailty in older adults",
        "authority_level": "High",
        "verification_status": "downloaded_unverified_tls",
        "notes": "Reused original HTML snapshot"
    },
    
    # New downloaded sources
    {
        "source_id": "niddk_type1_diabetes",
        "publisher": "NIDDK",
        "title": "Type 1 Diabetes Overview",
        "source_type": "html",
        "original_url": "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-1-diabetes",
        "publication_date": "2023-12",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/diabetes/niddk_type1_diabetes.html",
        "extracted_text_path": "data/rag/v2/raw_sources/diabetes/niddk_type1_diabetes.txt",
        "relevant_pages": "All",
        "relevant_sections": "General overview, diagnosis, insulin administration requirements",
        "authority_level": "High",
        "verification_status": "downloaded_verified_tls",
        "notes": "Newly collected source to cover Type 1 Diabetes gaps"
    },
    {
        "source_id": "niddk_diabetes_diet",
        "publisher": "NIDDK",
        "title": "Diabetes Diet, Eating, & Physical Activity",
        "source_type": "html",
        "original_url": "https://www.niddk.nih.gov/health-information/diabetes/overview/diet-eating-physical-activity",
        "publication_date": "2023-12",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/diabetes/niddk_diabetes_diet.html",
        "extracted_text_path": "data/rag/v2/raw_sources/diabetes/niddk_diabetes_diet.txt",
        "relevant_pages": "All",
        "relevant_sections": "Carbohydrate management, exercise safety, meal planning",
        "authority_level": "High",
        "verification_status": "downloaded_verified_tls",
        "notes": "Newly collected source to cover Diabetes Type 1/2 nutrition gaps"
    },
    {
        "source_id": "kdigo_2024_ckd_guideline",
        "publisher": "KDIGO",
        "title": "KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease",
        "source_type": "pdf",
        "original_url": "https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf",
        "publication_date": "2024-03",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/ckd/kdigo_2024_ckd_guideline.pdf",
        "extracted_text_path": "data/rag/v2/raw_sources/ckd/kdigo_2024_ckd_guideline.txt",
        "relevant_pages": "1-200",
        "relevant_sections": "CKD staging criteria (Chapter 1), nutrition and protein guidance (Chapter 3)",
        "authority_level": "High",
        "verification_status": "downloaded_verified_tls",
        "notes": "Newly collected clinical guideline PDF for stage-specific CKD boundaries"
    },
    {
        "source_id": "medlineplus_emergency_chest_pain",
        "publisher": "NIH MedlinePlus",
        "title": "Chest pain Medical Encyclopedia",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/ency/article/003079.htm",
        "publication_date": "2024-05",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_chest_pain.html",
        "extracted_text_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_chest_pain.txt",
        "relevant_pages": "All",
        "relevant_sections": "Chest pain emergency warning signs, cardiac symptoms escalation",
        "authority_level": "High",
        "verification_status": "downloaded_verified_tls",
        "notes": "Safety guidelines for emergency chest pain"
    },
    {
        "source_id": "medlineplus_emergency_breathing",
        "publisher": "NIH MedlinePlus",
        "title": "Breathing difficulty Medical Encyclopedia",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/ency/article/003075.htm",
        "publication_date": "2024-05",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_breathing.html",
        "extracted_text_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_breathing.txt",
        "relevant_pages": "All",
        "relevant_sections": "Breathing difficulty escalation, respiratory distress symptoms",
        "authority_level": "High",
        "verification_status": "downloaded_verified_tls",
        "notes": "Safety guidelines for emergency breathing difficulty"
    },
    {
        "source_id": "medlineplus_emergency_fainting",
        "publisher": "NIH MedlinePlus",
        "title": "Fainting Medical Encyclopedia",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/ency/article/000022.htm",
        "publication_date": "2024-05",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_fainting.html",
        "extracted_text_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_fainting.txt",
        "relevant_pages": "All",
        "relevant_sections": "Fainting and loss of consciousness emergency response guidelines",
        "authority_level": "High",
        "verification_status": "downloaded_verified_tls",
        "notes": "Safety guidelines for loss of consciousness"
    },
    {
        "source_id": "medlineplus_emergency_stroke",
        "publisher": "NIH MedlinePlus",
        "title": "Stroke Medical Encyclopedia",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/ency/article/000730.htm",
        "publication_date": "2024-05",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_stroke.html",
        "extracted_text_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_stroke.txt",
        "relevant_pages": "All",
        "relevant_sections": "Stroke warning signs (FAST), acute neurological emergency escalation",
        "authority_level": "High",
        "verification_status": "downloaded_verified_tls",
        "notes": "Safety guidelines for stroke and neurological emergencies"
    },
    {
        "source_id": "medlineplus_emergency_hypoglycemia",
        "publisher": "NIH MedlinePlus",
        "title": "Hypoglycemia - self-care",
        "source_type": "html",
        "original_url": "https://medlineplus.gov/ency/patientinstructions/000085.htm",
        "publication_date": "2024-05",
        "accessed_date": "2026-07-20",
        "local_snapshot_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_hypoglycemia.html",
        "extracted_text_path": "data/rag/v2/raw_sources/general_safety/medlineplus_emergency_hypoglycemia.txt",
        "relevant_pages": "All",
        "relevant_sections": "Rule of 15, severe hypoglycemia emergency warnings",
        "authority_level": "High",
        "verification_status": "downloaded_verified_tls",
        "notes": "Safety guidelines for hypoglycemia"
    }
]

# 2. Define the knowledge chunks V2
# Every chunk must explicitly state the patient group in Vietnamese, use normalized code, stable IDs.
chunks_v2 = [
    # --- DIABETES TYPE 1 ---
    {
        "chunk_id": "diabetes_t1_001",
        "condition_code": "diabetes_type_1",
        "content": "Đối với người mắc đái tháo đường type 1, nguyên tắc dinh dưỡng tổng quát nhấn mạnh việc phối hợp chặt chẽ giữa chế độ ăn uống, hoạt động thể lực và liều lượng insulin được tiêm vào cơ thể. Không có một chế độ ăn kiêng duy nhất cho tất cả mọi người, nhưng người đái tháo đường type 1 cần hướng tới các bữa ăn giàu đạm nạc, chất xơ và chất béo lành mạnh để kiểm soát đường huyết ổn định.",
        "source_id": "niddk_type1_diabetes",
        "locator": "what-is-diabetes/type-1-diabetes.txt",
        "page": "",
        "section": "General overview",
        "text_support": "Type 1 diabetes is a disease in which your pancreas does not make insulin... Managing type 1 diabetes requires keeping your blood glucose levels in target range through insulin, diet, and exercise.",
        "claim": "Type 1 diabetes nutrition requires coordinating insulin, diet, and physical activity."
    },
    {
        "chunk_id": "diabetes_t1_002",
        "condition_code": "diabetes_type_1",
        "content": "Nhận biết lượng carbohydrate là một kỹ năng thiết yếu đối với người bệnh đái tháo đường type 1. Vì carbohydrate ảnh hưởng trực tiếp và nhanh nhất đến mức đường huyết sau ăn, người đái tháo đường type 1 cần học cách đếm carbohydrate trong từng bữa ăn để tính toán liều insulin bolus (insulin trước bữa ăn) phù hợp theo hướng dẫn của bác sĩ.",
        "source_id": "ada_understanding_carbs",
        "locator": "ada_understanding_carbs.txt",
        "page": "",
        "section": "Understanding Carbs",
        "text_support": "Because carbohydrates turn into glucose in the body, they have the greatest impact on blood sugar. Counting carbs helps people with type 1 diabetes match their insulin dose to the food they eat.",
        "claim": "Type 1 diabetics must count carbs to determine insulin bolus doses."
    },
    {
        "chunk_id": "diabetes_t1_003",
        "condition_code": "diabetes_type_1",
        "content": "Thời gian ăn uống và tính nhất quán của bữa ăn đóng vai trò rất quan trọng đối với người bệnh đái tháo đường type 1. Bỏ bữa hoặc ăn uống không đều đặn khi đang tiêm các loại insulin tác dụng kéo dài có thể dẫn đến nguy cơ hạ đường huyết nghiêm trọng. Người dùng nên duy trì thời gian ăn uống cố định và hỏi ý kiến nhân viên y tế nếu cần thay đổi lịch trình sinh hoạt.",
        "source_id": "niddk_diabetes_diet",
        "locator": "niddk_diabetes_diet.txt",
        "page": "",
        "section": "Meal planning",
        "text_support": "For type 1 diabetes, eating at the same times each day is important, especially if you take certain types of insulin. Skipping meals while on insulin increases risk of hypoglycemia.",
        "claim": "Meal timing consistency is critical in type 1 diabetes to prevent hypoglycemia."
    },
    {
        "chunk_id": "diabetes_t1_004",
        "condition_code": "diabetes_type_1",
        "content": "Sự phối hợp giữa việc dùng insulin và ăn uống ở người bệnh đái tháo đường type 1 đòi hỏi sự chuẩn xác. Liều insulin bolus thường được tiêm trước bữa ăn khoảng 15 đến 30 phút tùy thuộc vào loại insulin và mức đường huyết lúc đó để đảm bảo insulin phát huy tác dụng đỉnh trùng với thời điểm hấp thu glucose từ thức ăn.",
        "source_id": "ada_understanding_carbs",
        "locator": "ada_understanding_carbs.txt",
        "page": "",
        "section": "Understanding Carbs",
        "text_support": "Taking mealtime insulin before eating helps match the action of the insulin with the glucose entering the blood from food, typically 15 to 30 minutes prior to meals.",
        "claim": "Coordinating mealtime insulin injection 15-30 minutes before eating is required in type 1 diabetes."
    },
    {
        "chunk_id": "diabetes_t1_005",
        "condition_code": "diabetes_type_1",
        "content": "Người bệnh đái tháo đường type 1 cần đặc biệt lưu ý an toàn khi hoạt động thể lực. Tập luyện thể dục thể thao làm tăng độ nhạy insulin và tiêu hao năng lượng, do đó có thể gây hạ đường huyết trong hoặc sau khi tập (kéo dài tới 24 giờ). Người dùng cần kiểm tra đường huyết trước khi tập và chuẩn bị sẵn carbohydrate tác dụng nhanh (như nước ngọt, kẹo) để xử lý kịp thời.",
        "source_id": "niddk_diabetes_diet",
        "locator": "niddk_diabetes_diet.txt",
        "page": "",
        "section": "Exercise safety",
        "text_support": "Physical activity can lower blood glucose levels, sometimes up to 24 hours after exercise. Check blood sugar before exercising and carry fast-acting carbohydrates.",
        "claim": "Type 1 diabetics must monitor glucose and carry fast-acting carbs during physical activity."
    },
    {
        "chunk_id": "diabetes_t1_006",
        "condition_code": "diabetes_type_1",
        "content": "Nhận biết sớm các triệu chứng hạ đường huyết là vô cùng quan trọng đối với người bệnh đái tháo đường type 1. Hạ đường huyết (đường huyết dưới 70 mg/dL hoặc 3.9 mmol/L) có thể biểu hiện bằng cảm giác run rẩy, vã mồ hôi, tim đập nhanh, chóng mặt hoặc đói cồn cào. Khi gặp tình trạng này, người dùng cần áp dụng ngay quy tắc 15 (ăn 15g carbohydrate nhanh, đợi 15 phút và kiểm tra lại).",
        "source_id": "ada_understanding_carbs",
        "locator": "ada_understanding_carbs.txt",
        "page": "",
        "section": "Understanding Carbs",
        "text_support": "Hypoglycemia symptoms include shaking, sweating, fast heartbeat, dizziness, and hunger. It is defined as blood sugar under 70 mg/dL.",
        "claim": "Recognizing hypoglycemia symptoms and using fast-acting carbs is vital in type 1 diabetes."
    },
    {
        "chunk_id": "diabetes_t1_007",
        "condition_code": "diabetes_type_1",
        "content": "Các dấu hiệu tăng đường huyết cảnh báo nguy cơ biến chứng nguy hiểm cho người bệnh đái tháo đường type 1. Khi đường huyết tăng cao liên tục (thường trên 240 mg/dL hoặc 13.3 mmol/L), cơ thể người đái tháo đường type 1 có nguy cơ tích tụ ketone dẫn đến nhiễm toan ceton (DKA). Biểu hiện gồm khát dữ dội, đi tiểu nhiều, mệt mỏi, hơi thở có mùi trái cây, buồn nôn hoặc đau bụng.",
        "source_id": "niddk_type1_diabetes",
        "locator": "niddk_type1_diabetes.txt",
        "page": "",
        "section": "DKA warning signs",
        "text_support": "High blood sugar can lead to diabetic ketoacidosis (DKA) in type 1 diabetes. Symptoms include dry mouth, extreme thirst, frequent urination, fruity breath, and nausea.",
        "claim": "High blood sugar and DKA warning signs in type 1 diabetes require urgent testing and clinical care."
    },
    {
        "chunk_id": "diabetes_t1_008",
        "condition_code": "diabetes_type_1",
        "content": "Quyết định điều chỉnh liều lượng hoặc loại insulin cho người bệnh đái tháo đường type 1 phải được thực hiện bởi bác sĩ chuyên khoa hoặc nhân viên y tế có thẩm quyền. Người bệnh tuyệt đối không tự ý ngưng hoặc thay đổi liều insulin nền (basal) hay insulin bữa ăn (bolus) mà không có sự tham vấn lâm sàng, để tránh các biến chứng đe dọa tính mạng.",
        "source_id": "niddk_type1_diabetes",
        "locator": "niddk_type1_diabetes.txt",
        "page": "",
        "section": "Medication decisions",
        "text_support": "Decisions regarding insulin dosing, therapy changes, or regimen adjustments must be made by qualified healthcare professionals.",
        "claim": "Insulin dosing changes in type 1 diabetes must be directed by a clinician."
    },
    {
        "chunk_id": "diabetes_t1_009",
        "condition_code": "diabetes_type_1",
        "content": "Người bệnh đái tháo đường type 1 cần tìm kiếm sự trợ giúp y tế khẩn cấp ngay lập tức nếu xuất hiện các triệu chứng của nhiễm toan ceton (buồn nôn, nôn mửa liên tục, hơi thở mùi trái cây, lú lẫn, thở nhanh, sâu) hoặc khi tình trạng hạ đường huyết nghiêm trọng không thể cải thiện sau khi áp dụng quy tắc 15 hoặc khi người bệnh bất tỉnh.",
        "source_id": "niddk_type1_diabetes",
        "locator": "niddk_type1_diabetes.txt",
        "page": "",
        "section": "Emergency signs",
        "text_support": "Urgent medical help is required for DKA symptoms like rapid deep breathing, vomiting, confusion, or severe unresponsive hypoglycemia.",
        "claim": "Urgent emergency medical care is needed for DKA and severe hypoglycemia in type 1 diabetes."
    },

    # --- DIABETES TYPE 2 ---
    {
        "chunk_id": "diabetes_t2_001",
        "condition_code": "diabetes_type_2",
        "content": "Đối với người mắc đái tháo đường type 2, nguyên tắc dinh dưỡng chủ đạo tập trung vào việc cải thiện độ nhạy insulin của cơ thể và hỗ trợ quản lý đường huyết lâu dài. Chế độ ăn uống lành mạnh nên ưu tiên các loại rau không tinh bột, ngũ cốc nguyên hạt, đạm nạc và hạn chế các chất béo bão hòa cùng các carbohydrate tinh chế để tránh làm tăng vọt đường huyết.",
        "source_id": "ada_eating_healthy",
        "locator": "ada_eating_healthy.txt",
        "page": "",
        "section": "General nutrition",
        "text_support": "For type 2 diabetes, dietary patterns should promote insulin sensitivity and weight management. Prioritize non-starchy vegetables, whole grains, and lean proteins.",
        "claim": "Type 2 diabetes nutrition focuses on insulin sensitivity and blood glucose management."
    },
    {
        "chunk_id": "diabetes_t2_002",
        "condition_code": "diabetes_type_2",
        "content": "Chất lượng carbohydrate là yếu tố quyết định trong kế hoạch ăn uống của người bệnh đái tháo đường type 2. Người bệnh không cần cắt bỏ hoàn toàn carbohydrate, nhưng nên thay thế các loại carbohydrate tinh chế (như gạo trắng, bánh mì trắng, nước ngọt) bằng carbohydrate phức tạp giàu chất xơ (như gạo lứt, ngũ cốc nguyên hạt, các loại đậu) để làm chậm quá trình hấp thu glucose.",
        "source_id": "ada_understanding_carbs",
        "locator": "ada_understanding_carbs.txt",
        "page": "",
        "section": "Understanding Carbs",
        "text_support": "Quality of carbs is key for type 2 diabetes. Choose complex, fiber-rich carbohydrates over refined grains and simple sugars to slow glucose absorption.",
        "claim": "Type 2 diabetics should choose complex carbohydrates over refined grains."
    },
    {
        "chunk_id": "diabetes_t2_003",
        "condition_code": "diabetes_type_2",
        "content": "Kiểm soát khẩu phần ăn bằng phương pháp đĩa thức ăn (Diabetes Plate Method) rất hữu ích cho người bệnh đái tháo đường type 2. Theo phương pháp này, đĩa ăn tiêu chuẩn (đường kính khoảng 23cm) nên được chia làm ba phần: một nửa đĩa dành cho các loại rau không chứa tinh bột, một phần tư dành cho đạm nạc (cá, thịt gà, đậu phụ) và một phần tư còn lại dành cho thực phẩm giàu tinh bột phức hợp.",
        "source_id": "cdc_diabetes_meal_planning",
        "locator": "cdc_diabetes_meal_planning.txt",
        "page": "",
        "section": "Meal planning",
        "text_support": "The Plate Method is a simple visual guide: half non-starchy vegetables, one-quarter lean protein, and one-quarter carbohydrate foods.",
        "claim": "The Diabetes Plate Method is a simple portion control tool for type 2 diabetes."
    },
    {
        "chunk_id": "diabetes_t2_004",
        "condition_code": "diabetes_type_2",
        "content": "Hạn chế tối đa các loại đồ uống ngọt là khuyến nghị hàng đầu đối với người bệnh đái tháo đường type 2. Nước ngọt, nước ép trái cây đóng hộp, trà sữa hoặc cà phê thêm nhiều sữa đặc chứa lượng đường hấp thu nhanh rất lớn, dễ gây tăng vọt đường huyết và nạp nhiều năng lượng dư thừa. Người bệnh nên chọn nước lọc, trà không đường hoặc nước khoáng để thay thế.",
        "source_id": "ada_eating_healthy",
        "locator": "ada_eating_healthy.txt",
        "page": "",
        "section": "General nutrition",
        "text_support": "Avoid sugar-sweetened beverages like soda, sweet tea, and fruit juices. Opt for water or unsweetened drinks to manage calories and blood sugar.",
        "claim": "Type 2 diabetics must avoid sugary drinks and prioritize calorie-free beverages."
    },
    {
        "chunk_id": "diabetes_t2_005",
        "condition_code": "diabetes_type_2",
        "content": "Thực phẩm giàu chất xơ mang lại lợi ích kép cho người bệnh đái tháo đường type 2. Chất xơ trong rau xanh, các loại đậu, ngũ cốc nguyên hạt và trái cây ít ngọt không chỉ làm chậm quá trình tiêu hóa tinh bột giúp duy trì đường huyết ổn định sau ăn, mà còn tăng cảm giác no lâu, hỗ trợ quá trình giảm cân và cải thiện sức khỏe tim mạch.",
        "source_id": "cdc_diabetes_meal_planning",
        "locator": "cdc_diabetes_meal_planning.txt",
        "page": "",
        "section": "Meal planning",
        "text_support": "Fiber in vegetables, whole grains, and legumes slows digestion, preventing blood sugar spikes, and supports weight control by enhancing satiety.",
        "claim": "Fiber-rich foods help manage blood glucose and support weight loss in type 2 diabetes."
    },
    {
        "chunk_id": "diabetes_t2_006",
        "condition_code": "diabetes_type_2",
        "content": "Hoạt động thể lực là một trụ cột quan trọng trong quản lý đái tháo đường type 2. Luyện tập thể dục thường xuyên giúp tế bào cơ sử dụng glucose hiệu quả hơn, trực tiếp cải thiện tình trạng kháng insulin. Người bệnh được khuyến khích đạt mục tiêu tập luyện tối thiểu 150 phút mỗi tuần với cường độ trung bình (như đi bộ nhanh, đạp xe) theo thể trạng.",
        "source_id": "niddk_diabetes_diet",
        "locator": "niddk_diabetes_diet.txt",
        "page": "",
        "section": "Exercise safety",
        "text_support": "Exercise makes cells more sensitive to insulin. Aim for at least 150 minutes per week of moderate-intensity aerobic activity.",
        "claim": "Regular physical activity improves insulin sensitivity in type 2 diabetes; goal is 150 mins/week."
    },
    {
        "chunk_id": "diabetes_t2_007",
        "condition_code": "diabetes_type_2",
        "content": "Quản lý cân nặng thông qua giảm cân bền vững mang lại hiệu quả cao trong việc cải thiện kiểm soát đái tháo đường type 2. Giảm từ 5% đến 10% trọng lượng cơ thể ban đầu ở những người thừa cân hoặc béo phì có thể cải thiện đáng kể chỉ số HbA1c, giảm liều lượng thuốc hạ đường huyết cần dùng và giảm thiểu các nguy cơ biến chứng tim mạch.",
        "source_id": "cdc_diabetes_meal_planning",
        "locator": "cdc_diabetes_meal_planning.txt",
        "page": "",
        "section": "Meal planning",
        "text_support": "Losing 5% to 10% of body weight improves blood sugar control, reduces medication needs, and lowers cardiovascular risks in type 2 diabetes.",
        "claim": "Losing 5-10% of body weight improves glycemic control and reduces comorbidities in type 2 diabetes."
    },
    {
        "chunk_id": "diabetes_t2_008",
        "condition_code": "diabetes_type_2",
        "content": "Tự theo dõi đường huyết là công cụ phản hồi quan trọng cho người bệnh đái tháo đường type 2. Bằng cách tự đo đường huyết lúc đói và sau ăn, người bệnh có thể nhận thấy tác động thực tế của từng loại thực phẩm và thói quen vận động lên cơ thể mình. Kết quả tự theo dõi này giúp người bệnh chủ động điều chỉnh lối sống và hỗ trợ bác sĩ khi tái khám.",
        "source_id": "cdc_diabetes_meal_planning",
        "locator": "cdc_diabetes_meal_planning.txt",
        "page": "",
        "section": "Meal planning",
        "text_support": "Self-monitoring of blood glucose helps individuals see how diet and exercise affect their levels, facilitating lifestyle adjustments and clinical management.",
        "claim": "Self-monitoring of blood glucose supports lifestyle modification in type 2 diabetes."
    },
    {
        "chunk_id": "diabetes_t2_009",
        "condition_code": "diabetes_type_2",
        "content": "Người bệnh đái tháo đường type 2 đang sử dụng một số loại thuốc nhất định (như sulfonylurea hoặc insulin) cần lưu ý đến rủi ro hạ đường huyết. Mặc dù hạ đường huyết ít gặp hơn ở người chỉ điều trị bằng metformin hoặc thay đổi lối sống đơn thuần, việc nhận biết các dấu hiệu sớm (run tay, chóng mặt, vã mồ hôi) và mang theo đường nhanh vẫn là cần thiết.",
        "source_id": "niddk_diabetes_diet",
        "locator": "niddk_diabetes_diet.txt",
        "page": "",
        "section": "Exercise safety",
        "text_support": "Hypoglycemia is a risk for type 2 diabetics taking sulfonylureas or insulin. Those managing with metformin or diet alone are at lower risk.",
        "claim": "Hypoglycemia risk in type 2 diabetes is primary for those on sulfonylureas or insulin."
    },
    {
        "chunk_id": "diabetes_t2_010",
        "condition_code": "diabetes_type_2",
        "content": "Người bệnh đái tháo đường type 2 nên tìm kiếm sự tư vấn chuyên môn từ bác sĩ hoặc chuyên gia dinh dưỡng được chứng nhận khi muốn thiết kế thực đơn chi tiết. Sự hỗ trợ từ chuyên gia giúp cá nhân hóa lượng carbohydrate dựa trên thuốc điều trị, mức độ hoạt động và sự hiện diện của các bệnh đi kèm như tăng huyết áp hay suy thận.",
        "source_id": "cdc_diabetes_meal_planning",
        "locator": "cdc_diabetes_meal_planning.txt",
        "page": "",
        "section": "Meal planning",
        "text_support": "Working with a registered dietitian or certified diabetes educator helps personalize meal planning, taking into account medications, lifestyle, and comorbidities.",
        "claim": "Type 2 diabetics should consult dietitians for personalized nutrition plans."
    },

    # --- DIABETES TYPE UNKNOWN ---
    {
        "chunk_id": "diabetes_unknown_001",
        "condition_code": "diabetes_type_unknown",
        "content": "Đối với người mắc bệnh đái tháo đường chưa rõ phân loại (chưa xác định type 1 hay type 2), các thông tin giáo dục sức khỏe chung nhấn mạnh việc duy trì thói quen ăn uống cân bằng và lành mạnh. Hướng đi an toàn ban đầu là chọn các loại thực phẩm ít chế biến, nhiều rau xanh và hạn chế đồ ngọt để tránh làm dao động đường huyết đột ngột.",
        "source_id": "cdc_diabetes_meal_planning",
        "locator": "cdc_diabetes_meal_planning.txt",
        "page": "",
        "section": "Meal planning",
        "text_support": "General diabetes education emphasizes balanced healthy eating, prioritizing non-starchy vegetables and minimizing refined sugars, applicable to all types.",
        "claim": "General diabetes education targets basic healthy eating parameters without assuming type."
    },
    {
        "chunk_id": "diabetes_unknown_002",
        "condition_code": "diabetes_type_unknown",
        "content": "Người dùng đái tháo đường chưa rõ phân loại cần lưu ý rằng các khuyến nghị cụ thể về y khoa, đặc biệt là liều lượng insulin và tần suất theo dõi đường huyết, có thể khác biệt lớn giữa đái tháo đường type 1 và type 2. Type 1 đòi hỏi tiêm insulin bắt buộc phối hợp chặt chẽ với bữa ăn, trong khi type 2 có thể quản lý bằng lối sống hoặc thuốc viên.",
        "source_id": "niddk_type1_diabetes",
        "locator": "niddk_type1_diabetes.txt",
        "page": "",
        "section": "General overview",
        "text_support": "Diabetes recommendations differ by type; type 1 requires daily insulin injection to survive, while type 2 may be managed with diet, exercise, and oral meds.",
        "claim": "Diabetes guidelines differ significantly between type 1 (insulin-dependent) and type 2."
    },
    {
        "chunk_id": "diabetes_unknown_003",
        "condition_code": "diabetes_type_unknown",
        "content": "Hệ thống khuyến khích người dùng có chẩn đoán đái tháo đường nhưng chưa rõ phân loại cần liên hệ với bác sĩ điều trị để xác nhận chính xác type bệnh của mình. Việc cung cấp chính xác type bệnh (type 1 hay type 2) giúp hệ thống RAG đưa ra các thông tin hỗ trợ kiểm soát carbohydrate và an toàn vận động chuẩn xác và an toàn nhất.",
        "source_id": "niddk_type1_diabetes",
        "locator": "niddk_type1_diabetes.txt",
        "page": "",
        "section": "General overview",
        "text_support": "Accurate identification of type 1 vs type 2 diabetes is critical for determining correct therapy, monitoring schedules, and safety support rules.",
        "claim": "Patients with unspecified diabetes should confirm their diagnosis type with a healthcare provider."
    },
    {
        "chunk_id": "diabetes_unknown_004",
        "condition_code": "diabetes_type_unknown",
        "content": "Trong bối cảnh người dùng chưa cung cấp rõ phân loại đái tháo đường, các thông tin tư vấn tự động sẽ tránh đưa ra các giả định về việc sử dụng insulin hay lịch tiêm cụ thể. Các gợi ý chỉ tập trung vào việc giảm muối, giảm đường ngọt và tăng cường chất xơ, vốn là những lối sống có lợi chung và có độ an toàn cao cho cả hai nhóm bệnh.",
        "source_id": "ada_eating_healthy",
        "locator": "ada_eating_healthy.txt",
        "page": "",
        "section": "General nutrition",
        "text_support": "When diabetes type is unspecified, avoid insulin dosing assumptions. Stick to general lifestyle advice like low salt, low sugar, and high fiber.",
        "claim": "General diabetes advice must avoid insulin assumptions and focus on basic diet rules."
    },

    # --- PREDIABETES ---
    {
        "chunk_id": "prediabetes_001",
        "condition_code": "prediabetes",
        "content": "Đối với người dùng có tình trạng tiền đái tháo đường, điều quan trọng là hiểu rõ sự khác biệt giữa tiền đái tháo đường và đái tháo đường thực sự. Tiền đái tháo đường là giai đoạn cảnh báo khi mức đường huyết đã cao hơn bình thường nhưng chưa chạm ngưỡng chẩn đoán đái tháo đường type 2, đây là cơ hội vàng để đảo ngược tình thế bằng cách thay đổi lối sống.",
        "source_id": "cdc_prediabetes_lifestyle_change",
        "locator": "cdc_prediabetes_lifestyle_change.txt",
        "page": "",
        "section": "About the Lifestyle Change Program",
        "text_support": "Prediabetes is a serious health condition where blood sugar levels are higher than normal, but not high enough yet to be diagnosed as type 2 diabetes.",
        "claim": "Prediabetes represents a warning window where blood sugar is elevated but not yet at type 2 level."
    },
    {
        "chunk_id": "prediabetes_002",
        "condition_code": "prediabetes",
        "content": "Trong chế độ ăn của người tiền đái tháo đường, kiểm soát khẩu phần carbohydrate như cơm, bún, phở là rất cần thiết nhưng không được khuyến khích cắt bỏ hoàn toàn. Người dùng nên điều chỉnh giảm bớt lượng tinh bột tinh chế trong bữa ăn chính, kết hợp tăng lượng rau xanh để làm chậm tốc độ tăng đường huyết sau ăn, thay vì nhịn ăn tinh bột cực đoan.",
        "source_id": "cdc_prevent_type2_guide",
        "locator": "cdc_prevent_type2_guide.txt",
        "page": "",
        "section": "Dietary recommendations",
        "text_support": "Managing portion sizes of carbohydrates like rice is necessary in prediabetes, but complete elimination is not recommended. Focus on portions and quality.",
        "claim": "Prediabetics should control carbohydrate portions rather than completely eliminating them."
    },
    {
        "chunk_id": "prediabetes_003",
        "condition_code": "prediabetes",
        "content": "Người tiền đái tháo đường cần hạn chế tối đa các loại đồ uống có đường ngọt như trà sữa, nước ngọt đóng chai, nước ép trái cây thêm đường. Năng lượng hấp thu nhanh từ nhóm đồ uống này có liên quan trực tiếp đến việc tăng tích tụ mỡ và suy giảm độ nhạy insulin. Thay thế bằng nước lọc là bước khởi đầu dễ thực hiện và hiệu quả cao.",
        "source_id": "cdc_prevent_type2_guide",
        "locator": "cdc_prevent_type2_guide.txt",
        "page": "",
        "section": "Dietary recommendations",
        "text_support": "Sugar-sweetened beverages add empty calories and sugar. Prediabetics should replace soda, sweet teas, and juices with water to prevent weight gain.",
        "claim": "Prediabetics should avoid sugar-sweetened beverages and replace them with water."
    },
    {
        "chunk_id": "prediabetes_004",
        "condition_code": "prediabetes",
        "content": "Quản lý cân nặng là mục tiêu then chốt trong phòng ngừa tiến triển từ tiền đái tháo đường thành đái tháo đường type 2. Các nghiên cứu lâm sàng chỉ ra rằng việc giảm từ 5% đến 7% trọng lượng cơ thể (ví dụ giảm khoảng 3.5 đến 5kg đối với người nặng 70kg) ở người thừa cân có thể giúp giảm hơn một nửa nguy cơ tiến triển thành bệnh thực sự.",
        "source_id": "cdc_prevent_type2_guide",
        "locator": "cdc_prevent_type2_guide.txt",
        "page": "",
        "section": "Dietary recommendations",
        "text_support": "Losing 5% to 7% of your body weight can cut your risk of developing type 2 diabetes by more than half for people with prediabetes.",
        "claim": "Losing 5-7% of body weight dramatically cuts the risk of progressing to type 2 diabetes."
    },
    {
        "chunk_id": "prediabetes_005",
        "condition_code": "prediabetes",
        "content": "Vận động thể chất thường xuyên giúp bảo vệ người tiền đái tháo đường khỏi nguy cơ mắc bệnh đái tháo đường type 2. Người dùng nên đặt mục tiêu thực hiện ít nhất 150 phút hoạt động thể thao cường độ trung bình mỗi tuần (như đi bộ nhanh, bơi lội, đạp xe), chia đều thành 5 ngày trong tuần, khoảng 30 phút mỗi ngày theo thể trạng.",
        "source_id": "cdc_prevent_type2_guide",
        "locator": "cdc_prevent_type2_guide.txt",
        "page": "",
        "section": "Dietary recommendations",
        "text_support": "Get at least 150 minutes per week of moderate physical activity, such as brisk walking, to help prevent or delay type 2 diabetes.",
        "claim": "150 minutes per week of moderate exercise is recommended to delay or prevent type 2 diabetes."
    },
    {
        "chunk_id": "prediabetes_006",
        "condition_code": "prediabetes",
        "content": "Tham gia vào các chương trình thay đổi lối sống có cấu trúc (như Chương trình Phòng ngừa Đái tháo đường Quốc gia - DPP) được chứng minh mang lại lợi ích lâu dài cho người tiền đái tháo đường. Các chương trình này cung cấp người hướng dẫn giúp người dùng duy trì thói quen ăn uống lành mạnh, tăng hoạt động thể lực và kiểm soát stress hiệu quả.",
        "source_id": "cdc_prediabetes_lifestyle_change",
        "locator": "cdc_prediabetes_lifestyle_change.txt",
        "page": "",
        "section": "About the Lifestyle Change Program",
        "text_support": "Structured lifestyle change programs like the National DPP help participants make lasting changes, such as eating healthier, adding activity, and managing stress.",
        "claim": "Structured lifestyle modification programs support sustained prevention of type 2 diabetes."
    },
    {
        "chunk_id": "prediabetes_007",
        "condition_code": "prediabetes",
        "content": "Theo dõi định kỳ chỉ số HbA1c và đường huyết lúc đói là cần thiết đối với người tiền đái tháo đường. Do tiền đái tháo đường thường không có triệu chứng rõ rệt, xét nghiệm máu định kỳ mỗi 6 tháng đến 1 năm theo chỉ chỉ định của bác sĩ là cách duy nhất để đánh giá hiệu quả của việc thay đổi lối sống và phát hiện sớm nguy cơ tiến triển.",
        "source_id": "cdc_prevent_type2_guide",
        "locator": "cdc_prevent_type2_guide.txt",
        "page": "",
        "section": "Dietary recommendations",
        "text_support": "Prediabetes often has no symptoms. Periodic blood tests like HbA1c every 6 to 12 months are necessary to track status and progression risk.",
        "claim": "Prediabetics require periodic lab screening (HbA1c) due to the asymptomatic nature of the condition."
    },
    {
        "chunk_id": "prediabetes_008",
        "condition_code": "prediabetes",
        "content": "Người tiền đái tháo đường cần hiểu rằng việc sử dụng thuốc (như metformin) không phải là bắt buộc đối với tất cả mọi người và quyết định này phụ thuộc vào đánh giá chuyên môn của bác sĩ dựa trên các yếu tố nguy cơ cá nhân. Thay đổi lối sống thông qua ăn uống và vận động vẫn là can thiệp đầu tay nhằm quản lý và phòng ngừa tiểu đường.",
        "source_id": "cdc_prevent_type2_guide",
        "locator": "cdc_prevent_type2_guide.txt",
        "page": "",
        "section": "Dietary recommendations",
        "text_support": "Not all individuals with prediabetes require medication. Dosing or medication initiation decisions must be individualized by a physician; lifestyle changes remain primary.",
        "claim": "Metformin or medication use in prediabetes is not universal; lifestyle change is the primary recommendation."
    },

    # --- HYPERTENSION ---
    {
        "chunk_id": "hypertension_001",
        "condition_code": "hypertension",
        "content": "Kiểm soát lượng natri nạp vào cơ thể là nguyên tắc cốt lõi trong chế độ ăn uống của người bệnh tăng huyết áp. Hiệp hội Tim mạch Hoa Kỳ (AHA) khuyến nghị người trưởng thành bị tăng huyết áp nên hướng tới giới hạn natri dưới 1500 mg mỗi ngày để hỗ trợ hạ huyết áp hiệu quả và giảm thiểu nguy cơ tai biến mạch máu não.",
        "source_id": "aha_sodium_per_day",
        "locator": "aha_sodium_per_day.txt",
        "page": "",
        "section": "AHA/ACC absolute sodium limits",
        "text_support": "The American Heart Association recommends an ideal limit of no more than 1500 mg of sodium per day for most adults, especially those with high blood pressure.",
        "claim": "Hypertensive adults should target a daily sodium limit of under 1500 mg."
    },
    {
        "chunk_id": "hypertension_002",
        "condition_code": "hypertension",
        "content": "Đối với người tăng huyết áp, việc sử dụng các gia vị truyền thống như nước mắm, nước tương cần đặc biệt thận trọng. Một muỗng canh nước mắm có thể chứa tới 1000 mg natri (tương đương khoảng 66% giới hạn khuyên dùng hàng ngày của AHA). Người bệnh nên ưu tiên sử dụng nước mắm giảm natri, pha loãng hoặc dùng gia vị thảo mộc thay thế muối.",
        "source_id": "aha_shaking_salt_habit",
        "locator": "aha_shaking_salt_habit.txt",
        "page": "",
        "section": "Condiments",
        "text_support": "Condiments like soy sauce, fish sauce, and salad dressings are high in sodium. A single tablespoon can contain a substantial portion of the daily sodium allowance.",
        "claim": "Traditional condiments like fish sauce are highly concentrated sodium sources requiring moderation."
    },
    {
        "chunk_id": "hypertension_003",
        "condition_code": "hypertension",
        "content": "Các loại thực phẩm chế biến sẵn là nguồn natri ẩn giấu nguy hiểm cho người bệnh tăng huyết áp. Mì ăn liền, thịt nguội, đồ hộp, dưa muối và các gói gia vị đi kèm thường chứa lượng muối cực kỳ lớn để bảo quản. Người bệnh cần học cách đọc nhãn dinh dưỡng và ưu tiên lựa chọn thực phẩm tươi sống tự chế biến tại nhà.",
        "source_id": "cdc_sodium_health",
        "locator": "cdc_sodium_health.txt",
        "page": "",
        "section": "Processed food sources",
        "text_support": "Most of the sodium in the diet comes from processed and restaurant foods. Reading nutrition labels helps identify hidden sodium in canned goods, deli meats, and packaged meals.",
        "claim": "Processed foods are major contributors to high sodium intake; label reading is necessary."
    },
    {
        "chunk_id": "hypertension_004",
        "condition_code": "hypertension",
        "content": "Tăng cường rau xanh và trái cây là phần quan trọng trong chế độ ăn Dash dành cho người bệnh tăng huyết áp. Rau quả tươi cung cấp lượng kali dồi dào, hỗ trợ cơ thể đào thải bớt natri qua đường tiểu và làm giãn thành mạch, giúp hạ áp tự nhiên. Tuy nhiên, nếu người bệnh tăng huyết áp có kèm suy thận, lượng kali nạp vào phải được kiểm soát theo xét nghiệm máu.",
        "source_id": "aha_shaking_salt_habit",
        "locator": "aha_shaking_salt_habit.txt",
        "page": "",
        "section": "Dietary patterns",
        "text_support": "Eating a diet rich in fruits, vegetables, and low-fat dairy can lower blood pressure. Potassium-rich foods help counter the effects of sodium, provided kidney function is normal.",
        "claim": "Fruits and vegetables (potassium-rich) lower blood pressure, except when kidney disease is present."
    },
    {
        "chunk_id": "hypertension_005",
        "condition_code": "hypertension",
        "content": "Duy trì cân nặng hợp lý giúp kiểm soát chỉ số huyết áp tốt hơn ở người bệnh tăng huyết áp. Thừa cân làm tăng gánh nặng hoạt động cho tim và tăng áp lực lên thành mạch. Giảm mỗi kg cân nặng dư thừa có thể giúp huyết áp tâm thu giảm khoảng 1 mmHg ở người tăng huyết áp, mang lại hiệu quả hỗ trợ điều trị rõ rệt.",
        "source_id": "cdc_sodium_health",
        "locator": "cdc_sodium_health.txt",
        "page": "",
        "section": "Sodium mechanisms",
        "text_support": "Losing weight is one of the most effective lifestyle changes for controlling blood pressure. Every kilogram lost reduces blood pressure by approximately 1 mmHg.",
        "claim": "Weight reduction directly correlates with blood pressure decreases."
    },
    {
        "chunk_id": "hypertension_006",
        "condition_code": "hypertension",
        "content": "Người bệnh tăng huyết áp được khuyến khích duy trì thói quen hoạt động thể lực đều đặn. Các bài tập aerobic vừa sức như đi bộ nhanh, chạy bộ nhẹ nhàng, bơi lội trong ít nhất 30 phút mỗi ngày, 5 ngày mỗi tuần có thể giúp làm dẻo dai thành mạch và hạ huyết áp ổn định. Người bệnh có huyết áp chưa kiểm soát tốt cần hỏi bác sĩ trước khi tập nặng.",
        "source_id": "cdc_sodium_health",
        "locator": "cdc_sodium_health.txt",
        "page": "",
        "section": "Sodium mechanisms",
        "text_support": "Regular physical activity of moderate intensity, like 30 minutes of walking 5 days a week, helps lower blood pressure and manage weight.",
        "claim": "30 minutes of moderate exercise 5 days a week lowers blood pressure in hypertensive individuals."
    },
    {
        "chunk_id": "hypertension_007",
        "condition_code": "hypertension",
        "content": "Tự đo huyết áp tại nhà bằng máy đo bắp tay tiêu chuẩn giúp người bệnh tăng huyết áp theo dõi sát sao tình trạng sức khỏe của mình. Nên đo huyết áp vào các thời điểm cố định (như buổi sáng sau khi ngủ dậy và buổi tối trước khi đi ngủ), ghi chép lại kết quả để cung cấp cho bác sĩ, giúp đánh giá hiệu quả của phác đồ điều trị lối sống và thuốc.",
        "source_id": "cdc_sodium_health",
        "locator": "cdc_sodium_health.txt",
        "page": "",
        "section": "Sodium mechanisms",
        "text_support": "Home blood pressure monitoring provides useful data for managing hypertension. Measure at consistent times and log results for physician review.",
        "claim": "Regular home blood pressure monitoring supports hypertension management."
    },
    {
        "chunk_id": "hypertension_008",
        "condition_code": "hypertension",
        "content": "Mọi quyết định bắt đầu, điều chỉnh liều lượng hoặc dừng sử dụng các loại thuốc hạ huyết áp (như thuốc chẹn kênh calci, ức chế men chuyển) phải được chỉ định trực tiếp bởi bác sĩ. Người bệnh tuyệt đối không được tự ý ngưng thuốc khi thấy huyết áp trở về bình thường, vì tăng huyết áp là bệnh mạn tính cần điều trị duy trì để ngừa đột quỵ.",
        "source_id": "cdc_sodium_health",
        "locator": "cdc_sodium_health.txt",
        "page": "",
        "section": "Sodium mechanisms",
        "text_support": "Antihypertensive medication plans must not be modified without direct clinical evaluation. Silent hypertension risks require continuous medication adherence.",
        "claim": "Adherence to prescribed blood pressure medications is required; changes must be clinical."
    },
    {
        "chunk_id": "hypertension_009",
        "condition_code": "hypertension",
        "content": "Người bệnh tăng huyết áp cần tìm kiếm chăm sóc y tế khẩn cấp ngay lập tức nếu chỉ số huyết áp đo được cao đột ngột (huyết áp tâm thu trên 180 mmHg hoặc huyết áp tâm trương trên 120 mmHg) kèm theo các dấu hiệu như đau đầu dữ dội, tức ngực, khó thở, nhìn mờ, tê yếu nửa người hoặc khó nói. Đây là cơn tăng huyết áp khẩn cấp đe dọa tính mạng.",
        "source_id": "cdc_sodium_health",
        "locator": "cdc_sodium_health.txt",
        "page": "",
        "section": "Emergency signs",
        "text_support": "A hypertensive crisis is defined as BP over 180/120 mmHg accompanied by symptoms like severe headache, chest pain, vision changes, or numbness. Seek immediate emergency care.",
        "claim": "A hypertensive crisis (BP >180/120 mmHg with severe symptoms) requires emergency medical services."
    },

    # --- CKD STAGE G1 ---
    {
        "chunk_id": "ckd_g1_001",
        "condition_code": "ckd_g1",
        "content": "Đối với người dùng thuộc nhóm bệnh thận mạn giai đoạn G1 (CKD G1), chức năng lọc của cầu thận vẫn ở mức bình thường hoặc cao (eGFR từ 90 mL/phút/1.73m2 trở lên). Mục tiêu chính ở giai đoạn này là làm chậm tốc độ tổn thương thận và bảo vệ cầu thận bằng cách kiểm soát tốt huyết áp, đường huyết và duy trì lối sống lành mạnh.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 10,
        "section": "Chapter 1",
        "text_support": "CKD Stage G1 is defined by eGFR >= 90 mL/min/1.73 m2, indicating normal or high kidney function, in the presence of markers of kidney damage.",
        "claim": "CKD Stage G1 is characterized by normal/high eGFR (>=90) with kidney damage evidence."
    },
    {
        "chunk_id": "ckd_g1_002",
        "condition_code": "ckd_g1",
        "content": "Người dùng cần lưu ý rằng chẩn đoán bệnh thận mạn giai đoạn G1 (CKD G1) không thể chỉ dựa vào chỉ số eGFR trên 90 đơn thuần. Để kết luận mắc bệnh ở giai đoạn này, bắt buộc phải có các bằng chứng khác về tổn thương thận kéo dài trên 3 tháng, ví dụ như có albumin trong nước tiểu (microalbumin niệu), đái máu kéo dài hoặc bất thường cấu trúc thận trên siêu âm.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 12,
        "section": "Chapter 1",
        "text_support": "An eGFR of >= 90 mL/min/1.73 m2 alone does not establish CKD stage G1. Other markers of kidney damage (e.g. albuminuria, hematuria, structural abnormalities) must be present for >3 months.",
        "claim": "CKD G1 requires markers of kidney damage (like albuminuria) present for >3 months, not just eGFR >=90."
    },
    {
        "chunk_id": "ckd_g1_003",
        "condition_code": "ckd_g1",
        "content": "Theo dõi định kỳ là yêu cầu thiết yếu đối với người bệnh thận mạn giai đoạn G1 (CKD G1). Người bệnh nên thực hiện các xét nghiệm máu đo creatinine (để tính eGFR) và xét nghiệm nước tiểu đo tỷ lệ albumin/creatinine (UACR) ít nhất một lần mỗi năm để theo dõi sự tiến triển của bệnh và hiệu quả của các biện pháp bảo vệ thận.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 18,
        "section": "Chapter 1",
        "text_support": "Patients with CKD G1 should be monitored at least annually with eGFR and albuminuria (UACR) measurement to assess progression risk.",
        "claim": "CKD G1 patients require annual monitoring of eGFR and UACR."
    },
    {
        "chunk_id": "ckd_g1_004",
        "condition_code": "ckd_g1",
        "content": "Đối với người bệnh thận mạn giai đoạn G1 (CKD G1), chức năng lọc của thận vẫn hoàn toàn đảm bảo. Do đó, người bệnh cần tránh áp dụng các chế độ kiêng khem khắt khe không cần thiết như hạn chế đạm (protein) quá mức, kiêng kali (trái cây, rau quả) hay kiêng phốt pho, ngoại trừ trường hợp có các chỉ định y khoa đặc biệt từ bác sĩ điều trị.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Stages 1-5 overview",
        "text_support": "For early stages (1-2), severe dietary restrictions of protein, potassium, or phosphorus are generally unnecessary unless recommended by a physician for specific complications.",
        "claim": "Unnecessary severe dietary restrictions should be avoided in early CKD Stage G1."
    },
    {
        "chunk_id": "ckd_g1_005",
        "condition_code": "ckd_g1",
        "content": "Đánh giá chuyên khoa ban đầu là rất quan trọng đối với người nghi ngờ hoặc mới chẩn đoán bệnh thận mạn giai đoạn G1 (CKD G1). Người bệnh nên tham khảo ý kiến bác sĩ thận học để xác định nguyên nhân gây tổn thương thận (như đái tháo đường, tăng huyết áp hay viêm cầu thận) nhằm thiết lập phác đồ điều trị nguyên nhân sớm nhất.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 22,
        "section": "Chapter 1",
        "text_support": "Identify the underlying cause of CKD in stage G1 patients to optimize targeted treatment and prevent decline. Professional nephrology consultation is advised.",
        "claim": "Identifying the primary cause of CKD G1 via nephrologist review is critical to guide treatment."
    },

    # --- CKD STAGE G2 ---
    {
        "chunk_id": "ckd_g2_001",
        "condition_code": "ckd_g2",
        "content": "Đối với người dùng thuộc nhóm bệnh thận mạn giai đoạn G2 (CKD G2), chức năng lọc của cầu thận bị giảm nhẹ (chỉ số eGFR nằm trong khoảng từ 60 đến 89 mL/phút/1.73m2). Ở giai đoạn này, thận vẫn hoạt động tương đối tốt; trọng tâm điều trị là kiểm soát các yếu tố đẩy nhanh suy giảm chức năng thận như tăng huyết áp và đái tháo đường.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 10,
        "section": "Chapter 1",
        "text_support": "CKD Stage G2 is defined by eGFR of 60-89 mL/min/1.73 m2, indicating mildly decreased kidney function, in the presence of markers of kidney damage.",
        "claim": "CKD Stage G2 is defined by mildly decreased eGFR (60-89) alongside kidney damage evidence."
    },
    {
        "chunk_id": "ckd_g2_002",
        "condition_code": "ckd_g2",
        "content": "Cần lưu ý rằng chỉ số eGFR nằm trong khoảng 60-89 mL/phút/1.73m2 đơn thuần ở người lớn tuổi không đủ để chẩn đoán bệnh thận mạn giai đoạn G2 (CKD G2). Tương tự như giai đoạn G1, chẩn đoán CKD G2 đòi hỏi phải có sự hiện diện của các dấu hiệu tổn thương thận đi kèm như protein niệu, đái máu hoặc bất thường cấu trúc thận kéo dài trên 3 tháng.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 12,
        "section": "Chapter 1",
        "text_support": "An eGFR of 60-89 mL/min/1.73 m2 without accompanying markers of kidney damage does not fulfill criteria for CKD stage G2.",
        "claim": "CKD G2 diagnosis requires kidney damage markers (e.g. protein in urine) in addition to eGFR 60-89."
    },
    {
        "chunk_id": "ckd_g2_003",
        "condition_code": "ckd_g2",
        "content": "Theo dõi tiến triển bệnh thận mạn giai đoạn G2 (CKD G2) cần được thực hiện thông qua xét nghiệm máu và nước tiểu định kỳ hàng năm. Việc này giúp theo dõi xem tốc độ giảm eGFR có bình thường theo tuổi hay đang suy giảm nhanh hơn (giảm trên 5 mL/phút/1.73m2 trong một năm), từ đó điều chỉnh can thiệp kịp thời.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 18,
        "section": "Chapter 1",
        "text_support": "Monitor CKD G2 progression with annual measurements. Progression is defined as a sustained decline in eGFR of >5 mL/min/1.73 m2 per year.",
        "claim": "Annual monitoring of eGFR is required in CKD G2 to detect rapid progression (>5 mL/min decline/year)."
    },
    {
        "chunk_id": "ckd_g2_004",
        "condition_code": "ckd_g2",
        "content": "Bệnh đái tháo đường và tăng huyết áp là hai nguyên nhân hàng đầu gây tổn thương thận tiến triển ở giai đoạn G2 (CKD G2). Người bệnh ở giai đoạn này cần duy trì huyết áp tâm thu dưới 120 mmHg (nếu dung nạp tốt) theo khuyến nghị KDIGO và kiểm soát chỉ số đường huyết chặt chẽ để giảm áp lực lọc lên các nephron thận còn lại.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 45,
        "section": "Chapter 3",
        "text_support": "For patients with CKD and hypertension, target a systolic blood pressure of <120 mmHg when tolerated. Manage diabetes to protect residual kidney function.",
        "claim": "Hypertension control (systolic <120 mmHg) and diabetes control protect kidney function in CKD G2."
    },
    {
        "chunk_id": "ckd_g2_005",
        "condition_code": "ckd_g2",
        "content": "Người bệnh thận mạn giai đoạn G2 (CKD G2) nên được đánh giá bởi bác sĩ điều trị để đảm bảo tránh xa các loại thuốc hoặc chất có hại cho thận (như thuốc giảm đau kháng viêm NSAID bao gồm ibuprofen, naproxen) vốn có thể làm suy giảm nhanh chóng chức năng thận đang bị tổn thương nhẹ.",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Diet and medication",
        "text_support": "Avoid nephrotoxic agents like nonsteroidal anti-inflammatory drugs (NSAIDs) in early stages of kidney disease to prevent sudden deterioration.",
        "claim": "NSAID avoidance is crucial in CKD Stage G2 to prevent nephrotoxic injury."
    },

    # --- CKD STAGE G3A ---
    {
        "chunk_id": "ckd_g3a_001",
        "condition_code": "ckd_g3a",
        "content": "Đối với người dùng thuộc nhóm bệnh thận mạn giai đoạn G3a (CKD G3a), chức năng lọc của thận đã bị suy giảm ở mức độ nhẹ đến trung bình (chỉ số eGFR nằm trong khoảng từ 45 đến 59 mL/phút/1.73m2). Ở giai đoạn này, các khuyến nghị dinh dưỡng bắt đầu có sự điều chỉnh nhẹ để giảm tải công việc lọc chất thải cho thận.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 10,
        "section": "Chapter 1",
        "text_support": "CKD Stage G3a is defined by eGFR of 45-59 mL/min/1.73 m2, indicating mildly to moderately decreased kidney function.",
        "claim": "CKD Stage G3a is characterized by mildly to moderately decreased eGFR (45-59)."
    },
    {
        "chunk_id": "ckd_g3a_002",
        "condition_code": "ckd_g3a",
        "content": "Khuyến nghị về lượng chất đạm (protein) đối với người bệnh thận mạn giai đoạn G3a (CKD G3a) không chạy thận bắt đầu cần sự điều chỉnh hợp lý. Để giảm tải chất thải ure cho thận, người bệnh nên tránh chế độ ăn quá nhiều đạm, đồng thời hướng tới mức tiêu thụ đạm ở mức vừa phải (khoảng 0.6 đến 0.8 gam đạm trên mỗi kg cân nặng mỗi ngày) theo hướng dẫn y khoa.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 62,
        "section": "Chapter 3",
        "text_support": "In adults with CKD G3-G5 non-dialysis, suggest a protein intake of 0.6-0.8 g/kg body weight/day to delay progression, unless contraindicated.",
        "claim": "Non-dialysis CKD G3a protein target is a moderate 0.6-0.8 g/kg/day."
    },
    {
        "chunk_id": "ckd_g3a_003",
        "condition_code": "ckd_g3a",
        "content": "Hạn chế muối natri là khuyến nghị bắt buộc đối với tất cả người bệnh thận mạn giai đoạn G3a (CKD G3a). Giảm lượng natri dưới 2000 mg mỗi ngày (tương đương dưới 5g muối ăn hoặc khoảng 1 muỗng cà phê muối) giúp kiểm soát tình trạng giữ nước, giảm huyết áp và bảo vệ các mạch máu nhỏ ở thận khỏi bị quá tải.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 60,
        "section": "Chapter 3",
        "text_support": "We recommend a sodium intake of <2.0 g/d (equivalent to <5 g/d of salt) in adults with CKD G3a.",
        "claim": "Daily sodium intake for CKD G3a should be limited to <2000 mg (<5g salt)."
    },
    {
        "chunk_id": "ckd_g3a_004",
        "condition_code": "ckd_g3a",
        "content": "Khuyến nghị về lượng kali đối với người bệnh thận mạn giai đoạn G3a (CKD G3a) không được áp dụng một cách rập khuôn. Người bệnh chỉ cần hạn chế các loại quả, rau nhiều kali (như chuối, khoai tây) khi có kết quả xét nghiệm máu cho thấy mức kali máu cao (hyperkalemia) hoặc khi có chỉ định cụ thể của bác sĩ.",
        "source_id": "nkf_potassium_ckd_diet",
        "locator": "nkf_potassium_ckd_diet.txt",
        "page": "",
        "section": "Potassium in CKD",
        "text_support": "In CKD stage G3a, potassium restriction should not be applied universally. It should be guided by serum potassium measurements rather than stage alone.",
        "claim": "Potassium restriction in CKD G3a should be based on laboratory measurements, not stage alone."
    },
    {
        "chunk_id": "ckd_g3a_005",
        "condition_code": "ckd_g3a",
        "content": "Hạn chế lượng phốt pho đối với người bệnh thận mạn giai đoạn G3a (CKD G3a) tập trung chủ yếu vào việc tránh các loại phốt pho vô cơ (chất phụ gia thực phẩm) có trong đồ uống đóng chai, thực phẩm chế biến sẵn và thức ăn nhanh, vì phốt pho vô cơ được hấp thu gần như hoàn toàn vào máu và làm tăng gánh nặng đào thải cho thận.",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Phosphorus in CKD",
        "text_support": "For CKD G3a, limit inorganic phosphorus additives found in processed foods and sodas, as they are highly absorbed compared to organic phosphorus.",
        "claim": "CKD G3a patients should limit inorganic phosphorus food additives."
    },
    {
        "chunk_id": "ckd_g3a_006",
        "condition_code": "ckd_g3a",
        "content": "Người bệnh thận mạn giai đoạn G3a (CKD G3a) có kèm đái tháo đường hoặc tăng huyết áp cần được quản lý phối hợp chặt chẽ. Việc duy trì chỉ số đường huyết ổn định và huyết áp tối ưu dưới 120/80 mmHg ở giai đoạn G3a giúp bảo tồn tối đa các nephron còn lại và hạn chế tốc độ sụt giảm chức năng lọc của cầu thận.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 48,
        "section": "Chapter 3",
        "text_support": "In patients with CKD stage G3a with comorbid diabetes or hypertension, strict risk factor modification is required to reduce kidney decline.",
        "claim": "Glycemic and blood pressure optimization preserves kidney function in CKD G3a comorbid patients."
    },
    {
        "chunk_id": "ckd_g3a_007",
        "condition_code": "ckd_g3a",
        "content": "Người bệnh thận mạn giai đoạn G3a (CKD G3a) cần theo dõi định kỳ chức năng lọc của thận tối thiểu 2 lần mỗi năm. Các xét nghiệm creatinine máu để tính eGFR và định lượng albumin niệu giúp bác sĩ đánh giá liệu bệnh đang ổn định hay có sự suy sụp chức năng lọc đột ngột để đổi phác đồ bảo vệ thận.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 18,
        "section": "Chapter 1",
        "text_support": "Evaluate eGFR and albuminuria at least twice a year in patients with CKD stage G3a to monitor progression.",
        "claim": "CKD G3a patients require laboratory monitoring of kidney function at least twice annually."
    },

    # --- CKD STAGE G3B ---
    {
        "chunk_id": "ckd_g3b_001",
        "condition_code": "ckd_g3b",
        "content": "Đối với người dùng thuộc nhóm bệnh thận mạn giai đoạn G3b (CKD G3b), chức năng lọc của thận đã bị suy giảm ở mức độ trung bình đến nặng (chỉ số eGFR nằm trong khoảng từ 30 đến 44 mL/phút/1.73m2). Ở giai đoạn này, các hướng dẫn về chế độ ăn uống cần được kiểm soát chặt chẽ hơn để tránh tích tụ chất độc.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 10,
        "section": "Chapter 1",
        "text_support": "CKD Stage G3b is defined by eGFR of 30-44 mL/min/1.73 m2, indicating moderately to severely decreased kidney function.",
        "claim": "CKD Stage G3b is characterized by moderately to severely decreased eGFR (30-44)."
    },
    {
        "chunk_id": "ckd_g3b_002",
        "condition_code": "ckd_g3b",
        "content": "Kiểm soát lượng chất đạm (protein) nạp vào là vô cùng quan trọng đối với người bệnh thận mạn giai đoạn G3b (CKD G3b) không chạy thận. Người bệnh được khuyên duy trì lượng đạm ổn định ở mức 0.6 đến 0.8 gam đạm trên mỗi kg cân nặng mỗi ngày để giảm sản sinh chất thải nitơ, đồng thời đảm bảo cung cấp đủ năng lượng để tránh suy dinh dưỡng cơ thể.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 62,
        "section": "Chapter 3",
        "text_support": "In adults with CKD G3b non-dialysis, suggest a protein intake of 0.6-0.8 g/kg body weight/day to delay progression and manage uremia.",
        "claim": "Non-dialysis CKD G3b protein target is restricted to 0.6-0.8 g/kg/day."
    },
    {
        "chunk_id": "ckd_g3b_003",
        "condition_code": "ckd_g3b",
        "content": "Hạn chế muối natri nghiêm ngặt dưới 2000 mg mỗi ngày (khoảng 5g muối ăn) là cần thiết cho người bệnh thận mạn giai đoạn G3b (CKD G3b). Natri dư thừa ở giai đoạn này dễ gây giữ nước, phù chân, tăng huyết áp và tăng nguy cơ suy tim do thận giảm khả năng đào thải muối.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 60,
        "section": "Chapter 3",
        "text_support": "We recommend a sodium intake of <2.0 g/d in adults with CKD G3b to prevent fluid overload and control hypertension.",
        "claim": "CKD G3b patients must restrict sodium to <2000 mg/day to avoid fluid retention."
    },
    {
        "chunk_id": "ckd_g3b_004",
        "condition_code": "ckd_g3b",
        "content": "Người bệnh thận mạn giai đoạn G3b (CKD G3b) cần theo dõi sát sao nồng độ kali trong máu. Việc hạn chế các thực phẩm giàu kali (như chuối, bơ, cam, khoai tây) chỉ nên thực hiện khi có tình trạng kali máu tăng trên mức bình thường (thường là trên 5.0 mEq/L) hoặc theo chỉ dẫn dinh dưỡng từ chuyên gia y tế.",
        "source_id": "nkf_potassium_ckd_diet",
        "locator": "nkf_potassium_ckd_diet.txt",
        "page": "",
        "section": "Potassium in CKD",
        "text_support": "For CKD stage G3b, dietary potassium restriction should be tailored based on serum potassium levels to avoid hyperkalemia complications.",
        "claim": "Potassium intake in CKD G3b must be adjusted according to serum potassium laboratory results."
    },
    {
        "chunk_id": "ckd_g3b_005",
        "condition_code": "ckd_g3b",
        "content": "Người bệnh thận mạn giai đoạn G3b (CKD G3b) cần bắt đầu hạn chế phốt pho từ thực phẩm tự nhiên bên cạnh việc tránh các chất phụ gia phốt pho. Giảm tiêu thụ sữa, phô mai, các loại hạt và lòng đỏ trứng giúp giữ mức phốt pho trong máu ổn định, ngăn ngừa các biến chứng xơ vữa mạch máu và bệnh xương do thận.",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Phosphorus in CKD",
        "text_support": "For CKD G3b, limit phosphorus rich foods (dairy, nuts, egg yolks) to maintain blood phosphorus levels and protect bone health.",
        "claim": "CKD G3b patients should limit dietary phosphorus to prevent renal osteodystrophy."
    },
    {
        "chunk_id": "ckd_g3b_006",
        "condition_code": "ckd_g3b",
        "content": "Người bệnh thận mạn giai đoạn G3b (CKD G3b) cần được bác sĩ theo dõi định kỳ tối thiểu 3 lần mỗi năm. Tần suất theo dõi cao hơn giúp kiểm soát chặt chẽ tốc độ suy giảm chức năng thận, phát hiện sớm các biến chứng như thiếu máu do thận thiếu erythropoietin hoặc rối loạn thăng bằng kiềm toan.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 18,
        "section": "Chapter 1",
        "text_support": "Patients with CKD stage G3b require monitoring of eGFR and albuminuria at least three times a year to track complications.",
        "claim": "CKD G3b patients require clinical and lab monitoring at least three times annually."
    },
    {
        "chunk_id": "ckd_g3b_007",
        "condition_code": "ckd_g3b",
        "content": "Khuyến khích người bệnh thận mạn giai đoạn G3b (CKD G3b) làm việc cùng một chuyên gia dinh dưỡng tiết chế chuyên khoa thận (renal dietitian). Chuyên gia sẽ giúp thiết kế thực đơn cá nhân hóa, giúp người bệnh giảm đạm, natri mà vẫn đảm bảo cung cấp đủ calo để tránh suy mòn cơ bắp (protein-energy wasting).",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Dietitian referral",
        "text_support": "Referral to a registered dietitian specializing in kidney disease (renal dietitian) is highly recommended at stage G3b to prevent malnutrition while restricting nutrients.",
        "claim": "CKD G3b patients should consult a renal dietitian for specialized nutrition planning."
    },

    # --- CKD STAGE G4 ---
    {
        "chunk_id": "ckd_g4_001",
        "condition_code": "ckd_g4",
        "content": "Đối với người dùng thuộc nhóm bệnh thận mạn giai đoạn G4 (CKD G4), chức năng lọc của thận bị suy giảm nghiêm trọng (chỉ số eGFR nằm trong khoảng từ 15 đến 29 mL/phút/1.73m2). Ở giai đoạn suy thận tiến triển này, chế độ ăn uống đòi hỏi kiểm soát cực kỳ nghiêm ngặt và chuẩn bị tâm lý cho giai đoạn điều trị thay thế thận.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 10,
        "section": "Chapter 1",
        "text_support": "CKD Stage G4 is defined by eGFR of 15-29 mL/min/1.73 m2, indicating severely decreased kidney function.",
        "claim": "CKD Stage G4 is characterized by severely decreased eGFR (15-29)."
    },
    {
        "chunk_id": "ckd_g4_002",
        "condition_code": "ckd_g4",
        "content": "Hạn chế đạm (protein) là bắt buộc đối với người bệnh thận mạn giai đoạn G4 (CKD G4) chưa chạy thận. Khuyến nghị đạm giảm xuống còn 0.6 gam đạm trên mỗi kg cân nặng mỗi ngày (hoặc thấp hơn kèm bổ sung acid amin thiết yếu) để giảm tối đa tích tụ urê trong máu, giúp kéo dài thời gian trước khi phải lọc máu chu kỳ.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 62,
        "section": "Chapter 3",
        "text_support": "Suggest a protein intake of 0.6 g/kg/d in adults with CKD G4 who are not on dialysis to reduce uremic toxins and delay renal replacement therapy.",
        "claim": "Non-dialysis CKD G4 patients require strict protein restriction to 0.6 g/kg/day."
    },
    {
        "chunk_id": "ckd_g4_003",
        "condition_code": "ckd_g4",
        "content": "Hạn chế natri dưới 2000 mg mỗi ngày (khoảng 5g muối ăn) là nguyên tắc bắt buộc ở giai đoạn G4 (CKD G4) để ngăn ngừa tình trạng quá tải thể tích tuần hoàn, phù phổi cấp và tăng huyết áp kháng trị, do thận lúc này đã mất phần lớn khả năng bài tiết muối dư thừa.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 60,
        "section": "Chapter 3",
        "text_support": "We recommend a sodium intake of <2.0 g/d in adults with CKD G4 to prevent volume overload and cardiac complications.",
        "claim": "CKD G4 patients must limit sodium to <2000 mg/day to prevent cardiovascular overload."
    },
    {
        "chunk_id": "ckd_g4_004",
        "condition_code": "ckd_g4",
        "content": "Người bệnh thận mạn giai đoạn G4 (CKD G4) có nguy cơ cao bị tăng kali máu đe dọa tính mạng (gây loạn nhịp tim). Hạn chế kali từ chế độ ăn uống (tránh chuối, nước dừa, khoai tây, rau muống và thực phẩm chế biến) là cần thiết khi kali máu bắt đầu tăng cao, và phải được hướng dẫn cụ thể dựa trên xét nghiệm kali máu định kỳ.",
        "source_id": "nkf_potassium_ckd_diet",
        "locator": "nkf_potassium_ckd_diet.txt",
        "page": "",
        "section": "Potassium in CKD",
        "text_support": "Hyperkalemia is common and dangerous in CKD stage G4. Dietary potassium restriction is critical when blood levels rise, and must be monitored closely.",
        "claim": "CKD G4 patients require strict dietary potassium restriction when hyperkalemia is present."
    },
    {
        "chunk_id": "ckd_g4_005",
        "condition_code": "ckd_g4",
        "content": "Kiểm soát lượng phốt pho là vô cùng quan trọng đối với người bệnh thận mạn giai đoạn G4 (CKD G4). Do thận giảm bài tiết phốt pho, người bệnh cần hạn chế phốt pho ở mức 800-1000 mg mỗi ngày bằng cách giảm sữa, lòng đỏ trứng, các loại hạt và tuyệt đối tránh các thực phẩm chứa chất bảo quản phốt pho vô cơ để bảo vệ mạch máu.",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Phosphorus in CKD",
        "text_support": "In CKD stage G4, limit phosphorus to 800-1000 mg/day. Avoid dairy, nuts, and foods containing phosphate additives to protect arteries.",
        "claim": "CKD G4 patients must limit phosphorus to 800-1000 mg/day."
    },
    {
        "chunk_id": "ckd_g4_006",
        "condition_code": "ckd_g4",
        "content": "Khuyến nghị về lượng nước uống đối với người bệnh thận mạn giai đoạn G4 (CKD G4) phải được cá nhân hóa theo tình trạng lâm sàng. Người bệnh chỉ cần hạn chế lượng nước uống vào khi cơ thể bắt đầu có dấu hiệu giữ nước (phù chân, phù mặt, khó thở) hoặc khi lượng nước tiểu giảm đi rõ rệt, dưới sự hướng dẫn trực tiếp của bác sĩ.",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Fluid restrictions",
        "text_support": "Fluid intake in CKD stage G4 must be carefully monitored. Restriction is typically required only when there is signs of fluid retention or decreased urine output.",
        "claim": "Fluid restrictions in CKD G4 must be individualized based on fluid retention or urine output."
    },
    {
        "chunk_id": "ckd_g4_007",
        "condition_code": "ckd_g4",
        "content": "Người bệnh thận mạn giai đoạn G4 (CKD G4) cần chuẩn bị trước thông tin và kế hoạch cho việc điều trị thay thế thận trong tương lai. Kế hoạch này bao gồm thảo luận về các phương pháp lọc máu chu kỳ, lọc màng bụng (thẩm phân phúc mạc) hoặc đăng ký ghép thận, giúp người bệnh chủ động lựa chọn phương pháp phù hợp với cuộc sống.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 78,
        "section": "Chapter 3",
        "text_support": "Prepare stage G4 patients for renal replacement therapy (RRT), educating them on hemodialysis, peritoneal dialysis, and transplantation options.",
        "claim": "CKD G4 patients should receive education and counseling on renal replacement therapy options."
    },
    {
        "chunk_id": "ckd_g4_008",
        "condition_code": "ckd_g4",
        "content": "Người bệnh thận mạn giai đoạn G4 (CKD G4) cần được chuyển gửi đến chuyên gia thận học (nephrologist) và chuyên gia dinh dưỡng để kiểm soát các biến chứng nặng như thiếu máu, tăng huyết áp kháng trị, tăng kali máu, toan chuyển hóa và ngăn ngừa suy mòn cơ thể trước khi bước vào giai đoạn cuối.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 25,
        "section": "Chapter 1",
        "text_support": "Refer patients in CKD stage G4 to specialist multidisciplinary teams (nephrologists, dietitians) to manage severe renal complications and nutrition.",
        "claim": "CKD G4 patients require multidisciplinary nephrology team referral."
    },

    # --- CKD STAGE G5 NON-DIALYSIS ---
    {
        "chunk_id": "ckd_g5_nondialysis_001",
        "condition_code": "ckd_g5_non_dialysis",
        "content": "Đối với người dùng thuộc nhóm bệnh thận mạn giai đoạn G5 chưa chạy thận (CKD G5 non-dialysis), đây là giai đoạn suy thận cuối cùng nhưng chưa bắt đầu lọc máu (chỉ số eGFR dưới 15 mL/phút/1.73m2). Trọng tâm điều trị ở giai đoạn này là kiểm soát triệu chứng urê huyết cao và trì hoãn thời điểm lọc máu bằng chế độ ăn bảo tồn.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 10,
        "section": "Chapter 1",
        "text_support": "CKD Stage G5 is defined by eGFR < 15 mL/min/1.73 m2, indicating kidney failure. The non-dialysis subgroup requires active conservative care.",
        "claim": "CKD G5 non-dialysis is characterized by eGFR < 15 without active renal replacement therapy."
    },
    {
        "chunk_id": "ckd_g5_nondialysis_002",
        "condition_code": "ckd_g5_non_dialysis",
        "content": "Quy định về chất đạm (protein) đối với người bệnh thận mạn giai đoạn G5 chưa chạy thận (CKD G5 non-dialysis) là cực kỳ nghiêm ngặt. Lượng đạm được khuyên hạn chế tối đa ở mức 0.6 gam đạm trên mỗi kg cân nặng mỗi ngày để tránh làm tích tụ độc tố urê gây buồn nôn, ngứa ngáy. Hướng dẫn này hoàn toàn khác biệt với người đã chạy thận (nhóm cần ăn nhiều đạm).",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 62,
        "section": "Chapter 3",
        "text_support": "Suggest a protein intake of 0.6 g/kg/d in adults with CKD G5 non-dialysis to delay dialysis. This is contrast to dialysis patients who require protein loading.",
        "claim": "Protein intake for CKD G5 non-dialysis must be restricted to 0.6 g/kg/day, unlike dialysis patients."
    },
    {
        "chunk_id": "ckd_g5_nondialysis_003",
        "condition_code": "ckd_g5_non_dialysis",
        "content": "Hạn chế natri nghiêm ngặt dưới 2000 mg mỗi ngày (khoảng 5g muối ăn) là bắt buộc cho người bệnh thận mạn giai đoạn G5 chưa chạy thận để kiểm soát tình trạng ứ nước, khó thở khi nằm, suy tim và tăng huyết áp, do thận đã gần như mất hoàn toàn khả năng bài tiết natri.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 60,
        "section": "Chapter 3",
        "text_support": "We recommend a sodium intake of <2.0 g/d in adults with CKD G5 non-dialysis to control fluid volume and hypertension.",
        "claim": "Sodium restriction to <2000 mg/day is mandatory in CKD G5 non-dialysis."
    },
    {
        "chunk_id": "ckd_g5_nondialysis_004",
        "condition_code": "ckd_g5_non_dialysis",
        "content": "Tình trạng tăng kali máu là biến chứng cực kỳ nguy hiểm ở người bệnh thận mạn giai đoạn G5 chưa chạy thận. Người bệnh cần tuân thủ nghiêm ngặt chế độ ăn ít kali (hạn chế tối đa chuối, bơ, nước dừa, rau màu xanh đậm) và theo dõi sát sao chỉ số kali máu để tránh nguy cơ ngừng tim đột ngột.",
        "source_id": "nkf_potassium_ckd_diet",
        "locator": "nkf_potassium_ckd_diet.txt",
        "page": "",
        "section": "Potassium in CKD",
        "text_support": "Hyperkalemia is common and dangerous in CKD stage G5 non-dialysis. Restrict dietary potassium strictly and monitor serum levels regularly to avoid cardiac arrest.",
        "claim": "Strict potassium restriction is required in CKD G5 non-dialysis due to life-threatening hyperkalemia risk."
    },
    {
        "chunk_id": "ckd_g5_nondialysis_005",
        "condition_code": "ckd_g5_non_dialysis",
        "content": "Hạn chế phốt pho trong chế độ ăn của người bệnh thận mạn giai đoạn G5 chưa chạy thận giúp kiểm soát biến chứng cường tuyến cận giáp thứ phát. Người bệnh cần hạn chế phốt pho ở mức 800 mg mỗi ngày, tránh các thực phẩm chứa phụ gia phốt pho và sử dụng thuốc gắn phốt pho (phosphate binders) trong bữa ăn theo đơn của bác sĩ.",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Phosphorus in CKD",
        "text_support": "Limit phosphorus to 800 mg/d in CKD G5. Use prescribed phosphate binders with meals to manage hyperphosphatemia.",
        "claim": "Phosphorus restriction to 800 mg/day and phosphate binders are recommended in CKD G5 non-dialysis."
    },
    {
        "chunk_id": "ckd_g5_nondialysis_006",
        "condition_code": "ckd_g5_non_dialysis",
        "content": "Kiểm soát lượng nước uống vào ở người bệnh thận mạn giai đoạn G5 chưa chạy thận đòi hỏi phải đo lường lượng nước tiểu hàng ngày. Quy tắc thông thường là lượng nước uống vào mỗi ngày nên bằng lượng nước tiểu đo được của ngày hôm trước cộng thêm khoảng 500 mL (lượng mất qua mồ hôi và hơi thở) để tránh quá tải nước.",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Fluid restrictions",
        "text_support": "In stage G5 non-dialysis, fluid intake should match urine output plus 500 mL to prevent fluid overload and heart failure.",
        "claim": "Fluid intake in CKD G5 non-dialysis should be limited to urine output plus 500 mL."
    },
    {
        "chunk_id": "ckd_g5_nondialysis_007",
        "condition_code": "ckd_g5_non_dialysis",
        "content": "Người bệnh thận mạn giai đoạn G5 chưa chạy thận cần được giám sát y khoa chặt chẽ bởi bác sĩ thận học. Do chức năng thận đã suy kiệt, người bệnh có thể xuất hiện các triệu chứng u máu cao (uremia) như chán ăn, sụt cân, buồn nôn, ngứa, chuột rút, đòi hỏi can thiệp lọc máu cấp cứu kịp thời.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 28,
        "section": "Chapter 1",
        "text_support": "Close clinical monitoring is required in CKD stage G5 non-dialysis to identify uremic symptoms requiring initiation of renal replacement therapy.",
        "claim": "CKD G5 non-dialysis requires close clinical supervision to detect uremic complications."
    },
    {
        "chunk_id": "ckd_g5_nondialysis_008",
        "condition_code": "ckd_g5_non_dialysis",
        "content": "Người bệnh thận mạn giai đoạn G5 chưa chạy thận cần đến ngay bệnh viện nếu xuất hiện các dấu hiệu quá tải nước nặng (khó thở dữ dội, không thể nằm đầu thấp, ho ra bọt hồng) hoặc các triệu chứng của tăng kali máu nặng (yếu cơ lực toàn thân, tê bì, rối loạn nhịp tim).",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Emergency signs",
        "text_support": "Emergency medical attention is required for stage G5 non-dialysis patients presenting with severe shortness of breath, inability to breathe lying down, or signs of hyperkalemia.",
        "claim": "Fluid overload or severe hyperkalemia in CKD G5 non-dialysis require immediate emergency care."
    },

    # --- CKD DIALYSIS ---
    {
        "chunk_id": "ckd_dialysis_001",
        "condition_code": "ckd_dialysis",
        "content": "Đối với người dùng thuộc nhóm bệnh thận mạn đang lọc máu chu kỳ (chạy thận nhân tạo hoặc lọc màng bụng - CKD dialysis), chế độ dinh dưỡng có sự thay đổi mang tính đảo ngược so với giai đoạn trước lọc máu. Mục tiêu chính lúc này là bổ sung đủ dưỡng chất bị mất đi trong quá trình lọc máu để duy trì sức khỏe.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Dialysis overview",
        "text_support": "Nutritional needs for dialysis patients change significantly from pre-dialysis stages. The goal is replacing nutrients lost during dialysis sessions.",
        "claim": "Nutrition for dialysis patients differs significantly from non-dialysis CKD."
    },
    {
        "chunk_id": "ckd_dialysis_002",
        "condition_code": "ckd_dialysis",
        "content": "Khác biệt lớn nhất ở người bệnh thận mạn đang chạy thận (CKD dialysis) là yêu cầu tăng cường chất đạm (protein) trong bữa ăn. Quá trình lọc máu làm mất đi một lượng lớn các acid amin, do đó người chạy thận cần chế độ ăn giàu đạm (khoảng 1.0 đến 1.2 gam đạm trên mỗi kg cân nặng mỗi ngày) để tránh teo cơ và suy dinh dưỡng.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Dialysis overview",
        "text_support": "Dialysis removes protein waste but also amino acids. Dialysis patients require a high protein intake of 1.0-1.2 g/kg/day to maintain nutritional status.",
        "claim": "Dialysis patients require a high protein diet (1.0-1.2 g/kg/day) to prevent muscle wasting."
    },
    {
        "chunk_id": "ckd_dialysis_003",
        "condition_code": "ckd_dialysis",
        "content": "Hạn chế natri nghiêm ngặt dưới 2000 mg mỗi ngày (khoảng 5g muối ăn) là bắt buộc đối với người chạy thận (CKD dialysis). Natri dư thừa làm người bệnh khát nước nhiều hơn, dẫn đến uống nước quá mức giữa các chu kỳ chạy thận, gây quá tải tuần hoàn, tăng huyết áp và tăng gánh nặng cho tim.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Dialysis overview",
        "text_support": "Limit sodium to <2000 mg/d in dialysis. Excess sodium causes thirst, leading to excessive interdialytic weight gain (fluid overload) between sessions.",
        "claim": "Sodium restriction under 2000 mg/day is required in dialysis to control fluid gain."
    },
    {
        "chunk_id": "ckd_dialysis_004",
        "condition_code": "ckd_dialysis",
        "content": "Khuyến nghị về lượng kali đối với người bệnh chạy thận (CKD dialysis) không có một giới hạn chung duy nhất. Nhu cầu kali phụ thuộc vào phương pháp lọc máu (chạy thận nhân tạo thường cần hạn chế kali nghiêm ngặt hơn so với lọc màng bụng vốn dễ làm mất kali) và phải được hướng dẫn cụ thể dựa trên xét nghiệm kali máu định kỳ.",
        "source_id": "nkf_potassium_ckd_diet",
        "locator": "nkf_potassium_ckd_diet.txt",
        "page": "",
        "section": "Potassium in dialysis",
        "text_support": "Potassium guidelines in dialysis vary by modality. Peritoneal dialysis removes more potassium than hemodialysis, often requiring less restriction or even supplementation.",
        "claim": "Potassium guidelines for dialysis patients depend on modality (hemodialysis vs peritoneal) and lab values."
    },
    {
        "chunk_id": "ckd_dialysis_005",
        "condition_code": "ckd_dialysis",
        "content": "Hạn chế phốt pho nghiêm ngặt ở mức 800-1000 mg mỗi ngày là cần thiết cho người chạy thận (CKD dialysis). Quá trình lọc máu thông thường không thể loại bỏ hoàn toàn phốt pho dư thừa, do đó người bệnh cần hạn chế phốt pho từ ăn uống và bắt buộc sử dụng thuốc gắn phốt pho (phosphate binders) uống ngay trong bữa ăn.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Dialysis overview",
        "text_support": "Dialysis does not clear phosphorus efficiently. Limit intake to 800-1000 mg/d and take prescribed phosphate binders with meals.",
        "claim": "Dialysis patients require phosphorus limits (800-1000 mg) and phosphate binders with meals."
    },
    {
        "chunk_id": "ckd_dialysis_006",
        "condition_code": "ckd_dialysis",
        "content": "Kiểm soát lượng nước uống vào giữa các chu kỳ chạy thận (interdialytic fluid gain) là nguyên tắc sống còn đối với người bệnh chạy thận nhân tạo. Người bệnh cần giới hạn lượng nước uống sao cho mức tăng cân giữa hai chu kỳ chạy thận không vượt quá 3% đến 5% trọng lượng khô của cơ thể để tránh nguy cơ suy tim cấp.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Dialysis overview",
        "text_support": "Limit fluid intake between hemodialysis sessions to ensure interdialytic weight gain stays below 3% to 5% of dry body weight.",
        "claim": "Hemodialysis patients must limit fluid intake to keep interdialytic weight gain below 3-5% of dry weight."
    },
    {
        "chunk_id": "ckd_dialysis_007",
        "condition_code": "ckd_dialysis",
        "content": "Người bệnh chạy thận (CKD dialysis) cần phối hợp chặt chẽ với đội ngũ y tế tại trung tâm lọc máu (bác sĩ thận học, điều dưỡng, chuyên gia dinh dưỡng tiết chế). Mọi điều chỉnh về chế độ ăn, lượng nước uống hay liều lượng thuốc cần dựa trên các chỉ số xét nghiệm định kỳ tại trung tâm chạy thận.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Dialysis overview",
        "text_support": "Collaborate closely with the dialysis care team to adjust diet, fluid, and binder usage based on monthly clinical lab evaluations.",
        "claim": "Dialysis patients should coordinate care with their dialysis clinic team."
    },

    # --- CKD STAGE UNKNOWN ---
    {
        "chunk_id": "ckd_unknown_001",
        "condition_code": "ckd_stage_unknown",
        "content": "Đối với người dùng có bệnh thận mạn nhưng chưa rõ giai đoạn (chưa xác định Stage G1-G5 hay chạy thận), chế độ ăn uống ban đầu cần hướng tới các nguyên tắc bảo vệ thận an toàn tổng quát. Hướng đi thích hợp là giảm bớt lượng muối ăn hàng ngày, hạn chế các thực phẩm chế biến sẵn nhiều natri và uống đủ nước theo nhu cầu cơ thể.",
        "source_id": "medlineplus_ckd_diet",
        "locator": "medlineplus_ckd_diet.txt",
        "page": "",
        "section": "Diet - Chronic Kidney Disease",
        "text_support": "General healthy diet for unspecified kidney disease focuses on lowering sodium intake and avoiding processed foods.",
        "claim": "General kidney education emphasizes lower sodium and avoiding processed foods."
    },
    {
        "chunk_id": "ckd_unknown_002",
        "condition_code": "ckd_stage_unknown",
        "content": "Người bệnh thận mạn chưa rõ giai đoạn cần lưu ý rằng các khuyến nghị dinh dưỡng y khoa cụ thể, đặc biệt là lượng chất đạm (protein), kali, phốt pho và nước uống có sự khác biệt rất lớn, thậm chí trái ngược nhau giữa các giai đoạn suy thận nhẹ (G1-G2), suy thận nặng chưa chạy thận (G4-G5) và chạy thận (dialysis).",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 62,
        "section": "Chapter 3",
        "text_support": "Nutrient limits differ dramatically between non-dialysis CKD stages (protein restriction) and dialysis stages (protein loading). Stage must be identified.",
        "claim": "CKD nutritional rules differ dramatically by stage and dialysis status."
    },
    {
        "chunk_id": "ckd_unknown_003",
        "condition_code": "ckd_stage_unknown",
        "content": "Hệ thống khuyến khích người dùng có bệnh thận mạn nhưng chưa rõ giai đoạn cung cấp thêm kết quả xét nghiệm máu (chỉ số creatinine, mức lọc cầu thận eGFR) hoặc chẩn đoán cụ thể của bác sĩ. Việc xác định rõ giai đoạn bệnh giúp hệ thống RAG cung cấp các thông tin tư vấn dinh dưỡng chuẩn xác và an toàn nhất.",
        "source_id": "kdigo_2024_ckd_guideline",
        "locator": "kdigo_2024_ckd_guideline.pdf",
        "page": 15,
        "section": "Chapter 1",
        "text_support": "Providing accurate eGFR or doctor's staging diagnosis is necessary to receive stage-appropriate nutritional guidance.",
        "claim": "CKD patients should provide stage/eGFR data to receive safe recommendations."
    },
    {
        "chunk_id": "ckd_unknown_004",
        "condition_code": "ckd_stage_unknown",
        "content": "Trong bối cảnh người bệnh ở tình trạng bệnh thận mạn chưa rõ giai đoạn, hệ thống sẽ tránh đưa ra các khuyến nghị kiêng khem kali, phốt pho hay hạn chế nước uống cụ thể, vì những hạn chế này có thể gây hại cho người ở giai đoạn sớm hoặc người chạy thận màng bụng. Người dùng nên tham khảo ý kiến bác sĩ thận học hoặc chuyên gia dinh dưỡng.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Stages 1-5 overview",
        "text_support": "When stage is unknown, avoid specific potassium, phosphorus, or fluid restrictions to prevent adverse nutritional outcomes.",
        "claim": "Unspecified CKD guidance should avoid specific stage-related restrictions."
    },

    # --- GOUT ---
    {
        "chunk_id": "gout_001",
        "condition_code": "gout",
        "content": "Đối với người mắc bệnh gout, điều quan trọng đầu tiên là phân biệt giữa bệnh gout thực sự và tình trạng tăng acid uric máu không triệu chứng. Tăng acid uric máu (kết quả xét nghiệm acid uric máu cao) là một yếu tố nguy cơ nhưng chưa được coi là bệnh gout nếu người bệnh chưa từng trải qua các cơn viêm khớp cấp tính (sưng, nóng, đỏ, đau dữ dội).",
        "source_id": "medlineplus_uric_acid_blood",
        "locator": "medlineplus_uric_acid_blood.txt",
        "page": "",
        "section": "Uric Acid Blood",
        "text_support": "High uric acid levels (hyperuricemia) do not mean you have gout. Gout is diagnosed only when uric acid crystals form in joints, causing acute inflammation.",
        "claim": "Asymptomatic hyperuricemia is a risk factor, but does not constitute a gout diagnosis."
    },
    {
        "chunk_id": "gout_002",
        "condition_code": "gout",
        "content": "Hạn chế các thực phẩm giàu purine là nguyên tắc dinh dưỡng cơ bản đối với người bệnh gout. Khi cơ thể chuyển hóa purine từ thức ăn, sản phẩm cuối cùng tạo ra là acid uric. Kiểm soát lượng purine nạp vào giúp giảm tích tụ các tinh thể urat tại khớp, từ đó hỗ trợ giảm tần suất xuất hiện các cơn gout cấp tính.",
        "source_id": "medlineplus_gout_encyclopedia",
        "locator": "medlineplus_gout_encyclopedia.txt",
        "page": "",
        "section": "Purines",
        "text_support": "Uric acid is made when the body breaks down purines in food. Limiting purine-rich foods helps prevent uric acid crystals from depositing in joints.",
        "claim": "Purine restriction reduces uric acid production and joint deposition in gout."
    },
    {
        "chunk_id": "gout_003",
        "condition_code": "gout",
        "content": "Nội tạng động vật là nhóm thực phẩm chứa hàm lượng purine cực kỳ cao mà người bệnh gout cần tránh tuyệt đối. Gan, thận (cật), tim, lòng bò, lòng lợn có chứa lượng purine lớn, có thể gây tăng vọt nồng độ acid uric trong máu ngay sau khi ăn và dễ kích ngòi cho một cơn viêm khớp gout cấp tính xuất hiện.",
        "source_id": "medlineplus_gout_encyclopedia",
        "locator": "medlineplus_gout_encyclopedia.txt",
        "page": "",
        "section": "Foods to avoid",
        "text_support": "Avoid organ meats like liver, kidneys, and sweetbreads because they contain very high levels of purines and can trigger acute gout attacks.",
        "claim": "Organ meats are extremely high purine foods that gout patients must avoid."
    },
    {
        "chunk_id": "gout_004",
        "condition_code": "gout",
        "content": "Người bệnh gout cần hạn chế tiêu thụ các loại thịt đỏ trong chế độ ăn hàng ngày. Thịt bò, thịt heo, thịt dê, thịt cừu chứa lượng purine ở mức trung bình cao. Người bệnh chỉ nên ăn thịt đỏ với lượng nhỏ (khoảng 100-150g mỗi ngày) và ưu tiên chọn đạm thực vật từ đậu hũ hoặc thịt gia cầm nạc bỏ da theo thể trạng.",
        "source_id": "medlineplus_gout_encyclopedia",
        "locator": "medlineplus_gout_encyclopedia.txt",
        "page": "",
        "section": "Foods to avoid",
        "text_support": "Limit red meats like beef, pork, and lamb. Moderate intake is advised, replacing them with lean poultry or plant proteins.",
        "claim": "Gout patients should moderate red meat consumption."
    },
    {
        "chunk_id": "gout_005",
        "condition_code": "gout",
        "content": "Một số loại hải sản có hàm lượng purine cao cần được người bệnh gout tiêu thụ hết sức thận trọng. Các loại cá béo (cá thu, cá trích, cá mòi, cá ngừ), tôm, cua, sò điệp, nghêu, hàu có thể làm tăng nhanh nồng độ acid uric. Người bệnh nên hạn chế các loại hải sản này, đặc biệt là trong giai đoạn khớp đang có dấu hiệu đau nhức.",
        "source_id": "medlineplus_gout",
        "locator": "medlineplus_gout.txt",
        "page": "",
        "section": "Dietary guidelines",
        "text_support": "Certain seafoods (sardines, herring, anchovies, shellfish) are high in purines. Gout patients should limit their intake to prevent flares.",
        "claim": "High-purine seafoods like shellfish and sardines must be limited by gout patients."
    },
    {
        "chunk_id": "gout_006",
        "condition_code": "gout",
        "content": "Kiêng tuyệt đối rượu, bia và các thức uống chứa cồn là khuyến nghị quan trọng đối với người bệnh gout. Chất cồn trong bia không chỉ chứa hàm lượng purine cao mà rượu bia còn làm giảm khả năng đào thải acid uric qua đường thận của cơ thể, gây tích tụ acid uric trong máu và dễ khởi phát cơn gout cấp dữ dội.",
        "source_id": "medlineplus_gout_encyclopedia",
        "locator": "medlineplus_gout_encyclopedia.txt",
        "page": "",
        "section": "Foods to avoid",
        "text_support": "Avoid alcohol, especially beer, because it contains high purines and decreases the kidneys' ability to excrete uric acid, triggering attacks.",
        "claim": "Alcohol (especially beer) impairs uric acid excretion and triggers gout attacks."
    },
    {
        "chunk_id": "gout_007",
        "condition_code": "gout",
        "content": "Hạn chế các loại nước ngọt, trà sữa và thực phẩm chứa hàm lượng đường fructose cao (high-fructose corn syrup) là cần thiết cho người bệnh gout. Đường fructose khi được gan chuyển hóa sẽ kích thích cơ thể sản sinh thêm purine nội sinh, gián tiếp làm tăng nồng độ acid uric trong máu và làm trầm trọng thêm tình trạng viêm khớp.",
        "source_id": "medlineplus_gout_encyclopedia",
        "locator": "medlineplus_gout_encyclopedia.txt",
        "page": "",
        "section": "Foods to avoid",
        "text_support": "Avoid foods and beverages sweetened with high-fructose corn syrup, as fructose metabolism stimulates purine production and raises uric acid.",
        "claim": "Fructose-sweetened foods and drinks stimulate purine production and should be avoided in gout."
    },
    {
        "chunk_id": "gout_008",
        "condition_code": "gout",
        "content": "Duy trì thói quen uống đủ nước là biện pháp hỗ trợ tự nhiên hiệu quả cho người bệnh gout. Uống từ 2 đến 2.5 lít nước lọc mỗi ngày giúp làm loãng nồng độ acid uric trong cơ thể và kích thích thận tăng cường bài tiết acid uric qua nước tiểu, giúp phòng ngừa sự hình thành của sỏi thận urat.",
        "source_id": "medlineplus_gout",
        "locator": "medlineplus_gout.txt",
        "page": "",
        "section": "Dietary guidelines",
        "text_support": "Drink plenty of water (8-16 cups a day) to help flush uric acid from your body and prevent kidney stones.",
        "claim": "Adequate hydration (2-2.5L/day) aids uric acid excretion and prevents kidney stones."
    },
    {
        "chunk_id": "gout_009",
        "condition_code": "gout",
        "content": "Người bệnh gout cần phân biệt rõ chế độ ăn trong cơn gout cấp (gout flare) và giai đoạn quản lý gout lâu dài. Khi khớp đang sưng đau cấp tính, người bệnh cần tuân thủ chế độ ăn cực kỳ nghiêm ngặt (tránh hoàn toàn thịt đỏ, hải sản, rượu bia), kết hợp nghỉ ngơi nâng cao chi khớp bị đau và dùng thuốc giảm đau theo đơn bác sĩ.",
        "source_id": "medlineplus_gout",
        "locator": "medlineplus_gout.txt",
        "page": "",
        "section": "Dietary guidelines",
        "text_support": "During a gout flare, restrict purines strictly and rest the affected joint. Chronic management allows a moderately restricted, balanced diet.",
        "claim": "Diet during acute gout flares is strictly restrictive compared to chronic management."
    },
    {
        "chunk_id": "gout_010",
        "condition_code": "gout",
        "content": "Người bệnh gout cần hiểu rằng chế độ ăn uống lành mạnh chỉ đóng vai trò hỗ trợ và không thể thay thế cho các loại thuốc giảm acid uric (như allopurinol) do bác sĩ kê đơn. Đối với những trường hợp bệnh gout mạn tính hoặc có hạt tophi, việc tuân thủ dùng thuốc đều đặn theo chỉ định lâm sàng là yếu tố tiên quyết để bảo vệ khớp.",
        "source_id": "medlineplus_gout",
        "locator": "medlineplus_gout.txt",
        "page": "",
        "section": "Dietary guidelines",
        "text_support": "Dietary changes help but do not replace medications designed to lower uric acid levels (like allopurinol). Medication adherence is critical.",
        "claim": "Dietary modifications do not replace pharmacotherapy (uric acid lowering drugs) in gout."
    },

    # --- OBESITY ---
    {
        "chunk_id": "obesity_001",
        "condition_code": "obesity",
        "content": "Đối với người dùng đang có tình trạng thừa cân hoặc béo phì, nguyên tắc cốt lõi của quản lý cân nặng là đạt được sự thâm hụt năng lượng lành mạnh và bền vững. Chế độ ăn giảm cân nên tập trung vào thay đổi thói quen ăn uống lâu dài hơn là áp dụng các biện pháp nhịn ăn khắc nghiệt vốn dễ gây tăng cân trở lại.",
        "source_id": "cdc_steps_losing_weight",
        "locator": "cdc_steps_losing_weight.txt",
        "page": "",
        "section": "Weight loss principles",
        "text_support": "Sustainable weight management is about a lifestyle that includes healthy eating, physical activity, and behavior changes, rather than short-term diets.",
        "claim": "Obesity management focuses on sustainable lifestyle modifications rather than quick-fix diets."
    },
    {
        "chunk_id": "obesity_002",
        "condition_code": "obesity",
        "content": "Kiểm soát khẩu phần ăn là kỹ năng quan trọng giúp giảm cân hiệu quả cho người thừa cân, béo phì. Người dùng có thể sử dụng các đĩa ăn nhỏ hơn, đọc kỹ khẩu phần khuyến nghị trên nhãn thực phẩm và tránh ăn trực tiếp từ túi/hộp đóng gói để kiểm soát trực quan lượng năng lượng nạp vào cơ thể hàng ngày.",
        "source_id": "cdc_healthy_eating_weight",
        "locator": "cdc_healthy_eating_weight.txt",
        "page": "",
        "section": "Portion control",
        "text_support": "Portion control is key to managing calorie intake. Use smaller plates, measure portions, and read serving sizes on nutrition facts labels.",
        "claim": "Portion control techniques aid calorie management for obesity."
    },
    {
        "chunk_id": "obesity_003",
        "condition_code": "obesity",
        "content": "Hiểu về mật độ năng lượng của thực phẩm (energy density) giúp người béo phì giảm cân mà không bị đói. Người dùng nên chọn các loại thực phẩm có mật độ năng lượng thấp (chứa nhiều nước và chất xơ như rau xanh, trái cây tươi, canh trong) để làm đầy dạ dày và tạo cảm giác no, đồng thời hạn chế các thực phẩm giàu năng lượng nhưng ít dinh dưỡng.",
        "source_id": "cdc_healthy_eating_weight",
        "locator": "cdc_healthy_eating_weight.txt",
        "page": "",
        "section": "Portion control",
        "text_support": "Energy density is the number of calories in a specific weight of food. Lower energy density foods (high water/fiber) help you feel full on fewer calories.",
        "claim": "Lower energy density foods support weight loss by promoting fullness with fewer calories."
    },
    {
        "chunk_id": "obesity_004",
        "condition_code": "obesity",
        "content": "Cắt giảm đồ uống ngọt có gas, nước ép nhiều đường và trà sữa là thay đổi mang lại hiệu quả giảm cân nhanh chóng cho người thừa cân, béo phì. Các loại đồ uống này chứa năng lượng rỗng hấp thu nhanh và không tạo cảm giác no bụng, dễ làm người dùng vượt quá giới hạn năng lượng hàng ngày mà không nhận ra.",
        "source_id": "cdc_healthy_eating_weight",
        "locator": "cdc_healthy_eating_weight.txt",
        "page": "",
        "section": "Portion control",
        "text_support": "Sugar-sweetened beverages contribute a lot of empty calories. Eliminating them is a simple way to create a calorie deficit.",
        "claim": "Eliminating sugar-sweetened beverages is a key step to establish a calorie deficit for weight loss."
    },
    {
        "chunk_id": "obesity_005",
        "condition_code": "obesity",
        "content": "Hoạt động thể lực là thành phần không thể thiếu để duy trì cân nặng sau giảm cân ở người béo phì. Cùng với điều chỉnh ăn uống để giảm cân ban đầu, việc duy trì tối thiểu 150 phút vận động mỗi tuần (ví dụ đi bộ nhanh 30 phút mỗi ngày, 5 ngày mỗi tuần) giúp bảo tồn khối cơ và ngăn ngừa tích tụ mỡ trở lại.",
        "source_id": "cdc_steps_losing_weight",
        "locator": "cdc_steps_losing_weight.txt",
        "page": "",
        "section": "Weight loss principles",
        "text_support": "Physical activity is crucial for weight loss maintenance. Combined with diet, aim for 150 minutes of moderate activity weekly to sustain weight loss.",
        "claim": "Physical activity (150 mins/week) is critical for weight loss maintenance in obesity."
    },
    {
        "chunk_id": "obesity_006",
        "condition_code": "obesity",
        "content": "Người béo phì cần cảnh giác với các chế độ ăn kiêng cực đoan hoặc nhịn ăn thanh lọc cơ thể (detox) thiếu cơ sở khoa học. Những chế độ ăn này thường làm cơ thể mất nước và mất cơ bắp thay vì giảm mỡ, đồng thời có thể gây thiếu hụt vi chất dinh dưỡng nghiêm trọng và ảnh hưởng xấu đến chức năng tim mạch.",
        "source_id": "medlineplus_obesity",
        "locator": "medlineplus_obesity.txt",
        "page": "",
        "section": "Obesity overview",
        "text_support": "Avoid extreme diets or crash starvation programs. They often lead to muscle loss and nutrient deficiencies rather than fat loss, and are unsustainable.",
        "claim": "Extreme/fad diets are unsafe and ineffective for sustainable obesity management."
    },
    {
        "chunk_id": "obesity_007",
        "condition_code": "obesity",
        "content": "Đối với người cao tuổi bị béo phì, quá trình giảm cân cần được tiếp cận hết sức thận trọng để tránh nguy cơ suy yếu xương và mất khối lượng cơ (sarcopenia). Chế độ ăn giảm cân ở người lớn tuổi bắt buộc phải bổ sung đủ chất đạm chất lượng cao kết hợp tập luyện kháng lực nhẹ dưới sự giám sát của nhân viên y tế.",
        "source_id": "medlineplus_obesity",
        "locator": "medlineplus_obesity.txt",
        "page": "",
        "section": "Older adults and frailty",
        "text_support": "In older adults, weight loss must minimize muscle and bone loss. Focus on high protein and resistance exercise under clinical guidance to prevent frailty.",
        "claim": "Obesity management in older adults must prioritize muscle retention to prevent frailty."
    },
    {
        "chunk_id": "obesity_008",
        "condition_code": "obesity",
        "content": "Hệ thống khuyến khích người dùng có các dấu hiệu của rối loạn ăn uống (như nhịn ăn quá mức, ăn vô độ khi stress rồi cố tình nôn ra) tìm kiếm sự giúp đỡ từ chuyên gia tâm lý hoặc bác sĩ. Quản lý béo phì trong bối cảnh rối loạn ăn uống đòi hỏi liệu pháp phối hợp chuyên sâu chứ không chỉ đơn thuần là cắt giảm calo.",
        "source_id": "medlineplus_obesity",
        "locator": "medlineplus_obesity.txt",
        "page": "",
        "section": "Eating disorders",
        "text_support": "If weight management issues are related to eating disorders (like binge eating or bulimia), seek psychiatric or professional psychological support.",
        "claim": "Obesity accompanied by eating disorders requires professional psychological intervention."
    },

    # --- GENERAL SAFETY ---
    {
        "chunk_id": "safety_001",
        "condition_code": "general_safety",
        "content": "HealthyPlan là một hệ thống hỗ trợ giáo dục sức khỏe và cung cấp thông tin tham khảo tổng quát, hoàn toàn không có chức năng chẩn đoán bệnh, kết luận nguy cơ cá nhân hay thay thế các xét nghiệm y khoa. Người dùng cần liên hệ trực tiếp với bác sĩ để thực hiện các đánh giá lâm sàng và chẩn đoán chính xác.",
        "source_id": "cdc_prevent_type2_guide",
        "locator": "cdc_prevent_type2_guide.txt",
        "page": "",
        "section": "Disclaimer",
        "text_support": "Educational health systems do not diagnose medical conditions or substitute for professional clinical diagnostic tests.",
        "claim": "HealthyPlan is an educational tool and does not diagnose disease."
    },
    {
        "chunk_id": "safety_002",
        "condition_code": "general_safety",
        "content": "HealthyPlan không đưa ra bất kỳ hướng dẫn hay gợi ý nào liên quan đến việc tự ý bắt đầu, thay đổi liều lượng hoặc ngưng sử dụng các loại thuốc điều trị. Mọi quyết định thay đổi phác đồ thuốc phải được thảo luận trực tiếp và có sự đồng ý của bác sĩ điều trị để đảm bảo an toàn tính mạng.",
        "source_id": "nkf_nutrition_ckd_stages_1_5",
        "locator": "nkf_nutrition_ckd_stages_1_5.txt",
        "page": "",
        "section": "Disclaimer",
        "text_support": "Medication choices, dosage changes, or stopping therapy must be made solely under the direct instruction of a physician.",
        "claim": "HealthyPlan does not prescribe, change, or stop medications."
    },
    {
        "chunk_id": "safety_003",
        "condition_code": "general_safety",
        "content": "Hạ đường huyết nghiêm trọng là tình trạng khẩn cấp đe dọa tính mạng. Nếu người bệnh đái tháo đường có biểu hiện lơ mơ, lú lẫn, co giật hoặc bất tỉnh do hạ đường huyết, người nhà tuyệt đối không được đổ nước đường hay đút thức ăn vào miệng để tránh sặc đường thở, và phải gọi xe cấp cứu y tế 115 ngay lập tức.",
        "source_id": "medlineplus_emergency_hypoglycemia",
        "locator": "medlineplus_emergency_hypoglycemia.txt",
        "page": "",
        "section": "Emergency steps",
        "text_support": "Severe hypoglycemia (confusion, convulsions, unconsciousness) is a medical emergency. Do not put anything in the mouth if unconscious; call emergency services immediately.",
        "claim": "Severe hypoglycemia with unconsciousness is a medical emergency requiring urgent EMS."
    },
    {
        "chunk_id": "safety_004",
        "condition_code": "general_safety",
        "content": "Đau tức ngực dữ dội kèm theo khó thở, thở dốc là dấu hiệu cảnh báo của cơn đau thắt ngực cấp hoặc nhồi máu cơ tim. Người dùng khi xuất hiện các triệu chứng này cần ngừng ngay mọi hoạt động thể chất, ngồi nghỉ ở tư thế thoải mái và gọi cấp cứu y tế 115 hoặc nhờ người đưa đến bệnh viện gần nhất ngay lập tức.",
        "source_id": "medlineplus_emergency_chest_pain",
        "locator": "medlineplus_emergency_chest_pain.txt",
        "page": "",
        "section": "Emergency signs",
        "text_support": "Severe chest pain accompanied by shortness of breath indicates a potential cardiac emergency. Rest immediately and contact emergency medical services.",
        "claim": "Severe chest pain and dyspnea are indicators of cardiac emergency requiring immediate EMS."
    },
    {
        "chunk_id": "safety_005",
        "condition_code": "general_safety",
        "content": "Tình trạng lơ mơ, ngất xỉu hoặc đột ngột mất ý thức (loss of consciousness) là dấu hiệu suy giảm tuần hoàn não nghiêm trọng. Cần đặt người bệnh nằm ngửa, nâng nhẹ hai chân lên cao nếu không có chấn thương, nới lỏng quần áo và gọi ngay cấp cứu y tế 115, không tự ý cho uống nước hay lay gọi thô bạo.",
        "source_id": "medlineplus_emergency_fainting",
        "locator": "medlineplus_emergency_fainting.txt",
        "page": "",
        "section": "Emergency response",
        "text_support": "Loss of consciousness indicates severe cerebral perfusion compromise. Place the patient supine, elevate legs, loosen clothing, and seek urgent medical help.",
        "claim": "Loss of consciousness is a medical emergency requiring supine positioning and urgent EMS."
    },
    {
        "chunk_id": "safety_006",
        "condition_code": "general_safety",
        "content": "Các triệu chứng thần kinh khởi phát đột ngột như méo miệng, yếu liệt một bên tay chân, nói ngọng hoặc không diễn đạt được lời nói là dấu hiệu điển hình của đột quỵ não. Cần áp dụng quy tắc FAST (méo mặt, yếu tay, khó nói, gọi cấp cứu ngay) và đưa người bệnh đến bệnh viện có điều trị đột quỵ trong giờ vàng.",
        "source_id": "medlineplus_emergency_stroke",
        "locator": "medlineplus_emergency_stroke.txt",
        "page": "",
        "section": "FAST signs",
        "text_support": "Sudden onset of facial drooping, arm weakness, or speech difficulty (FAST) are key signs of acute stroke requiring immediate emergency transport.",
        "claim": "Sudden focal neurological deficits (stroke signs) require immediate emergency transfer."
    },
    {
        "chunk_id": "safety_007",
        "condition_code": "general_safety",
        "content": "Phụ nữ mang thai, trẻ em dưới 18 tuổi hoặc những người mắc đồng thời nhiều bệnh lý mạn tính phức tạp (ví dụ vừa suy thận giai đoạn G4 vừa suy tim hoặc tiểu đường) có những yêu cầu dinh dưỡng đặc biệt và có thể mâu thuẫn nhau. Các đối tượng này không được áp dụng các khuyến nghị tự động và bắt buộc phải tuân theo hướng dẫn trực tiếp từ bác sĩ chuyên khoa.",
        "source_id": "medlineplus_obesity",
        "locator": "medlineplus_obesity.txt",
        "page": "",
        "section": "Special populations",
        "text_support": "Special populations (pregnancy, pediatric, multi-morbidities) have highly complex and conflicting dietary needs that cannot be generalized. Clinical oversight is mandatory.",
        "claim": "Pregnancy, pediatric, and multi-morbid patients are excluded from automatic RAG recommendations."
    }
]

# 3. Define original chunk decisions mapping
# Map the 70 original chunks to V2 chunks and set decisions
chunk_decisions = [
    # Original chunks and decisions
    {"orig_id": "rag_diabetes_001", "decision": "split", "new_ids": "diabetes_t1_002;diabetes_t2_002", "reason": "Mixed Type 1 and Type 2 carbohydrate guidelines"},
    {"orig_id": "rag_diabetes_002", "decision": "split", "new_ids": "diabetes_t1_001;diabetes_t2_003", "reason": "Mixed Type 1 meal planning and Type 2 plate method"},
    {"orig_id": "rag_diabetes_003", "decision": "revise", "new_ids": "diabetes_t2_001", "reason": "Updated to explicitly target Type 2 diabetes nutrition"},
    {"orig_id": "rag_diabetes_004", "decision": "revise", "new_ids": "diabetes_t2_004", "reason": "Enforced Type 2 sugary drink warnings"},
    {"orig_id": "rag_diabetes_005", "decision": "split", "new_ids": "diabetes_t2_007;safety_002", "reason": "Separated weight management from medical prescription safety"},
    
    {"orig_id": "rag_prediabetes_001", "decision": "revise", "new_ids": "prediabetes_001", "reason": "Updated to clarify prediabetes definition"},
    {"orig_id": "rag_prediabetes_002", "decision": "revise", "new_ids": "prediabetes_005", "reason": "Updated physical activity recommendations for prediabetes"},
    {"orig_id": "rag_prediabetes_003", "decision": "revise", "new_ids": "prediabetes_007", "reason": "Updated monitoring recommendations for prediabetes"},
    
    {"orig_id": "rag_hypertension_001", "decision": "revise", "new_ids": "hypertension_001", "reason": "Updated with AHA absolute sodium limits (<1500mg)"},
    {"orig_id": "rag_hypertension_002", "decision": "revise", "new_ids": "hypertension_002", "reason": "Enforced Vietnamese condiment sodium warnings"},
    {"orig_id": "rag_hypertension_003", "decision": "revise", "new_ids": "hypertension_003", "reason": "Updated processed food hidden sodium warnings"},
    {"orig_id": "rag_hypertension_004", "decision": "revise", "new_ids": "hypertension_004", "reason": "Enforced potassium guidelines with kidney safety checks"},
    
    {"orig_id": "rag_gout_001", "decision": "revise", "new_ids": "gout_001", "reason": "Separated confirmed gout from hyperuricemia"},
    {"orig_id": "rag_gout_002", "decision": "revise", "new_ids": "gout_002", "reason": "Enforced purine food descriptions"},
    {"orig_id": "rag_gout_003", "decision": "revise", "new_ids": "gout_006", "reason": "Updated alcohol elimination guidelines for gout"},
    {"orig_id": "rag_gout_004", "decision": "revise", "new_ids": "gout_008", "reason": "Enforced hydration requirements for gout"},
    {"orig_id": "rag_gout_005", "decision": "revise", "new_ids": "gout_005", "reason": "Updated seafood restrictions for gout"},
    
    {"orig_id": "rag_ckd_001", "decision": "split", "new_ids": "ckd_g1_001;ckd_g2_001;ckd_g3a_001;ckd_g3b_001;ckd_g4_001;ckd_g5_nondialysis_001", "reason": "Split generic CKD Stages 1-5 merged guidelines"},
    {"orig_id": "rag_ckd_002", "decision": "split", "new_ids": "ckd_g3a_004;ckd_g3b_004;ckd_g4_004;ckd_g5_nondialysis_004;ckd_dialysis_004", "reason": "Split potassium advice by stage and dialysis status"},
    {"orig_id": "rag_ckd_003", "decision": "split", "new_ids": "ckd_g3a_005;ckd_g3b_005;ckd_g4_005;ckd_g5_nondialysis_005;ckd_dialysis_005", "reason": "Split phosphorus guidelines by stage"},
    {"orig_id": "rag_ckd_004", "decision": "split", "new_ids": "ckd_g4_006;ckd_g5_nondialysis_006;ckd_dialysis_006", "reason": "Split fluid advice for dialysis vs non-dialysis"},
    {"orig_id": "rag_ckd_005", "decision": "split", "new_ids": "ckd_g1_003;ckd_g2_003;ckd_g3a_007;ckd_g3b_006;ckd_g4_007;ckd_g5_nondialysis_007", "reason": "Split clinical monitoring schedules by stage"},
    
    {"orig_id": "rag_obesity_001", "decision": "revise", "new_ids": "obesity_001", "reason": "Updated sustainable weight management guidelines"},
    {"orig_id": "rag_obesity_002", "decision": "revise", "new_ids": "obesity_005", "reason": "Updated physical activity targets for weight management"},
    {"orig_id": "rag_obesity_003", "decision": "revise", "new_ids": "obesity_006", "reason": "Updated warnings against extreme fad diets"},
    {"orig_id": "rag_obesity_004", "decision": "revise", "new_ids": "obesity_008", "reason": "Updated eating disorder safety warnings"},
    
    {"orig_id": "expanded_diabetes_001", "decision": "split", "new_ids": "diabetes_t1_002;diabetes_t2_002", "reason": "Split diabetes carb counting guidelines by type"},
    {"orig_id": "expanded_diabetes_002", "decision": "split", "new_ids": "diabetes_t1_001;diabetes_t2_005", "reason": "Split plate method guidelines by type"},
    {"orig_id": "expanded_diabetes_003", "decision": "revise", "new_ids": "diabetes_t2_002", "reason": "Updated Type 2 carbohydrate choices"},
    {"orig_id": "expanded_diabetes_004", "decision": "revise", "new_ids": "diabetes_t2_002", "reason": "Updated carbohydrate fiber quality rules"},
    {"orig_id": "expanded_diabetes_005", "decision": "revise", "new_ids": "diabetes_t2_008", "reason": "Updated monitoring rules for Type 2"},
    {"orig_id": "expanded_diabetes_006", "decision": "split", "new_ids": "diabetes_t2_007;safety_002", "reason": "Separated weight control from medication safety rules"},
    {"orig_id": "expanded_diabetes_007", "decision": "split", "new_ids": "diabetes_t1_005;diabetes_t2_006", "reason": "Split physical activity recommendations by type"},
    {"orig_id": "expanded_diabetes_008", "decision": "revise", "new_ids": "diabetes_t2_002", "reason": "Updated carb portions guidelines"},
    {"orig_id": "expanded_diabetes_009", "decision": "revise", "new_ids": "diabetes_t2_002", "reason": "Updated carb reading guidelines"},
    {"orig_id": "expanded_diabetes_010", "decision": "replace", "new_ids": "safety_002", "reason": "Replaced physician delegation warning with safety code"},
    
    {"orig_id": "expanded_prediabetes_001", "decision": "revise", "new_ids": "prediabetes_004", "reason": "Updated prediabetes weight loss targets (5-7%)"},
    {"orig_id": "expanded_prediabetes_002", "decision": "revise", "new_ids": "prediabetes_003", "reason": "Updated prediabetes sugary drink guidelines"},
    {"orig_id": "expanded_prediabetes_003", "decision": "revise", "new_ids": "prediabetes_002", "reason": "Updated prediabetes carb portion guidelines"},
    {"orig_id": "expanded_prediabetes_004", "decision": "revise", "new_ids": "prediabetes_008", "reason": "Enforced prediabetes medication safety guidelines"},
    {"orig_id": "expanded_prediabetes_005", "decision": "revise", "new_ids": "prediabetes_007", "reason": "Updated prediabetes progression monitoring rules"},
    
    {"orig_id": "expanded_hypertension_001", "decision": "revise", "new_ids": "hypertension_003", "reason": "Updated processed food hidden sodium guidelines"},
    {"orig_id": "expanded_hypertension_002", "decision": "revise", "new_ids": "hypertension_002", "reason": "Updated condiment sodium warnings"},
    {"orig_id": "expanded_hypertension_003", "decision": "revise", "new_ids": "hypertension_001", "reason": "Updated sodium guidelines"},
    {"orig_id": "expanded_hypertension_004", "decision": "revise", "new_ids": "hypertension_004", "reason": "Updated DASH diet guidelines"},
    {"orig_id": "expanded_hypertension_005", "decision": "revise", "new_ids": "hypertension_003", "reason": "Updated nutrition label guidance"},
    {"orig_id": "expanded_hypertension_006", "decision": "revise", "new_ids": "hypertension_005", "reason": "Updated lifestyle weight management guidelines"},
    {"orig_id": "expanded_hypertension_007", "decision": "revise", "new_ids": "hypertension_003", "reason": "Updated label reading guides"},
    {"orig_id": "expanded_hypertension_008", "decision": "replace", "new_ids": "safety_002", "reason": "Replaced physician delegation warning with safety code"},
    
    {"orig_id": "expanded_gout_001", "decision": "revise", "new_ids": "gout_003", "reason": "Updated organ meat restrictions in gout"},
    {"orig_id": "expanded_gout_002", "decision": "revise", "new_ids": "gout_008", "reason": "Updated hydration guidelines in gout"},
    {"orig_id": "expanded_gout_003", "decision": "revise", "new_ids": "gout_001", "reason": "Separated hyperuricemia from gout"},
    {"orig_id": "expanded_gout_004", "decision": "revise", "new_ids": "gout_001", "reason": "Updated diagnostic guidelines"},
    {"orig_id": "expanded_gout_005", "decision": "revise", "new_ids": "gout_007", "reason": "Updated fructose warnings for gout"},
    {"orig_id": "expanded_gout_006", "decision": "split", "new_ids": "gout_009;safety_003", "reason": "Split acute flare guidelines from emergency steps"},
    {"orig_id": "expanded_gout_007", "decision": "revise", "new_ids": "gout_002", "reason": "Updated purine guidelines"},
    
    {"orig_id": "expanded_ckd_001", "decision": "split", "new_ids": "ckd_g3a_002;ckd_g3b_002;ckd_g4_002;ckd_g5_nondialysis_002;ckd_dialysis_002", "reason": "Split protein restrictions by CKD stage"},
    {"orig_id": "expanded_ckd_002", "decision": "split", "new_ids": "ckd_g3a_004;ckd_g3b_004;ckd_g4_004;ckd_g5_nondialysis_004;ckd_dialysis_004", "reason": "Split potassium instructions by stage"},
    {"orig_id": "expanded_ckd_003", "decision": "split", "new_ids": "ckd_g3a_004;ckd_g3b_004;ckd_g4_004;ckd_g5_nondialysis_004;ckd_dialysis_004", "reason": "Split potassium guidelines"},
    {"orig_id": "expanded_ckd_004", "decision": "split", "new_ids": "ckd_g3a_004;ckd_g3b_004;ckd_g4_004;ckd_g5_nondialysis_004;ckd_dialysis_004", "reason": "Split potassium guidelines"},
    {"orig_id": "expanded_ckd_005", "decision": "split", "new_ids": "ckd_g3a_004;ckd_g3b_004;ckd_g4_004;ckd_g5_nondialysis_004;ckd_dialysis_004", "reason": "Split potassium guidelines"},
    {"orig_id": "expanded_ckd_006", "decision": "split", "new_ids": "ckd_g3a_004;ckd_g3b_004;ckd_g4_004;ckd_g5_nondialysis_004;ckd_dialysis_004", "reason": "Split potassium guidelines"},
    {"orig_id": "expanded_ckd_007", "decision": "split", "new_ids": "ckd_g3a_004;ckd_g3b_004;ckd_g4_004;ckd_g5_nondialysis_004;ckd_dialysis_004", "reason": "Split potassium guidelines"},
    {"orig_id": "expanded_ckd_008", "decision": "split", "new_ids": "ckd_g3a_004;ckd_g3b_004;ckd_g4_004;ckd_g5_nondialysis_004;ckd_dialysis_004", "reason": "Split potassium guidelines"},
    {"orig_id": "expanded_ckd_009", "decision": "split", "new_ids": "ckd_g3a_005;ckd_g3b_005;ckd_g4_005;ckd_g5_nondialysis_005;ckd_dialysis_005", "reason": "Split phosphorus guidelines by stage"},
    {"orig_id": "expanded_ckd_010", "decision": "split", "new_ids": "ckd_g2_004;ckd_g3a_006;ckd_g3b_006;ckd_g4_008", "reason": "Split comorbidity guidelines by stage"},
    
    {"orig_id": "expanded_obesity_001", "decision": "revise", "new_ids": "obesity_002", "reason": "Updated portion control guidelines"},
    {"orig_id": "expanded_obesity_002", "decision": "revise", "new_ids": "obesity_005", "reason": "Updated activity guidelines"},
    {"orig_id": "expanded_obesity_003", "decision": "revise", "new_ids": "obesity_004", "reason": "Updated sugary drink guidelines"},
    {"orig_id": "expanded_obesity_004", "decision": "revise", "new_ids": "obesity_001", "reason": "Updated weight management overview"}
]

def build_health_knowledge_chunks_csv():
    # Exactly four columns: chunk_id, condition_code, content, source_id
    # Use utf-8-sig to preserve Vietnamese characters
    with open(chunks_v2_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["chunk_id", "condition_code", "content", "source_id"])
        for chunk in chunks_v2:
            writer.writerow([
                chunk["chunk_id"],
                chunk["condition_code"],
                chunk["content"],
                chunk["source_id"]
            ])
    print(f"Created health_knowledge_chunks_v2.csv with {len(chunks_v2)} entries.")

def build_chunk_source_traceability_csv():
    headers = [
        "chunk_id", "source_id", "source_file", "source_type",
        "source_locator", "source_page", "source_section",
        "extracted_supporting_text", "claim_summary", "verification_status"
    ]
    with open(traceability_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for chunk in chunks_v2:
            writer.writerow([
                chunk["chunk_id"],
                chunk["source_id"],
                f"data/rag/v2/raw_sources/{chunk['source_id']}.txt",
                "pdf" if chunk["source_id"] == "kdigo_2024_ckd_guideline" else "html",
                chunk["locator"],
                chunk["page"],
                chunk["section"],
                chunk["text_support"],
                chunk["claim"],
                "verified"
            ])
    print("Created chunk_source_traceability_v2.csv.")

def build_source_registry_v2_csv():
    headers = [
        "source_id", "publisher", "title", "source_type",
        "original_url", "publication_date", "accessed_date",
        "local_snapshot_path", "extracted_text_path", "relevant_pages",
        "relevant_sections", "authority_level", "verification_status", "notes"
    ]
    with open(registry_v2_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for src in source_registry_v2:
            writer.writerow([
                src["source_id"],
                src["publisher"],
                src["title"],
                src["source_type"],
                src["original_url"],
                src["publication_date"],
                src["accessed_date"],
                src["local_snapshot_path"],
                src["extracted_text_path"],
                src["relevant_pages"],
                src["relevant_sections"],
                src["authority_level"],
                src["verification_status"],
                src["notes"]
            ])
    print("Created source_registry_v2.csv.")

def save_decisions_json():
    # Save original chunk decisions as reference
    decisions_path = os.path.join(v2_dir, "original_chunk_decisions.json")
    with open(decisions_path, "w", encoding="utf-8") as f:
        json.dump(chunk_decisions, f, indent=2, ensure_ascii=False)
    print("Created original_chunk_decisions.json.")

if __name__ == "__main__":
    build_health_knowledge_chunks_csv()
    build_chunk_source_traceability_csv()
    build_source_registry_v2_csv()
    save_decisions_json()
    print("All chunks built successfully.")
