import os
import csv

v2_dir = r"data/rag/v2"
os.makedirs(v2_dir, exist_ok=True)
eval_v2_path = os.path.join(v2_dir, "rag_eval_set_v2.csv")

# Structure of rag_eval_set_v2.csv:
# eval_id,query,condition_code,expected_chunk_type,expected_answer_points,language,review_status,supporting_chunk_ids,review_flags,review_notes
eval_data = [
    # --- Diabetes Type 1 ---
    {
        "eval_id": "eval_0001",
        "query": "Người bị đái tháo đường type 1 cần lưu ý gì khi đếm carb?",
        "condition_code": "diabetes_type_1",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Đếm carbohydrate để tính liều insulin bolus (tiền ăn) phù hợp; carbohydrate ảnh hưởng nhanh nhất đến đường huyết sau ăn.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t1_002",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0002",
        "query": "Tôi bị tiểu đường type 1, tại sao không nên bỏ bữa?",
        "condition_code": "diabetes_type_1",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Bỏ bữa khi đang tiêm insulin tác dụng kéo dài có nguy cơ gây hạ đường huyết nghiêm trọng; cần duy trì thời gian ăn cố định.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t1_003",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0003",
        "query": "Bị đái tháo đường type 1 có tập thể thao được không và cần chuẩn bị gì?",
        "condition_code": "diabetes_type_1",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Tập thể thao được nhưng cần kiểm tra đường huyết trước tập và chuẩn bị sẵn carbohydrate nhanh để ngừa hạ đường huyết.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t1_005",
        "review_flags": "",
        "review_notes": ""
    },

    # --- Diabetes Type 2 ---
    {
        "eval_id": "eval_0004",
        "query": "Người đái tháo đường type 2 có được ăn chất xơ không?",
        "condition_code": "diabetes_type_2",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Ăn được và rất tốt; chất xơ làm chậm tiêu hóa tinh bột, ngừa tăng đường huyết sau ăn, tăng cảm giác no hỗ trợ giảm cân.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t2_005",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0005",
        "query": "Phương pháp đĩa thức ăn cho người tiểu đường type 2 là gì?",
        "condition_code": "diabetes_type_2",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Chia đĩa ăn 23cm thành: 1/2 đĩa rau không tinh bột, 1/4 đĩa đạm nạc, và 1/4 đĩa carbohydrate phức hợp.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_t2_003",
        "review_flags": "",
        "review_notes": ""
    },

    # --- Diabetes Type Unknown ---
    {
        "eval_id": "eval_0006",
        "query": "Tôi bị tiểu đường nhưng chưa rõ type nào, tôi nên ăn uống ra sao?",
        "condition_code": "diabetes_type_unknown",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Nên ăn uống lành mạnh tổng quát (nhiều rau, giảm đường ngọt); liên hệ bác sĩ để xác nhận rõ type bệnh để có hướng dẫn chi tiết.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "diabetes_unknown_001;diabetes_unknown_002;diabetes_unknown_003",
        "review_flags": "",
        "review_notes": ""
    },

    # --- Prediabetes ---
    {
        "eval_id": "eval_0007",
        "query": "Tiền tiểu đường có cần kiêng hoàn toàn cơm không?",
        "condition_code": "prediabetes",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Không cần kiêng hoàn toàn tinh bột; nên kiểm soát giảm bớt khẩu phần cơm trắng và tăng rau xanh để tránh tăng đường huyết đột ngột.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "prediabetes_002;prediabetes_008",
        "review_flags": "",
        "review_notes": "Answers the previously orphaned eval_0011 query"
    },
    {
        "eval_id": "eval_0008",
        "query": "Mục tiêu giảm cân cho người tiền tiểu đường là bao nhiêu?",
        "condition_code": "prediabetes",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Mục tiêu giảm 5% đến 7% trọng lượng cơ thể ban đầu để giảm hơn một nửa nguy cơ tiến triển thành đái tháo đường type 2.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "prediabetes_004",
        "review_flags": "",
        "review_notes": ""
    },

    # --- Hypertension ---
    {
        "eval_id": "eval_0009",
        "query": "Hiệp hội Tim mạch Hoa Kỳ khuyên giới hạn natri bao nhiêu một ngày cho người tăng huyết áp?",
        "condition_code": "hypertension",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Nên hướng tới giới hạn natri dưới 1500 mg mỗi ngày.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "hypertension_001",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0010",
        "query": "Người cao huyết áp có nên dùng nhiều nước mắm không?",
        "condition_code": "hypertension",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Nên hạn chế nước mắm vì 1 muỗng canh chứa tới 1000mg natri (66% giới hạn ngày); khuyên dùng muối giảm natri hoặc gia vị thảo mộc.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "hypertension_002",
        "review_flags": "",
        "review_notes": ""
    },

    # --- CKD Stage G1 & G2 ---
    {
        "eval_id": "eval_0011",
        "query": "Có phải cứ eGFR trên 90 là bị suy thận giai đoạn G1 không?",
        "condition_code": "ckd_g1",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Không thể chẩn đoán chỉ bằng eGFR >= 90; bắt buộc phải có dấu hiệu tổn thương thận đi kèm như albumin niệu kéo dài trên 3 tháng.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g1_002",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0012",
        "query": "Bệnh thận mạn giai đoạn G2 cần chú ý gì về thuốc giảm đau?",
        "condition_code": "ckd_g2",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Tránh dùng các loại thuốc kháng viêm giảm đau NSAID (ibuprofen, naproxen) vì có thể làm suy giảm nhanh chức năng thận tổn thương.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g2_005",
        "review_flags": "",
        "review_notes": ""
    },

    # --- CKD Stage G3a & G3b ---
    {
        "eval_id": "eval_0025",
        "query": "Tôi bị suy thận giai đoạn G3a, tôi có cần ăn kiêng đạm hay kiêng kali nghiêm ngặt không?",
        "condition_code": "ckd_g3a",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Khuyên dùng lượng đạm vừa phải khoảng 0.6 đến 0.8 gam trên mỗi kg cân nặng mỗi ngày; không kiêng kali rập khuôn mà nên dựa vào kết quả xét nghiệm máu.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g3a_002;ckd_g3a_004",
        "review_flags": "",
        "review_notes": "Added during QA audit to ensure 100% condition code coverage"
    },
    {
        "eval_id": "eval_0013",
        "query": "Chế độ ăn cho người bệnh thận mạn giai đoạn G3b cần lượng protein là bao nhiêu?",
        "condition_code": "ckd_g3b",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Khuyên dùng lượng đạm vừa phải khoảng 0.6 đến 0.8 gam trên mỗi kg cân nặng mỗi ngày để tránh sản sinh chất thải nitơ dư thừa.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g3b_002",
        "review_flags": "",
        "review_notes": ""
    },

    # --- CKD Stage G4 & G5 Non-Dialysis ---
    {
        "eval_id": "eval_0014",
        "query": "Người bị suy thận giai đoạn G4 cần kiêng protein thế nào?",
        "condition_code": "ckd_g4",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Hạn chế đạm nghiêm ngặt xuống còn 0.6g/kg/ngày để giảm tải ure trong máu, trì hoãn lọc máu.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g4_002",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0015",
        "query": "Cách uống nước cho người suy thận giai đoạn G5 chưa lọc máu là gì?",
        "condition_code": "ckd_g5_non_dialysis",
        "expected_chunk_type": "lifestyle",
        "expected_answer_points": "Lượng nước uống bằng lượng nước tiểu ngày hôm trước cộng thêm 500 mL.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_g5_nondialysis_006",
        "review_flags": "",
        "review_notes": ""
    },

    # --- CKD Dialysis ---
    {
        "eval_id": "eval_0016",
        "query": "Tôi đang chạy thận nhân tạo, tôi có cần kiêng protein như trước không?",
        "condition_code": "ckd_dialysis",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Không kiêng đạm nữa mà ngược lại cần tăng cường ăn đạm (1.0-1.2g/kg/ngày) để bù đắp acid amin mất trong lọc máu.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_dialysis_002",
        "review_flags": "",
        "review_notes": ""
    },

    # --- CKD Stage Unknown ---
    {
        "eval_id": "eval_0017",
        "query": "Tôi bị suy thận nhưng không rõ giai đoạn mấy, tôi nên kiêng kali hay uống nước thế nào?",
        "condition_code": "ckd_stage_unknown",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Không nên tự ý kiêng kali hay hạn chế nước uống khi chưa rõ giai đoạn; hãy cung cấp eGFR và xin tư vấn của chuyên gia thận học.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "ckd_unknown_002;ckd_unknown_003;ckd_unknown_004",
        "review_flags": "",
        "review_notes": ""
    },

    # --- Gout & Hyperuricemia ---
    {
        "eval_id": "eval_0018",
        "query": "Axit uric máu của tôi cao nhưng chân tôi chưa sưng đau lần nào, tôi có bị bệnh gout không?",
        "condition_code": "gout",
        "expected_chunk_type": "explanation",
        "expected_answer_points": "Chưa được coi là bệnh gout mà chỉ là tăng acid uric máu không triệu chứng. Bệnh gout chỉ chẩn đoán khi có viêm khớp cấp.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "gout_001",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0019",
        "query": "Người bị bệnh gout cần tránh ăn thực phẩm gì?",
        "condition_code": "gout",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Tránh tuyệt đối nội tạng động vật; hạn chế thịt đỏ, hải sản béo, rượu bia và nước ngọt chứa đường fructose cao.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "gout_003;gout_004;gout_005;gout_006;gout_007",
        "review_flags": "",
        "review_notes": ""
    },

    # --- Obesity ---
    {
        "eval_id": "eval_0020",
        "query": "Người lớn tuổi bị béo phì khi giảm cân cần chú ý gì?",
        "condition_code": "obesity",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Tránh mất cơ xương gây suy yếu (frailty); tập trung vào đạm chất lượng cao kết hợp kháng lực nhẹ dưới giám sát y khoa.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "obesity_007",
        "review_flags": "",
        "review_notes": ""
    },

    # --- General Safety / Medication & Diagnosis & Emergencies ---
    {
        "eval_id": "eval_0021",
        "query": "Ứng dụng này có thể giúp tôi chẩn đoán bệnh tiểu đường và kê đơn thuốc không?",
        "condition_code": "general_safety",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Ứng dụng chỉ cung cấp thông tin tham khảo giáo dục, không chẩn đoán bệnh và không tự ý điều chỉnh hay ngưng đơn thuốc của bác sĩ.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_001;safety_002",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0022",
        "query": "Tôi bị đau ngực đột ngột kèm khó thở dữ dội, tôi có nên ăn gì hay làm gì không?",
        "condition_code": "general_safety",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Đây là dấu hiệu khẩn cấp về tim mạch; ngừng mọi vận động, nghỉ ngơi tư thế thoải mái và gọi cấp cứu y tế 115 lập tức.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_004",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0023",
        "query": "Nếu người nhà bị tiểu đường đột ngột ngất xỉu bất tỉnh, tôi nên xử lý thế nào?",
        "condition_code": "general_safety",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Đây là tình trạng cấp cứu khẩn cấp. Nằm ngửa, nâng chân cao, nới lỏng quần áo và gọi 115 ngay lập tức. Tuyệt đối không đút thức ăn hay nước đường vào miệng.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_003;safety_005",
        "review_flags": "",
        "review_notes": ""
    },
    {
        "eval_id": "eval_0024",
        "query": "Bà bầu vừa bị tiểu đường vừa có sỏi thận thì nên ăn kiêng theo quy tắc nào trên app?",
        "condition_code": "general_safety",
        "expected_chunk_type": "warning",
        "expected_answer_points": "Phụ nữ mang thai hoặc người mắc nhiều bệnh đồng thời phức tạp không được áp dụng các khuyến nghị tự động mà phải tuân theo hướng dẫn trực tiếp từ bác sĩ chuyên khoa.",
        "language": "vi",
        "review_status": "approved",
        "supporting_chunk_ids": "safety_007",
        "review_flags": "",
        "review_notes": ""
    }
]

def build_eval_set():
    headers = [
        "eval_id", "query", "condition_code", "expected_chunk_type",
        "expected_answer_points", "language", "review_status",
        "supporting_chunk_ids", "review_flags", "review_notes"
    ]
    with open(eval_v2_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for ev in eval_data:
            writer.writerow([
                ev["eval_id"],
                ev["query"],
                ev["condition_code"],
                ev["expected_chunk_type"],
                ev["expected_answer_points"],
                ev["language"],
                ev["review_status"],
                ev["supporting_chunk_ids"],
                ev["review_flags"],
                ev["review_notes"]
            ])
    print(f"Created rag_eval_set_v2.csv with {len(eval_data)} questions.")

if __name__ == "__main__":
    build_eval_set()
