from django.shortcuts import render, redirect
from django.db.models import Q, Max
import random

from .models import Patient, DiagnosisRecord, CardioRecord


def home(request):
    return render(request, 'prediction/home.html')


def register_patient(request):
    if request.method != 'POST':
        return redirect('home')

    patient = Patient.objects.create(
        name=request.POST.get('name'),
        age=int(request.POST.get('age')),
        phone=request.POST.get('phone'),
        email=request.POST.get('email')
    )
    return redirect('diagnosis_form', patient_id=patient.id)


def diagnosis_form(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'prediction/diagnosis.html', {'patient': patient})


def predict(request):
    if request.method != 'POST':
        return redirect('home')

    patient = Patient.objects.get(id=request.POST.get('patient_id'))

    age = int(request.POST.get('age'))
    gender = int(request.POST.get('gender'))
    height = int(request.POST.get('height'))
    weight = float(request.POST.get('weight'))
    ap_hi = int(request.POST.get('ap_hi'))
    ap_lo = int(request.POST.get('ap_lo'))
    cholesterol = int(request.POST.get('cholesterol'))
    gluc = int(request.POST.get('gluc'))
    smoke = int(request.POST.get('smoke'))
    alco = int(request.POST.get('alco'))
    active = int(request.POST.get('active'))

    bp_category = (request.POST.get('bp_category') or '').strip() or None
    bp_category_encoded = (request.POST.get('bp_category_encoded') or '').strip() or None

    age_years = float(age)
    bmi = round(weight / ((height / 100) ** 2), 2) if height else None

    symptoms_data = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "ap_hi": ap_hi,
        "ap_lo": ap_lo,
        "cholesterol": cholesterol,
        "gluc": gluc,
        "smoke": smoke,
        "alco": alco,
        "active": active,
        "age_years": age_years,
        "bmi": bmi,
        "bp_category": bp_category,
        "bp_category_encoded": bp_category_encoded,
    }

    # تحليل القلب
    confidence = random.random()
    result = "Positive (Sick)" if confidence > 0.5 else "Negative (Healthy)"

    # تحليل السكري
    if gluc >= 3:
        diabetes_probability = 85
        diabetes_result = "positive"
    elif gluc == 2:
        diabetes_probability = 60
        diabetes_result = "positive"
    else:
        diabetes_probability = 15
        diabetes_result = "negative"

    # تحليل ضغط الدم
    if ap_hi >= 140 or ap_lo >= 90:
        pressure_probability = 85
        pressure_result = "positive"
    elif ap_hi >= 130 or ap_lo >= 80:
        pressure_probability = 60
        pressure_result = "positive"
    else:
        pressure_probability = 15
        pressure_result = "negative"

    # نتيجة القلب للواجهة
    heart_probability = round(confidence * 100, 2)
    heart_result = "positive" if result == "Positive (Sick)" else "negative"

    next_id = (CardioRecord.objects.aggregate(m=Max("id"))["m"] or 0) + 1

    cardio = CardioRecord(
        id=next_id,
        age=age,
        gender=gender,
        height=height,
        weight=weight,
        ap_hi=ap_hi,
        ap_lo=ap_lo,
        cholesterol=cholesterol,
        gluc=gluc,
        smoke=smoke,
        alco=alco,
        active=active,
        cardio=1 if result == "Positive (Sick)" else 0,
        age_years=age_years,
        bmi=bmi,
        bp_category=bp_category,
        bp_category_encoded=bp_category_encoded,
    )
    cardio.save()

    DiagnosisRecord.objects.create(
        patient=patient,
        cardio_record_id=cardio.id,
        symptoms_data=symptoms_data,
        prediction_result=result,
        confidence_score=confidence
    )

    return render(request, 'prediction/result.html', {
        "patient": patient,
        "result": result,
        "probability": heart_probability,
        "heart_result": heart_result,
        "heart_probability": heart_probability,
        "diabetes_result": diabetes_result,
        "diabetes_probability": diabetes_probability,
        "pressure_result": pressure_result,
        "pressure_probability": pressure_probability,
    })


def reports(request):
    records = DiagnosisRecord.objects.select_related('patient', 'cardio_record').order_by('-date')

    q = (request.GET.get('q') or '').strip()
    if q:
        records = records.filter(
            Q(patient__name__icontains=q) |
            Q(prediction_result__icontains=q) |
            Q(cardio_record__id__icontains=q)
        )

    all_records = DiagnosisRecord.objects.select_related('cardio_record')

    total_records = all_records.count()

    heart_cases = all_records.filter(prediction_result="Positive (Sick)").count()

    diabetes_cases = all_records.filter(cardio_record__gluc__gte=2).count()

    pressure_cases = all_records.filter(
        Q(cardio_record__bp_category__icontains="Hypertension") |
        Q(cardio_record__ap_hi__gte=140) |
        Q(cardio_record__ap_lo__gte=90)
    ).count()

    heart_percent = round((heart_cases / total_records) * 100, 2) if total_records > 0 else 0
    diabetes_percent = round((diabetes_cases / total_records) * 100, 2) if total_records > 0 else 0
    pressure_percent = round((pressure_cases / total_records) * 100, 2) if total_records > 0 else 0

    return render(request, 'prediction/reports.html', {
        'records': records,
        'search_term': q,
        'total_records': total_records,
        'heart_cases': heart_cases,
        'diabetes_cases': diabetes_cases,
        'pressure_cases': pressure_cases,
        'heart_percent': heart_percent,
        'diabetes_percent': diabetes_percent,
        'pressure_percent': pressure_percent,
    })