from rest_framework.response import Response
from rest_framework.decorators import api_view
from .sms import send_otp, verify_otp
from .verificationhandler import mark_user_verified


@api_view(['POST'])
def send_otp_view(request):
    try:
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({"error": "Phone number required"}, status=400)

        status = send_otp(phone_number)
        return Response({"status": status})
    except Exception as e :
        print(e)
        return Response({"error": "Twilo has some issues"}, status=500)


@api_view(['POST'])
def verify_otp_view(request):
    try:
        phone_number = request.data.get("phone_number")
        code = request.data.get("code")

        if not phone_number or not code:
            return Response({"error": "Phone and code required"}, status=400)

        status = verify_otp(phone_number, code)
        if status == "approved":
            mark_user_verified(phone_number)
            return Response({"status": "verified"})
        return Response({"status": "failed"}, status=400)
    except Exception as e:
        print(e)
        return Response({"error": "Twilo has some issues"}, status=500)