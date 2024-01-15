from django.db.models import EmailField, BooleanField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = EmailField(blank=False, max_length=254, verbose_name="email address")
    is_student = BooleanField(blank=False, default=False)
    is_teacher = BooleanField(blank=False, default=False)
    is_parent = BooleanField(blank=False, default=False)
    is_employee = BooleanField(blank=False, default=False)

    USERNAME_FIELD = "username"   # e.g: "bagsh", "NBjAZW4nBwVcKm6"
    EMAIL_FIELD = "email" 

    class Meta:
        permissions = [
            ("change_user_password", "Change user password"),
        ]
