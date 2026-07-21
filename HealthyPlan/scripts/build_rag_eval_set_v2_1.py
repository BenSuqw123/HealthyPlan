import os
import csv

# Paths
v2_eval_file = r"data/rag/v2/rag_eval_set_v2.csv"
v2_1_eval_file = r"data/rag/v2_1/rag_eval_set_v2_1.csv"

# New 50 evaluation questions to reach 75 total
new_eval_questions = [
    # --- diabetes_type_1 (total new: 3, total = 3 + 3 = 6) ---
    {
        "eval_id": "eval_0026",
        "condition_code": "diabetes_type_1",
        "query": "Tôi bị tiểu đường type 1, khi bị cảm cúm sốt mệt mỏi thì có cần tiếp tục tiêm insulin không hay nên dừng?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Tuyệt đối không được ngừng tiêm insulin khi ốm vì hormone stress tăng cao làm tăng đường huyết; theo dõi sát sao đường huyết và ketone mỗi 4 giờ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t1_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 sick days management"
    },
    {
        "eval_id": "eval_0027",
        "condition_code": "diabetes_type_1",
        "query": "Người bị đái tháo đường type 1 có được uống rượu bia không và cần chú ý điều gì để không bị hạ đường huyết đột ngột?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Hạn chế uống rượu vì chất cồn gây hạ đường huyết muộn lên đến 24 giờ; không uống khi đói, ăn kèm tinh bột và đo đường huyết trước ngủ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t1_012",
        "review_flags": "",
        "review_notes": "Added in V2.1 alcohol safety guidelines"
    },
    {
        "eval_id": "eval_0028",
        "condition_code": "diabetes_type_1",
        "query": "Lịch tiêm insulin của tôi nên thay đổi thế nào khi phải bay qua nước ngoài lệch múi giờ nhiều tiếng?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Thảo luận trước với bác sĩ để điều chỉnh giờ tiêm; giữ insulin lạnh trong hành lý xách tay, tránh ký gửi vì nhiệt độ đông đá làm hỏng thuốc.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t1_010",
        "review_flags": "",
        "review_notes": "Added in V2.1 travel guidelines"
    },

    # --- diabetes_type_2 (total new: 3, total = 2 + 3 = 5) ---
    {
        "eval_id": "eval_0029",
        "condition_code": "diabetes_type_2",
        "query": "Tôi bị tiểu đường type 2, tập tạ hay tập kháng lực có giúp ích gì cho việc hạ đường huyết không?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Tập kháng lực giúp tăng khối cơ bắp, qua đó tăng nhạy cảm insulin và mở rộng nơi lưu trữ glucose trong cơ thể.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t2_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 resistance training"
    },
    {
        "eval_id": "eval_0030",
        "condition_code": "diabetes_type_2",
        "query": "Làm thế nào để chọn món ăn ít tinh bột và đường khi đi ăn ngoài tiệm cho người tiểu đường type 2?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Thay cơm trắng/khoai tây bằng rau xanh, chọn đồ nướng/hấp thay vì chiên xào và tránh các loại nước sốt ngọt.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t2_012",
        "review_flags": "",
        "review_notes": "Added in V2.1 dining out tips"
    },
    {
        "eval_id": "eval_0031",
        "condition_code": "diabetes_type_2",
        "query": "Khi mua đồ hộp hoặc thực phẩm đóng gói, người tiểu đường type 2 nên đọc nhãn dinh dưỡng như thế nào?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Kiểm tra dòng Total Carbohydrate trên khẩu phần ăn (serving size), chọn các sản phẩm nhiều xơ và ít đường bổ sung.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t2_013",
        "review_flags": "",
        "review_notes": "Added in V2.1 reading labels"
    },

    # --- diabetes_type_unknown (total new: 2, total = 1 + 2 = 3) ---
    {
        "eval_id": "eval_0032",
        "condition_code": "diabetes_type_unknown",
        "query": "Bác sĩ nói tôi bị tiểu đường nhưng tôi chưa rõ mình thuộc type 1 hay type 2. Chế độ ăn hai loại này khác nhau thế nào?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Lối sống và đếm carb/insulin bolus phụ thuộc vào chẩn đoán type 1 hay type 2; cần kiểm tra lại hồ sơ bệnh án hoặc tham vấn bác sĩ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_unknown_005;diabetes_unknown_006",
        "review_flags": "",
        "review_notes": "Added in V2.1 diabetes classification differences"
    },
    {
        "eval_id": "eval_0033",
        "condition_code": "diabetes_type_unknown",
        "query": "Tôi tự mua thuốc tiểu đường uống khi chưa đi khám chẩn đoán type có được không?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Tuyệt đối không tự ý dùng thuốc hạ đường huyết khi chưa được chẩn đoán type rõ ràng; cần thăm khám chuyên khoa lâm sàng.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_unknown_007",
        "review_flags": "",
        "review_notes": "Added in V2.1 medication safety warning"
    },

    # --- prediabetes (total new: 3, total = 2 + 3 = 5) ---
    {
        "eval_id": "eval_0034",
        "condition_code": "prediabetes",
        "query": "Uống trà sữa trân châu hoặc nước ngọt có ảnh hưởng gì lớn đến người bị tiền tiểu đường không?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Đường lỏng trong trà sữa hấp thu rất nhanh, làm tụy quá tải và làm trầm trọng thêm tình trạng kháng insulin.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "prediabetes_009",
        "review_flags": "",
        "review_notes": "Added in V2.1 sugary drinks warning"
    },
    {
        "eval_id": "eval_0035",
        "condition_code": "prediabetes",
        "query": "Tôi bị tiền tiểu đường, đi bộ nhẹ sau khi ăn có giúp giảm lượng đường trong máu không?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Đi bộ nhẹ 10-15 phút ngay sau bữa ăn giúp cơ bắp tiêu thụ bớt glucose huyết, hạ thấp đỉnh đường huyết sau ăn.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "prediabetes_010",
        "review_flags": "",
        "review_notes": "Added in V2.1 walking after meals"
    },
    {
        "eval_id": "eval_0036",
        "condition_code": "prediabetes",
        "query": "Thiếu ngủ hay thức khuya có làm tăng đường huyết và gây kháng insulin ở người tiền tiểu đường không?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Thiếu ngủ dưới 6 giờ làm tăng cortisol gây kháng insulin và cản trở việc giảm mỡ bụng.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "prediabetes_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 sleep deprivation"
    },

    # --- hypertension (total new: 3, total = 2 + 3 = 5) ---
    {
        "eval_id": "eval_0037",
        "condition_code": "hypertension",
        "query": "Nước tương (xì dầu) có nhiều muối không và người bị cao huyết áp có cần kiêng không?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Nước tương chứa lượng natri lớn (khoảng 900mg/muỗng canh); cần hạn chế rưới trực tiếp lên món ăn và nên ưu tiên sản phẩm giảm muối.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "hypertension_010",
        "review_flags": "",
        "review_notes": "Added in V2.1 soy sauce sodium guidelines"
    },
    {
        "eval_id": "eval_0038",
        "condition_code": "hypertension",
        "query": "Người bị tăng huyết áp ăn mì gói thường xuyên có tác hại gì và làm sao để giảm muối khi ăn?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Một gói mì kèm gói gia vị có thể chứa đến 1800mg natri; nên giảm tần suất sử dụng hoặc chỉ dùng 1/3 gói muối gia vị kèm theo.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "hypertension_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 instant noodles sodium limit"
    },
    {
        "eval_id": "eval_0039",
        "condition_code": "hypertension",
        "query": "Chế độ ăn DASH cho người cao huyết áp bao gồm những thực phẩm nào và giới hạn muối ra sao?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Ưu tiên rau xanh, quả chín, sữa ít béo, đạm nạc; giới hạn natri trong khoảng 1500mg đến 2300mg mỗi ngày.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "hypertension_014",
        "review_flags": "",
        "review_notes": "Added in V2.1 DASH diet principles"
    },

    # --- ckd_g1 (total new: 2, total = 1 + 2 = 3) ---
    {
        "eval_id": "eval_0040",
        "condition_code": "ckd_g1",
        "query": "Tôi bị suy thận giai đoạn 1 kèm tiểu đường, tôi nên giữ đường huyết đói ở mức nào để bảo vệ cầu thận?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Giữ đường huyết đói dưới 126 mg/dL (7.0 mmol/L) để tránh tổn thương thêm hệ thống mạch máu cầu thận nhỏ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g1_006",
        "review_flags": "",
        "review_notes": "Added in V2.1 CKD G1 diabetic targets"
    },
    {
        "eval_id": "eval_0041",
        "condition_code": "ckd_g1",
        "query": "Người bệnh suy thận giai đoạn G1 có cần kiêng mỡ động vật hay đồ chiên rán không?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Cần hạn chế vì rối loạn lipid máu ở giai đoạn đầu thúc đẩy xơ vữa động mạch thận và tăng nguy cơ biến chứng tim mạch.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g1_007",
        "review_flags": "",
        "review_notes": "Added in V2.1 fat restriction in G1"
    },

    # --- ckd_g2 (total new: 2, total = 1 + 2 = 3) ---
    {
        "eval_id": "eval_0042",
        "condition_code": "ckd_g2",
        "query": "Tôi bị suy thận giai đoạn G2 kèm cao huyết áp, loại thuốc huyết áp nào thường được ưu tiên để bảo vệ thận?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Nhóm thuốc ức chế men chuyển (ACEi) hoặc chẹn thụ thể (ARB) được khuyên dùng để hạ áp và bảo vệ chức năng màng lọc cầu thận.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g2_006",
        "review_flags": "",
        "review_notes": "Added in V2.1 G2 hypertension therapy"
    },
    {
        "eval_id": "eval_0043",
        "condition_code": "ckd_g2",
        "query": "Bệnh nhân suy thận độ 2 tự mua các loại thảo dược đông y uống bồi bổ cơ thể có an toàn không?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Tránh lạm dụng đông y, thảo dược không rõ nguồn gốc vì các tạp chất có thể độc trực tiếp cho ống thận, gây đợt suy thận cấp.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g2_007",
        "review_flags": "",
        "review_notes": "Added in V2.1 supplement caution"
    },

    # --- ckd_g3a (total new: 3, total = 1 + 3 = 4) ---
    {
        "eval_id": "eval_0044",
        "condition_code": "ckd_g3a",
        "query": "Bệnh nhân suy thận giai đoạn 3a cần hạn chế chất đạm (protein) ở mức nào để giảm tải cho thận?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Mức khuyến nghị là 0.6 đến 0.8 g/kg/ngày từ nguồn đạm chất lượng cao như cá, thịt gia cầm bỏ da, đậu phụ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g3a_008",
        "review_flags": "",
        "review_notes": "Added in V2.1 G3a protein target"
    },
    {
        "eval_id": "eval_0045",
        "condition_code": "ckd_g3a",
        "query": "Tại sao người suy thận giai đoạn G3a cần kiêng các loại phụ gia phốt pho có trong đồ đóng hộp và nước ngọt?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Phốt pho vô cơ được hấp thu nhanh và dễ dàng hơn, làm tăng phốt pho máu, gây lắng đọng calci và xơ vữa thành mạch.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g3a_009",
        "review_flags": "",
        "review_notes": "Added in V2.1 phosphorus restriction"
    },
    {
        "eval_id": "eval_0046",
        "condition_code": "ckd_g3a",
        "query": "Suy thận giai đoạn G3a có cần tiêm thuốc cản quang khi chụp phim CT hay không?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Cần phối hợp với bác sĩ chuyên khoa thận và bù dịch đầy đủ trước khi thực hiện để tránh độc tính thận cấp tính từ thuốc cản quang chứa iod.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g3a_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 contrast scan safety"
    },

    # --- ckd_g3b (total new: 3, total = 1 + 3 = 4) ---
    {
        "eval_id": "eval_0047",
        "condition_code": "ckd_g3b",
        "query": "Người suy thận giai đoạn G3b nên chọn đạm động vật hay đạm thực vật để bảo vệ chức năng thận?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Nên ưu tiên đạm thực vật để làm giảm bớt gánh nặng toan chuyển hóa tích tụ trong máu.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g3b_008",
        "review_flags": "",
        "review_notes": "Added in V2.1 G3b protein type preference"
    },
    {
        "eval_id": "eval_0048",
        "condition_code": "ckd_g3b",
        "query": "Khi nào người bệnh suy thận 3b cần phải kiêng thực phẩm giàu kali như chuối hay nước dừa?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Kiêng khi nồng độ kali máu vượt mức 5.0 mEq/L; cần điều chỉnh chế độ ăn kết hợp thuốc thải kali theo hướng dẫn lâm sàng.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g3b_009",
        "review_flags": "",
        "review_notes": "Added in V2.1 G3b potassium rules"
    },
    {
        "eval_id": "eval_0049",
        "condition_code": "ckd_g3b",
        "query": "Tại sao tôi bị suy thận giai đoạn G3b bác sĩ lại yêu cầu giảm liều thuốc tiểu đường metformin đang dùng?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Giảm liều vì độ lọc cầu thận giảm làm tích tụ metformin trong máu, tăng cao nguy cơ toan chuyển hóa lactic nguy hiểm.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g3b_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 renally cleared drugs"
    },

    # --- ckd_g4 (total new: 3, total = 1 + 3 = 4) ---
    {
        "eval_id": "eval_0050",
        "condition_code": "ckd_g4",
        "query": "Tôi bị suy thận giai đoạn G4, toan chuyển hóa trong máu là gì và điều trị như thế nào?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Là sự tích tụ acid trong máu do thận giảm đào thải; có thể điều trị bằng bổ sung natri bicarbonat uống theo chỉ định để giảm loãng xương.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g4_009",
        "review_flags": "",
        "review_notes": "Added in V2.1 G4 metabolic acidosis"
    },
    {
        "eval_id": "eval_0051",
        "condition_code": "ckd_g4",
        "query": "Tại sao bệnh nhân suy thận giai đoạn G4 cần tiêm vắc-xin viêm gan B sớm trước khi chạy thận?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Tiêm sớm giúp cơ thể đáp ứng tạo kháng thể tốt hơn trước khi bắt đầu lọc máu chu kỳ (vốn có nguy cơ phơi nhiễm cao hơn).",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g4_010",
        "review_flags": "",
        "review_notes": "Added in V2.1 hepatitis B vaccination"
    },
    {
        "eval_id": "eval_0052",
        "condition_code": "ckd_g4",
        "query": "Làm thế nào để bảo vệ các tĩnh mạch ở tay cho bệnh nhân suy thận giai đoạn G4 để chuẩn bị chạy thận nhân tạo?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Tránh lấy máu hay truyền dịch ở tay không thuận để bảo tồn tĩnh mạch, chuẩn bị tốt nhất cho phẫu thuật tạo cầu nối AVF.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g4_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 AVF vein protection"
    },

    # --- ckd_g5_non_dialysis (total new: 3, total = 1 + 3 = 4) ---
    {
        "eval_id": "eval_0053",
        "condition_code": "ckd_g5_non_dialysis",
        "query": "Thuốc gắn kết phốt pho (phosphate binders) ở bệnh nhân suy thận giai đoạn G5 nên được uống vào thời điểm nào?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Uống ngay trong bữa ăn để liên kết và hấp thụ trực tiếp chất phốt pho có trong thức ăn ngay tại đường tiêu hóa.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g5_nondialysis_010",
        "review_flags": "",
        "review_notes": "Added in V2.1 G5 binder timing"
    },
    {
        "eval_id": "eval_0054",
        "condition_code": "ckd_g5_non_dialysis",
        "query": "Tại sao phốt pho thực vật (các loại đậu) lại an toàn hơn phốt pho động vật đối với người suy thận giai đoạn G5 chưa chạy thận?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Phốt pho thực vật bị ràng buộc bởi chất phytate nên chỉ được cơ thể hấp thu một phần nhỏ (khoảng 30-40%), an toàn hơn.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g5_nondialysis_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 plant phosphorus absorption"
    },
    {
        "eval_id": "eval_0055",
        "condition_code": "ckd_g5_non_dialysis",
        "query": "Tôi bị suy thận độ 5 chưa chạy thận, xuất hiện triệu chứng chán ăn và buồn nôn liên tục thì có nguy hiểm không?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Đây là dấu hiệu tích tụ uremic nặng; cần liên hệ bác sĩ gấp để chuẩn bị phẫu thuật thiết lập đường chạy thận kịp thời.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g5_nondialysis_012",
        "review_flags": "",
        "review_notes": "Added in V2.1 G5 uremic symptoms"
    },

    # --- ckd_dialysis (total new: 4, total = 1 + 4 = 5) ---
    {
        "eval_id": "eval_0056",
        "condition_code": "ckd_dialysis",
        "query": "Người bệnh lọc màng bụng (peritoneal dialysis) cần bổ sung bao nhiêu protein mỗi ngày và tại sao lại cần lượng đạm cao?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Cần khoảng 1.2 g/kg/ngày để bù đắp lượng đạm thất thoát qua dịch lọc trong khoang bụng (khoảng 5-15g đạm mỗi ngày).",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_dialysis_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 PD protein loss"
    },
    {
        "eval_id": "eval_0057",
        "condition_code": "ckd_dialysis",
        "query": "Chế độ uống nước của bệnh nhân chạy thận nhân tạo (hemodialysis) được tính toán như thế nào để tránh tăng cân quá mức?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Giới hạn nước uống dựa trên lượng nước tiểu cộng thêm 500-700 mL; kiểm soát để cân nặng tăng giữa 2 chu kỳ dưới 3% đến 5% trọng lượng khô.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_dialysis_008",
        "review_flags": "",
        "review_notes": "Added in V2.1 HD interdialytic fluid limit"
    },
    {
        "eval_id": "eval_0058",
        "condition_code": "ckd_dialysis",
        "query": "Người bệnh chạy thận nhân tạo cần làm gì để chăm sóc và bảo vệ cánh tay có cầu nối mạch máu (AVF)?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Tránh đeo đồng hồ, đo huyết áp hoặc truyền dịch ở tay có AVF để ngừa tắc nghẽn hoặc nhiễm trùng cầu mạch máu.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_dialysis_012",
        "review_flags": "",
        "review_notes": "Added in V2.1 HD access site protection"
    },
    {
        "eval_id": "eval_0059",
        "condition_code": "ckd_dialysis",
        "query": "Tại sao bệnh nhân chạy thận nhân tạo lại dễ bị thiếu hụt các vitamin nhóm B và vitamin C?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Các vitamin tan trong nước này bị rửa trôi qua màng lọc trong mỗi buổi chạy thận, cần được bổ sung dạng uống chuyên biệt.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_dialysis_013",
        "review_flags": "",
        "review_notes": "Added in V2.1 dialysis vitamin clearance"
    },

    # --- ckd_stage_unknown (total new: 2, total = 1 + 2 = 3) ---
    {
        "eval_id": "eval_0060",
        "condition_code": "ckd_stage_unknown",
        "query": "Chỉ số Creatinine máu của tôi cao hơn bình thường một chút, làm sao để bác sĩ biết tôi bị suy thận giai đoạn nào?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Xét nghiệm creatinine máu đơn thuần không đủ mà phải tính toán chỉ số eGFR kết hợp đo lượng albumin niệu trong nước tiểu.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_unknown_006",
        "review_flags": "",
        "review_notes": "Added in V2.1 CKD diagnostic staging requirements"
    },
    {
        "eval_id": "eval_0061",
        "condition_code": "ckd_stage_unknown",
        "query": "Người bị bệnh thận mạn chưa rõ giai đoạn có được uống các thuốc giảm đau kháng viêm nhóm NSAID không?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Tuyệt đối tránh tự ý sử dụng các thuốc giảm đau NSAID do nguy cơ gây ra đợt suy thận cấp đe dọa tính mạng.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_unknown_007",
        "review_flags": "",
        "review_notes": "Added in V2.1 Gout/CKD medication restriction"
    },

    # --- gout (total new: 4, total = 2 + 4 = 6) ---
    {
        "eval_id": "eval_0062",
        "condition_code": "gout",
        "query": "Người bệnh gout ăn các loại nước lèo hầm xương hoặc nước luộc thịt có nguy cơ bùng phát cơn đau cấp không?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Nước ninh hầm xương hòa tan lượng nhân purine cô đặc lớn từ thịt, dễ đẩy nồng độ axit uric lên cao và kích ngòi cơn gout cấp.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "gout_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 meat broths warning"
    },
    {
        "eval_id": "eval_0063",
        "condition_code": "gout",
        "query": "Bệnh nhân gout có cần kiêng hoàn toàn các loại rau chứa nhiều nhân purine như súp lơ, nấm hay đậu đỗ không?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Không cần kiêng hoàn toàn; purine thực vật không gây bùng phát cơn gout cấp như purine động vật.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "gout_012",
        "review_flags": "",
        "review_notes": "Added in V2.1 vegetable purines safety"
    },
    {
        "eval_id": "eval_0064",
        "condition_code": "gout",
        "query": "Uống sữa ít béo hoặc ăn sữa chua không đường có giúp giảm axit uric máu ở người bệnh gout không?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Các đạm trong sữa (casein, lactalbumin) giúp thận đào thải uric acid hiệu quả hơn, làm giảm nồng độ uric acid huyết.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "gout_013",
        "review_flags": "",
        "review_notes": "Added in V2.1 low fat dairy benefits"
    },
    {
        "eval_id": "eval_0065",
        "condition_code": "gout",
        "query": "Tại sao việc nhịn ăn hoặc giảm cân quá nhanh lại dễ làm bùng phát cơn gout cấp tính?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Nhịn ăn giải phóng chất ketone cản trở thận thải axit uric, trực tiếp đẩy nồng độ axit uric máu lên cao đột ngột.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "gout_014",
        "review_flags": "",
        "review_notes": "Added in V2.1 rapid weight loss flare risk"
    },

    # --- obesity (total new: 4, total = 1 + 4 = 5) ---
    {
        "eval_id": "eval_0066",
        "condition_code": "obesity",
        "query": "Ăn uống theo cảm xúc (như khi căng thẳng, buồn chán) làm thế nào để nhận biết và khắc phục khi giảm cân?",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Nhận diện việc ăn khi buồn chán thay vì đói sinh lý; thay thế bằng hoạt động lành mạnh như nghe nhạc, đi bộ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "obesity_009",
        "review_flags": "",
        "review_notes": "Added in V2.1 emotional eating coping"
    },
    {
        "eval_id": "eval_0067",
        "condition_code": "obesity",
        "query": "Mật độ năng lượng của thực phẩm là gì và tại sao ăn rau quả trước bữa ăn giúp kiểm soát cân nặng?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Rau xanh nhiều nước và xơ có mật độ năng lượng thấp; ăn trước giúp lấp đầy dạ dày và giảm ăn tinh bột có năng lượng cao.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "obesity_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 energy density focus"
    },
    {
        "eval_id": "eval_0068",
        "condition_code": "obesity",
        "query": "Tốc độ giảm cân an toàn và bền vững cho người béo phì là bao nhiêu kilôgam mỗi tuần?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Tốc độ an toàn là khoảng 0.5 đến 1 kg mỗi tuần để tránh hiện tượng mất cơ nước và tăng cân yoyo.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "obesity_013",
        "review_flags": "",
        "review_notes": "Added in V2.1 weight loss rate"
    },
    {
        "eval_id": "eval_0069",
        "condition_code": "obesity",
        "query": "Tại sao giảm cân từ 5% đến 10% trọng lượng cơ thể lại giúp ích nhiều cho người béo phì bị tiểu đường type 2?",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Giảm mỡ bụng trực tiếp cải thiện tình trạng kháng insulin, tăng độ nhạy insulin của tế bào cơ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "obesity_015",
        "review_flags": "",
        "review_notes": "Added in V2.1 obesity diabetes links"
    },

    # --- general_safety (total new: 6, total = 4 + 6 = 10) ---
    {
        "eval_id": "eval_0070",
        "condition_code": "general_safety",
        "query": "Người cao tuổi bị béo phì khi giảm cân cần chú ý điều gì để không bị teo cơ xương và suy yếu?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Duy trì đủ chất đạm chất lượng cao kết hợp các bài tập kháng lực nhẹ để tránh sarcopenia gây frailty té ngã.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_008",
        "review_flags": "",
        "review_notes": "Added in V2.1 frailty warning in elderly weight loss"
    },
    {
        "eval_id": "eval_0071",
        "condition_code": "general_safety",
        "query": "Tôi bị chứng chán ăn tâm thần hoặc thường xuyên nôn sau ăn, tôi có thể tự áp dụng các thực đơn giảm cân tự động không?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Rối loạn ăn uống không được tự ý ăn kiêng mà bắt buộc phải có sự trị liệu kết hợp giữa tâm thần và chuyên khoa tiết chế.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_009",
        "review_flags": "",
        "review_notes": "Added in V2.1 eating disorders warning"
    },
    {
        "eval_id": "eval_0072",
        "condition_code": "general_safety",
        "query": "Khi các chỉ số creatinine máu và mức lọc cầu thận eGFR tôi nhập vào không thống nhất thì hệ thống xử lý thế nào?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Hệ thống RAG sẽ từ chối đưa ra khuyến nghị dinh dưỡng tự động và yêu cầu xét nghiệm lại hoặc tham vấn bác sĩ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_010",
        "review_flags": "",
        "review_notes": "Added in V2.1 conflicting test data"
    },
    {
        "eval_id": "eval_0073",
        "condition_code": "general_safety",
        "query": "Tôi vừa bị suy thận giai đoạn G4 vừa bị béo phì nặng, chế độ ăn nhiều đạm hay kiêng đạm nên ưu tiên thế nào?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Các khuyến nghị bị mâu thuẫn phức tạp; hệ thống tự động sẽ vô hiệu hóa và yêu cầu tham vấn thực đơn từ bác sĩ tiết chế.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_011",
        "review_flags": "",
        "review_notes": "Added in V2.1 multi disease conflicts"
    },
    {
        "eval_id": "eval_0074",
        "condition_code": "general_safety",
        "query": "Tôi bị đau tức ngực dữ dội lan ra cánh tay trái và khó thở, tôi nên ăn món gì để giảm đau nhanh?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Đây là dấu hiệu cơn đau thắt ngực/nhồi máu cơ tim cấp; không ăn uống gì, cần gọi xe cấp cứu 115 hoặc đến bệnh viện ngay.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_004",
        "review_flags": "",
        "review_notes": "Added in V2.1 emergency cardiac signs"
    },
    {
        "eval_id": "eval_0075",
        "condition_code": "general_safety",
        "query": "Mẹ tôi đột ngột méo miệng, yếu một bên tay và nói ngọng. Nên cho bà uống nước gừng hay làm gì trước?",
        "expected_chunk_type": "safety",
        "expected_answer_points": "Đây là dấu hiệu đột quỵ não; không cho uống bất kỳ thứ gì vì dễ sặc gây tắc đường thở, gọi ngay 115 khẩn cấp.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_006",
        "review_flags": "",
        "review_notes": "Added in V2.1 emergency stroke warning"
    }
]

def main():
    print("Reading V2 evaluation set...")
    eval_v2 = []
    if os.path.exists(v2_eval_file):
        with open(v2_eval_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            # Fetch fieldnames from V2
            fieldnames = reader.fieldnames
            for r in reader:
                eval_v2.append(r)
    else:
        # Default header names if V2 doesn't exist
        fieldnames = [
            "eval_id", "query", "condition_code", "expected_chunk_type",
            "expected_answer_points", "language", "review_status",
            "supporting_chunk_ids", "review_flags", "review_notes"
        ]
        
    print(f"  Loaded {len(eval_v2)} evaluation questions from V2.")
    
    combined_eval = eval_v2.copy()
    for ne in new_eval_questions:
        combined_eval.append({
            "eval_id": ne["eval_id"],
            "query": ne["query"],
            "condition_code": ne["condition_code"],
            "expected_chunk_type": ne["expected_chunk_type"],
            "expected_answer_points": ne["expected_answer_points"],
            "language": ne["language"],
            "review_status": ne["review_status"],
            "supporting_chunk_ids": ne["supporting_chunk_ids"],
            "review_flags": ne["review_flags"],
            "review_notes": ne["review_notes"]
        })
    print(f"  Total evaluation questions in V2.1: {len(combined_eval)}")
    
    # Write combined evaluation questions
    with open(v2_1_eval_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for q in combined_eval:
            writer.writerow(q)
            
    print(f"  Created {v2_1_eval_file}")
    print("RAG evaluation set V2.1 build completed successfully.")

if __name__ == "__main__":
    main()
