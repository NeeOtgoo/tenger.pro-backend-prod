from django.contrib import admin
from .models import School
from .models import School_location

# Register your models here.
admin.site.register(School)
admin.site.register(School_location)