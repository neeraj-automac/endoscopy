from rest_framework import serializers
from .models import Patientreports,Patientsdetails

class DetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Patientreports
        fields = '__all__'


class ReportSerializers(serializers.ModelSerializer):
    class Meta:
        model = Patientsdetails
        fields = '__all__'



