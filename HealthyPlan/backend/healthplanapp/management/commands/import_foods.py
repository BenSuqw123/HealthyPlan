import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from healthplanapp.models import Food


class Command(BaseCommand):
    help = "Import dữ liệu thực phẩm từ CSV"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def parse_decimal(self, value, column, row_number, required=False):
        value = (value or "").strip()

        if not value:
            if required:
                raise CommandError(f"Dòng {row_number}: {column} không được để trống")
            return None

        try:
            number = Decimal(value)
        except InvalidOperation as error:
            raise CommandError(f"Dòng {row_number}: {column} phải là số hợp lệ") from error

        if number < 0:
            raise CommandError(f"Dòng {row_number}: {column} không được là số âm")

        return number

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])

        if not csv_path.is_file():
            raise CommandError(f"Không tìm thấy file CSV: {csv_path}")

        required_columns = ["food_id", "source_name", "name_vi", "name_en", "category_vi", "category_en", "item_type", "processing_level", "kcal_per_100g", "protein_g", "fat_g", "carb_g", "fiber_g", "sodium_mg", "potassium_mg", "saturated_fat_g"]
        required_text_columns = ["food_id", "source_name", "name_vi", "category_vi", "category_en", "item_type", "processing_level"]
        created_count = 0
        updated_count = 0

        with transaction.atomic():
            with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
                reader = csv.DictReader(file)
                columns = reader.fieldnames or []
                missing_columns = [column for column in required_columns if column not in columns]

                if missing_columns:
                    raise CommandError(f"CSV thiếu các cột: {', '.join(missing_columns)}")

                for row_number, row in enumerate(reader, start=2):
                    if not any((value or "").strip() for value in row.values()):
                        continue

                    for column in required_text_columns:
                        if not (row[column] or "").strip():
                            raise CommandError(f"Dòng {row_number}: {column} không được để trống")

                    item_type = row["item_type"].strip()
                    processing_level = row["processing_level"].strip()

                    if item_type not in Food.ItemType.values:
                        raise CommandError(f"Dòng {row_number}: item_type không hợp lệ")

                    if processing_level not in Food.ProcessingLevel.values:
                        raise CommandError(f"Dòng {row_number}: processing_level không hợp lệ")

                    food_data = {}
                    food_data["source_name"] = row["source_name"].strip()
                    food_data["name_vi"] = row["name_vi"].strip()
                    food_data["name_en"] = (row["name_en"] or "").strip()
                    food_data["category_vi"] = row["category_vi"].strip()
                    food_data["category_en"] = row["category_en"].strip()
                    food_data["item_type"] = item_type
                    food_data["processing_level"] = processing_level
                    food_data["kcal_per_100g"] = self.parse_decimal(row["kcal_per_100g"], "kcal_per_100g", row_number, required=True)
                    food_data["protein_g"] = self.parse_decimal(row["protein_g"], "protein_g", row_number, required=True)
                    food_data["fat_g"] = self.parse_decimal(row["fat_g"], "fat_g", row_number, required=True)
                    food_data["carb_g"] = self.parse_decimal(row["carb_g"], "carb_g", row_number, required=True)
                    food_data["fiber_g"] = self.parse_decimal(row["fiber_g"], "fiber_g", row_number)
                    food_data["sodium_mg"] = self.parse_decimal(row["sodium_mg"], "sodium_mg", row_number)
                    food_data["potassium_mg"] = self.parse_decimal(row["potassium_mg"], "potassium_mg", row_number)
                    food_data["saturated_fat_g"] = self.parse_decimal(row["saturated_fat_g"], "saturated_fat_g", row_number)

                    food, created = Food.objects.update_or_create(food_id=row["food_id"].strip(), defaults=food_data)

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Import hoàn tất: tạo mới {created_count}, cập nhật {updated_count}"))