import csv
from pathlib import Path
from django.core.management.base import BaseCommand

from healthplanapp.models import Food

class Command(BaseCommand):
    help = "Xuất tên Food nguồn USDA để làm sạch tiếng Việt"

    def add_arguments(self, parser):
        parser.add_argument("output_path", type=str)

    def handle(self, *args, **options):
        output_path = Path(options["output_path"]).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        foods = Food.objects.exclude(source_name="VTN_FCT_2007").order_by("food_id").values("food_id", "source_name", "name_en", "name_vi")

        with output_path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["food_id", "source_name", "name_en", "current_name_vi"])
            writer.writeheader()

            for food in foods.iterator():
                writer.writerow({"food_id": food["food_id"], "source_name": food["source_name"], "name_en": food["name_en"], "current_name_vi": food["name_vi"]})

        self.stdout.write(f"Đã xuất {foods.count()} Food cần làm sạch")
        self.stdout.write(f"File: {output_path}")