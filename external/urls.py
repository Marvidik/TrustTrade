from django.urls import path
from .views import verify_otp_view,send_otp_view,initialize_payment_view,verify_payment_view,verify_payment_and_credit_wallet

urlpatterns=[
    path("sms-verify/",verify_otp_view,name="verify-sms"),
    path('send-sms/',send_otp_view,name="send-otp-view"),

    path('payment/initialize/', initialize_payment_view, name='initialize-payment'),
    path('payment/verify/<str:reference>/', verify_payment_view, name='verify-payment'),

    path('payment/credit-wallet/',verify_payment_and_credit_wallet,name="credit-verification")
]