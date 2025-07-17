from django.urls import path
from .views import verify_otp_view,send_otp_view

urlpatterns=[
    path("sms-verify/",verify_otp_view,name="verify-sms"),
    path('send-sms/',send_otp_view,name="send-otp-view"),
]