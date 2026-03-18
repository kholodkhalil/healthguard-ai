from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DiagnosisRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)

    cardio_record = models.ForeignKey(
        "CardioRecord",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    symptoms_data = models.JSONField()
    prediction_result = models.CharField(max_length=50)
    confidence_score = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.cardio_record_id:
            return f"Cardio #{self.cardio_record_id} - {self.prediction_result}"
        if self.patient_id:
            return f"{self.patient} - {self.prediction_result}"
        return f"Diagnosis - {self.prediction_result}"


class CardioRecord(models.Model):
    id = models.IntegerField(primary_key=True)

    age = models.IntegerField()
    gender = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()

    ap_hi = models.IntegerField()
    ap_lo = models.IntegerField()

    cholesterol = models.IntegerField()
    gluc = models.IntegerField()
    smoke = models.IntegerField()
    alco = models.IntegerField()
    active = models.IntegerField()

    cardio = models.IntegerField()

    age_years = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)

    bp_category = models.CharField(max_length=50, null=True, blank=True)

    # ✅ مطابق للملف عندك: نص مثل "Hypertension Stage 1"
    bp_category_encoded = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CardioRecord {self.id} (cardio={self.cardio})"
