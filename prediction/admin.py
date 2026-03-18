from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Patient, DiagnosisRecord, CardioRecord


class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient
        fields = ("id", "name", "age", "email", "phone", "created_at")


@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    resource_class = PatientResource
    list_display = ("id", "name", "age", "email", "phone", "created_at")
    search_fields = ("name", "phone", "email")


class DiagnosisRecordResource(resources.ModelResource):
    class Meta:
        model = DiagnosisRecord
        fields = ("id", "patient", "cardio_record", "symptoms_data", "prediction_result", "confidence_score", "date")


@admin.register(DiagnosisRecord)
class DiagnosisRecordAdmin(ImportExportModelAdmin):
    resource_class = DiagnosisRecordResource
    list_display = ("id", "patient", "cardio_record", "prediction_result", "confidence_score", "date")
    search_fields = ("patient__name", "patient__phone", "prediction_result", "cardio_record__id")


class CardioRecordResource(resources.ModelResource):
    class Meta:
        model = CardioRecord
        fields = (
            "id", "age", "gender", "height", "weight",
            "ap_hi", "ap_lo", "cholesterol", "gluc",
            "smoke", "alco", "active", "cardio",
            "age_years", "bmi", "bp_category", "bp_category_encoded",
            "created_at",
        )
        skip_unchanged = True
        report_skipped = False
        use_bulk = True
        batch_size = 1000


@admin.register(CardioRecord)
class CardioRecordAdmin(ImportExportModelAdmin):
    resource_class = CardioRecordResource
    list_display = ("id", "age", "gender", "height", "weight", "ap_hi", "ap_lo", "cardio")
    search_fields = ("id",)
    list_filter = ("cardio", "gender", "cholesterol", "gluc")
