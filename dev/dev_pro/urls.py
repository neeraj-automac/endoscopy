from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view,name='login_view'),
    path('register/',register_view,name='register_view'),
    path('forgot/',email_verification,name='email_verification'),
    path('verify/',validate_otp,name='validate_otp'),
    path('update/',update_password,name='update_password'),
    path('all/',patient_list,name='patient_list'),
    path('logout/',logout_view,name='logout_view'),


]