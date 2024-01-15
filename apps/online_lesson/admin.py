from django.contrib import admin
from .models import Online_lesson, Online_file, Online_attendance, Online_student, Online_sub, Online_sub_file, Online_type, Online_file_folder

# Register your models here.
admin.site.register(Online_lesson)
admin.site.register(Online_file)
admin.site.register(Online_attendance)
admin.site.register(Online_student)
admin.site.register(Online_type)
admin.site.register(Online_sub)
admin.site.register(Online_file_folder)
admin.site.register(Online_sub_file)
