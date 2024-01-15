from django.contrib import admin
from apps.employee.models import Employee, Employee_attandance

# Register your models here.

admin.site.register(Employee)
admin.site.register(Employee_attandance)

