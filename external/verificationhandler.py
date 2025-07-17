from django.contrib.auth import get_user_model

User = get_user_model()

def mark_user_verified(phone_number):
    try:
        user = User.objects.get(phone_number=phone_number)
        user.is_verified = True
        user.save()
        return True
    except User.DoesNotExist:
        return False