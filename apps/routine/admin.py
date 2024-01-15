from django.contrib import admin
from .models import Routine, Routine_student, Routine_time, Routine_attendance

# Register your models here.
admin.site.register(Routine)
admin.site.register(Routine_student)
admin.site.register(Routine_time)
admin.site.register(Routine_attendance)