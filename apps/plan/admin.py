from django.contrib import admin
from .models import PlanMark, Plan, PlanAction

# Register your models here.
admin.site.register(PlanMark)
admin.site.register(Plan)
admin.site.register(PlanAction)