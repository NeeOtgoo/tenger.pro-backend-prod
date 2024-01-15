from django.db.models import Model, BooleanField, CASCADE, ForeignKey, DateTimeField
from django.conf import settings

# Create your models here.
class Employee_attandance(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    is_in = BooleanField(default=True)
    is_out = BooleanField(default=False)
    time_in = DateTimeField(auto_now_add=True)
    time_out = DateTimeField(auto_now=True)
    
