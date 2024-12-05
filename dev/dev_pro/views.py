from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import random
from .serializers import LoginSerializer, ReportSerializers,PatientDetailSerializers,RegistrationSerializer,UserDetailsSerializer,EmailVerificationSerializer,PasswordUpdateSerializer


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            print("Username:",username)
            print("Password:",password)

            user = authenticate(username=username,password=password)

            if user is not None:
                login(request, user)
                # user_id = User.objects.get(username=request.user)
                return Response({"status": "user_validated"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)


        return Response({'status': 'Invalid_Credentials'}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "User_created_successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def email_verification(request):
    serializer = EmailVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = random.randint(100000, 999999)

        try:
            user = User.objects.get(email=email)
            user_details, created = UserDetails.objects.get_or_create(user_id=user)
            user_details.otp = otp
            user_details.save()

            send_mail(
                subject="Your OTP for Email Verification",
                message=f"Your OTP is: {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({"message": "OTP_sent_successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User_with_this_email_does_not_exist."}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def validate_otp(request):
    otp = request.data.get('otp')

    if not otp:
        return Response({"error": "OTP_is_required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_details = UserDetails.objects.get(otp=otp)

        if user_details:
            return Response({"message": "OTP_verified_successfully."}, status=status.HTTP_200_OK)

    except UserDetails.DoesNotExist:
        return Response({"error": "Invalid_OTP."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_password(request):
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    if not email or not password or not confirm_password:
        return Response({"error": "Email, password, and confirm_password are_required."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(password)
            user.save()
            return Response({"message": "Password_updated_successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "User_with_this_email_does_not_exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def patient_list(request):
    patients = Patientsdetails.objects.all()
    serializer = PatientDetailSerializers(patients,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def logout_view(request):
        logout(request)
        return Response({"message": "Successfully_logged_out."}, status=status.HTTP_200_OK)
