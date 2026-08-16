import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from healthplanapp.models import HealthConditionNutrientRule


SUPPORTED_EVALUATION_FIELDS = {"kcal_per_100g", "protein_g", "fat_g", "carb_g", "fiber_g", "sodium_mg", "potassium_mg", "saturated_fat_g", "processing_level"}


class Command(BaseCommand):
    help = "Import luật dinh dưỡng theo bệnh lý từ CSV"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def parse_threshold(self, value, row_number):
        value = (value or "").strip()

        if not value:
            return None

        try:
            threshold = Decimal(value)
        except InvalidOperation as error:
            raise CommandError(f"Dòng {row_number}: threshold_value phải là số hợp lệ") from error

        if threshold < 0:
            raise CommandError(f"Dòng {row_number}: threshold_value không được là số âm")

        return threshold

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])

        if not csv_path.is_file():
            raise CommandError(f"Không tìm thấy file CSV: {csv_path}")

        required_columns = ["rule_id", "condition_code", "evaluation_field", "rule_type", "priority", "threshold_value", "threshold_unit", "applies_when", "recommendation_vi", "clinical_caution_vi", "source_name", "source_url"]
        required_text_columns = ["rule_id", "condition_code", "evaluation_field", "rule_type", "priority", "threshold_unit", "applies_when", "recommendation_vi", "source_name", "source_url"]
        created_count = 0
        updated_count = 0
        skipped_count = 0

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

                    evaluation_field = row["evaluation_field"].strip()

                    if evaluation_field not in SUPPORTED_EVALUATION_FIELDS:
                        skipped_count += 1
                        continue

                    for column in required_text_columns:
                        if not (row[column] or "").strip():
                            raise CommandError(f"Dòng {row_number}: {column} không được để trống")

                    rule_type = row["rule_type"].strip()
                    priority = row["priority"].strip()

                    if rule_type not in HealthConditionNutrientRule.RuleType.values:
                        raise CommandError(f"Dòng {row_number}: rule_type không hợp lệ")

                    if priority not in HealthConditionNutrientRule.Priority.values:
                        raise CommandError(f"Dòng {row_number}: priority không hợp lệ")

                    rule_data = {}
                    rule_data["condition_code"] = row["condition_code"].strip()
                    rule_data["evaluation_field"] = evaluation_field
                    rule_data["rule_type"] = rule_type
                    rule_data["priority"] = priority
                    rule_data["threshold_value"] = self.parse_threshold(row["threshold_value"], row_number)
                    rule_data["threshold_unit"] = row["threshold_unit"].strip()
                    rule_data["applies_when"] = row["applies_when"].strip()
                    rule_data["recommendation_vi"] = row["recommendation_vi"].strip()
                    rule_data["clinical_caution_vi"] = (row["clinical_caution_vi"] or "").strip()
                    rule_data["source_name"] = row["source_name"].strip()
                    rule_data["source_url"] = row["source_url"].strip()

                    rule, created = HealthConditionNutrientRule.objects.update_or_create(rule_id=row["rule_id"].strip(), defaults=rule_data)

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Import hoàn tất: tạo mới {created_count}, cập nhật {updated_count}, bỏ qua {skipped_count}"))