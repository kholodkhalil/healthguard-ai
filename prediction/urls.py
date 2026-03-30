from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # تسجيل المريض
    path('register/', views.register_patient, name='register_patient'),

    # صفحة إدخال بيانات الفحص
    path('diagnosis/<int:patient_id>/', views.diagnosis_form, name='diagnosis_form'),

    # تنفيذ التنبؤ
    path('predict/', views.predict, name='predict'),

    # صفحة السجلات + التقرير الإحصائي
    path('reports/', views.reports, name='reports'),

    # التقرير الشهري لمرضى القلب
    path('heart-report/', views.heart_monthly_report, name='heart_report'),
]
