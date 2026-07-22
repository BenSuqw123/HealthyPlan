from entity_extractor import extract_medical_entities


test_cases = [
    ("Tôi bị tiểu đường type 1.", ["diabetes_type_1"]),
    ("Người bệnh suy thận 3b cần ăn gì?", ["ckd_g3b"]),
    ("Tôi bị suy thận G4 và béo phì.", ["ckd_g4", "obesity"]),
    ("Bệnh nhân CKD G5 chưa lọc máu.", ["ckd_g5_non_dialysis"]),
    ("Người bệnh đang chạy thận nhân tạo.", ["ckd_dialysis"]),
    ("Tôi bị tiền tiểu đường và cao huyết áp.", ["prediabetes", "hypertension"]),
    ("Người béo phì bị tiểu đường type 2.", ["obesity", "diabetes_type_2"]),(
    "Người bệnh đang chạy thận nhân tạo.",
    ["ckd_dialysis"],
),
(
    "Bệnh nhân suy thận G4 đang chuẩn bị chạy thận nhân tạo.",
    ["ckd_g4"],
),
(
    "Người bệnh CKD G4 cần bảo vệ tĩnh mạch để chuẩn bị chạy thận.",
    ["ckd_g4"],
),
(
    "Bệnh nhân suy thận độ 4 cần làm cầu nối chạy thận.",
    ["ckd_g4"],
),
(
    "Người bệnh CKD G5 chưa chạy thận.",
    ["ckd_g5_non_dialysis"],
),
(
    "Người bệnh CKD G5 đang chạy thận.",
    ["ckd_dialysis"],
),
]


for query, expected_condition_codes in test_cases:
    extraction_result = extract_medical_entities(query)
    actual_condition_codes = extraction_result["condition_codes"]

    assert actual_condition_codes == expected_condition_codes, (
        f"Query: {query}\n"
        f"Expected: {expected_condition_codes}\n"
        f"Actual: {actual_condition_codes}"
    )


print("MEDICAL ENTITY EXTRACTOR TEST: PASS")