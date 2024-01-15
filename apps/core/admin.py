from django.contrib import admin
from .models import City, District, Khoroo, Student_status, Teacher_status, Student_status_extra, Activity, Degree, Classtime, Employee_compartment

# Register your models here.
admin.site.register(City)
admin.site.register(District)
admin.site.register(Khoroo)
admin.site.register(Student_status)
admin.site.register(Teacher_status)
admin.site.register(Student_status_extra)
admin.site.register(Activity)
admin.site.register(Degree)
admin.site.register(Classtime)
admin.site.register(Employee_compartment)