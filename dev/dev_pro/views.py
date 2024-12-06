from asyncio import current_task
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *

@api_view(['POST'])

def add_patient(request):
    # current_user = request.user
    patient_email=Patientsdetails.objects.filter(patient_email=request.data.get('patient_email'))
    if request.method == 'POST':
        if patient_email.exists():
            return JsonResponse({"status": "patient_already_exists"})
        serializer = PatientsdetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "patient_added_successfully"})

        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_patients(request):
    ids_to_delete = request.data.get('ids', [])  # Expects a list of ids to delete
    if not ids_to_delete:
        return JsonResponse({"status": "No_IDs_provided"}, status=status.HTTP_400_BAD_REQUEST)
    patients = Patientsdetails.objects.filter(id__in=ids_to_delete)

    if patients.exists():
        patients.delete()
        return JsonResponse({"status": "Patients_deleted_successfully"}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({"status": "No_patients_found_with_the_provided_IDs"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def patient_report_file(request):
    reports = Patientreports.objects.filter(patient_details_id=request.query_params.get("patient_id"))
    if reports.exists():
        serializer = PatientreportsSerializer(reports, many=True)
        return JsonResponse(
            {"status": "Patient_report_file_retrieved_successfully", "patient_reports": serializer.data},
            status=status.HTTP_200_OK  # Correct usage of status code
        )
    else:
        return JsonResponse(
            {"status": "No_reports_found_for_this_patient."},
            status=status.HTTP_404_NOT_FOUND  # Correct usage of status code
        )
@api_view(['POST'])
def patient_save_report(request):
    if request.method == 'POST':
        serializer = Patient_save_report(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status':'successfully_added_Patient_report'})
        else:
            return JsonResponse({'status':'please_add_valid_id_or_valid_Report'})







