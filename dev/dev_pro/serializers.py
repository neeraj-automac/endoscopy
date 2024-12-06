# from django.contrib.gis.serializers.geojson import Serializer
from rest_framework import serializers
from .models import Patientreports,Patientsdetails

from rest_framework import serializers
from .models import Patientsdetails

class PatientsdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patientsdetails
        fields = '__all__'

class PatientreportsSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient_details_id.patient_name')
    class Meta:
        model = Patientreports
        fields = ['id', 'patient_name', 'report_file', 'date', 'time']


class Patient_save_report(serializers.ModelSerializer):
    class Meta:
        model = Patientreports
        fields = '__all__'


