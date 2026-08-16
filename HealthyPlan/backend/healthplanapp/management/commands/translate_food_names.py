import csv
import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from langchain_ollama import ChatOllama

class Command(BaseCommand):
    help = "Dịch tên Food tiếng Anh sang tiếng Việt theo batch"

    def add_arguments(self, parser):
        parser.add_argument("input_path", type=str)
        parser.add_argument("output_path", type=str)
        parser.add_argument("--batch-size", type=int, default=10)
        parser.add_argument("--limit", type=int, default=None)
        parser.add_argument("--base-url", type=str, default="http://127.0.0.1:11434")
        parser.add_argument("--model", type=str, required=True)

    def handle(self, *args, **options):
        input_path = Path(options["input_path"]).resolve()
        output_path = Path(options["output_path"]).resolve()
        batch_size = options["batch_size"]
        limit = options["limit"]
        base_url = options["base_url"]
        model_name = options["model"]

        if not input_path.exists():
            raise CommandError(f"Không tìm thấy file: {input_path}")

        if batch_size <= 0:
            raise CommandError("Batch size phải lớn hơn 0.")

        if limit is not None and limit <= 0:
            raise CommandError("Limit phải lớn hơn 0.")

        with input_path.open("r", encoding="utf-8-sig", newline="") as file:
            foods = list(csv.DictReader(file))

        translated_food_ids = set()
        has_output = output_path.exists() and output_path.stat().st_size > 0

        if has_output:
            with output_path.open("r", encoding="utf-8-sig", newline="") as file:
                translated_food_ids = {row["food_id"] for row in csv.DictReader(file) if row.get("food_id")}

        pending_foods = [food for food in foods if food["food_id"] not in translated_food_ids]

        if limit is not None:
            pending_foods = pending_foods[:limit]

        if not pending_foods:
            self.stdout.write("Không còn Food nào cần dịch.")

            return

        model = ChatOllama(base_url=base_url, model=model_name, temperature=0, format="json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("a", encoding="utf-8" if has_output else "utf-8-sig", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=["food_id", "source_name", "name_en", "name_vi"])

            if not has_output:
                writer.writeheader()

            for start in range(0, len(pending_foods), batch_size):
                batch = pending_foods[start:start + batch_size]
                translations = self.translate_batch(model, batch)

                for food in batch:
                    writer.writerow({"food_id": food["food_id"], "source_name": food["source_name"], "name_en": food["name_en"], "name_vi": translations[food["food_id"]]})

                output_file.flush()
                completed = min(start + batch_size, len(pending_foods))
                self.stdout.write(f"Đã dịch {completed}/{len(pending_foods)} Food")

        self.stdout.write(f"File kết quả: {output_path}")

    def translate_batch(self, model, batch):
        input_data = [{"food_id": food["food_id"], "name_en": food["name_en"]} for food in batch]
        prompt = f"""
Bạn là biên dịch viên chuyên về tên thực phẩm Anh - Việt.

Hãy dịch trường name_en sang tiếng Việt tự nhiên và chính xác.

Yêu cầu:
- Giữ nguyên food_id.
- Dịch đầy đủ tên thực phẩm, bộ phận, trạng thái, cách chế biến và điều kiện có hoặc không có muối.
- Không rút gọn làm mất thông tin.
- Không thêm thông tin không có trong tên tiếng Anh.
- Giữ nguyên tên thương hiệu, giống cây, địa danh và tên riêng khi cần thiết.
- Không để sót các từ mô tả thông dụng bằng tiếng Anh như cooked, raw, without salt, flour, beef, pork, roasted.
- Chỉ trả về JSON, không giải thích và không dùng Markdown.
- JSON phải có đúng cấu trúc:
{{"translations": [{{"food_id": "FOOD000001", "name_vi": "Tên tiếng Việt"}}]}}

Ví dụ:
Garlic, raw → Tỏi, sống
Flour, soy, defatted → Bột đậu nành đã khử béo
Flour, rice, brown → Bột gạo lứt
Squash, winter, cooked, baked, without salt → Bí mùa đông, đã nấu chín, nướng, không thêm muối

Dữ liệu:
{json.dumps(input_data, ensure_ascii=False)}
"""
        last_error = None

        for attempt in range(3):
            try:
                response = model.invoke(prompt)
                result = json.loads(response.content)
                translations = result.get("translations", [])
                translation_map = {item["food_id"]: str(item["name_vi"]).strip() for item in translations}
                expected_food_ids = {food["food_id"] for food in batch}

                if set(translation_map) != expected_food_ids:
                    raise ValueError("Danh sách food_id trả về không khớp batch.")

                if any(not name_vi for name_vi in translation_map.values()):
                    raise ValueError("Có name_vi rỗng.")

                return translation_map
            except Exception as error:
                last_error = error
                self.stdout.write(f"Batch lỗi, thử lại {attempt + 1}/3: {error}")

        raise CommandError(f"Không thể dịch batch sau 3 lần: {last_error}")
        