import csv
from django.core.management.base import BaseCommand
from prediction.models import CardioRecord


def to_int(v):
    if v is None:
        return None
    v = str(v).strip()
    if v == "":
        return None
    return int(float(v))


def to_float(v):
    if v is None:
        return None
    v = str(v).strip().replace(",", ".")
    if v == "":
        return None
    return float(v)


class Command(BaseCommand):
    help = "Import large cardio CSV into CardioRecord"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)
        parser.add_argument("--batch", type=int, default=4000)

    def handle(self, *args, **options):
        path = options["csv_path"]
        batch_size = options["batch"]

        buffer = []
        total = 0

        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                obj = CardioRecord(
                    id=to_int(row["id"]),
                    age=to_int(row["age"]),
                    gender=to_int(row["gender"]),
                    height=to_int(row["height"]),
                    weight=to_float(row["weight"]),
                    ap_hi=to_int(row["ap_hi"]),
                    ap_lo=to_int(row["ap_lo"]),
                    cholesterol=to_int(row["cholesterol"]),
                    gluc=to_int(row["gluc"]),
                    smoke=to_int(row["smoke"]),
                    alco=to_int(row["alco"]),
                    active=to_int(row["active"]),
                    cardio=to_int(row["cardio"]),
                    age_years=to_float(row["age_years"]),
                    bmi=to_float(row["bmi"]),
                    bp_category=row["bp_category"],
                    bp_category_encoded=row["bp_category_encoded"],
                )

                buffer.append(obj)
                total += 1

                if len(buffer) >= batch_size:
                    CardioRecord.objects.bulk_create(buffer, ignore_conflicts=True)
                    buffer.clear()
                    self.stdout.write(f"Imported {total} rows...")

            if buffer:
                CardioRecord.objects.bulk_create(buffer, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"Done ✅ Imported {total} rows"))
