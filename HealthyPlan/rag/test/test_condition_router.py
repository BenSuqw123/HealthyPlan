from condition_router import route_condition


TEST_CASES = [
    {
        "query": "Người bị gout nên hạn chế thực phẩm nào?",
        "expected_condition": "gout",
    },
    {
        "query": "Tôi bị đái tháo đường tuýp 1 thì cần đếm carb như thế nào?",
        "expected_condition": "diabetes_type_1",
    },
    {
        "query": "Người tiểu đường type 2 nên tập thể dục bao nhiêu phút mỗi tuần?",
        "expected_condition": "diabetes_type_2",
    },
    {
        "query": "Tôi bị tiểu đường nhưng chưa biết là type nào thì nên ăn uống ra sao?",
        "expected_condition": "diabetes_type_unknown",
    },
    {
        "query": "Tôi đang ở giai đoạn tiền tiểu đường thì nên thay đổi chế độ ăn như thế nào?",
        "expected_condition": "prediabetes",
    },
    {
        "query": "Người cao huyết áp nên hạn chế lượng muối bao nhiêu mỗi ngày?",
        "expected_condition": "hypertension",
    },
    {
        "query": "Tôi bị béo phì thì nên giảm cân an toàn như thế nào?",
        "expected_condition": "obesity",
    },
    {
        "query": "eGFR của tôi từ 45 đến 59 và được chẩn đoán CKD G3a thì nên ăn gì?",
        "expected_condition": "ckd_g3a",
    },
    {
        "query": "Tôi đang chạy thận nhân tạo thì cần hạn chế nước như thế nào?",
        "expected_condition": "ckd_dialysis",
    },
    {
        "query": "Tôi bị bệnh thận mạn nhưng chưa biết đang ở giai đoạn nào.",
        "expected_condition": "ckd_stage_unknown",
    },
    {
        "query": "Ứng dụng có thể tự điều chỉnh liều thuốc cho tôi không?",
        "expected_condition": "general_safety",
    },
]


def print_router_results(result):
    print(f"Status: {result['status']}")
    print(f"Condition: {result['condition_code']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Score gap: {result['score_gap']:.4f}")

    print("Nearest examples:")

    for index, router_result in enumerate(result["router_results"], start=1):
        condition_code = router_result["condition_code"]
        similarity = router_result["similarity"]
        matched_query = router_result["query"]

        print(f"  {index}. [{condition_code}] {similarity:.4f}")
        print(f"     {matched_query}")


def run_test_case(test_case):
    query = test_case["query"]
    expected_condition = test_case["expected_condition"]

    print("\n" + "=" * 80)
    print(f"Query: {query}")
    print(f"Expected condition: {expected_condition}")

    result = route_condition(query)

    print_router_results(result)

    detected_condition = result["condition_code"]

    if result["status"] != "detected":
        print("Result: FAIL")
        print(f"Reason: Router status is {result['status']}")
        return False

    if detected_condition != expected_condition:
        print("Result: FAIL")
        print(f"Reason: Expected {expected_condition}, detected {detected_condition}")
        return False

    print("Result: PASS")
    return True


def main():
    passed_count = 0
    failed_count = 0

    for test_case in TEST_CASES:
        test_passed = run_test_case(test_case)

        if test_passed:
            passed_count += 1
        else:
            failed_count += 1

    total_count = len(TEST_CASES)

    print("\n" + "=" * 80)
    print("CONDITION ROUTER TEST SUMMARY")
    print(f"Total tests: {total_count}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")

    if failed_count == 0:
        print("Validation: PASS")
    else:
        print("Validation: FAIL")

    print("=" * 80)


if __name__ == "__main__":
    main()