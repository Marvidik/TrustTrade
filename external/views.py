from rest_framework.response import Response
from rest_framework.decorators import api_view
from .sms import send_otp, verify_otp
from .verificationhandler import mark_user_verified
from .payment import verify_payment,initialize_payment
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import permission_classes
from wallet.models import Wallet, WalletTransaction
from django.db import transaction as db_transaction
from lend.models import Match
import requests
import os

# Now use them
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')

# Twilo Phone number Verification endpoints
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
    


# PAystack Initialization and verification endpoints
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initialize_payment_view(request):
    email = request.data.get("email")
    amount = request.data.get("amount")

    if not email or not amount:
        return Response({"error": "Email and amount are required"}, status=400)

    data = initialize_payment(email, amount)

    wallet=Wallet.objects.filter(user=request.user).first()

    if not data.get("status"):
        return Response({"error": "Payment initialization failed"}, status=400)

    reference = data["data"]["reference"]

    # Save the transaction to database
    with db_transaction.atomic():
        WalletTransaction.objects.create(
            wallet=wallet,  # or fetch user’s wallet if user is authenticated
            amount=amount,
            reference=reference,
            type="credit"
        )

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_payment_view(request, reference):
    try:
        result = verify_payment(reference)

        if result["status"] and result["data"]["status"] == "success":
            data = result["data"]
            return Response({
                "status": "success",
                "reference": data["reference"],
                "amount": data["amount"] / 100,
                "currency": data["currency"],
                "email": data["customer"]["email"],
                "transaction_date": data["transaction_date"],
                "gateway_response": data["gateway_response"]
            })

        return Response({
            "status": "failed",
            "message": result["data"].get("gateway_response", "Payment not successful")
        }, status=400)

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment_and_credit_wallet(request):
    reference = request.data.get("reference")
    
    if not reference:
        return Response({"error": "Reference is required"}, status=400)

    # Step 1: Verify Paystack payment
    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers={"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    )

    result = response.json()
    if not result['status'] or result['data']['status'] != "success":
        return Response({"error": "Payment not successful"}, status=400)


    # Step 3: Credit wallet in a transaction
    with db_transaction.atomic():
        # Step 1: Check if wallet has already been funded with this reference
        if not WalletTransaction.objects.filter(reference=reference).exists():
            return Response({"message": "Transaction not found"}, status=404)
        
        if WalletTransaction.objects.filter(reference=reference,success=True).exists():
            return Response({"message": "Account Already Funded"}, status=404)

        # Step 2: Get the transaction
        try:
            tx = WalletTransaction.objects.get(reference=reference)
        except WalletTransaction.DoesNotExist:
            return Response({"message": "Transaction not found"}, status=404)

        # Step 3: Get amount and user from transaction
        user = tx.wallet.user
        amount = tx.amount

        # Step 4: Get or create the user's wallet
        wallet, _ = Wallet.objects.get_or_create(user=user)

        # Step 5: Credit the wallet
        wallet.credit(amount)

        

        # Step 7: Mark transaction as completed
        tx.success = True
        tx.save()

        return Response({"message": "Wallet funded successfully"}, status=200)

    
