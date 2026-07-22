from safety_flag_extractor import extract_safety_flags


test_cases = [
    # Pregnancy
    (
        "Bà bầu bị tiểu đường nên ăn thế nào?",
        ["pregnancy"],
    ),
    (
        "Người đang mang thai có nên giảm cân không?",
        ["pregnancy"],
    ),
    (
        "Thai phụ bị cao huyết áp cần chú ý gì?",
        ["pregnancy"],
    ),
    (
        "Trong thai kỳ tôi có cần kiêng hoàn toàn tinh bột không?",
        ["pregnancy"],
    ),

    # Elderly frailty
    (
        "Người cao tuổi giảm cân cần tránh teo cơ và suy yếu.",
        ["elderly_frailty", "malnutrition_risk"],
    ),
    (
        "Người già đang bị mất cơ và suy nhược thì nên ăn gì?",
        ["elderly_frailty", "malnutrition_risk"],
    ),
    (
        "Người lớn tuổi bị suy kiệt sau khi giảm cân.",
        ["elderly_frailty", "malnutrition_risk"],
    ),
    (
        "Người cao tuổi nên kiểm tra huyết áp bao lâu một lần?",
        [],
    ),
    (
        "Tôi bị teo cơ sau khi giảm cân quá nhanh.",
        ["malnutrition_risk"],
    ),

    # Multiple conditions
    (
        "Tôi bị suy thận G4 và béo phì.",
        ["multiple_conditions"],
    ),
    (
        "Tôi bị tiền tiểu đường và cao huyết áp.",
        ["multiple_conditions"],
    ),
    (
        "Người béo phì bị tiểu đường type 2 nên giảm cân thế nào?",
        ["multiple_conditions"],
    ),
    (
        "Tôi vừa bị gout vừa bị béo phì.",
        ["multiple_conditions"],
    ),
    (
        "Tôi bị suy thận G3b và tiểu đường type 1.",
        ["multiple_conditions"],
    ),
    (
        "Tôi bị béo phì và obesity.",
        [],
    ),

    # Conflicting diet rules
    (
        "Tôi bị suy thận G4 và béo phì, chế độ ăn nhiều đạm hay kiêng đạm?",
        ["multiple_conditions", "conflicting_diet_rules"],
    ),
    (
        "Người suy thận G3b nên ăn nhiều đạm hay kiêng đạm?",
        ["conflicting_diet_rules"],
    ),
    (
        "Tôi bị gout và béo phì, chế độ ăn nên chọn thịt hay rau?",
        ["multiple_conditions", "conflicting_diet_rules"],
    ),
    (
        "Hai chế độ ăn này đang mâu thuẫn với nhau.",
        ["conflicting_diet_rules"],
    ),
    (
        "Quy tắc dinh dưỡng cho suy thận và giảm cân đang xung đột.",
        ["conflicting_diet_rules"],
    ),
    (
        "Tôi bị suy thận G4, nên ưu tiên thế nào khi lựa chọn chế độ ăn?",
        ["conflicting_diet_rules"],
    ),

    # Inconsistent lab results
    (
        "Chỉ số creatinine và eGFR của tôi không thống nhất.",
        ["inconsistent_lab_results"],
    ),
    (
        "Kết quả xét nghiệm eGFR và creatinine không khớp.",
        ["inconsistent_lab_results"],
    ),
    (
        "Mức lọc cầu thận và creatinine của tôi đang chênh lệch.",
        ["inconsistent_lab_results"],
    ),
    (
        "Chỉ số kali máu của hai lần xét nghiệm trái ngược nhau.",
        ["inconsistent_lab_results"],
    ),
    (
        "Kết quả đường huyết của tôi không phù hợp với lần xét nghiệm trước.",
        ["inconsistent_lab_results"],
    ),
    (
        "Chỉ số creatinine của tôi là bao nhiêu thì bình thường?",
        [],
    ),
    (
        "Tôi muốn kiểm tra eGFR và creatinine.",
        [],
    ),

    # Medication risk
    (
        "Tôi có được tự ý tăng liều thuốc tiểu đường không?",
        ["medication_risk"],
    ),
    (
        "Tôi có thể tự giảm liều insulin đang dùng không?",
        ["medication_risk"],
    ),
    (
        "Tôi có được ngừng thuốc huyết áp khi thấy khỏe hơn không?",
        ["medication_risk"],
    ),
    (
        "Tôi muốn tự đổi thuốc tiểu đường sang loại khác.",
        ["medication_risk"],
    ),
    (
        "Tôi có thể uống thêm thuốc khi đường huyết tăng không?",
        ["medication_risk"],
    ),
    (
        "Tôi muốn tự bỏ thuốc metformin.",
        ["medication_risk"],
    ),
    (
        "Bác sĩ yêu cầu giảm liều thuốc metformin vì tôi bị suy thận G3b.",
        [],
    ),
    (
        "Bác sĩ chỉ định đổi liều insulin cho tôi.",
        [],
    ),
    (
        "Tôi giảm liều thuốc theo hướng dẫn của bác sĩ.",
        [],
    ),
    (
        "Nhân viên y tế yêu cầu tôi điều chỉnh thuốc.",
        [],
    ),
    (
        "Thuốc metformin có tác dụng gì?",
        [],
    ),

    # Malnutrition risk
    (
        "Kiêng khem quá mức có gây suy dinh dưỡng không?",
        ["malnutrition_risk"],
    ),
    (
        "Tôi đang bị suy dinh dưỡng sau thời gian ăn kiêng.",
        ["malnutrition_risk"],
    ),
    (
        "Giảm cân quá mức khiến tôi bị mất cơ.",
        ["malnutrition_risk"],
    ),
    (
        "Tôi bị sút cân quá mức và thiếu chất.",
        ["malnutrition_risk"],
    ),
    (
        "Người bệnh suy thận có nguy cơ suy kiệt không?",
        ["malnutrition_risk"],
    ),

    # Possible emergency
    (
        "Tôi đang khó thở và đau ngực, có cần cấp cứu không?",
        ["possible_emergency"],
    ),
    (
        "Tôi vừa ngất xỉu và bị co giật.",
        ["possible_emergency"],
    ),
    (
        "Người bệnh đang hôn mê có cần đưa đi cấp cứu không?",
        ["possible_emergency"],
    ),
    (
        "Tôi bị hạ đường huyết nghiêm trọng.",
        ["possible_emergency"],
    ),
    (
        "Tôi có dấu hiệu nhiễm toan ceton.",
        ["possible_emergency"],
    ),
    (
        "Vết thương đang chảy máu không cầm.",
        ["possible_emergency"],
    ),
    (
        "Tôi chỉ hơi mệt sau khi tập thể dục.",
        [],
    ),

    # Combined safety flags
    (
        "Bà bầu bị tiểu đường type 2 và cao huyết áp nên ăn kiêng thế nào?",
        ["pregnancy", "multiple_conditions"],
    ),
    (
        "Bà bầu bị béo phì và tiểu đường type 2, nên ăn nhiều hay kiêng hoàn toàn?",
        ["pregnancy", "multiple_conditions", "conflicting_diet_rules"],
    ),
    (
        "Người cao tuổi bị suy thận G4 và béo phì đang bị teo cơ.",
        ["elderly_frailty", "multiple_conditions", "malnutrition_risk"],
    ),
    (
        "Tôi bị suy thận G4 và béo phì, chế độ ăn đang mâu thuẫn và làm tôi suy dinh dưỡng.",
        ["multiple_conditions", "conflicting_diet_rules", "malnutrition_risk"],
    ),
    (
        "Creatinine và eGFR không thống nhất, đồng thời tôi đang khó thở.",
        ["inconsistent_lab_results", "possible_emergency"],
    ),
    (
        "Tôi tự ý tăng liều thuốc tiểu đường rồi bị đau ngực.",
        ["medication_risk", "possible_emergency"],
    ),
    (
        "Người cao tuổi đang mang thai bị suy yếu.",
        ["pregnancy", "elderly_frailty"],
    ),

    # No safety flags
    (
        "Người bị gout nên hạn chế thực phẩm nào?",
        [],
    ),
    (
        "Người béo phì nên tập thể dục bao nhiêu phút?",
        [],
    ),
    (
        "Người suy thận G3b cần theo dõi eGFR bao lâu một lần?",
        [],
    ),
    (
        "Người tiểu đường type 1 nên đếm carbohydrate thế nào?",
        [],
    ),
    (
        "Bác sĩ yêu cầu tôi tái khám vào tuần sau.",
        [],
    ),
]


passed_count = 0

for test_index, test_case in enumerate(test_cases, start=1):
    query, expected_safety_flags = test_case

    extraction_result = extract_safety_flags(query)
    actual_safety_flags = extraction_result["safety_flags"]

    assert actual_safety_flags == expected_safety_flags, (
        f"Test #{test_index} failed\n"
        f"Query: {query}\n"
        f"Expected: {expected_safety_flags}\n"
        f"Actual: {actual_safety_flags}\n"
        f"Matches: {extraction_result['matches']}"
    )

    passed_count += 1


print(f"SAFETY FLAG EXTRACTOR TEST: PASS ({passed_count}/{len(test_cases)})")