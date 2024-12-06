from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('add-patient/', add_patient, name='add_patient'),  # Update to match with hyphen
    path('delete_patients/multiple-delete/',delete_patients, name='delete_patients'),
    path('patient_report_file/',patient_report_file,name='patient_report_file'),
    path('patient_save_report/',patient_save_report,name='patient_save_report'),
]